<p align="center">
  <h1 align="center">🔱 Argus AI</h1>
  <p align="center">
    <strong>Privacy-Preserving Digital Employee Twins for Continuous Insider Threat Detection in Banking Environments</strong>
  </p>
  <p align="center">
    <a href="#architecture">Architecture</a> •
    <a href="#features">Features</a> •
    <a href="#tech-stack">Tech Stack</a> •
    <a href="#getting-started">Getting Started</a> •
    <a href="#documentation">Documentation</a>
  </p>
</p>

---

## 🎯 Problem Statement

> Design a **privacy-first, risk-based Identity Trust framework** that continuously validates customer and enterprise identities across digital channels. Detect high-risk events — anomalous behavior, new device usage, suspicious onboarding or account recovery attempts, and misuse of privileged access — and trigger real-time verification only when risk levels are elevated.

**Our Focus**: **Insider Threats in Banking** — detecting employees, contractors, and admins who misuse privileged access to download customer data, access unauthorized accounts, or exfiltrate sensitive information.

---

## 💡 The Idea: Digital Employee Twins

Most teams will build: `Login → Risk Score → OTP`

**We build**: `Employee Behavior → Digital Twin → Trust Score → Privileged Access Monitoring`

### What is a Digital Employee Twin?

A **behavioral twin** is a dynamic, compressed representation of every employee's "normal" behavior. It captures:

| Dimension | What It Learns | How It's Used |
|-----------|---------------|---------------|
| 🕐 **Circadian Rhythms** | When they login, session durations, daily patterns | Detect after-hours access |
| 🖥️ **Access Topology** | Which systems, databases, and resources they use | Detect cross-role access |
| 📊 **Data Patterns** | Normal download volumes, record access counts | Detect bulk exfiltration |
| 🔄 **Behavioral Velocity** | How fast their behavior is changing | Detect sudden behavioral shifts |
| 👥 **Peer Context** | How they compare to colleagues in the same role | Detect slow-burn normalization |

Current activity is **continuously compared against the twin**. Deviations trigger risk elevation — but only when they matter.

---

## 🏗️ Architecture

<a name="architecture"></a>

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           ARGUS AI PLATFORM                              │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐   │
│  │  Data Layer  │  │ Behavioral  │  │   Risk      │  │  Privilege   │   │
│  │             │  │  Profiling   │  │   Scoring   │  │   Context    │   │
│  │ • CERT r4.2 │→│  Engine      │→│   Engine    │→│   Engine     │   │
│  │ • Synthetic │  │             │  │             │  │              │   │
│  │   Banking   │  │ • Feature   │  │ • LSTM AE   │  │ • Role-Risk  │   │
│  │   Data Gen  │  │   Pipeline  │  │ • Isolation  │  │   Matrix     │   │
│  │             │  │ • Digital   │  │   Forest    │  │ • Privilege  │   │
│  │             │  │   Twin      │  │ • Hybrid    │  │   Decay Fn   │   │
│  │             │  │   Builder   │  │   Ensemble  │  │ • Dynamic    │   │
│  │             │  │ • Behavioral│  │             │  │   Trust Score│   │
│  │             │  │   Genome    │  │             │  │   (0-100)    │   │
│  └─────────────┘  └─────────────┘  └─────────────┘  └──────────────┘   │
│         │                                                    │           │
│         ▼                                                    ▼           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                  Explainable Alert Engine                        │   │
│  │                                                                  │   │
│  │  • Intent Signal Chain Detection (attack narrative recognition)  │   │
│  │  • Natural Language Alert Generation                             │   │
│  │  • Peer Constellation Comparison                                 │   │
│  │  • Recommended Actions                                           │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│         │                                                                │
│         ▼                                                                │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │              Interactive Monitoring Dashboard                    │   │
│  │                                                                  │   │
│  │  Trust Heatmap │ Alert Queue │ Twin Comparison │ Privilege Decay  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │           Privacy Layer (Cross-Department FL + DP)                │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

<a name="features"></a>

### 🧬 Module 1: Digital Employee Twin (Behavioral Genome)
- Builds a multi-dimensional behavioral profile for every employee
- Captures circadian rhythms via Fourier coefficients
- Tracks access topology, data patterns, and behavioral velocity
- Living model that evolves with the employee over time

### 🧠 Module 2: Hybrid Risk Scoring Engine
- **LSTM Autoencoder** — detects temporal anomalies (behavior unusual given recent history)
- **Isolation Forest** — detects static anomalies (extreme single-day deviations)
- **XGBoost + LightGBM** — supervised classifiers with 211 engineered features
- **Meta-Learner Ensemble** — stacks all 4 models for SOTA detection (F1=0.95, AUC=0.98)

