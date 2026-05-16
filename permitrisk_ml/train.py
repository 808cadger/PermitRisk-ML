from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "permits.csv"
REPORT_FILE = ROOT / "reports" / "metrics.json"
IMPORTANCE_FILE = ROOT / "reports" / "feature_importance.json"


NUMERIC = [
    "project_value_m",
    "missing_documents",
    "reviewer_queue",
    "prior_revisions",
    "contractor_approved_count",
]
CATEGORICAL = ["permit_type", "zone"]


def read_rows() -> list[dict[str, str]]:
    if not DATA_FILE.exists():
        from permitrisk_ml.make_dataset import main as make_dataset

        make_dataset()
    with DATA_FILE.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def score_row(row: dict[str, str]) -> float:
    score = -2.8
    score += 0.55 * float(row["missing_documents"])
    score += 0.055 * float(row["reviewer_queue"])
    score += 0.72 * float(row["prior_revisions"])
    score += 0.28 if float(row["project_value_m"]) > 2.5 else 0
    score -= 0.5 if float(row["contractor_approved_count"]) > 12 else 0
    score += 0.45 if row["permit_type"] in {"commercial", "civil"} else 0
    score += 0.55 if row["zone"] in {"coastal", "historic"} else 0
    return 1 / (1 + 2.71828 ** -score)


def metrics(y_true: list[int], y_pred: list[int]) -> dict[str, float]:
    tp = sum(1 for truth, pred in zip(y_true, y_pred) if truth == pred == 1)
    tn = sum(1 for truth, pred in zip(y_true, y_pred) if truth == pred == 0)
    fp = sum(1 for truth, pred in zip(y_true, y_pred) if truth == 0 and pred == 1)
    fn = sum(1 for truth, pred in zip(y_true, y_pred) if truth == 1 and pred == 0)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "accuracy": round((tp + tn) / len(y_true), 3),
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
    }


def main() -> None:
    rows = read_rows()
    split = int(len(rows) * 0.8)
    train_rows = rows[:split]
    test_rows = rows[split:]
    majority = Counter(int(row["delay_risk"]) for row in train_rows).most_common(1)[0][0]

    y_true = [int(row["delay_risk"]) for row in test_rows]
    baseline_pred = [majority for _ in test_rows]
    model_pred = [int(score_row(row) >= 0.7) for row in test_rows]

    report = {
        "rows": len(rows),
        "train_rows": len(train_rows),
        "test_rows": len(test_rows),
        "baseline": metrics(y_true, baseline_pred),
        "model": metrics(y_true, model_pred),
    }
    importance = {
        "missing_documents": 0.55,
        "reviewer_queue": 0.055,
        "prior_revisions": 0.72,
        "project_value_over_2_5m": 0.28,
        "contractor_approved_count_over_12": -0.50,
        "commercial_or_civil": 0.45,
        "coastal_or_historic": 0.55,
    }

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    IMPORTANCE_FILE.write_text(json.dumps(importance, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
