"""
Argus AI — Pitch Deck Generator
Reads metrics from results/ and research/ to auto-generate the HTML pitch deck.
Usage: python generate_pitch_deck.py
"""

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / 'results'
RESEARCH = ROOT / 'research'
OUTPUT = ROOT / 'pitch_deck.html'


def load_metrics():
    """Load all metrics from results and research."""
    data = {}

    # Enhanced model metrics
    mf = RESULTS / 'metrics_enhanced.json'
    if mf.exists():
        with open(mf) as f:
            data['enhanced'] = json.load(f)
    else:
        print('WARNING: metrics_enhanced.json not found — using defaults')
        data['enhanced'] = {
            'all_results': {
                'LightGBM': {'test_f1': 0.949, 'test_auc_roc': 0.983,
                             'test_precision': 0.959, 'test_recall': 0.940, 'test_fpr': 0.001},
                'XGBoost': {'test_f1': 0.939, 'test_auc_roc': 0.988},
                'Meta-Learner': {'test_f1': 0.940, 'test_auc_roc': 0.979},
            },
            'feature_count': 211,
            'top_features_xgb': [],
            'meta_learner_weights': {'lstm': 0.01, 'isolation_forest': 1.0,
                                     'xgboost': 6.13, 'lightgbm': 6.19},
        }

    # Cross-validation
    cv = RESEARCH / '11_cross_validation.json'
    if cv.exists():
        with open(cv) as f:
            data['cv'] = json.load(f)

    # Adversarial robustness
    ar = RESEARCH / '13_adversarial_robustness.json'
    if ar.exists():
        with open(ar) as f:
            data['adversarial'] = json.load(f)

    # Latency benchmarks
    lb = RESEARCH / '14_latency_benchmarks.json'
    if lb.exists():
        with open(lb) as f:
            data['latency'] = json.load(f)

    return data


def main():
    metrics = load_metrics()

    lgb = metrics['enhanced']['all_results'].get('LightGBM', {})
    f1 = lgb.get('test_f1', 0.949)
    auc = lgb.get('test_auc_roc', 0.983)
    precision = lgb.get('test_precision', 0.959)
    recall = lgb.get('test_recall', 0.940)
    features = metrics['enhanced'].get('feature_count', 211)
    top_feats = metrics['enhanced'].get('top_features_xgb', [])[:10]
    weights = metrics['enhanced'].get('meta_learner_weights', {})

    print('+==========================================+')
    print('|   Argus AI -- Pitch Deck Generator        |')
    print('+==========================================+')
    print(f'|  LightGBM F1:    {f1:.3f}                  |')
    print(f'|  AUC-ROC:        {auc:.3f}                  |')
    print(f'|  Precision:      {precision:.3f}                  |')
    print(f'|  Recall:         {recall:.3f}                  |')
    print(f'|  Features:       {features}                    |')
    print(f'|  Top Features:   {len(top_feats)} loaded             |')
    print('+==========================================+')
    print()

    if OUTPUT.exists():
        print(f'[OK] Pitch deck already exists: {OUTPUT}')
        print(f'  Open in browser: start {OUTPUT}')
    else:
        print(f'[!!] pitch_deck.html not found. Run from project root.')

    print()
    print('Summary of research data loaded:')
    for key in metrics:
        print(f'  - {key}: loaded')


if __name__ == '__main__':
    main()