### 🔐 Module 3: Privilege Context Engine
- Role-Resource risk matrix (same action = different risk for different roles)
- **Privilege Decay Function** — trust decays exponentially without normal behavior reinforcement
- Dynamic Trust Score (0-100) with real-time updates

### 🔍 Module 4: Explainable Alert Engine
- **Intent Signal Chains** — detects attack *narratives* (suspicious sequences), not isolated events
- Natural language alerts explaining *why* the risk is elevated
- **Peer Constellation Analysis** — compares against peer group, not just self-history

### 🛡️ Module 5: Privacy-Preserving Intelligence
- Cross-department Federated Learning (model gradients only, never raw data)
- Differential Privacy (ε-DP) on gradient updates
- Aligned with India's Digital Personal Data Protection Act

---

## 🛠️ Tech Stack

<a name="tech-stack"></a>

### Backend (Python ML Pipeline)

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| **Core ML** | PyTorch | 2.x | LSTM Autoencoder (temporal anomaly detection) |
| **Classical ML** | scikit-learn | 1.5+ | Isolation Forest, preprocessing, metrics |
| **Gradient Boosting** | XGBoost | 2.x | Baseline comparisons |
| **Data Processing** | pandas, numpy | Latest | Feature engineering, data manipulation |
| **Synthetic Data** | SDV (CTGAN) | 1.x | Synthetic data experiment (SMOTE preferred for augmentation) |
| **Explainability** | SHAP | 0.45+ | Feature-level explanations |
| **API** | FastAPI | 0.110+ | Real-time scoring REST API (<200ms) |
| **API Server** | Uvicorn | Latest | ASGI server for FastAPI |
| **Experiment Tracking** | MLflow | 2.x | Model versioning & experiment management |
| **Statistical** | scipy | Latest | Statistical tests, distributions |

### Frontend (Dashboard)

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| **Framework** | Next.js | 14+ | React-based dashboard application |
| **Language** | TypeScript | 5.x | Type-safe frontend development |
| **Charts** | Chart.js + react-chartjs-2 | 4.x | Interactive visualizations |
| **Additional Charts** | Recharts | 2.x | Trust score heatmaps, timelines |
| **Styling** | Vanilla CSS | — | Custom premium design system |
| **HTTP Client** | Axios | 1.x | API communication with Python backend |

### Data & Privacy

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Federated Learning** | Flower | Cross-department model training |
| **Differential Privacy** | Opacus | Gradient-level privacy |
| **Data Validation** | Pydantic | Schema validation for data pipeline |

### DevOps & Tooling

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Environment** | Python 3.11+ venv | Isolated Python environment |
| **Package Manager** | pip + requirements.txt | Dependency management |
| **Version Control** | Git + GitHub | Source control |
| **GPU Support** | CUDA 12.x | Local GPU acceleration for PyTorch |
| **Notebooks** | Jupyter Lab | Exploratory data analysis |

---

## 📁 Project Structure

