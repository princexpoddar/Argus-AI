# 01 — Dataset Overview

**Generated**: 2026-06-16 01:15

| Metric | Value |
|--------|-------|
| Total feature vectors (emp-day pairs) | **12,710** |
| Unique employees | **200** |
| Days in observation | **90** |
| Feature dimensions | **47** |
| Normal samples | 12,399 (97.6%) |
| Insider samples | 311 (2.4%) |
| Imbalance ratio | **39.9 : 1** |
| Unique insiders | 14 |
| Insider scenarios | 6 |
| Memory usage | 9.5 MB |


---

# 02 — Target Variable & Class Imbalance

## Insider Scenarios

| Scenario | Insiders | Samples | Attack Duration (days) |
|----------|----------|---------|----------------------|
| data_exfiltration | EMP_001 | 19 | 19 |
| credential_compromise | EMP_005 | 4 | 5 |
| data_exfiltration | EMP_006 | 18 | 19 |
| pre_resignation_theft | EMP_009 | 22 | 28 |
| credential_compromise | EMP_010 | 4 | 5 |
| credential_compromise | EMP_049 | 4 | 5 |
| privilege_escalation | EMP_095 | 11 | 10 |
| privilege_escalation | EMP_111 | 11 | 10 |
| unauthorized_snooping | EMP_137 | 34 | 35 |
| unauthorized_snooping | EMP_148 | 34 | 34 |
| slow_burn_recon | EMP_160 | 40 | 59 |
| pre_resignation_theft | EMP_164 | 23 | 28 |
| slow_burn_recon | EMP_185 | 43 | 59 |
| slow_burn_recon | EMP_191 | 44 | 59 |

## Scenario Distribution

| Scenario | Count | % of Insiders |
|----------|-------|---------------|
| credential_compromise | 3 | 21.4% |
| slow_burn_recon | 3 | 21.4% |
| data_exfiltration | 2 | 14.3% |
| pre_resignation_theft | 2 | 14.3% |
| privilege_escalation | 2 | 14.3% |
| unauthorized_snooping | 2 | 14.3% |

## Insider Department Distribution

| Department | Role | Insider Count |
|-----------|------|--------------|
| retail_banking | relationship_manager | 1 |
| retail_banking | relationship_manager | 1 |
| retail_banking | relationship_manager | 1 |
| retail_banking | relationship_manager | 1 |
| retail_banking | relationship_manager | 1 |
| retail_banking | branch_manager | 1 |
| it_admin | system_admin | 1 |
| it_admin | help_desk | 1 |
| hr | recruiter | 1 |
| hr | payroll | 1 |
| compliance | aml_analyst | 1 |
| compliance | aml_analyst | 1 |
| compliance | risk_officer | 1 |
| compliance | risk_officer | 1 |


---

# 03 — Feature Distribution Analysis (Normal vs Insider)


## Temporal Features

| Feature | Normal μ | Normal σ | Insider μ | Insider σ | Ratio (I/N) | Direction |
|---------|---------|---------|----------|----------|------------|-----------|
| login_hour | 9.0615 | 0.3777 | 10.0228 | 2.8214 | 1.11x | ↑ |
| logout_hour | 18.1347 | 0.7172 | 18.3959 | 1.3496 | 1.01x | ↑ |
| session_duration_hrs | 9.0732 | 0.8183 | 8.3732 | 2.3875 | 0.92x | ↓ |
| is_weekend | 0.0204 | 0.1414 | 0.1190 | 0.3243 | 5.83x | ↑ |
| is_after_hours | 0.7609 | 0.4265 | 0.7878 | 0.4095 | 1.04x | ↑ |
| time_since_last_session | 1.3888 | 0.7869 | 1.2797 | 0.7109 | 0.92x | ↓ |
| login_regularity_score | 0.2905 | 0.2491 | 1.1368 | 2.7773 | 3.91x | ↑ |
| temporal_entropy | 2.2813 | 0.1046 | 1.9848 | 0.6741 | 0.87x | ↓ |

## Access Volume Features

| Feature | Normal μ | Normal σ | Insider μ | Insider σ | Ratio (I/N) | Direction |
|---------|---------|---------|----------|----------|------------|-----------|
| files_accessed | 6.5513 | 4.4365 | 7.1511 | 4.7158 | 1.09x | ↑ |
| emails_sent | 3.6645 | 2.6529 | 3.6495 | 2.6045 | 1.00x | ↓ |
| emails_received | 1.8243 | 1.6301 | 1.7106 | 1.5387 | 0.94x | ↓ |
| urls_visited | 0.0000 | 0.0000 | 0.0514 | 0.2213 | 999.00x | ↑ |
| usb_events | 0.0000 | 0.0000 | 0.0643 | 0.2457 | 999.00x | ↑ |
| data_volume_mb | 2.2478 | 1.2311 | 12.1721 | 13.5920 | 5.42x | ↑ |
| unique_systems_accessed | 4.2728 | 0.6387 | 4.7717 | 1.2112 | 1.12x | ↑ |

## Device & Location Features

| Feature | Normal μ | Normal σ | Insider μ | Insider σ | Ratio (I/N) | Direction |
|---------|---------|---------|----------|----------|------------|-----------|
| is_new_device | 0.0000 | 0.0000 | 0.3569 | 0.4799 | 999.00x | ↑ |
| device_count | 1.0000 | 0.0000 | 1.3344 | 0.5657 | 1.33x | ↑ |
| unique_pcs | 1.0000 | 0.0000 | 1.3344 | 0.5657 | 1.33x | ↑ |
| geo_anomaly_flag | 0.0000 | 0.0000 | 0.0257 | 0.1586 | 999.00x | ↑ |
| vpn_usage | 0.0000 | 0.0000 | 0.0257 | 0.1586 | 999.00x | ↑ |

## Communication Features

