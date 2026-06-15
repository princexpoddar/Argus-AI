# Data Pipeline — Source to Model

**Date**: 2026-06-16
**Author**: Argus AI Team
**Status**: Production

---

## Overview

Argus AI uses **100% synthetic data** generated to simulate realistic Indian banking employee
behavior. No real Bank of India data is used. The pipeline flows through 4 layers:

```
Raw Generation → Feature Engineering (47) → Enhancement (211) → Model Input (7-day sequences)
```

**Scale**: 200 employees × 90 days × ~28 actions/day = **505,023 raw events** → **11,510 employee-day feature vectors** × 211 dimensions.

---

## Layer 1: Raw Synthetic Data

The synthetic generator (`argus/data/synthetic_generator.py`) produces 3 CSV files:

### 1.1 Employee Roster — `employees.csv`

| Property | Value |
|----------|-------|
| Rows | 200 |
| Columns | 16 |
| Purpose | Static employee profiles with behavioral baselines |

**Schema**:

| Column | Type | Description |
|--------|------|-------------|
| `emp_id` | str | Unique identifier (EMP_001 to EMP_200) |
| `name` | str | Indian name (e.g., "Aarav Sharma") |
| `department` | str | One of 5 departments |
| `role` | str | One of 14 role types |
| `clearance_level` | int | 1–5 (teller=1, system_admin=5) |
| `branch` | str | 8 Indian city branches |
| `tenure_months` | int | Employment duration (Poisson ~36 months) |
| `hire_date` | date | Computed from tenure |
| `typical_login_hour` | float | Gaussian baseline (e.g., 9.25 ± 0.3 for relationship_manager) |
| `typical_logout_hour` | float | Gaussian baseline (e.g., 18.5 ± 0.4) |
| `typical_actions_per_day` | int | Gaussian baseline (e.g., 45 ± 12) |
| `typical_records_per_day` | int | Gaussian baseline (e.g., 55 ± 15) |
| `is_insider` | bool | Ground truth label |
| `insider_scenario` | str | Attack type (null for normal employees) |
| `attack_start_day` | int | Day index when attack begins |
| `attack_end_day` | int | Day index when attack ends |

**Department Distribution**:

| Department | Count | Roles |
|------------|-------|-------|
| Retail Banking | 60 | relationship_manager, teller, branch_manager |
| Treasury | 30 | trader, treasury_analyst |
| IT Admin | 40 | system_admin, dba_admin, help_desk |
| HR | 35 | hr_generalist, recruiter, payroll |
| Compliance | 35 | aml_analyst, auditor, risk_officer |

### 1.2 Activity Log — `activity_log.csv`

| Property | Value |
|----------|-------|
| Rows | 505,023 |
| Columns | 15 |
| Purpose | Every individual action performed by every employee over 90 days |

**Schema**:

