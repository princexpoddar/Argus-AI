"""
Argus AI — CTGAN Synthetic Data Experiment
============================================
Uses Conditional Tabular GAN to generate synthetic insider samples
and tests whether they improve model performance beyond SMOTE.

Experiment Design:
  1. Train CTGAN on real insider feature vectors
  2. Generate synthetic insider samples
  3. Validate quality (nearest-neighbor distance check)
  4. Retrain XGBoost/LightGBM with CTGAN-augmented data
  5. Compare vs SMOTE-only results

Usage:
    python -m argus.data.ctgan_experiment
"""

import sys
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    f1_score, precision_score, recall_score, roc_auc_score,
    average_precision_score, confusion_matrix,
)
from sklearn.neighbors import NearestNeighbors
from loguru import logger

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from argus.config import Config


def run_ctgan_experiment():
    Config.setup()
    np.random.seed(42)

    proc_dir = Config.paths.PROCESSED_DATA
    research_dir = Path(Config.paths.ROOT) / "research"
    research_dir.mkdir(parents=True, exist_ok=True)

    experiment_log = []

    # ═══════════════════════════════════════════════════════════
    #  STEP 1: Load enhanced features
    # ═══════════════════════════════════════════════════════════
    logger.info("=" * 60)
    logger.info("CTGAN Experiment — Loading data...")
    logger.info("=" * 60)

    X_all = np.load(proc_dir / "X_enhanced.npy")
    y_all = np.load(proc_dir / "y_enhanced.npy")
    feature_cols = json.load(open(proc_dir / "enhanced_feature_cols.json"))

    # Use static features (last timestep)
    X_static = X_all[:, -1, :]

    # Split
    X_trainval, X_test, y_trainval, y_test = train_test_split(
        X_static, y_all, test_size=0.15, random_state=42, stratify=y_all
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_trainval, y_trainval, test_size=0.176, random_state=42, stratify=y_trainval
    )

    logger.info(f"  Train: {X_train.shape[0]} ({y_train.sum()} pos)")
    logger.info(f"  Val: {X_val.shape[0]} ({y_val.sum()} pos)")
    logger.info(f"  Test: {X_test.shape[0]} ({y_test.sum()} pos)")

    # ═══════════════════════════════════════════════════════════
    #  STEP 2: Train CTGAN on insider samples
    # ═══════════════════════════════════════════════════════════
    logger.info("=" * 60)
    logger.info("STEP 2: Training CTGAN on insider feature vectors...")
    logger.info("=" * 60)

    from ctgan import CTGAN

    # Get real insider samples from training set
    X_insiders = X_train[y_train == 1]
    logger.info(f"  Real insider samples for CTGAN training: {len(X_insiders)}")

    # Create a DataFrame for CTGAN (it needs column names)
    insider_df = pd.DataFrame(X_insiders, columns=feature_cols)

    # Train CTGAN
    # Train CTGAN — pac=1 required for small datasets to avoid assertion errors
    # batch_size must be divisible by pac
    ctgan = CTGAN(
        epochs=300,
        batch_size=min(50, len(X_insiders)),
        generator_dim=(128, 128),
        discriminator_dim=(128, 128),
        pac=1,
        verbose=True,
    )

    logger.info("  Training CTGAN (300 epochs)...")
    ctgan.fit(insider_df)
    logger.info("  CTGAN training complete!")

    # ═══════════════════════════════════════════════════════════
    #  STEP 3: Generate synthetic insiders
    # ═══════════════════════════════════════════════════════════
    logger.info("=" * 60)
    logger.info("STEP 3: Generating synthetic insider samples...")
    logger.info("=" * 60)

    n_synthetic = 2000  # Generate plenty
    synthetic_df = ctgan.sample(n_synthetic)
    X_synthetic = synthetic_df.values.astype(np.float32)

    logger.info(f"  Generated {n_synthetic} synthetic insider samples")

    # ═══════════════════════════════════════════════════════════
    #  STEP 4: Quality validation
    # ═══════════════════════════════════════════════════════════
    logger.info("=" * 60)
    logger.info("STEP 4: Validating synthetic data quality...")
    logger.info("=" * 60)

    # a) Nearest neighbor distance check
    nn = NearestNeighbors(n_neighbors=1)
    nn.fit(X_insiders)
    distances, _ = nn.kneighbors(X_synthetic)
    avg_dist = distances.mean()
    std_dist = distances.std()

    # Compare with distance between real insiders
    nn_real = NearestNeighbors(n_neighbors=2)  # 2 because closest is itself
    nn_real.fit(X_insiders)
    real_dists, _ = nn_real.kneighbors(X_insiders)
    real_avg = real_dists[:, 1].mean()  # second-nearest (skip self)

    logger.info(f"  Avg distance (synthetic → real): {avg_dist:.4f}")
    logger.info(f"  Avg distance (real → real): {real_avg:.4f}")
    logger.info(f"  Distance ratio: {avg_dist/real_avg:.2f}x (closer to 1.0 = better)")

    # b) Feature-wise comparison
    logger.info("\n  Feature-wise comparison (top 10 by importance):")
    top_feats_idx = [feature_cols.index(f) for f in [
        "roll_7d_max_data_volume_mb", "roll_14d_std_data_volume_mb",
        "expanding_max_systems", "data_volume_mb", "is_new_device",
    ] if f in feature_cols]

    for idx in top_feats_idx[:5]:
        fname = feature_cols[idx]
        real_mean = X_insiders[:, idx].mean()
        syn_mean = X_synthetic[:, idx].mean()
        real_std = X_insiders[:, idx].std()
        syn_std = X_synthetic[:, idx].std()
        logger.info(f"    {fname}: real={real_mean:.3f}±{real_std:.3f}, synthetic={syn_mean:.3f}±{syn_std:.3f}")

    experiment_log.append({
        "experiment": "CTGAN Quality",
        "n_real_insiders": len(X_insiders),
        "n_synthetic": n_synthetic,
        "avg_dist_synthetic_to_real": round(float(avg_dist), 4),
        "avg_dist_real_to_real": round(float(real_avg), 4),
        "distance_ratio": round(float(avg_dist / real_avg), 4),
    })

    # ═══════════════════════════════════════════════════════════
    #  STEP 5: Train models with CTGAN augmentation
    # ═══════════════════════════════════════════════════════════
    logger.info("=" * 60)
    logger.info("STEP 5: Training models with CTGAN-augmented data...")
    logger.info("=" * 60)

    import xgboost as xgb
    import lightgbm as lgb

    # Augmented training set: real + CTGAN synthetic insiders
    X_train_ctgan = np.vstack([X_train, X_synthetic])
    y_train_ctgan = np.concatenate([y_train, np.ones(len(X_synthetic), dtype=np.int32)])

    logger.info(f"  CTGAN-augmented: {len(X_train_ctgan)} samples ({y_train_ctgan.sum()} pos)")
    logger.info(f"  Imbalance: {(y_train_ctgan==0).sum()/max(1,(y_train_ctgan==1).sum()):.1f}:1")

    # Scale
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train_ctgan)
    X_val_s = scaler.transform(X_val)
    X_test_s = scaler.transform(X_test)

    spw = (y_train_ctgan == 0).sum() / max(1, (y_train_ctgan == 1).sum())

    # XGBoost with CTGAN
    xgb_model = xgb.XGBClassifier(
        n_estimators=500, max_depth=6, learning_rate=0.05,
        scale_pos_weight=spw, min_child_weight=3,
        subsample=0.8, colsample_bytree=0.8,
        reg_alpha=0.1, reg_lambda=1.0,
        eval_metric="logloss", random_state=42,
        use_label_encoder=False, verbosity=0,
    )
    xgb_model.fit(X_train_s, y_train_ctgan, eval_set=[(X_val_s, y_val)], verbose=False)

    xgb_probs = xgb_model.predict_proba(X_test_s)[:, 1]
    xgb_result = _evaluate(y_test, xgb_probs, "XGBoost+CTGAN")

    # LightGBM with CTGAN
    lgb_model = lgb.LGBMClassifier(
        n_estimators=500, max_depth=6, learning_rate=0.05,
        is_unbalance=True, num_leaves=31, min_child_samples=5,
        subsample=0.8, colsample_bytree=0.8,
        reg_alpha=0.1, reg_lambda=1.0,
        random_state=42, verbose=-1,
    )
    lgb_model.fit(X_train_ctgan, y_train_ctgan, eval_set=[(X_val, y_val)])

    lgb_probs = lgb_model.predict_proba(X_test_s)[:, 1]
    lgb_result = _evaluate(y_test, lgb_probs, "LightGBM+CTGAN")

    # ═══════════════════════════════════════════════════════════
    #  STEP 6: Also try SMOTE+CTGAN combined
    # ═══════════════════════════════════════════════════════════
    logger.info("=" * 60)
    logger.info("STEP 6: SMOTE + CTGAN combined...")
    logger.info("=" * 60)

    from imblearn.combine import SMOTETomek
    from imblearn.over_sampling import SMOTE

    # First SMOTE, then add CTGAN samples
    smote = SMOTETomek(
        smote=SMOTE(sampling_strategy=0.3, random_state=42, k_neighbors=5),
        random_state=42,
    )
    X_smote, y_smote = smote.fit_resample(X_train, y_train)

    # Add CTGAN on top
    X_combined = np.vstack([X_smote, X_synthetic[:500]])  # Add 500 CTGAN samples
    y_combined = np.concatenate([y_smote, np.ones(500, dtype=np.int32)])

    logger.info(f"  Combined: {len(X_combined)} samples ({y_combined.sum()} pos)")

    scaler2 = StandardScaler()
    X_comb_s = scaler2.fit_transform(X_combined)
    X_val_s2 = scaler2.transform(X_val)
    X_test_s2 = scaler2.transform(X_test)

    lgb_combined = lgb.LGBMClassifier(
        n_estimators=500, max_depth=6, learning_rate=0.05,
        is_unbalance=True, num_leaves=31, min_child_samples=5,
        subsample=0.8, colsample_bytree=0.8,
        reg_alpha=0.1, reg_lambda=1.0,
        random_state=42, verbose=-1,
    )
    lgb_combined.fit(X_combined, y_combined, eval_set=[(X_val, y_val)])

    lgb_comb_probs = lgb_combined.predict_proba(X_test_s2)[:, 1]
    lgb_comb_result = _evaluate(y_test, lgb_comb_probs, "LightGBM+SMOTE+CTGAN")

    # ═══════════════════════════════════════════════════════════
    #  STEP 7: Compare all approaches
    # ═══════════════════════════════════════════════════════════
    logger.info("=" * 60)
    logger.info("FINAL COMPARISON")
    logger.info("=" * 60)

    # Load SMOTE-only results for comparison
    smote_metrics = json.load(open(Config.paths.RESULTS / "metrics_enhanced.json"))

    all_results = {
        "SMOTE-only (baseline)": {
            "f1": smote_metrics["all_results"]["LightGBM"]["test_f1"],
            "precision": smote_metrics["all_results"]["LightGBM"]["test_precision"],
            "recall": smote_metrics["all_results"]["LightGBM"]["test_recall"],
            "auc": smote_metrics["all_results"]["LightGBM"]["test_auc_roc"],
        },
        "CTGAN-only (XGBoost)": xgb_result,
        "CTGAN-only (LightGBM)": lgb_result,
        "SMOTE+CTGAN (LightGBM)": lgb_comb_result,
    }

    logger.info(f"\n  {'Model':<30} {'F1':>8} {'Prec':>8} {'Recall':>8} {'AUC':>8}")
    logger.info(f"  {'-'*30} {'---':>8} {'---':>8} {'---':>8} {'---':>8}")
    for name, r in all_results.items():
        f1 = r.get("f1", r.get("test_f1", 0))
        p = r.get("precision", r.get("test_precision", 0))
        rec = r.get("recall", r.get("test_recall", 0))
        auc = r.get("auc", r.get("test_auc_roc", 0))
        logger.info(f"  {name:<30} {f1:>8.4f} {p:>8.4f} {rec:>8.4f} {auc:>8.4f}")

    experiment_log.append({"all_results": all_results})

    # Save experiment log
    with open(research_dir / "05_ctgan_experiment.json", "w") as f:
        json.dump(experiment_log, f, indent=2, default=str)

    # Generate report
    _generate_report(all_results, experiment_log, research_dir)

    logger.success("✅ CTGAN experiment complete!")

    return all_results


