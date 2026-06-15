"""
Argus AI — Deep Data Investigation (Phase 1)
==============================================
Comprehensive EDA modeled after the BOI Hackathon methodology.
Produces statistical analysis, visualizations, and markdown reports.

Sections:
    01. Dataset Overview
    02. Target Variable & Class Imbalance
    03. Feature Distribution Analysis (Normal vs Insider)
    04. Statistical Significance Tests
    05. Correlation Analysis
    06. Feature Importance (Mutual Information)
    07. Temporal Attack Pattern Analysis
    08. Per-Scenario Profiling
    09. Dead Feature Audit
    10. Cross-Feature Interactions
    11. Insider Behavioral Fingerprints

Usage:
    python -m argus.data.deep_investigation
"""

import sys
import json
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
from scipy import stats as sp_stats
from sklearn.feature_selection import mutual_info_classif
from sklearn.preprocessing import StandardScaler
from loguru import logger

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from argus.config import Config

# Try to import matplotlib — if not available, skip plots
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    logger.warning("matplotlib not available — skipping plots")

try:
    import seaborn as sns
    HAS_SNS = True
except ImportError:
    HAS_SNS = False


FEATURE_COLS = [
    "login_hour", "logout_hour", "session_duration_hrs", "is_weekend",
    "is_after_hours", "time_since_last_session", "login_regularity_score",
    "temporal_entropy",
    "files_accessed", "emails_sent", "emails_received", "urls_visited",
    "usb_events", "data_volume_mb", "unique_systems_accessed",
    "is_new_device", "device_count", "unique_pcs", "geo_anomaly_flag",
    "vpn_usage",
    "external_email_ratio", "avg_attachment_size", "unique_recipients",
    "cc_bcc_ratio", "email_content_sentiment", "unusual_recipient_flag",
    "file_copy_count", "usb_file_transfers", "large_download_flag",
    "sensitive_file_access", "data_egress_volume", "print_count",
    "cloud_upload_count",
    "access_to_role_ratio", "peer_deviation_score", "weekday_vs_weekend_ratio",
    "morning_vs_evening_ratio", "productive_vs_idle_ratio",
    "command_diversity_index",
    "action_sequence_entropy", "longest_unusual_chain",
    "role_boundary_crossings", "privilege_escalation_count",
    "session_action_diversity", "repeat_pattern_score",
    "novelty_score", "behavioral_velocity",
]

# Feature categories for organized reporting
FEATURE_CATEGORIES = {
    "Temporal": ["login_hour", "logout_hour", "session_duration_hrs", "is_weekend",
                 "is_after_hours", "time_since_last_session", "login_regularity_score",
                 "temporal_entropy"],
    "Access Volume": ["files_accessed", "emails_sent", "emails_received", "urls_visited",
                      "usb_events", "data_volume_mb", "unique_systems_accessed"],
    "Device & Location": ["is_new_device", "device_count", "unique_pcs", "geo_anomaly_flag",
                          "vpn_usage"],
    "Communication": ["external_email_ratio", "avg_attachment_size", "unique_recipients",
                      "cc_bcc_ratio", "email_content_sentiment", "unusual_recipient_flag"],
    "Data Movement": ["file_copy_count", "usb_file_transfers", "large_download_flag",
                      "sensitive_file_access", "data_egress_volume", "print_count",
                      "cloud_upload_count"],
    "Behavioral Ratios": ["access_to_role_ratio", "peer_deviation_score",
                          "weekday_vs_weekend_ratio", "morning_vs_evening_ratio",
                          "productive_vs_idle_ratio", "command_diversity_index"],
    "Sequence": ["action_sequence_entropy", "longest_unusual_chain",
                 "role_boundary_crossings", "privilege_escalation_count",
                 "session_action_diversity", "repeat_pattern_score",
                 "novelty_score", "behavioral_velocity"],
}