| Feature | Normal μ | Normal σ | Insider μ | Insider σ | Ratio (I/N) | Direction |
|---------|---------|---------|----------|----------|------------|-----------|
| external_email_ratio | 0.2966 | 0.2375 | 0.3086 | 0.2393 | 1.04x | ↑ |
| avg_attachment_size | 0.6661 | 0.6969 | 3.2073 | 5.5031 | 4.82x | ↑ |
| unique_recipients | 3.8003 | 2.4819 | 3.7846 | 2.4314 | 1.00x | ↓ |
| cc_bcc_ratio | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.00x | = |
| email_content_sentiment | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.00x | = |
| unusual_recipient_flag | 0.1490 | 0.3561 | 0.1576 | 0.3649 | 1.06x | ↑ |

## Data Movement Features

| Feature | Normal μ | Normal σ | Insider μ | Insider σ | Ratio (I/N) | Direction |
|---------|---------|---------|----------|----------|------------|-----------|
| file_copy_count | 0.8332 | 1.5535 | 1.3826 | 1.4563 | 1.66x | ↑ |
| usb_file_transfers | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.00x | = |
| large_download_flag | 0.0000 | 0.0000 | 0.3762 | 0.4852 | 999.00x | ↑ |
| sensitive_file_access | 1.0719 | 4.5723 | 1.2412 | 3.4299 | 1.16x | ↑ |
| data_egress_volume | 0.3385 | 0.3995 | 2.7358 | 3.9724 | 8.08x | ↑ |
| print_count | 0.2288 | 0.8098 | 0.0450 | 0.3826 | 0.20x | ↓ |
| cloud_upload_count | 0.1496 | 0.7634 | 0.0000 | 0.0000 | 0.00x | ↓ |

## Behavioral Ratios Features

| Feature | Normal μ | Normal σ | Insider μ | Insider σ | Ratio (I/N) | Direction |
|---------|---------|---------|----------|----------|------------|-----------|
| access_to_role_ratio | 0.0000 | 0.0000 | 0.1221 | 0.2852 | 999.00x | ↑ |
| peer_deviation_score | -0.0177 | 0.4671 | 0.7044 | 0.6869 | -39.87x | ↑ |
| weekday_vs_weekend_ratio | 0.0232 | 0.0726 | 0.1015 | 0.1236 | 4.38x | ↑ |
| morning_vs_evening_ratio | 0.3396 | 0.0360 | 0.2641 | 0.1265 | 0.78x | ↓ |
| productive_vs_idle_ratio | 1.1112 | 0.4429 | 1.0198 | 0.3473 | 0.92x | ↓ |
| command_diversity_index | 0.3653 | 0.1328 | 0.4642 | 0.1904 | 1.27x | ↑ |

## Sequence Features

| Feature | Normal μ | Normal σ | Insider μ | Insider σ | Ratio (I/N) | Direction |
|---------|---------|---------|----------|----------|------------|-----------|
| action_sequence_entropy | 2.3495 | 0.1773 | 2.3412 | 0.5271 | 1.00x | ↓ |
| longest_unusual_chain | 0.0000 | 0.0000 | 0.8424 | 1.4517 | 999.00x | ↑ |
| role_boundary_crossings | 0.0000 | 0.0000 | 1.2830 | 2.1290 | 999.00x | ↑ |
| privilege_escalation_count | 0.0000 | 0.0000 | 0.0450 | 0.2077 | 999.00x | ↑ |
| session_action_diversity | 12.8385 | 2.0239 | 13.6367 | 4.1184 | 1.06x | ↑ |
| repeat_pattern_score | 0.6347 | 0.1328 | 0.5358 | 0.1904 | 0.84x | ↓ |
| novelty_score | 0.0614 | 0.2400 | 0.7878 | 1.0686 | 12.84x | ↑ |
| behavioral_velocity | 4.4446 | 1.7718 | 4.0061 | 1.4609 | 0.90x | ↓ |

---

# 04 — Statistical Significance Tests

Tests: Welch's t-test, Mann-Whitney U, Cohen's d effect size

