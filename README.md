# PermitRisk-ML

Small tabular ML project that predicts permit-delay risk from structured construction project data.

The goal is not a giant model. The goal is a clean, reproducible ML workflow: dataset, baseline, model, metrics, feature importance, and a model card.

## Problem

Given early project signals such as permit type, reviewer workload, missing documents, project value, and contractor history, estimate whether a permit is likely to miss the target approval date.

## Quick start

```bash
python -m permitrisk_ml.make_dataset
python -m permitrisk_ml.train
```

## Current benchmark

Synthetic seed: `42`

| Model | Accuracy | Precision | Recall | F1 |
| --- | ---: | ---: | ---: | ---: |
| Majority baseline | 0.55 | 0.55 | 1.00 | 0.71 |
| Calibrated risk score | 0.70 | 0.73 | 0.73 | 0.73 |

## ML engineering signals

- Reproducible synthetic dataset generator.
- Explicit train/test split.
- Baseline model for comparison.
- Pipeline with preprocessing and model in one object.
- Feature importance exported for review.
- Model card in `reports/model_card.md`.

## Why this belongs on the profile

It proves fundamentals that agent/chat apps do not: tabular features, metrics, leakage awareness, baseline comparison, and deployable model packaging.