| Column | Type | Description |
|--------|------|-------------|
| `event_id` | str | Unique event ID (EVT_EMP001_042_0007) |
| `timestamp` | datetime | ISO-8601 timestamp of the action |
| `emp_id` | str | Employee who performed the action |
| `day_index` | int | Day number (0–89) |
| `action_type` | str | What the employee did (see action taxonomy below) |
| `system` | str | Which system was accessed (see system list below) |
| `resource` | str | Resource category (customer_records, treasury_data, etc.) |
| `records_accessed` | int | Number of records touched (Poisson distributed) |
| `data_volume_mb` | float | Data transferred in MB (exponential distributed) |
| `device_id` | str | Workstation identifier (WS_MUM_042) |
| `ip_address` | str | Internal IP (10.x.x.x) |
| `is_after_hours` | bool | True if action occurred before 9am or after 6pm |
| `is_new_device` | bool | True if device not previously seen for this employee |
| `is_weekend` | bool | True if Saturday or Sunday |
| `geo_location` | str | Branch location (matches employee's assigned branch) |

**Generation Techniques**:

| Aspect | Method | Reference |
|--------|--------|-----------|
| Action sequences | Markov Chain across system states | Le & Zincir-Heywood, 2021 |
| Login/logout times | Gaussian Mixture Model per role | Yuan & Wu, 2021 |
| Records accessed | Poisson distribution scaled by role baseline | — |
| Data volume | Exponential distribution scaled by role | — |
| Weekend/sick absence | Bernoulli (5% weekend work, 3% sick day) | — |

### 1.3 Ground Truth — `ground_truth.csv`

| Property | Value |
|----------|-------|
| Rows | 14 |
| Columns | 9 |
| Purpose | Labels identifying which employees are insiders and their attack type |

**Schema**: `emp_id, name, department, role, is_insider, scenario, attack_start_day, attack_end_day, description`

**Insider rate**: 14/200 employees (7%), 333/11,510 employee-days (2.9%)

---

## Layer 2: Attack Scenario Injection

6 insider threat scenarios are injected via perturbation of normal activity patterns.
Each scenario has a ramp-up phase (gradual behavioral shift) and an attack phase (active threat).

### Scenario Details

#### 1. Data Exfiltration
- **Description**: Bulk customer data download via USB after hours
- **Eligible roles**: relationship_manager, teller, aml_analyst
- **Timeline**: 14-day ramp-up → 5-day attack
- **Perturbations**:
  - After-hours activity probability: 80%
  - Records accessed: ramp from 1.5× to 15× baseline
  - Data volume: 12× multiplier
  - USB device connection
  - Access to `Customer_Records_DB` (normally forbidden)
  - File copy probability: 90%

#### 2. Privilege Escalation
- **Description**: IT admin using superadmin credentials on production systems
- **Eligible roles**: help_desk, system_admin, dba_admin
- **Timeline**: 7-day ramp-up → 3-day attack
- **Perturbations**:
  - After-hours: 60%
  - Access to `Production_CBS` and `Audit_Logs`
  - Privilege escalation events
  - Admin account creation
  - Records: ramp from 1× to 5×

#### 3. Pre-Resignation Theft
- **Description**: Employee downloading data before leaving the organization
- **Eligible roles**: relationship_manager, treasury_analyst, aml_analyst, trader
- **Timeline**: 21-day ramp-up → 7-day attack
- **Perturbations**:
  - Job search activity: 40%
  - Records: ramp from 1.2× to 5×
  - External emails: 3× multiplier
  - Cloud upload probability: 50%
  - Large attachments: 60%

#### 4. Unauthorized Snooping
- **Description**: HR employee accessing customer financial records without authorization
- **Eligible roles**: hr_generalist, recruiter, payroll
- **Timeline**: 21-day ramp-up → 14-day attack
- **Perturbations**:
  - Access to `CBS` and `Customer_Records_DB` (outside HR scope)
  - Records: ramp from 1× to 2.5×
  - Cross-role access flag

#### 5. Credential Compromise
- **Description**: Account used from two locations simultaneously (impossible travel)
- **Eligible roles**: relationship_manager, branch_manager, system_admin
- **Timeline**: 0-day ramp-up → 5-day attack (sudden onset)
- **Perturbations**:
  - Geographic anomaly (multiple branch logins)
  - Rapid system switching
  - New device probability: 90%
  - Records: 3× to 5× spike
  - Login time anomaly

#### 6. Slow-Burn Reconnaissance
- **Description**: Gradually expanding access scope over weeks
- **Eligible roles**: system_admin, dba_admin, aml_analyst, risk_officer
- **Timeline**: 30-day ramp-up → 30-day attack (longest campaign)
- **Perturbations**:
  - 1 new system access per week
  - Records: ramp from 1.05× to 1.5× (very subtle)
  - Data volume: 5% daily growth

---

## Layer 3: Feature Engineering

### Stage 1 — Base Features (47 dimensions)

**Script**: `argus/data/feature_engineer.py`
**Input**: 505,023 raw activity events
**Output**: 11,510 employee-day rows × 47 features

Each employee-day's ~28 raw events are aggregated into 47 features across 7 categories:

#### Temporal Features (8)

| Feature | Computation |
|---------|-------------|
| `login_hour` | Hour of first login event (fractional, e.g., 9.25 = 9:15 AM) |
| `logout_hour` | Hour of last logout event |
| `session_duration_hrs` | logout_hour − login_hour |
| `is_weekend` | 1 if Saturday/Sunday |
| `is_after_hours` | 1 if any action before 9am or after 6pm |
| `time_since_last_session` | Hours since previous day's logout |
| `login_regularity_score` | |login_hour − 9.0| (deviation from expected 9am) |
| `temporal_entropy` | Shannon entropy of action timestamps across hours |

#### Access Volume Features (7)

| Feature | Computation |
|---------|-------------|
| `files_accessed` | Count of file/doc/view actions |
| `emails_sent` | Count of send_email actions |
| `emails_received` | Count of read_email actions |
| `urls_visited` | Count of browse/web actions |
| `usb_events` | Count of USB-related actions |
| `data_volume_mb` | Sum of data_volume_mb across all events |
| `unique_systems_accessed` | Count of distinct systems used that day |

#### Device & Location Features (5)

| Feature | Computation |
|---------|-------------|
| `is_new_device` | 1 if any event on a previously unseen device |
| `device_count` | Number of distinct device IDs used |
| `unique_pcs` | Number of distinct non-USB devices |
| `geo_anomaly_flag` | 1 if events from multiple geographic locations |
| `vpn_usage` | 1 if VPN-like IP pattern detected |

#### Communication Features (6)

| Feature | Computation |
|---------|-------------|
| `external_email_ratio` | External emails / total emails |
| `avg_attachment_size` | data_volume_mb / emails_sent |
| `unique_recipients` | Proxy: max(1, emails_sent) |
| `cc_bcc_ratio` | Placeholder (always 0) — dropped in enhancement |
| `email_content_sentiment` | Placeholder (always 0) — dropped in enhancement |
| `unusual_recipient_flag` | 1 if external_email > 3 |

#### Data Movement Features (7)

| Feature | Computation |
|---------|-------------|
| `file_copy_count` | Count of copy/export actions |
| `usb_file_transfers` | Count of USB transfer actions (excl. connect) |
| `large_download_flag` | 1 if data_volume_mb > 10 |
| `sensitive_file_access` | Count of actions on SENSITIVE_SYSTEMS |
| `data_egress_volume` | data_volume × (0.3 if copy/USB, else 0.05) |
| `print_count` | Count of print actions |
| `cloud_upload_count` | Count of cloud/upload actions |

#### Behavioral Ratio Features (6)

| Feature | Computation |
|---------|-------------|
| `access_to_role_ratio` | Out-of-scope system accesses / total actions |
| `peer_deviation_score` | Z-score vs department peers (computed in post-pass) |
| `weekday_vs_weekend_ratio` | Context-dependent ratio |
| `morning_vs_evening_ratio` | Actions before noon / total actions |
| `productive_vs_idle_ratio` | Actions per quarter-hour of session |
| `command_diversity_index` | Unique action types / total actions |

#### Sequence Features (8)

| Feature | Computation |
|---------|-------------|
| `action_sequence_entropy` | Shannon entropy of action type distribution |
| `longest_unusual_chain` | Max consecutive out-of-scope actions |
| `role_boundary_crossings` | Total out-of-scope system accesses |
| `privilege_escalation_count` | Count of escalation/superadmin actions |
| `session_action_diversity` | Count of unique action types used |
| `repeat_pattern_score` | 1 − command_diversity_index |
| `novelty_score` | Sum of binary flags: new_device + geo_anomaly + usb + sensitive |
| `behavioral_velocity` | Total actions / session duration |

### Stage 2 — Enhanced Features (47 → 211)

**Script**: `argus/data/enhanced_feature_engineer.py`
**Based on**: Deep investigation findings (dead feature analysis, correlation study)

#### Step 1: Drop Dead Features (−7)

Removed 7 features that are constant-zero, perfectly correlated (r=1.0), or redundant:

| Dropped Feature | Reason |
|----------------|--------|
| `cc_bcc_ratio` | Always 0 (no CC/BCC simulation) |
| `email_content_sentiment` | Always 0 (no NLP simulation) |
| `usb_file_transfers` | Always 0 (USB events tracked differently) |
| `unique_pcs` | r=1.0 with device_count |
| `vpn_usage` | r=1.0 with geo_anomaly_flag |
| `repeat_pattern_score` | r=−1.0 with command_diversity_index |
| `productive_vs_idle_ratio` | r=0.999 with behavioral_velocity |

#### Step 2: Temporal Deltas (+24 features)

Day-over-day change and absolute change for 12 key features:

```
delta_{feature}     = value_today − value_yesterday
abs_delta_{feature} = |delta_{feature}|
```

**Features**: data_volume_mb, files_accessed, unique_systems_accessed, sensitive_file_access, login_hour, session_duration_hrs, behavioral_velocity, data_egress_volume, novelty_score, role_boundary_crossings, access_to_role_ratio, avg_attachment_size

#### Step 3: Rolling Window Statistics (+96 features)

For 12 features × 2 windows (7d, 14d) × 4 statistics = 96:

| Statistic | Purpose |
|-----------|---------|
| `roll_{7d,14d}_mean_{feature}` | Smoothed trend |
| `roll_{7d,14d}_std_{feature}` | Volatility / instability |
| `roll_{7d,14d}_max_{feature}` | Peak detection |
| `roll_{7d,14d}_sum_{feature}` | Cumulative activity |

**Features windowed**: data_volume_mb, files_accessed, sensitive_file_access, usb_events, is_after_hours, data_egress_volume, novelty_score, role_boundary_crossings, is_new_device, access_to_role_ratio, device_count, large_download_flag

#### Step 4: Velocity & Acceleration (+10 features)

```
velocity_{feature}  = 7-day rolling mean of delta_{feature}
accel_{feature}     = day-over-day change in velocity_{feature}
```

**Features**: data_volume_mb, files_accessed, sensitive_file_access, data_egress_volume, unique_systems_accessed

#### Step 5: Feature Interactions (+13 features)

Multiplicative pairs selected from deep investigation (top discriminative combinations):

| Interaction | Signal |
|-------------|--------|
| access_to_role_ratio × unique_systems_accessed | +20.5% improvement |
| role_boundary_crossings × data_egress_volume | Out-of-scope + data leaving |
| behavioral_velocity × novelty_score | Fast + unusual = suspicious |
| is_after_hours × sensitive_file_access | After-hours sensitive access |
| usb_events × data_volume_mb | USB + large transfers |
| is_new_device × data_volume_mb | New device + large data |
| is_new_device × role_boundary_crossings | New device + out-of-scope |
| data_volume_mb × login_regularity_score | Large data + irregular login |
| files_accessed × is_after_hours | File access after hours |
| external_email_ratio × data_volume_mb | External email + data |
| sensitive_file_access × is_after_hours | Sensitive after hours |
| novelty_score × is_after_hours | Novel behavior after hours |
| data_volume_mb × is_weekend | Weekend data transfers |

#### Step 6: Peer Z-Scores (+18 features)

Department-level and role-level z-scores for 8 features, plus 2 aggregate:

```
zscore_dept_{feature} = (value − dept_mean) / dept_std
zscore_role_{feature} = (value − role_mean) / role_std
```

**Features**: data_volume_mb, files_accessed, unique_systems_accessed, login_hour, session_duration_hrs, data_egress_volume, sensitive_file_access, novelty_score

**Aggregates**: `max_dept_zscore` (worst deviation), `mean_dept_zscore` (average deviation)

#### Step 7: Cumulative Risk Indicators (+10 features)

| Feature | Computation |
|---------|-------------|
| `is_anomalous_day` | 1 if novelty_score > 0 |
| `anomaly_streak` | 7-day rolling sum of anomalous days |
| `expanding_max_systems` | Historical max of systems accessed |
| `expanding_max_data_volume` | Historical max of data volume |
| `data_volume_vs_personal_max` | Today's volume / personal historical max |
| `cum_7d_usb_events` | 7-day cumulative USB events |
| `cum_7d_is_new_device` | 7-day cumulative new device days |
| `cum_7d_large_download_flag` | 7-day cumulative large downloads |
| `cum_7d_is_after_hours` | 7-day cumulative after-hours days |
| `cum_7d_geo_anomaly_flag` | 7-day cumulative geo anomalies |
| `clearance_normalized` | clearance_level / 5.0 (0.2 to 1.0) |

---

## Layer 4: Model Input

### Sequence Construction

The 211-feature employee-day vectors are organized into **7-day sliding windows**:

```
Input shape:  (11,510, 7, 211)
              ───────  ─  ───
              samples  │  features
                       │
                   7-day window
```

Each sample represents 7 consecutive days of one employee's behavior.
The label is 1 if **any** day in the window is an insider attack day.

### Model Consumption

| Model | Input Format | How |
|-------|-------------|-----|
| LightGBM | `(11510, 211)` | Last timestep: `X[:, -1, :]` |
| XGBoost | `(11510, 211)` | Last timestep: `X[:, -1, :]` |
| LSTM-AE | `(11510, 7, 211)` | Full sequence |
| Isolation Forest | `(11510, 211)` | Last timestep |

---

## System & Action Taxonomy

### 24 Banking Systems Simulated

| Category | Systems |
|----------|---------|
| **Customer-facing** | CRM, CBS (Core Banking System), Teller_Terminal |
| **Treasury** | Treasury_Platform, Bloomberg |
| **IT Infrastructure** | Admin_Console, Servers, DB_Console, Staging_DB, JIRA |
| **HR & Admin** | HRMS, Payroll_System, ATS, Documents |
| **Compliance** | AML_Platform, Audit_System, Risk_Platform |
| **Communication** | Email, Reports, Ticketing, AD_Console, Web_Browser |
| **Threat-only** | Production_CBS, Customer_Records_DB, Treasury_DB, Audit_Logs |

### 70+ Action Types

Examples by system:
- **CBS**: account_lookup, transaction_view, balance_check, statement_gen
- **Email**: read_email, send_email, send_email_external, download_attachment
- **Admin_Console**: config_change, user_management, log_review, system_check
- **AML_Platform**: alert_review, case_create, sar_filing, rule_config
- **Production_CBS** (threat): direct_query, data_export, schema_modify

### 6 Sensitive Systems

Systems that flag `sensitive_file_access` when accessed:
`Production_CBS, Customer_Records_DB, Treasury_DB, Audit_Logs, Admin_Console, Servers`

---

## Data Quality Validation

| Metric | Value |
|--------|-------|
| Null rate (after enhancement) | <0.1% (filled with 0) |
| Infinity values | 0 (cleaned to 0) |
| Class balance | 2.9% positive (333/11,510 employee-days) |
| Employee coverage | 200/200 (100%) |
| Day coverage | 90 days per employee (weekends/sick excluded) |
| KS separation (top features) | p < 0.001 for top 15 discriminative features |
| Feature correlation (post-cleanup) | No r=1.0 duplicates remain |

---

## File Locations

| File | Path | Size |
|------|------|------|
| Employee roster | `data/synthetic/employees.csv` | ~15 KB |
| Activity log | `data/synthetic/activity_log.csv` | ~80 MB |
| Ground truth | `data/synthetic/ground_truth.csv` | ~1 KB |
| Base features | `data/processed/features_47d.csv` | 2.5 MB |
| Enhanced features | `data/processed/features_enhanced.csv` | 20 MB |
| Feature columns | `data/processed/enhanced_feature_cols.json` | 7 KB |
| LSTM sequences | `data/processed/X_enhanced.npy` | 68 MB |
| Labels | `data/processed/y_enhanced.npy` | 46 KB |

---

## Research Basis

| Technique | Paper |
|-----------|-------|
| Markov Chain activity models | Le & Zincir-Heywood, "Evaluating Insider Threat Detection Workflow Using Supervised and Unsupervised Learning" (CNSM 2021) |
| Gaussian Mixture temporal distributions | Yuan & Wu, "Deep Learning for Insider Threat Detection" (IEEE 2021) |
| CERT scenario methodology | Glasser & Lindauer, "Bridging the Gap: A Pragmatic Approach to Generating Insider Threat Data" (IEEE S&P 2013) |
| Perturbation-based threat generation | Adapted from CERT r4.2 synthetic injection methodology |
| Feature interaction selection | Deep investigation notebook (access_to_role × systems = +20.5%) |
| Rolling window temporal features | Standard time-series feature engineering for anomaly detection |