| Rank | Feature | t-stat | p-value | Mann-Whitney U p | Cohen's d | Significance |
|------|---------|--------|---------|-----------------|-----------|-------------|
| 1 | peer_deviation_score | 18.432 | 4.40e-52 | 5.17e-74 | 1.2308 | 🔴 LARGE |
| 2 | large_download_flag | 13.673 | 1.25e-33 | 0.00e+00 | 1.0983 | 🔴 LARGE |
| 3 | is_new_device | 13.117 | 1.44e-31 | 0.00e+00 | 1.0536 | 🔴 LARGE |
| 4 | data_volume_mb | 12.875 | 1.11e-30 | 4.04e-122 | 1.0300 | 🔴 LARGE |
| 5 | novelty_score | 11.980 | 1.90e-27 | 4.65e-112 | 0.9394 | 🔴 LARGE |
| 6 | role_boundary_crossings | 10.627 | 1.06e-22 | 0.00e+00 | 0.8536 | 🔴 LARGE |
| 7 | data_egress_volume | 10.641 | 9.49e-23 | 1.11e-107 | 0.8505 | 🔴 LARGE |
| 8 | device_count | 10.424 | 5.22e-22 | 0.00e+00 | 0.8373 | 🔴 LARGE |
| 9 | unique_pcs | 10.424 | 5.22e-22 | 0.00e+00 | 0.8373 | 🔴 LARGE |
| 10 | longest_unusual_chain | 10.234 | 2.27e-21 | 0.00e+00 | 0.8220 | 🔴 LARGE |
| 11 | morning_vs_evening_ratio | -10.524 | 2.33e-22 | 8.09e-34 | -0.8138 | 🔴 LARGE |
| 12 | weekday_vs_weekend_ratio | 11.135 | 1.65e-24 | 6.75e-63 | 0.7740 | 🟠 MEDIUM |
| 13 | avg_attachment_size | 8.142 | 9.56e-15 | 5.08e-51 | 0.6489 | 🟠 MEDIUM |
| 14 | temporal_entropy | -7.756 | 1.27e-13 | 1.76e-04 | -0.6158 | 🟠 MEDIUM |
| 15 | access_to_role_ratio | 7.547 | 5.00e-13 | 0.00e+00 | 0.6062 | 🟠 MEDIUM |
| 16 | command_diversity_index | 9.110 | 9.50e-18 | 1.94e-20 | 0.6035 | 🟠 MEDIUM |
| 17 | repeat_pattern_score | -9.110 | 9.50e-18 | 1.94e-20 | -0.6035 | 🟠 MEDIUM |
| 18 | unique_systems_accessed | 7.238 | 3.51e-12 | 3.41e-41 | 0.5159 | 🟠 MEDIUM |
| 19 | login_hour | 6.007 | 5.28e-09 | 1.18e-09 | 0.4783 | 🟡 SMALL |
| 20 | login_regularity_score | 5.373 | 1.52e-07 | 3.72e-01 | 0.4299 | 🟡 SMALL |
| 21 | is_weekend | 5.348 | 1.72e-07 | 1.36e-30 | 0.3946 | 🟡 SMALL |
| 22 | session_duration_hrs | -5.163 | 4.34e-07 | 5.06e-01 | -0.3928 | 🟡 SMALL |
| 23 | usb_events | 4.616 | 5.74e-06 | 1.11e-175 | 0.3708 | 🟡 SMALL |
| 24 | file_copy_count | 6.560 | 2.09e-10 | 6.29e-30 | 0.3652 | 🟡 SMALL |
| 25 | urls_visited | 4.100 | 5.27e-05 | 6.61e-141 | 0.3294 | 🟡 SMALL |
| 26 | privilege_escalation_count | 3.823 | 1.60e-04 | 1.60e-123 | 0.3070 | 🟡 SMALL |
| 27 | print_count | -8.033 | 1.18e-14 | 8.75e-07 | -0.2903 | 🟡 SMALL |
| 28 | cloud_upload_count | -21.822 | 1.26e-103 | 7.87e-05 | -0.2772 | 🟡 SMALL |
| 29 | behavioral_velocity | -5.199 | 3.51e-07 | 3.23e-03 | -0.2702 | 🟡 SMALL |
| 30 | session_action_diversity | 3.407 | 7.42e-04 | 2.45e-33 | 0.2463 | 🟡 SMALL |
| 31 | logout_hour | 3.401 | 7.59e-04 | 1.81e-04 | 0.2420 | 🟡 SMALL |
| 32 | geo_anomaly_flag | 2.861 | 4.51e-03 | 2.26e-71 | 0.2298 | 🟡 SMALL |
| 33 | vpn_usage | 2.861 | 4.51e-03 | 2.26e-71 | 0.2298 | 🟡 SMALL |
| 34 | productive_vs_idle_ratio | -4.548 | 7.56e-06 | 2.60e-02 | -0.2297 | 🟡 SMALL |
| 35 | time_since_last_session | -2.665 | 8.07e-03 | 1.00e-02 | -0.1456 | ⚪ NONE |
| 36 | files_accessed | 2.219 | 2.72e-02 | 2.07e-02 | 0.1311 | ⚪ NONE |
| 37 | emails_received | -1.286 | 2.00e-01 | 3.06e-01 | -0.0718 | ⚪ NONE |
| 38 | is_after_hours | 1.140 | 2.55e-01 | 2.73e-01 | 0.0642 | ⚪ NONE |
| 39 | external_email_ratio | 0.876 | 3.82e-01 | 2.76e-01 | 0.0505 | ⚪ NONE |
| 40 | sensitive_file_access | 0.851 | 3.95e-01 | 2.09e-72 | 0.0419 | ⚪ NONE |
| 41 | unusual_recipient_flag | 0.410 | 6.82e-01 | 6.74e-01 | 0.0239 | ⚪ NONE |
| 42 | action_sequence_entropy | -0.276 | 7.82e-01 | 2.08e-30 | -0.0211 | ⚪ NONE |
| 43 | unique_recipients | -0.113 | 9.10e-01 | 9.79e-01 | -0.0064 | ⚪ NONE |
| 44 | emails_sent | -0.100 | 9.20e-01 | 9.92e-01 | -0.0057 | ⚪ NONE |
| 45 | cc_bcc_ratio | nan | nan | 1.00e+00 | 0.0000 | ⚪ NONE |
| 46 | email_content_sentiment | nan | nan | 1.00e+00 | 0.0000 | ⚪ NONE |
| 47 | usb_file_transfers | nan | nan | 1.00e+00 | 0.0000 | ⚪ NONE |

---

# 05 — Correlation Analysis

## Feature-to-Target (label) Correlations

