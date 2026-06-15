# 02 — Key Findings & Cross-Analysis

**Generated**: 2026-06-16

---

## Critical Insight: The "Binary Explosion" Problem

Our most discriminative features are **structurally problematic**:

| Feature | Normal Value | Insider Value | Problem |
|---------|-------------|--------------|---------|
| is_new_device | **always 0** | 35.7% have 1 | Binary spike: 0→1 only for insiders |
| role_boundary_crossings | **always 0** | mean 1.28 | Only non-zero for insiders |
| longest_unusual_chain | **always 0** | mean 0.84 | Only non-zero for insiders |
| access_to_role_ratio | **always 0** | mean 0.12 | Only non-zero for insiders |
| privilege_escalation_count | **always 0** | mean 0.05 | Only non-zero for insiders |
| usb_events | **always 0** | mean 0.06 | Only non-zero for insiders |
| urls_visited | **always 0** | mean 0.05 | Only non-zero for insiders |
| geo_anomaly_flag | **always 0** | mean 0.03 | Only non-zero for insiders |

### Why this matters:
These features have **perfect zero-variance in the normal class** — they're 0 for ALL 12,399 normal samples.
This means:
1. ✅ A simple rule "if is_new_device=1 → insider" would catch 35.7% of insiders with 100% precision
2. ❌ But the LSTM autoencoder learns on NORMAL data only → it never sees these features activate
3. ❌ The Isolation Forest sees them as outliers but can't learn the COMBINATION patterns
4. 🔑 **This is why supervised learning will be transformative** — it can learn "is_new_device AND high data_volume → insider"

---

## Scenario Fingerprint Matrix

Each scenario has a unique behavioral signature:

| Signal | Data Exfil | Cred Compromise | Pre-Resign | Priv Esc | Unauth Snoop | Slow Burn |
|--------|-----------|----------------|------------|---------|-------------|-----------|
| data_volume_mb | **16x** ↑↑↑ | 3x ↑ | 5x ↑↑ | 6x ↑↑ | 7x ↑↑ | 2x ↑ |
| is_new_device | ✅ 81% | ✅ 67% | ❌ 0% | ✅ 73% | ✅ 84% | ❌ 0% |
| role_boundary | ✅ 1.7 | ❌ 0 | ❌ 0 | ✅ **3.6** | ✅ **3.8** | ❌ 0 |
| sensitive_access | ✅ 1.7 | ❌ 0 | ❌ 0 | ✅ **8.9** | ✅ 1.9 | ❌ 0 |
| usb_events | ✅ 0.5 | ❌ 0 | ❌ 0 | ❌ 0 | ❌ 0 | ❌ 0 |
| geo_anomaly | ❌ 0 | ✅ **67%** | ❌ 0 | ❌ 0 | ❌ 0 | ❌ 0 |
| priv_escalation | ❌ 0 | ❌ 0 | ❌ 0 | ✅ **64%** | ❌ 0 | ❌ 0 |
| novelty_score | ✅ 2.2 | ✅ 1.3 | ❌ 0 | ✅ 1.6 | ✅ 1.7 | ❌ 0 |

### Cross-Analysis Insights:
1. **pre_resignation_theft** and **slow_burn_recon** are the HARDEST to detect:
   - No new devices, no role boundary crossings, no USB events
   - Only signal: elevated data volume (5x and 2x respectively)
   - Slow burn is especially hard: only 1.76x data volume — barely above normal variation
   
2. **credential_compromise** has a UNIQUE signal: geo_anomaly_flag (67%)
   - This is the ONLY scenario with geographic anomalies
   
3. **privilege_escalation** has the HIGHEST sensitive_file_access (8.9x normal)
   - Combined with privilege_escalation_count, this is highly distinctive

4. **data_exfiltration** is the EASIEST to detect:
   - 16x data volume, USB events, new devices, role boundary crossings
   - Multiple strong signals converge

---

## Feature Redundancy Analysis

### Drop Candidates (redundant or zero-information):
1. `cc_bcc_ratio` — CONSTANT zero, no information
2. `email_content_sentiment` — CONSTANT zero, no information  
3. `usb_file_transfers` — CONSTANT zero, no information
4. `unique_pcs` — **IDENTICAL to device_count** (r=1.0) → drop one
5. `vpn_usage` — **IDENTICAL to geo_anomaly_flag** (r=1.0) → drop one
6. `repeat_pattern_score` — **INVERSE of command_diversity_index** (r=-1.0) → drop one
7. `productive_vs_idle_ratio` — **NEAR-IDENTICAL to behavioral_velocity** (r=0.999) → drop one

### Features that LOOK dead but are CRITICAL:
- `is_new_device`, `role_boundary_crossings`, `longest_unusual_chain` — 99%+ zero but HIGHLY discriminative
- These should be KEPT and enhanced with rolling/cumulative versions

---

## What Needs to Change in the Pipeline

### Problem 1: Unsupervised models can't use binary spike features
→ Solution: Add XGBoost/LightGBM supervised models

### Problem 2: Static features miss temporal build-up
→ Solution: Add temporal deltas, rolling windows, acceleration features

### Problem 3: Some scenarios have very subtle signals  
→ Solution: Feature interactions (data_volume × after_hours, etc.)

### Problem 4: 39:1 class imbalance
→ Solution: SMOTE + class weights + threshold optimization

### Problem 5: 3 completely dead features waste model capacity
→ Solution: Drop them, add 75+ new engineered features
