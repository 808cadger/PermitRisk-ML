# PermitRisk-ML

[![Release](https://img.shields.io/github/v/release/808cadger/PermitRisk-ML?include_prereleases&label=release)](https://github.com/808cadger/PermitRisk-ML/releases)
[![Last commit](https://img.shields.io/github/last-commit/808cadger/PermitRisk-ML)](https://github.com/808cadger/PermitRisk-ML/commits)
[![License](https://img.shields.io/github/license/808cadger/PermitRisk-ML)](https://github.com/808cadger/PermitRisk-ML/blob/HEAD/LICENSE)
![Platforms](https://img.shields.io/badge/platform-Python%2FTabular%20ML-2563eb)

Small tabular ML project that predicts permit-delay risk from structured construction project data.

The goal is not a giant model. The goal is a clean, reproducible ML workflow: dataset, baseline, model, metrics, feature importance, and a model card.

## Project Snapshot

| Area | Details |
|------|---------|
| Primary use case | Predict construction permit-delay risk from structured project signals. |
| Platforms | Python CLI, reproducible reports |
| Core stack | Python, synthetic data generation, tabular scoring, JSON metrics |
| Review first | `permitrisk_ml/make_dataset.py`, `permitrisk_ml/train.py`, `reports/model_card.md` |

## Download Links

| Platform | Link |
|----------|------|
| Source | [Download the GitHub source ZIP](https://github.com/808cadger/PermitRisk-ML/archive/refs/heads/main.zip) |
| Repository | [View on GitHub](https://github.com/808cadger/PermitRisk-ML) |
| Releases | [Download release artifacts](https://github.com/808cadger/PermitRisk-ML/releases) |

<!-- INSTALL-START -->
## Install and run

These instructions install and run `PermitRisk-ML` from a fresh clone.

### Clone
```bash
git clone https://github.com/808cadger/PermitRisk-ML.git
cd PermitRisk-ML
```

### Run the workflow
```bash
python -m permitrisk_ml.make_dataset
python -m permitrisk_ml.train
```

### AI/API setup
- No API key is required.
- The current project is a deterministic tabular ML workflow.

### License
- Apache License 2.0. See [`LICENSE`](./LICENSE).
<!-- INSTALL-END -->

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