| Rank | Feature | Pearson r | Spearman ρ | Direction |
|------|---------|----------|-----------|-----------|
| 1 | is_new_device | 0.592661 | 0.592661 | + |
| 2 | data_volume_mb | 0.531089 | 0.208459 | + |
| 3 | device_count | 0.504783 | 0.530224 | + |
| 4 | unique_pcs | 0.504783 | 0.530224 | + |
| 5 | cc_bcc_ratio | nan | nan | - |
| 6 | email_content_sentiment | nan | nan | - |
| 7 | usb_file_transfers | nan | nan | - |
| 8 | large_download_flag | 0.608613 | 0.608613 | + |
| 9 | role_boundary_crossings | 0.512066 | 0.570718 | + |
| 10 | longest_unusual_chain | 0.497888 | 0.613834 | + |
| 11 | data_egress_volume | 0.449901 | 0.195533 | + |
| 12 | access_to_role_ratio | 0.389868 | 0.570717 | + |
| 13 | novelty_score | 0.361006 | 0.199540 | + |
| 14 | avg_attachment_size | 0.335862 | 0.133273 | + |
| 15 | temporal_entropy | -0.296672 | -0.033275 | - |
| 16 | morning_vs_evening_ratio | -0.275992 | -0.107526 | - |
| 17 | login_regularity_score | 0.253651 | 0.007922 | + |
| 18 | usb_events | 0.250667 | 0.250667 | + |
| 19 | login_hour | 0.249140 | 0.053962 | + |
| 20 | peer_deviation_score | 0.229295 | 0.161441 | + |
| 21 | urls_visited | 0.224168 | 0.224168 | + |
| 22 | privilege_escalation_count | 0.209674 | 0.209674 | + |
| 23 | weekday_vs_weekend_ratio | 0.160841 | 0.148487 | + |
| 24 | geo_anomaly_flag | 0.158461 | 0.158461 | + |
| 25 | vpn_usage | 0.158461 | 0.158461 | + |
| 26 | session_duration_hrs | -0.120613 | -0.005900 | - |
| 27 | unique_systems_accessed | 0.116236 | 0.119241 | + |
| 28 | command_diversity_index | 0.112939 | 0.082192 | + |
| 29 | repeat_pattern_score | -0.112939 | -0.082192 | - |
| 30 | is_weekend | 0.101986 | 0.101986 | + |
| 31 | session_action_diversity | 0.058623 | 0.106719 | + |
| 32 | file_copy_count | 0.054645 | 0.100807 | + |
| 33 | logout_hour | 0.054521 | 0.033209 | + |
| 34 | behavioral_velocity | -0.038364 | -0.026120 | - |
| 35 | print_count | -0.035384 | -0.043624 | - |
| 36 | productive_vs_idle_ratio | -0.032009 | -0.019744 | - |
| 37 | cloud_upload_count | -0.030642 | -0.035023 | - |
| 38 | time_since_last_session | -0.021462 | -0.022840 | - |
| 39 | files_accessed | 0.020851 | 0.020514 | + |
| 40 | emails_received | -0.010794 | -0.009075 | - |
| 41 | is_after_hours | 0.009729 | 0.009729 | + |
| 42 | external_email_ratio | 0.007829 | 0.009659 | + |
| 43 | action_sequence_entropy | -0.006606 | 0.101660 | - |
| 44 | sensitive_file_access | 0.005749 | 0.159632 | + |
| 45 | unusual_recipient_flag | 0.003726 | 0.003726 | + |
| 46 | unique_recipients | -0.000980 | 0.000236 | - |
| 47 | emails_sent | -0.000872 | -0.000084 | - |

## Top Cross-Feature Correlations (|r| > 0.7)

| Feature A | Feature B | Correlation | Notes |
|-----------|-----------|-------------|-------|
| device_count | unique_pcs | 1.0000 | Near-duplicate |
| geo_anomaly_flag | vpn_usage | 1.0000 | Near-duplicate |
| command_diversity_index | repeat_pattern_score | -1.0000 | Near-duplicate |
| productive_vs_idle_ratio | behavioral_velocity | 0.9992 | Near-duplicate |
| emails_sent | unique_recipients | 0.9933 | Near-duplicate |
| action_sequence_entropy | session_action_diversity | 0.9281 | Strong |
| longest_unusual_chain | role_boundary_crossings | 0.8885 | Strong |
| command_diversity_index | behavioral_velocity | -0.8711 | Strong |
| repeat_pattern_score | behavioral_velocity | 0.8711 | Strong |
| productive_vs_idle_ratio | command_diversity_index | -0.8673 | Strong |
| productive_vs_idle_ratio | repeat_pattern_score | 0.8673 | Strong |
| is_new_device | role_boundary_crossings | 0.8640 | Strong |
| data_volume_mb | data_egress_volume | 0.8503 | Strong |
| access_to_role_ratio | longest_unusual_chain | 0.8015 | Moderate |
| is_new_device | longest_unusual_chain | 0.7883 | Moderate |
| login_hour | login_regularity_score | 0.7877 | Moderate |
| data_volume_mb | large_download_flag | 0.7669 | Moderate |
| login_regularity_score | access_to_role_ratio | 0.7655 | Moderate |
| logout_hour | session_duration_hrs | 0.7507 | Moderate |
| is_new_device | device_count | 0.7443 | Moderate |
| is_new_device | unique_pcs | 0.7443 | Moderate |
| data_volume_mb | device_count | 0.7430 | Moderate |
| data_volume_mb | unique_pcs | 0.7430 | Moderate |
| sensitive_file_access | novelty_score | 0.7224 | Moderate |
| session_duration_hrs | temporal_entropy | 0.7135 | Moderate |
| large_download_flag | role_boundary_crossings | 0.7073 | Moderate |
| unique_systems_accessed | action_sequence_entropy | 0.7039 | Moderate |
| unique_systems_accessed | session_action_diversity | 0.7021 | Moderate |
| device_count | large_download_flag | 0.7006 | Moderate |
| unique_pcs | large_download_flag | 0.7006 | Moderate |

---

# 06 — Feature Importance (Mutual Information)