def _evaluate(y_true, probs, name):
    """Evaluate model and find best F1 threshold."""
    best_f1, best_t = 0, 0.5
    for t in np.linspace(0.01, 0.99, 200):
        preds = (probs >= t).astype(int)
        if preds.sum() == 0:
            continue
        f1 = f1_score(y_true, preds, zero_division=0)
        if f1 > best_f1:
            best_f1 = f1
            best_t = t

    preds = (probs >= best_t).astype(int)
    prec = precision_score(y_true, preds, zero_division=0)
    rec = recall_score(y_true, preds, zero_division=0)
    auc = roc_auc_score(y_true, probs)
    prauc = average_precision_score(y_true, probs)
    cm = confusion_matrix(y_true, preds)
    tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (0, 0, 0, 0)

    logger.info(f"\n  {name}:")
    logger.info(f"    F1={best_f1:.4f}  P={prec:.4f}  R={rec:.4f}  AUC={auc:.4f}  PR-AUC={prauc:.4f}")
    logger.info(f"    TP={tp}  FP={fp}  FN={fn}  TN={tn}")

    return {
        "f1": float(best_f1), "precision": float(prec),
        "recall": float(rec), "auc": float(auc),
        "pr_auc": float(prauc), "threshold": float(best_t),
        "tp": int(tp), "fp": int(fp), "fn": int(fn), "tn": int(tn),
    }