def run_investigation():
    """Run the full deep investigation pipeline."""
    Config.setup()
    research_dir = Path(Config.paths.ROOT) / "research"
    fig_dir = research_dir / "figures"
    research_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    report_lines = []
    findings = {}

    def log(text):
        report_lines.append(text)
        if not text.startswith("|") and not text.startswith("---"):
            logger.info(text.replace("#", "").strip()[:120])

    # ═══════════════════════════════════════════════════════════
    #  LOAD DATA
    # ═══════════════════════════════════════════════════════════
    logger.info("Loading data...")
    features_df = pd.read_csv(Config.paths.PROCESSED_DATA / "features_47d.csv")
    employees = pd.read_csv(Config.paths.SYNTHETIC_DATA / "employees.csv")
    ground_truth = pd.read_csv(Config.paths.SYNTHETIC_DATA / "ground_truth.csv")
    activity = pd.read_csv(Config.paths.SYNTHETIC_DATA / "activity_log.csv", nrows=100000)

    features_df = features_df.merge(
        employees[["emp_id", "department", "role", "branch", "clearance_level"]],
        on="emp_id", how="left"
    )
    gt_cols = ["emp_id", "scenario", "attack_start_day", "attack_end_day"]
    gt_merge = ground_truth[gt_cols].copy()
    features_df = features_df.merge(gt_merge, on="emp_id", how="left")

    normal = features_df[features_df["label"] == 0]
    insider = features_df[features_df["label"] == 1]

    # ═══════════════════════════════════════════════════════════
    #  SECTION 01: DATASET OVERVIEW
    # ═══════════════════════════════════════════════════════════
    log("# 01 — Dataset Overview\n")
    log(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    log("| Metric | Value |")
    log("|--------|-------|")
    log(f"| Total feature vectors (emp-day pairs) | **{len(features_df):,}** |")
    log(f"| Unique employees | **{features_df['emp_id'].nunique()}** |")
    log(f"| Days in observation | **{features_df['day_index'].nunique()}** |")
    log(f"| Feature dimensions | **{len(FEATURE_COLS)}** |")
    log(f"| Normal samples | {len(normal):,} ({len(normal)/len(features_df)*100:.1f}%) |")
    log(f"| Insider samples | {len(insider):,} ({len(insider)/len(features_df)*100:.1f}%) |")
    log(f"| Imbalance ratio | **{len(normal)/max(1,len(insider)):.1f} : 1** |")
    log(f"| Unique insiders | {ground_truth['emp_id'].nunique()} |")
    log(f"| Insider scenarios | {ground_truth['scenario'].nunique()} |")
    log(f"| Memory usage | {features_df.memory_usage(deep=True).sum() / 1e6:.1f} MB |")
    log("")

    findings["dataset"] = {
        "total_samples": len(features_df),
        "normal_samples": len(normal),
        "insider_samples": len(insider),
        "imbalance_ratio": round(len(normal) / max(1, len(insider)), 1),
        "n_features": len(FEATURE_COLS),
        "n_employees": int(features_df["emp_id"].nunique()),
        "n_insiders": int(ground_truth["emp_id"].nunique()),
    }

    # ═══════════════════════════════════════════════════════════
    #  SECTION 02: TARGET VARIABLE & CLASS IMBALANCE
    # ═══════════════════════════════════════════════════════════
    log("\n---\n\n# 02 — Target Variable & Class Imbalance\n")

    # Per-scenario distribution
    log("## Insider Scenarios\n")
    log("| Scenario | Insiders | Samples | Attack Duration (days) |")
    log("|----------|----------|---------|----------------------|")
    for _, row in ground_truth.iterrows():
        n_samples = len(insider[insider["emp_id"] == row["emp_id"]])
        duration = row["attack_end_day"] - row["attack_start_day"]
        log(f"| {row['scenario']} | {row['emp_id']} | {n_samples} | {duration} |")

    scenario_counts = ground_truth["scenario"].value_counts()
    log("\n## Scenario Distribution\n")
    log("| Scenario | Count | % of Insiders |")
    log("|----------|-------|---------------|")
    for sc, cnt in scenario_counts.items():
        log(f"| {sc} | {cnt} | {cnt/len(ground_truth)*100:.1f}% |")
    log("")

    # Department distribution of insiders
    log("## Insider Department Distribution\n")
    insider_depts = ground_truth
    log("| Department | Role | Insider Count |")
    log("|-----------|------|--------------|")
    for _, row in insider_depts.iterrows():
        log(f"| {row['department']} | {row['role']} | 1 |")
    log("")

    findings["class_imbalance"] = {
        "positive_rate": round(len(insider) / len(features_df) * 100, 2),
        "scenarios": scenario_counts.to_dict(),
    }

    # ═══════════════════════════════════════════════════════════
    #  SECTION 03: FEATURE DISTRIBUTION ANALYSIS
    # ═══════════════════════════════════════════════════════════
    log("\n---\n\n# 03 — Feature Distribution Analysis (Normal vs Insider)\n")

    feature_stats = []
    for cat_name, cat_features in FEATURE_CATEGORIES.items():
        log(f"\n## {cat_name} Features\n")
        log("| Feature | Normal μ | Normal σ | Insider μ | Insider σ | Ratio (I/N) | Direction |")
        log("|---------|---------|---------|----------|----------|------------|-----------|")

        for feat in cat_features:
            if feat not in features_df.columns:
                continue
            n_mean = normal[feat].mean()
            n_std = normal[feat].std()
            i_mean = insider[feat].mean()
            i_std = insider[feat].std()

            ratio = i_mean / n_mean if abs(n_mean) > 1e-8 else (999.0 if abs(i_mean) > 1e-8 else 1.0)
            direction = "↑" if i_mean > n_mean else ("↓" if i_mean < n_mean else "=")

            log(f"| {feat} | {n_mean:.4f} | {n_std:.4f} | {i_mean:.4f} | {i_std:.4f} | {ratio:.2f}x | {direction} |")

            feature_stats.append({
                "feature": feat,
                "category": cat_name,
                "normal_mean": round(float(n_mean), 6),
                "normal_std": round(float(n_std), 6),
                "insider_mean": round(float(i_mean), 6),
                "insider_std": round(float(i_std), 6),
                "ratio": round(float(ratio), 4),
                "direction": direction,
            })

    findings["feature_stats"] = feature_stats

    # ═══════════════════════════════════════════════════════════
    #  SECTION 04: STATISTICAL SIGNIFICANCE TESTS
    # ═══════════════════════════════════════════════════════════
    log("\n---\n\n# 04 — Statistical Significance Tests\n")
    log("Tests: Welch's t-test, Mann-Whitney U, Cohen's d effect size\n")
    log("| Rank | Feature | t-stat | p-value | Mann-Whitney U p | Cohen's d | Significance |")
    log("|------|---------|--------|---------|-----------------|-----------|-------------|")

    stat_results = []
    for feat in FEATURE_COLS:
        if feat not in features_df.columns:
            continue
        n_vals = normal[feat].dropna().values
        i_vals = insider[feat].dropna().values

        if len(n_vals) < 2 or len(i_vals) < 2:
            continue

        # Welch's t-test
        t_stat, t_p = sp_stats.ttest_ind(i_vals, n_vals, equal_var=False)

        # Mann-Whitney U (non-parametric)
        try:
            u_stat, u_p = sp_stats.mannwhitneyu(i_vals, n_vals, alternative='two-sided')
        except ValueError:
            u_p = 1.0

        # Cohen's d
        pooled_std = np.sqrt((n_vals.std()**2 + i_vals.std()**2) / 2)
        cohens_d = (i_vals.mean() - n_vals.mean()) / pooled_std if pooled_std > 1e-10 else 0.0

        # Significance level
        if t_p < 0.001 and abs(cohens_d) > 0.8:
            sig = "🔴 LARGE"
        elif t_p < 0.01 and abs(cohens_d) > 0.5:
            sig = "🟠 MEDIUM"
        elif t_p < 0.05 and abs(cohens_d) > 0.2:
            sig = "🟡 SMALL"
        else:
            sig = "⚪ NONE"

        stat_results.append({
            "feature": feat,
            "t_stat": round(float(t_stat), 4),
            "t_p": float(t_p),
            "u_p": float(u_p),
            "cohens_d": round(float(cohens_d), 4),
            "significance": sig,
        })

    # Sort by absolute Cohen's d
    stat_results.sort(key=lambda x: abs(x["cohens_d"]), reverse=True)
    for rank, sr in enumerate(stat_results, 1):
        log(f"| {rank} | {sr['feature']} | {sr['t_stat']:.3f} | {sr['t_p']:.2e} | {sr['u_p']:.2e} | {sr['cohens_d']:.4f} | {sr['significance']} |")

    findings["statistical_tests"] = stat_results

    # ═══════════════════════════════════════════════════════════
    #  SECTION 05: CORRELATION ANALYSIS
    # ═══════════════════════════════════════════════════════════
    log("\n---\n\n# 05 — Correlation Analysis\n")

    # Feature-to-target correlations
    log("## Feature-to-Target (label) Correlations\n")
    log("| Rank | Feature | Pearson r | Spearman ρ | Direction |")
    log("|------|---------|----------|-----------|-----------|")

    corr_results = []
    for feat in FEATURE_COLS:
        if feat not in features_df.columns:
            continue
        vals = features_df[feat].dropna()
        labels = features_df.loc[vals.index, "label"]

        pearson_r = vals.corr(labels)
        spearman_r = vals.corr(labels, method="spearman")

        corr_results.append({
            "feature": feat,
            "pearson": round(float(pearson_r), 6),
            "spearman": round(float(spearman_r), 6),
        })

    corr_results.sort(key=lambda x: abs(x["pearson"]), reverse=True)
    for rank, cr in enumerate(corr_results, 1):
        direction = "+" if cr["pearson"] > 0 else "-"
        log(f"| {rank} | {cr['feature']} | {cr['pearson']:.6f} | {cr['spearman']:.6f} | {direction} |")

    findings["correlations"] = corr_results

    # Top cross-feature correlations
    log("\n## Top Cross-Feature Correlations (|r| > 0.7)\n")
    log("| Feature A | Feature B | Correlation | Notes |")
    log("|-----------|-----------|-------------|-------|")

    corr_matrix = features_df[FEATURE_COLS].corr()
    cross_corrs = []
    for i in range(len(FEATURE_COLS)):
        for j in range(i+1, len(FEATURE_COLS)):
            r = corr_matrix.iloc[i, j]
            if abs(r) > 0.7:
                cross_corrs.append({
                    "feat_a": FEATURE_COLS[i],
                    "feat_b": FEATURE_COLS[j],
                    "corr": round(float(r), 4),
                })
    cross_corrs.sort(key=lambda x: abs(x["corr"]), reverse=True)
    for cc in cross_corrs:
        note = "Near-duplicate" if abs(cc["corr"]) > 0.95 else ("Strong" if abs(cc["corr"]) > 0.85 else "Moderate")
        log(f"| {cc['feat_a']} | {cc['feat_b']} | {cc['corr']:.4f} | {note} |")

    findings["cross_correlations"] = cross_corrs

    # ═══════════════════════════════════════════════════════════
    #  SECTION 06: FEATURE IMPORTANCE (MUTUAL INFORMATION)
    # ═══════════════════════════════════════════════════════════
    log("\n---\n\n# 06 — Feature Importance (Mutual Information)\n")

    X_mi = features_df[FEATURE_COLS].fillna(0).values
    y_mi = features_df["label"].values

    mi_scores = mutual_info_classif(X_mi, y_mi, random_state=42, n_neighbors=5)
    mi_results = sorted(
        zip(FEATURE_COLS, mi_scores),
        key=lambda x: x[1], reverse=True
    )

    log("| Rank | Feature | MI Score | Category | Notes |")
    log("|------|---------|---------|----------|-------|")
    for rank, (feat, mi) in enumerate(mi_results, 1):
        cat = next((c for c, fs in FEATURE_CATEGORIES.items() if feat in fs), "?")
        note = "★ TOP" if mi > 0.01 else ("◆ Useful" if mi > 0.005 else "○ Weak")
        log(f"| {rank} | {feat} | {mi:.6f} | {cat} | {note} |")

    findings["mutual_information"] = [
        {"feature": f, "mi_score": round(float(s), 6)}
        for f, s in mi_results
    ]

    # ═══════════════════════════════════════════════════════════
    #  SECTION 07: TEMPORAL ATTACK PATTERN ANALYSIS
    # ═══════════════════════════════════════════════════════════
    log("\n---\n\n# 07 — Temporal Attack Pattern Analysis\n")
    log("How do insider features evolve relative to their attack window?\n")

    key_features = ["data_volume_mb", "sensitive_file_access", "unique_systems_accessed",
                    "usb_events", "is_after_hours", "novelty_score",
                    "role_boundary_crossings", "behavioral_velocity"]

    for emp_id in ground_truth["emp_id"].values[:5]:  # Top 5 insiders
        gt_row = ground_truth[ground_truth["emp_id"] == emp_id].iloc[0]
        emp_data = features_df[features_df["emp_id"] == emp_id].sort_values("day_index")
        scenario = gt_row["scenario"]
        start = gt_row["attack_start_day"]
        end = gt_row["attack_end_day"]

        log(f"\n### {emp_id} — {scenario} (attack days {start}-{end})\n")

        # Pre-attack vs attack comparison
        pre_attack = emp_data[emp_data["day_index"] < start]
        during_attack = emp_data[(emp_data["day_index"] >= start) & (emp_data["day_index"] <= end)]

        if len(pre_attack) > 0 and len(during_attack) > 0:
            log("| Feature | Pre-Attack μ | During Attack μ | Change | Multiplier |")
            log("|---------|-------------|----------------|--------|------------|")
            for feat in key_features:
                if feat not in emp_data.columns:
                    continue
                pre_val = pre_attack[feat].mean()
                att_val = during_attack[feat].mean()
                change = att_val - pre_val
                mult = att_val / pre_val if abs(pre_val) > 1e-8 else (999.0 if abs(att_val) > 1e-8 else 1.0)
                arrow = "🔺" if change > 0 else ("🔻" if change < 0 else "—")
                log(f"| {feat} | {pre_val:.4f} | {att_val:.4f} | {arrow} {abs(change):.4f} | {mult:.2f}x |")

    findings["temporal_analysis"] = "See per-insider tables in report"

    # ═══════════════════════════════════════════════════════════
    #  SECTION 08: PER-SCENARIO PROFILING
    # ═══════════════════════════════════════════════════════════
    log("\n---\n\n# 08 — Per-Scenario Statistical Fingerprints\n")
    log("Average feature values during active attack windows, grouped by scenario.\n")

    scenarios = ground_truth["scenario"].unique()
    profile_features = [
        "data_volume_mb", "sensitive_file_access", "usb_events", "is_after_hours",
        "unique_systems_accessed", "role_boundary_crossings", "novelty_score",
        "privilege_escalation_count", "behavioral_velocity", "geo_anomaly_flag",
        "external_email_ratio", "is_new_device", "files_accessed", "access_to_role_ratio",
    ]

    scenario_profiles = {}
    for scenario in scenarios:
        sc_insiders = ground_truth[ground_truth["scenario"] == scenario]["emp_id"].values
        sc_data = insider[insider["emp_id"].isin(sc_insiders)]

        if len(sc_data) == 0:
            continue

        log(f"\n### {scenario}\n")
        log("| Feature | Mean | Std | Max | vs Normal Mean | Multiplier |")
        log("|---------|------|-----|-----|---------------|------------|")

        profile = {}
        for feat in profile_features:
            if feat not in sc_data.columns:
                continue
            sc_mean = sc_data[feat].mean()
            sc_std = sc_data[feat].std()
            sc_max = sc_data[feat].max()
            n_mean = normal[feat].mean()
            mult = sc_mean / n_mean if abs(n_mean) > 1e-8 else 0.0
            log(f"| {feat} | {sc_mean:.4f} | {sc_std:.4f} | {sc_max:.4f} | {n_mean:.4f} | {mult:.2f}x |")
            profile[feat] = round(float(sc_mean), 6)

        scenario_profiles[scenario] = profile

    findings["scenario_profiles"] = scenario_profiles

    # ═══════════════════════════════════════════════════════════
    #  SECTION 09: DEAD FEATURE AUDIT
    # ═══════════════════════════════════════════════════════════
    log("\n---\n\n# 09 — Dead Feature Audit\n")
    log("Features with zero variance, constant values, or no discriminative power.\n")
    log("| Feature | Issue | Normal Unique | Insider Unique | Recommendation |")
    log("|---------|-------|--------------|----------------|----------------|")

    dead_features = []
    for feat in FEATURE_COLS:
        if feat not in features_df.columns:
            continue
        all_vals = features_df[feat]
        n_unique = all_vals.nunique()
        n_unique_normal = normal[feat].nunique()
        n_unique_insider = insider[feat].nunique()
        variance = all_vals.var()

        issue = None
        if n_unique <= 1:
            issue = "CONSTANT — zero information"
        elif variance < 1e-10:
            issue = "NEAR-ZERO variance"
        elif all_vals.value_counts(normalize=True).iloc[0] > 0.99:
            issue = f"DOMINANT value ({all_vals.value_counts(normalize=True).iloc[0]*100:.1f}%)"

        if issue:
            dead_features.append(feat)
            log(f"| {feat} | {issue} | {n_unique_normal} | {n_unique_insider} | DROP or REPLACE |")

    if not dead_features:
        log("| — | No completely dead features found | — | — | — |")

    log(f"\n**Dead features identified**: {len(dead_features)}")
    if dead_features:
        log(f"**List**: {', '.join(dead_features)}")

    findings["dead_features"] = dead_features

    # ═══════════════════════════════════════════════════════════
    #  SECTION 10: CROSS-FEATURE INTERACTIONS
    # ═══════════════════════════════════════════════════════════
    log("\n---\n\n# 10 — Cross-Feature Interaction Analysis\n")
    log("Testing multiplicative feature interactions for discrimination power.\n")

    interaction_pairs = [
        ("is_after_hours", "sensitive_file_access"),
        ("usb_events", "data_volume_mb"),
        ("is_new_device", "geo_anomaly_flag"),
        ("role_boundary_crossings", "data_egress_volume"),
        ("behavioral_velocity", "novelty_score"),
        ("access_to_role_ratio", "unique_systems_accessed"),
        ("privilege_escalation_count", "is_after_hours"),
        ("files_accessed", "is_after_hours"),
        ("external_email_ratio", "data_volume_mb"),
        ("login_regularity_score", "is_new_device"),
    ]

    log("| Interaction (A × B) | Normal μ | Insider μ | Ratio | Pearson r (with label) | Improvement over best individual |")
    log("|--------------------|---------|---------|----|-----|------|")

    interaction_results = []
    for fa, fb in interaction_pairs:
        if fa not in features_df.columns or fb not in features_df.columns:
            continue
        interaction = features_df[fa] * features_df[fb]
        n_mean = interaction[features_df["label"] == 0].mean()
        i_mean = interaction[features_df["label"] == 1].mean()
        ratio = i_mean / n_mean if abs(n_mean) > 1e-8 else 999.0
        corr = interaction.corr(features_df["label"])

        # Compare to individual correlations
        corr_a = features_df[fa].corr(features_df["label"])
        corr_b = features_df[fb].corr(features_df["label"])
        best_individual = max(abs(corr_a), abs(corr_b))
        improvement = (abs(corr) - best_individual) / best_individual * 100 if best_individual > 1e-8 else 0

        log(f"| {fa} × {fb} | {n_mean:.4f} | {i_mean:.4f} | {ratio:.2f}x | {corr:.6f} | {improvement:+.1f}% |")
        interaction_results.append({
            "pair": f"{fa} × {fb}",
            "corr_with_label": round(float(corr), 6),
            "ratio": round(float(ratio), 4),
            "improvement_pct": round(float(improvement), 1),
        })

    interaction_results.sort(key=lambda x: abs(x["corr_with_label"]), reverse=True)
    findings["interactions"] = interaction_results

    # ═══════════════════════════════════════════════════════════
    #  SECTION 11: INSIDER BEHAVIORAL FINGERPRINT
    # ═══════════════════════════════════════════════════════════
    log("\n---\n\n# 11 — Insider Behavioral Fingerprint\n")
    log("What makes insiders look different from normal employees?\n")

    # Top discriminators (from Cohen's d)
    top_discriminators = sorted(stat_results, key=lambda x: abs(x["cohens_d"]), reverse=True)[:15]

    log("## Top 15 Most Discriminative Features\n")
    log("| Rank | Feature | Cohen's d | Direction | Insider Behavior |")
    log("|------|---------|----------|-----------|-----------------|")
    for rank, td in enumerate(top_discriminators, 1):
        feat = td["feature"]
        cd = td["cohens_d"]
        # Find the feature stats
        fs = next((s for s in feature_stats if s["feature"] == feat), None)
        if fs:
            if cd > 0:
                behavior = f"Insiders have HIGHER {feat} ({fs['insider_mean']:.3f} vs {fs['normal_mean']:.3f})"
            else:
                behavior = f"Insiders have LOWER {feat} ({fs['insider_mean']:.3f} vs {fs['normal_mean']:.3f})"
        else:
            behavior = "—"
        log(f"| {rank} | {feat} | {cd:.4f} | {'↑' if cd > 0 else '↓'} | {behavior} |")

    log("\n## Summary: The Insider Fingerprint\n")
    log("Based on the analysis, insider threat activity is characterized by:\n")
    # Generate summary from top features
    for td in top_discriminators[:8]:
        feat = td["feature"]
        cd = td["cohens_d"]
        if abs(cd) > 0.2:
            direction = "elevated" if cd > 0 else "reduced"
            log(f"- **{feat}**: {direction} (Cohen's d = {cd:.3f})")

    # ═══════════════════════════════════════════════════════════
    #  GENERATE PLOTS
    # ═══════════════════════════════════════════════════════════
    if HAS_MPL:
        logger.info("Generating visualizations...")
        _generate_plots(features_df, normal, insider, ground_truth,
                        stat_results, mi_results, corr_results, fig_dir)

    # ═══════════════════════════════════════════════════════════
    #  SAVE REPORT
    # ═══════════════════════════════════════════════════════════
    report_path = research_dir / "01_deep_investigation.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    findings_path = research_dir / "01_investigation_findings.json"
    with open(findings_path, "w") as f:
        json.dump(findings, f, indent=2, default=str)

    logger.success(f"✅ Deep investigation complete!")
    logger.info(f"   Report: {report_path}")
    logger.info(f"   Findings: {findings_path}")
    logger.info(f"   Figures: {fig_dir}")

    return findings


def _generate_plots(features_df, normal, insider, ground_truth,
                    stat_results, mi_results, corr_results, fig_dir):
    """Generate all investigation visualizations."""

    # Set style
    plt.style.use('default')
    if HAS_SNS:
        sns.set_theme(style="whitegrid", palette="Set2")

    # ─── Plot 1: Feature importance bar chart ───
    fig, ax = plt.subplots(figsize=(14, 8))
    mi_top20 = mi_results[:20]
    feats = [x[0] for x in mi_top20][::-1]
    scores = [x[1] for x in mi_top20][::-1]
    colors = ['#e74c3c' if s > 0.01 else '#3498db' if s > 0.005 else '#95a5a6' for s in scores]
    ax.barh(feats, scores, color=colors)
    ax.set_xlabel("Mutual Information Score")
    ax.set_title("Top 20 Features by Mutual Information with Target", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(fig_dir / "01_mutual_information_top20.png", dpi=150)
    plt.close()

    # ─── Plot 2: Cohen's d effect size ───
    fig, ax = plt.subplots(figsize=(14, 8))
    top15 = sorted(stat_results, key=lambda x: abs(x["cohens_d"]), reverse=True)[:15]
    feats = [x["feature"] for x in top15][::-1]
    ds = [x["cohens_d"] for x in top15][::-1]
    colors = ['#e74c3c' if d > 0 else '#3498db' for d in ds]
    ax.barh(feats, ds, color=colors)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.axvline(0.2, color='gray', linewidth=0.5, linestyle='--', alpha=0.5)
    ax.axvline(-0.2, color='gray', linewidth=0.5, linestyle='--', alpha=0.5)
    ax.axvline(0.8, color='gray', linewidth=0.5, linestyle='--', alpha=0.3)
    ax.axvline(-0.8, color='gray', linewidth=0.5, linestyle='--', alpha=0.3)
    ax.set_xlabel("Cohen's d (Effect Size)")
    ax.set_title("Top 15 Features by Statistical Discrimination Power", fontsize=14, fontweight='bold')
    ax.text(0.2, -0.5, 'Small', fontsize=8, color='gray')
    ax.text(0.8, -0.5, 'Large', fontsize=8, color='gray')
    plt.tight_layout()
    plt.savefig(fig_dir / "02_cohens_d_effect_size.png", dpi=150)
    plt.close()

    # ─── Plot 3: Normal vs Insider distributions for top features ───
    top_feats = [x["feature"] for x in sorted(stat_results, key=lambda x: abs(x["cohens_d"]), reverse=True)[:9]]
    fig, axes = plt.subplots(3, 3, figsize=(16, 12))
    for idx, feat in enumerate(top_feats):
        ax = axes[idx // 3][idx % 3]
        n_vals = normal[feat].dropna()
        i_vals = insider[feat].dropna()
        ax.hist(n_vals, bins=50, alpha=0.6, color='#3498db', label=f'Normal (n={len(n_vals)})', density=True)
        ax.hist(i_vals, bins=30, alpha=0.7, color='#e74c3c', label=f'Insider (n={len(i_vals)})', density=True)
        ax.set_title(feat, fontsize=11, fontweight='bold')
        ax.legend(fontsize=8)
    plt.suptitle("Feature Distributions: Normal vs Insider", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(fig_dir / "03_normal_vs_insider_distributions.png", dpi=150)
    plt.close()

    # ─── Plot 4: Correlation heatmap (feature-to-feature) ───
    corr_matrix = features_df[FEATURE_COLS].corr()
    fig, ax = plt.subplots(figsize=(18, 16))
    cax = ax.matshow(corr_matrix.values, cmap='RdBu_r', vmin=-1, vmax=1)
    fig.colorbar(cax, shrink=0.7)
    ax.set_xticks(range(len(FEATURE_COLS)))
    ax.set_yticks(range(len(FEATURE_COLS)))
    ax.set_xticklabels(FEATURE_COLS, rotation=90, fontsize=6)
    ax.set_yticklabels(FEATURE_COLS, fontsize=6)
    ax.set_title("Feature Correlation Matrix (47×47)", fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(fig_dir / "04_correlation_heatmap.png", dpi=150)
    plt.close()

    # ─── Plot 5: Temporal evolution for sample insiders ───
    key_feats = ["data_volume_mb", "sensitive_file_access", "novelty_score", "behavioral_velocity"]
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))

    for feat_idx, feat in enumerate(key_feats):
        ax = axes[feat_idx // 2][feat_idx % 2]
        for _, gt_row in ground_truth.iterrows():
            emp_id = gt_row["emp_id"]
            emp_data = features_df[features_df["emp_id"] == emp_id].sort_values("day_index")
            start = gt_row["attack_start_day"]
            ax.plot(emp_data["day_index"], emp_data[feat], alpha=0.5, linewidth=0.8)
            ax.axvline(start, color='red', alpha=0.3, linewidth=0.5, linestyle='--')
        ax.set_title(feat, fontsize=11, fontweight='bold')
        ax.set_xlabel("Day")
    plt.suptitle("Temporal Feature Evolution (All Insiders, red=attack start)", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(fig_dir / "05_temporal_evolution.png", dpi=150)
    plt.close()

    # ─── Plot 6: Class imbalance pie chart ───
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    labels_count = features_df["label"].value_counts()
    ax1.pie([labels_count[0], labels_count[1]],
            labels=["Normal", "Insider"],
            autopct='%1.1f%%',
            colors=['#3498db', '#e74c3c'],
            startangle=90)
    ax1.set_title("Sample Distribution", fontsize=12, fontweight='bold')

    # Scenario distribution
    sc_counts = ground_truth["scenario"].value_counts()
    ax2.bar(range(len(sc_counts)), sc_counts.values, color='#e74c3c', alpha=0.8)
    ax2.set_xticks(range(len(sc_counts)))
    ax2.set_xticklabels(sc_counts.index, rotation=45, ha='right', fontsize=9)
    ax2.set_ylabel("Count")
    ax2.set_title("Insider Scenarios", fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig(fig_dir / "06_class_imbalance.png", dpi=150)
    plt.close()

    logger.info(f"  Generated 6 investigation plots in {fig_dir}")


if __name__ == "__main__":
    run_investigation()