| Rank | Feature | MI Score | Category | Notes |
|------|---------|---------|----------|-------|
| 1 | data_volume_mb | 0.051804 | Access Volume | ★ TOP |
| 2 | data_egress_volume | 0.044568 | Data Movement | ★ TOP |
| 3 | longest_unusual_chain | 0.037867 | Sequence | ★ TOP |
| 4 | unique_systems_accessed | 0.035901 | Access Volume | ★ TOP |
| 5 | large_download_flag | 0.035540 | Data Movement | ★ TOP |
| 6 | is_new_device | 0.034512 | Device & Location | ★ TOP |
| 7 | novelty_score | 0.034463 | Sequence | ★ TOP |
| 8 | role_boundary_crossings | 0.032444 | Sequence | ★ TOP |
| 9 | peer_deviation_score | 0.031481 | Behavioral Ratios | ★ TOP |
| 10 | unique_pcs | 0.030814 | Device & Location | ★ TOP |
| 11 | access_to_role_ratio | 0.030387 | Behavioral Ratios | ★ TOP |
| 12 | device_count | 0.030008 | Device & Location | ★ TOP |
| 13 | sensitive_file_access | 0.025988 | Data Movement | ★ TOP |
| 14 | avg_attachment_size | 0.023713 | Communication | ★ TOP |
| 15 | session_action_diversity | 0.022264 | Sequence | ★ TOP |
| 16 | morning_vs_evening_ratio | 0.021570 | Behavioral Ratios | ★ TOP |
| 17 | action_sequence_entropy | 0.019844 | Sequence | ★ TOP |
| 18 | weekday_vs_weekend_ratio | 0.018672 | Behavioral Ratios | ★ TOP |
| 19 | temporal_entropy | 0.018228 | Temporal | ★ TOP |
| 20 | session_duration_hrs | 0.012768 | Temporal | ★ TOP |
| 21 | repeat_pattern_score | 0.011385 | Sequence | ★ TOP |
| 22 | command_diversity_index | 0.011312 | Behavioral Ratios | ★ TOP |
| 23 | login_hour | 0.011311 | Temporal | ★ TOP |
| 24 | login_regularity_score | 0.010464 | Temporal | ★ TOP |
| 25 | file_copy_count | 0.008143 | Data Movement | ◆ Useful |
| 26 | logout_hour | 0.006428 | Temporal | ◆ Useful |
| 27 | usb_events | 0.006281 | Access Volume | ◆ Useful |
| 28 | privilege_escalation_count | 0.005793 | Sequence | ◆ Useful |
| 29 | urls_visited | 0.004326 | Access Volume | ○ Weak |
| 30 | print_count | 0.003741 | Data Movement | ○ Weak |
| 31 | behavioral_velocity | 0.002880 | Sequence | ○ Weak |
| 32 | emails_received | 0.002423 | Access Volume | ○ Weak |
| 33 | geo_anomaly_flag | 0.002255 | Device & Location | ○ Weak |
| 34 | cloud_upload_count | 0.002236 | Data Movement | ○ Weak |
| 35 | is_weekend | 0.002011 | Temporal | ○ Weak |
| 36 | productive_vs_idle_ratio | 0.001977 | Behavioral Ratios | ○ Weak |
| 37 | external_email_ratio | 0.001505 | Communication | ○ Weak |
| 38 | vpn_usage | 0.001383 | Device & Location | ○ Weak |
| 39 | is_after_hours | 0.001262 | Temporal | ○ Weak |
| 40 | time_since_last_session | 0.000855 | Temporal | ○ Weak |
| 41 | files_accessed | 0.000795 | Access Volume | ○ Weak |
| 42 | unique_recipients | 0.000777 | Communication | ○ Weak |
| 43 | emails_sent | 0.000172 | Access Volume | ○ Weak |
| 44 | cc_bcc_ratio | 0.000000 | Communication | ○ Weak |
| 45 | email_content_sentiment | 0.000000 | Communication | ○ Weak |
| 46 | unusual_recipient_flag | 0.000000 | Communication | ○ Weak |
| 47 | usb_file_transfers | 0.000000 | Data Movement | ○ Weak |

---

# 07 — Temporal Attack Pattern Analysis

How do insider features evolve relative to their attack window?


### EMP_001 — data_exfiltration (attack days 69-88)

| Feature | Pre-Attack μ | During Attack μ | Change | Multiplier |
|---------|-------------|----------------|--------|------------|
| data_volume_mb | 2.3382 | 35.4272 | 🔺 33.0890 | 15.15x |
| sensitive_file_access | 0.0000 | 1.6316 | 🔺 1.6316 | 999.00x |
| unique_systems_accessed | 4.0000 | 4.4737 | 🔺 0.4737 | 1.12x |
| usb_events | 0.0000 | 0.5263 | 🔺 0.5263 | 999.00x |
| is_after_hours | 0.9149 | 0.9474 | 🔺 0.0325 | 1.04x |
| novelty_score | 0.0000 | 2.1053 | 🔺 2.1053 | 999.00x |
| role_boundary_crossings | 0.0000 | 1.6316 | 🔺 1.6316 | 999.00x |
| behavioral_velocity | 4.6987 | 4.3205 | 🔻 0.3782 | 0.92x |

### EMP_005 — credential_compromise (attack days 83-88)

| Feature | Pre-Attack μ | During Attack μ | Change | Multiplier |
|---------|-------------|----------------|--------|------------|
| data_volume_mb | 2.3597 | 5.5208 | 🔺 3.1610 | 2.34x |
| sensitive_file_access | 0.0000 | 0.0000 | — 0.0000 | 1.00x |
| unique_systems_accessed | 4.0000 | 4.0000 | — 0.0000 | 1.00x |
| usb_events | 0.0000 | 0.0000 | — 0.0000 | 1.00x |
| is_after_hours | 0.9831 | 1.0000 | 🔺 0.0169 | 1.02x |
| novelty_score | 0.0000 | 2.0000 | 🔺 2.0000 | 999.00x |
| role_boundary_crossings | 0.0000 | 0.0000 | — 0.0000 | 1.00x |
| behavioral_velocity | 5.2704 | 5.1376 | 🔻 0.1329 | 0.97x |

### EMP_006 — data_exfiltration (attack days 68-87)

| Feature | Pre-Attack μ | During Attack μ | Change | Multiplier |
|---------|-------------|----------------|--------|------------|
| data_volume_mb | 2.3419 | 36.3277 | 🔺 33.9858 | 15.51x |
| sensitive_file_access | 0.0000 | 1.7222 | 🔺 1.7222 | 999.00x |
| unique_systems_accessed | 4.0000 | 4.5000 | 🔺 0.5000 | 1.12x |
| usb_events | 0.0000 | 0.5556 | 🔺 0.5556 | 999.00x |
| is_after_hours | 0.8298 | 1.0000 | 🔺 0.1702 | 1.21x |
| novelty_score | 0.0000 | 2.2222 | 🔺 2.2222 | 999.00x |
| role_boundary_crossings | 0.0000 | 1.7222 | 🔺 1.7222 | 999.00x |
| behavioral_velocity | 5.1428 | 5.3469 | 🔺 0.2040 | 1.04x |