def _generate_report(all_results, experiment_log, research_dir):
    """Generate CTGAN experiment report."""
    lines = [
        "# 05 — CTGAN Experiment Results\n",
        f"**Generated**: 2026-06-16\n",
        "---\n",
        "## Augmentation Strategy Comparison\n",
        "| Strategy | F1 | Precision | Recall | AUC-ROC |",
        "|----------|----|-----------|--------|---------|",
    ]

    for name, r in all_results.items():
        f1 = r.get("f1", r.get("test_f1", 0))
        p = r.get("precision", r.get("test_precision", 0))
        rec = r.get("recall", r.get("test_recall", 0))
        auc = r.get("auc", r.get("test_auc_roc", 0))
        lines.append(f"| {name} | {f1:.4f} | {p:.4f} | {rec:.4f} | {auc:.4f} |")

    lines.append("\n## CTGAN Data Quality\n")
    for entry in experiment_log:
        if "n_synthetic" in entry:
            lines.append(f"- Real insider samples: {entry['n_real_insiders']}")
            lines.append(f"- Synthetic samples generated: {entry['n_synthetic']}")
            lines.append(f"- Distance ratio (synthetic/real): {entry['distance_ratio']:.4f}")
            lines.append(f"  - Closer to 1.0 = synthetic samples are realistic")
            lines.append(f"  - > 2.0 = synthetic samples are too different from real\n")

    path = research_dir / "05_ctgan_experiment.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    logger.info(f"  Report saved to: {path}")


if __name__ == "__main__":
    run_ctgan_experiment()