```
C:\Github\BOB Hackathon\
│
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── .gitignore                          # Git ignore rules
├── .env.example                        # Environment variable template
│
├── docs/                               # 📚 Project documentation
│   ├── IDEA_PROPOSAL.md               # Detailed idea & approach
│   ├── ARCHITECTURE.md                # System architecture deep-dive
│   ├── TECH_STACK.md                  # Technology stack details
│   ├── DATA_STRATEGY.md              # Dataset selection & synthetic generation
│   ├── BUILD_GUIDE.md                # Step-by-step build instructions
│   └── RESEARCH_REFERENCES.md        # Academic references & papers
│
├── argus/                              # 🐍 Python ML Backend
│   ├── __init__.py
│   ├── config.py                      # Global configuration
│   │
│   ├── data/                          # Data pipeline
│   │   ├── __init__.py
│   │   ├── cert_loader.py            # CERT r4.2 data loader
│   │   ├── synthetic_generator.py    # Banking synthetic data generator
│   │   ├── feature_engineer.py       # 47-feature extraction pipeline
│   │   └── schemas.py                # Pydantic data schemas
│   │
│   ├── models/                        # ML models
│   │   ├── __init__.py
│   │   ├── behavioral_twin.py        # Digital Employee Twin
│   │   ├── lstm_autoencoder.py       # Temporal anomaly detection
│   │   ├── isolation_forest.py       # Static anomaly detection
│   │   ├── risk_engine.py            # Hybrid ensemble scorer
│   │   ├── privilege_engine.py       # Role-aware risk + decay
│   │   └── explainer.py             # Intent chains + NL alerts
│   │
│   ├── privacy/                       # Privacy-preserving layer
│   │   ├── __init__.py
│   │   └── federated.py             # Federated learning architecture
│   │
│   ├── api/                           # REST API
│   │   ├── __init__.py
│   │   └── scoring_api.py           # FastAPI scoring endpoint
│   │
│   └── evaluation/                    # Evaluation & benchmarks
│       ├── __init__.py
│       ├── evaluate.py               # Metrics computation
│       └── benchmark.py             # Baseline comparisons
│
├── dashboard/                          # 🖥️ Next.js Frontend
│   ├── package.json
│   ├── next.config.js
│   ├── src/
│   │   ├── app/                      # Next.js app router
│   │   ├── components/               # React components
│   │   └── styles/                   # CSS styles
│   └── public/                       # Static assets
│
├── data/                               # 📊 Data directory
│   ├── cert_r4.2/                    # CERT dataset (downloaded)
│   ├── synthetic/                    # Generated synthetic banking data
│   └── processed/                    # Preprocessed features
│
├── demo/                               # 🎬 Demo scripts
│   └── run_demo.py                    # Automated demo walkthrough
│
├── experiments/                        # 🧪 Training scripts
│   ├── train_lstm.py
│   ├── train_if.py
│   ├── train_hybrid.py
│   └── ablation_study.py
│
├── models/                             # 💾 Saved model artifacts
│   └── .gitkeep
│
└── results/                            # 📈 Evaluation results & graphs
    └── .gitkeep
```

---

## 🚀 Getting Started

<a name="getting-started"></a>

### Prerequisites
- Python 3.11+
- Node.js 18+ (for dashboard)
- CUDA-capable GPU (recommended)
- Git

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/SK8-infi/BOB-Hackathon-ArgusAI.git
cd "BOB Hackathon"

# Create and activate Python virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows

# Install Python dependencies
pip install -r requirements.txt

# Generate synthetic banking data
python -m argus.data.synthetic_generator

# Train models
python -m argus.experiments.train_hybrid

# Start the scoring API
python -m argus.api.scoring_api

# In a separate terminal, start the dashboard
cd dashboard
npm install
npm run dev
```

---

## 📚 Documentation

<a name="documentation"></a>

| Document | Description |
|----------|-------------|
| [IDEA_PROPOSAL.md](docs/IDEA_PROPOSAL.md) | Full idea writeup with problem analysis, approach, and novelty |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture with module details |
| [TECH_STACK.md](docs/TECH_STACK.md) | Technology choices and justifications |
| [DATA_STRATEGY.md](docs/DATA_STRATEGY.md) | Dataset selection, synthetic generation, and feature engineering |
| [BUILD_GUIDE.md](docs/BUILD_GUIDE.md) | Step-by-step implementation guide |
| [RESEARCH_REFERENCES.md](docs/RESEARCH_REFERENCES.md) | Academic papers and references |

---

## 🏆 Novel Contributions

| # | Innovation | Why It's Novel |
|---|-----------|----------------|
| 1 | **Digital Employee Twin with Behavioral Genome** | Beyond simple baselines — captures circadian rhythms, access topology, behavioral velocity |
| 2 | **Privilege Decay Functions** | Trust as a perishable resource with exponential decay — Zero Trust formalized |
| 3 | **Intent Signal Chain Detection** | Attack *narratives*, not isolated anomalies — catches multi-step attacks |
| 4 | **Peer Constellation Analysis** | Contextual anomaly via social comparison — catches slow-burn insiders |
| 5 | **Hybrid LSTM + IF + XGBoost/LightGBM Ensemble** | 5-model meta-learner stack — unsupervised + supervised + temporal + static |
| 6 | **Banking Synthetic Data Generator** | Markov chains + scenario injection; CTGAN evaluated but SMOTE outperforms (233 samples insufficient for GAN) |
| 7 | **Privacy-Preserving Cross-Dept FL** | Federated Learning + Differential Privacy (ε-DP) for banking compliance |

---

## 👥 Team

**Team Argus**

---

## 📄 License

This project is developed for the CyberShield PSBs Hackathon Series 2026.

---

<p align="center">
  <strong>🔱 Argus AI</strong> — The All-Seeing Guardian of Banking Identity Trust
</p>