### EMP_009 — pre_resignation_theft (attack days 54-82)

| Feature | Pre-Attack μ | During Attack μ | Change | Multiplier |
|---------|-------------|----------------|--------|------------|
| data_volume_mb | 2.3150 | 9.8267 | 🔺 7.5117 | 4.24x |
| sensitive_file_access | 0.0000 | 0.0000 | — 0.0000 | 1.00x |
| unique_systems_accessed | 4.0000 | 4.2273 | 🔺 0.2273 | 1.06x |
| usb_events | 0.0000 | 0.0000 | — 0.0000 | 1.00x |
| is_after_hours | 0.9189 | 0.8636 | 🔻 0.0553 | 0.94x |
| novelty_score | 0.0000 | 0.0000 | — 0.0000 | 1.00x |
| role_boundary_crossings | 0.0000 | 0.0000 | — 0.0000 | 1.00x |
| behavioral_velocity | 4.7869 | 5.0539 | 🔺 0.2670 | 1.06x |

### EMP_010 — credential_compromise (attack days 82-87)

| Feature | Pre-Attack μ | During Attack μ | Change | Multiplier |
|---------|-------------|----------------|--------|------------|
| data_volume_mb | 2.4081 | 6.7535 | 🔺 4.3454 | 2.80x |
| sensitive_file_access | 0.0000 | 0.0000 | — 0.0000 | 1.00x |
| unique_systems_accessed | 4.0000 | 4.0000 | — 0.0000 | 1.00x |
| usb_events | 0.0000 | 0.0000 | — 0.0000 | 1.00x |
| is_after_hours | 0.9464 | 1.0000 | 🔺 0.0536 | 1.06x |
| novelty_score | 0.0000 | 1.5000 | 🔺 1.5000 | 999.00x |
| role_boundary_crossings | 0.0000 | 0.0000 | — 0.0000 | 1.00x |
| behavioral_velocity | 5.0232 | 4.1450 | 🔻 0.8782 | 0.83x |

---

# 08 — Per-Scenario Statistical Fingerprints

Average feature values during active attack windows, grouped by scenario.


### data_exfiltration

| Feature | Mean | Std | Max | vs Normal Mean | Multiplier |
|---------|------|-----|-----|---------------|------------|
| data_volume_mb | 35.8653 | 18.4986 | 78.8060 | 2.2478 | 15.96x |
| sensitive_file_access | 1.6757 | 1.1317 | 3.0000 | 1.0719 | 1.56x |
| usb_events | 0.5405 | 0.5052 | 1.0000 | 0.0000 | 0.00x |
| is_after_hours | 0.9730 | 0.1644 | 1.0000 | 0.7609 | 1.28x |
| unique_systems_accessed | 4.4865 | 1.7098 | 6.0000 | 4.2728 | 1.05x |
| role_boundary_crossings | 1.6757 | 1.1317 | 3.0000 | 0.0000 | 0.00x |
| novelty_score | 2.1622 | 1.1429 | 3.0000 | 0.0614 | 35.23x |
| privilege_escalation_count | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00x |
| behavioral_velocity | 4.8198 | 2.0893 | 8.4848 | 4.4446 | 1.08x |
| geo_anomaly_flag | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00x |
| external_email_ratio | 0.2808 | 0.1922 | 0.7143 | 0.2966 | 0.95x |
| is_new_device | 0.8108 | 0.3971 | 1.0000 | 0.0000 | 0.00x |
| files_accessed | 6.6216 | 4.5604 | 16.0000 | 6.5513 | 1.01x |
| access_to_role_ratio | 0.2045 | 0.3412 | 1.0000 | 0.0000 | 0.00x |

### credential_compromise

| Feature | Mean | Std | Max | vs Normal Mean | Multiplier |
|---------|------|-----|-----|---------------|------------|
| data_volume_mb | 6.4351 | 2.1991 | 11.7150 | 2.2478 | 2.86x |
| sensitive_file_access | 0.0000 | 0.0000 | 0.0000 | 1.0719 | 0.00x |
| usb_events | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00x |
| is_after_hours | 1.0000 | 0.0000 | 1.0000 | 0.7609 | 1.31x |
| unique_systems_accessed | 4.3333 | 0.4924 | 5.0000 | 4.2728 | 1.01x |
| role_boundary_crossings | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00x |
| novelty_score | 1.3333 | 0.9847 | 2.0000 | 0.0614 | 21.72x |
| privilege_escalation_count | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00x |
| behavioral_velocity | 4.6088 | 0.9006 | 6.8053 | 4.4446 | 1.04x |
| geo_anomaly_flag | 0.6667 | 0.4924 | 1.0000 | 0.0000 | 0.00x |
| external_email_ratio | 0.2897 | 0.1552 | 0.5000 | 0.2966 | 0.98x |
| is_new_device | 0.6667 | 0.4924 | 1.0000 | 0.0000 | 0.00x |
| files_accessed | 7.0833 | 1.7299 | 10.0000 | 6.5513 | 1.08x |
| access_to_role_ratio | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00x |

### pre_resignation_theft

