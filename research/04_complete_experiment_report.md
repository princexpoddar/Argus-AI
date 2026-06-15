# 04 — Complete Experiment Report

**Generated**: 2026-06-16
**Final Model**: LightGBM | F1=0.9495 | AUC=0.983 | 211 features
**Total Experiments**: 6 models across 6 phases

---

## Executive Summary

Starting from a baseline unsupervised pipeline (LSTM + Isolation Forest, F1=0.268),
we achieved **F1=0.9495** through systematic investigation and enhancement:

| Step | Change | F1 Impact |
|------|--------|-----------|
| Baseline | LSTM-AE + IF (47 features) | 0.268 |
| Phase 1 | Deep EDA → identified 15 dead features, 5 redundant pairs | — |
| Phase 2 | Feature engineering: 47 → 211 features | — |
| Phase 3 | SMOTE+Tomek: 233 → 2,348 positive samples | — |
| Phase 4 | XGBoost (supervised) | 0.939 |
| Phase 4 | LightGBM (supervised) | **0.950** |
| Phase 5 | Meta-Learner ensemble | 0.940 |

**Key Finding**: The jump from 0.268 → 0.950 came from TWO changes:
1. **Feature engineering** (rolling windows, z-scores, deltas → 211 features)
2. **Supervised learning** (XGBoost/LightGBM with class weights)

---

## Model Comparison — Final Test Set

| Model | F1 | Precision | Recall | AUC-ROC | PR-AUC | FPR | TP | FP | FN | TN |
|-------|----|-----------|--------|---------|--------|-----|----|----|----|----|
| **LightGBM** | **0.9495** | **0.959** | **0.940** | 0.983 | **0.959** | **0.12%** | **47** | **2** | **3** | **1675** |
| XGBoost | 0.939 | 0.958 | 0.920 | **0.988** | 0.959 | 0.12% | 46 | 2 | 4 | 1675 |
| Meta-Learner | 0.940 | 0.940 | 0.940 | 0.980 | 0.960 | 0.18% | 47 | 3 | 3 | 1674 |
| LSTM-AE (alone) | 0.333 | — | — | — | — | — | — | — | — | — |
| IsolationForest (alone) | 0.305 | — | — | — | — | — | — | — | — | — |
| **Baseline (old)** | **0.268** | **0.221** | **0.340** | **0.764** | — | **3.58%** | **17** | **60** | **33** | **1617** |

---

## Top 20 Most Important Features (XGBoost)

| Rank | Feature | Importance | Category | New? |
|------|---------|-----------|----------|------|
| 1 | roll_7d_max_data_volume_mb | 0.2572 | Rolling Window | ✅ NEW |
| 2 | roll_14d_std_data_volume_mb | 0.0672 | Rolling Window | ✅ NEW |
| 3 | expanding_max_systems | 0.0607 | Cumulative | ✅ NEW |
| 4 | roll_14d_std_novelty_score | 0.0443 | Rolling Window | ✅ NEW |
| 5 | zscore_role_unique_systems | 0.0317 | Z-Score | ✅ NEW |
| 6 | roll_7d_std_novelty_score | 0.0284 | Rolling Window | ✅ NEW |
| 7 | clearance_normalized | 0.0224 | Cumulative | ✅ NEW |
| 8 | roll_7d_std_data_egress | 0.0201 | Rolling Window | ✅ NEW |
| 9 | delta_novelty_score | 0.0172 | Temporal Delta | ✅ NEW |
| 10 | is_weekend | 0.0163 | Original | Original |
| 11 | roll_14d_max_data_volume_mb | 0.0156 | Rolling Window | ✅ NEW |
| 12 | zscore_dept_data_egress | 0.0127 | Z-Score | ✅ NEW |
| 13 | roll_14d_std_data_egress | 0.0123 | Rolling Window | ✅ NEW |
| 14 | is_new_device | 0.0117 | Original | Original |
| 15 | expanding_max_data_volume | 0.0115 | Cumulative | ✅ NEW |
| 16 | zscore_role_data_volume | 0.0111 | Z-Score | ✅ NEW |
| 17 | roll_7d_mean_data_volume | 0.0098 | Rolling Window | ✅ NEW |
| 18 | roll_14d_mean_is_after_hours | 0.0096 | Rolling Window | ✅ NEW |
| 19 | cum_7d_is_after_hours | 0.0082 | Cumulative | ✅ NEW |
| 20 | roll_14d_max_device_count | 0.0082 | Rolling Window | ✅ NEW |

**Critical Insight**: 18 of the top 20 features are NEW engineered features.
Only 2 original features (is_weekend, is_new_device) remain in the top 20.
This validates the BOI hackathon's finding: _"feature engineering is the single biggest driver of model performance"_.

---

## Feature Engineering Breakdown

| Category | Count | Top Contributor | Impact |
|----------|-------|----------------|--------|
| Rolling Windows (7d/14d) | 96 | roll_7d_max_data_volume_mb (#1) | ★★★★★ |
| Z-Scores (dept/role) | 18 | zscore_role_unique_systems (#5) | ★★★★ |
| Temporal Deltas | 24 | delta_novelty_score (#9) | ★★★ |
| Cumulative Risk | 11 | expanding_max_systems (#3) | ★★★★ |
| Feature Interactions | 13 | interact_access_to_role_x_systems | ★★ |
| Velocity/Acceleration | 10 | velocity_data_volume_mb | ★★ |
| Original (cleaned) | 40 | is_weekend (#10) | ★★ |
| **Total** | **211** | | |

---

## SMOTE Augmentation Impact

| Metric | Before SMOTE | After SMOTE |
|--------|-------------|-------------|
| Training samples | 8,061 | 10,176 |
| Positive samples | 233 | 2,348 |
| Imbalance ratio | 33.6:1 | 3.3:1 |

---

## Ensemble Meta-Learner Analysis

The meta-learner (Logistic Regression) learned these weights:

| Base Model | Coefficient | Interpretation |
|-----------|------------|----------------|
| LightGBM | **6.186** | Dominant predictor |
| XGBoost | **6.125** | Near-equal to LightGBM |
| Isolation Forest | 1.001 | Minor contribution |
| LSTM-AE | 0.011 | Negligible |

**Conclusion**: Supervised models completely dominate. The unsupervised models (LSTM + IF)
provide minimal additional signal when supervised models are available.

---

## Comparison with BOI Hackathon

| Metric | BOI Hackathon (F3924) | Argus AI (Insider Threat) |
|--------|----------------------|--------------------------|
| Dataset | 9,082 × 3,925 | 12,710 × 211 |
| Imbalance | High | 39.9:1 |
| Best Model | XGBoost Blend | LightGBM |
| F1 Score | 0.743 | **0.950** |
| AUC-ROC | 0.982 | 0.983 |
| Key Strategy | Feature engineering + ensemble | Feature engineering + SMOTE + supervised |

We **exceeded** the BOI hackathon's F1 (0.950 vs 0.743) while matching its AUC (0.983 vs 0.982).

---

## Remaining Opportunities

1. **CTGAN**: Generate synthetic insider samples via conditional tabular GAN
2. **Neural Network**: Train a supervised MLP on the 211 features
3. **Cross-validation**: Run full 5-fold CV for more robust estimates
4. **Feature selection**: Prune to top 80-100 features for deployment efficiency
5. **Temporal modeling**: Train supervised LSTM/GRU on sequences
