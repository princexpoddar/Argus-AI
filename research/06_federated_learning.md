# 06 — Federated Learning Experiment Results

**Privacy Budget**: ε=2.0, δ=1e-5

**Rounds**: 10, **Local Epochs**: 3

---

## Privacy Guarantee

- **ε-Differential Privacy**: ε=0.025 (budget: 2.0)

- **Noise multiplier**: σ=0.6656

- **Gradient clipping**: C=1.0

- **Raw data shared**: ZERO records (only gradient updates)


## Department Participation

| Department | Samples | Positive | Negative |
|------------|---------|----------|----------|
| retail_banking | 3811 | 71 | 3740 |
| treasury | 1593 | 0 | 1593 |
| it_admin | 2225 | 22 | 2203 |
| hr | 1909 | 68 | 1841 |
| compliance | 3172 | 150 | 3022 |

## Training Convergence

| Round | Avg Loss |
|-------|----------|
| 1 | 1.0478 |
| 2 | 0.9480 |
| 3 | 0.8990 |
| 4 | 0.8592 |
| 5 | 0.8274 |
| 6 | 0.7782 |
| 7 | 0.7413 |
| 8 | 0.7096 |
| 9 | 0.7218 |
| 10 | 0.7278 |

## DPDPA Compliance

- ✅ **Data Minimization**: Only gradient updates are shared, never raw employee data
- ✅ **Purpose Limitation**: Gradients are used only for model improvement
- ✅ **Storage Limitation**: Raw data stays local to each department
- ✅ **Consent**: Each department explicitly participates in FL rounds
- ✅ **Security**: Gaussian noise prevents gradient inversion attacks