| Feature | Mean | Std | Max | vs Normal Mean | Multiplier |
|---------|------|-----|-----|---------------|------------|
| data_volume_mb | 11.0400 | 4.7946 | 20.7950 | 2.2478 | 4.91x |
| sensitive_file_access | 0.0000 | 0.0000 | 0.0000 | 1.0719 | 0.00x |
| usb_events | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00x |
| is_after_hours | 0.7556 | 0.4346 | 1.0000 | 0.7609 | 0.99x |
| unique_systems_accessed | 4.5556 | 1.1393 | 6.0000 | 4.2728 | 1.07x |
| role_boundary_crossings | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00x |
| novelty_score | 0.0000 | 0.0000 | 0.0000 | 0.0614 | 0.00x |
| privilege_escalation_count | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00x |
| behavioral_velocity | 4.6786 | 1.4932 | 7.3084 | 4.4446 | 1.05x |
| geo_anomaly_flag | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00x |
| external_email_ratio | 0.3174 | 0.2227 | 0.8000 | 0.2966 | 1.07x |
| is_new_device | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00x |
| files_accessed | 8.0000 | 4.0283 | 20.0000 | 6.5513 | 1.22x |
| access_to_role_ratio | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00x |

### privilege_escalation

| Feature | Mean | Std | Max | vs Normal Mean | Multiplier |
|---------|------|-----|-----|---------------|------------|
| data_volume_mb | 13.0155 | 10.2514 | 30.3530 | 2.2478 | 5.79x |
| sensitive_file_access | 8.8636 | 9.5533 | 33.0000 | 1.0719 | 8.27x |
| usb_events | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00x |
| is_after_hours | 0.8636 | 0.3513 | 1.0000 | 0.7609 | 1.13x |
| unique_systems_accessed | 5.0909 | 1.8234 | 7.0000 | 4.2728 | 1.19x |
| role_boundary_crossings | 3.5909 | 2.7544 | 7.0000 | 0.0000 | 0.00x |
| novelty_score | 1.5909 | 0.7341 | 2.0000 | 0.0614 | 25.92x |
| privilege_escalation_count | 0.6364 | 0.4924 | 1.0000 | 0.0000 | 0.00x |
| behavioral_velocity | 3.6509 | 1.8752 | 7.2553 | 4.4446 | 0.82x |
| geo_anomaly_flag | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00x |
| external_email_ratio | 0.2777 | 0.2955 | 1.0000 | 0.2966 | 0.94x |
| is_new_device | 0.7273 | 0.4558 | 1.0000 | 0.0000 | 0.00x |
| files_accessed | 2.0000 | 3.5456 | 13.0000 | 6.5513 | 0.31x |
| access_to_role_ratio | 0.3137 | 0.3813 | 1.0000 | 0.0000 | 0.00x |

### unauthorized_snooping

| Feature | Mean | Std | Max | vs Normal Mean | Multiplier |
|---------|------|-----|-----|---------------|------------|
| data_volume_mb | 16.1141 | 12.6478 | 53.6130 | 2.2478 | 7.17x |
| sensitive_file_access | 1.8971 | 1.1348 | 3.0000 | 1.0719 | 1.77x |
| usb_events | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00x |
| is_after_hours | 0.3824 | 0.4896 | 1.0000 | 0.7609 | 0.50x |
| unique_systems_accessed | 4.6176 | 1.7366 | 6.0000 | 4.2728 | 1.08x |
| role_boundary_crossings | 3.7941 | 2.2696 | 6.0000 | 0.0000 | 0.00x |
| novelty_score | 1.6765 | 0.7419 | 2.0000 | 0.0614 | 27.31x |
| privilege_escalation_count | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00x |
| behavioral_velocity | 3.2439 | 1.1382 | 5.4545 | 4.4446 | 0.73x |
| geo_anomaly_flag | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00x |
| external_email_ratio | 0.2640 | 0.2713 | 1.0000 | 0.2966 | 0.89x |
| is_new_device | 0.8382 | 0.3710 | 1.0000 | 0.0000 | 0.00x |
| files_accessed | 3.1471 | 2.6161 | 9.0000 | 6.5513 | 0.48x |
| access_to_role_ratio | 0.3455 | 0.4011 | 1.0000 | 0.0000 | 0.00x |

### slow_burn_recon

| Feature | Mean | Std | Max | vs Normal Mean | Multiplier |
|---------|------|-----|-----|---------------|------------|
| data_volume_mb | 3.9558 | 0.8580 | 6.2260 | 2.2478 | 1.76x |
| sensitive_file_access | 0.0000 | 0.0000 | 0.0000 | 1.0719 | 0.00x |
| usb_events | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00x |
| is_after_hours | 0.9291 | 0.2576 | 1.0000 | 0.7609 | 1.22x |
| unique_systems_accessed | 5.0000 | 0.0000 | 5.0000 | 4.2728 | 1.17x |
| role_boundary_crossings | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00x |
| novelty_score | 0.0000 | 0.0000 | 0.0000 | 0.0614 | 0.00x |
| privilege_escalation_count | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00x |
| behavioral_velocity | 3.9435 | 1.0720 | 6.7347 | 4.4446 | 0.89x |
| geo_anomaly_flag | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00x |
| external_email_ratio | 0.3446 | 0.2332 | 1.0000 | 0.2966 | 1.16x |
| is_new_device | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00x |
| files_accessed | 10.0472 | 3.8768 | 22.0000 | 6.5513 | 1.53x |
| access_to_role_ratio | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00x |

---

# 09 — Dead Feature Audit

Features with zero variance, constant values, or no discriminative power.

| Feature | Issue | Normal Unique | Insider Unique | Recommendation |
|---------|-------|--------------|----------------|----------------|
| urls_visited | DOMINANT value (99.9%) | 1 | 2 | DROP or REPLACE |
| usb_events | DOMINANT value (99.8%) | 1 | 2 | DROP or REPLACE |
| is_new_device | DOMINANT value (99.1%) | 1 | 2 | DROP or REPLACE |
| device_count | DOMINANT value (99.3%) | 1 | 3 | DROP or REPLACE |
| unique_pcs | DOMINANT value (99.3%) | 1 | 3 | DROP or REPLACE |
| geo_anomaly_flag | DOMINANT value (99.9%) | 1 | 2 | DROP or REPLACE |
| vpn_usage | DOMINANT value (99.9%) | 1 | 2 | DROP or REPLACE |
| cc_bcc_ratio | CONSTANT — zero information | 1 | 1 | DROP or REPLACE |
| email_content_sentiment | CONSTANT — zero information | 1 | 1 | DROP or REPLACE |
| usb_file_transfers | CONSTANT — zero information | 1 | 1 | DROP or REPLACE |
| large_download_flag | DOMINANT value (99.1%) | 1 | 2 | DROP or REPLACE |
| access_to_role_ratio | DOMINANT value (99.2%) | 1 | 58 | DROP or REPLACE |
| longest_unusual_chain | DOMINANT value (99.1%) | 1 | 8 | DROP or REPLACE |
| role_boundary_crossings | DOMINANT value (99.2%) | 1 | 8 | DROP or REPLACE |
| privilege_escalation_count | DOMINANT value (99.9%) | 1 | 2 | DROP or REPLACE |

**Dead features identified**: 15
**List**: urls_visited, usb_events, is_new_device, device_count, unique_pcs, geo_anomaly_flag, vpn_usage, cc_bcc_ratio, email_content_sentiment, usb_file_transfers, large_download_flag, access_to_role_ratio, longest_unusual_chain, role_boundary_crossings, privilege_escalation_count

---

# 10 — Cross-Feature Interaction Analysis

Testing multiplicative feature interactions for discrimination power.

| Interaction (A × B) | Normal μ | Insider μ | Ratio | Pearson r (with label) | Improvement over best individual |
|--------------------|---------|---------|----|-----|------|
| is_after_hours × sensitive_file_access | 0.8587 | 0.9293 | 1.08x | 0.002663 | -72.6% |
| usb_events × data_volume_mb | 0.0000 | 2.8668 | 999.00x | 0.231717 | -56.4% |
| is_new_device × geo_anomaly_flag | 0.0000 | 0.0257 | 999.00x | 0.158461 | -73.3% |
| role_boundary_crossings × data_egress_volume | 0.0000 | 7.4950 | 999.00x | 0.406746 | -20.6% |
| behavioral_velocity × novelty_score | 0.2123 | 3.0591 | 14.41x | 0.350351 | -3.0% |
| access_to_role_ratio × unique_systems_accessed | 0.0000 | 0.3547 | 999.00x | 0.469870 | +20.5% |
| privilege_escalation_count × is_after_hours | 0.0000 | 0.0450 | 999.00x | 0.209674 | +0.0% |
| files_accessed × is_after_hours | 5.2606 | 6.2508 | 1.19x | 0.031941 | +53.2% |
| external_email_ratio × data_volume_mb | 0.6920 | 3.5279 | 5.10x | 0.375513 | -29.3% |
| login_regularity_score × is_new_device | 0.0000 | 0.9736 | 999.00x | 0.324027 | -45.3% |

---

# 11 — Insider Behavioral Fingerprint

What makes insiders look different from normal employees?

## Top 15 Most Discriminative Features

| Rank | Feature | Cohen's d | Direction | Insider Behavior |
|------|---------|----------|-----------|-----------------|
| 1 | peer_deviation_score | 1.2308 | ↑ | Insiders have HIGHER peer_deviation_score (0.704 vs -0.018) |
| 2 | large_download_flag | 1.0983 | ↑ | Insiders have HIGHER large_download_flag (0.376 vs 0.000) |
| 3 | is_new_device | 1.0536 | ↑ | Insiders have HIGHER is_new_device (0.357 vs 0.000) |
| 4 | data_volume_mb | 1.0300 | ↑ | Insiders have HIGHER data_volume_mb (12.172 vs 2.248) |
| 5 | novelty_score | 0.9394 | ↑ | Insiders have HIGHER novelty_score (0.788 vs 0.061) |
| 6 | role_boundary_crossings | 0.8536 | ↑ | Insiders have HIGHER role_boundary_crossings (1.283 vs 0.000) |
| 7 | data_egress_volume | 0.8505 | ↑ | Insiders have HIGHER data_egress_volume (2.736 vs 0.339) |
| 8 | device_count | 0.8373 | ↑ | Insiders have HIGHER device_count (1.334 vs 1.000) |
| 9 | unique_pcs | 0.8373 | ↑ | Insiders have HIGHER unique_pcs (1.334 vs 1.000) |
| 10 | longest_unusual_chain | 0.8220 | ↑ | Insiders have HIGHER longest_unusual_chain (0.842 vs 0.000) |
| 11 | morning_vs_evening_ratio | -0.8138 | ↓ | Insiders have LOWER morning_vs_evening_ratio (0.264 vs 0.340) |
| 12 | weekday_vs_weekend_ratio | 0.7740 | ↑ | Insiders have HIGHER weekday_vs_weekend_ratio (0.102 vs 0.023) |
| 13 | avg_attachment_size | 0.6489 | ↑ | Insiders have HIGHER avg_attachment_size (3.207 vs 0.666) |
| 14 | temporal_entropy | -0.6158 | ↓ | Insiders have LOWER temporal_entropy (1.985 vs 2.281) |
| 15 | access_to_role_ratio | 0.6062 | ↑ | Insiders have HIGHER access_to_role_ratio (0.122 vs 0.000) |

## Summary: The Insider Fingerprint

Based on the analysis, insider threat activity is characterized by:

- **peer_deviation_score**: elevated (Cohen's d = 1.231)
- **large_download_flag**: elevated (Cohen's d = 1.098)
- **is_new_device**: elevated (Cohen's d = 1.054)
- **data_volume_mb**: elevated (Cohen's d = 1.030)
- **novelty_score**: elevated (Cohen's d = 0.939)
- **role_boundary_crossings**: elevated (Cohen's d = 0.854)
- **data_egress_volume**: elevated (Cohen's d = 0.851)
- **device_count**: elevated (Cohen's d = 0.837)