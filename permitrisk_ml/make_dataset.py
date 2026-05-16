from __future__ import annotations

import csv
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "permits.csv"


PERMIT_TYPES = ["residential", "commercial", "tenant_improvement", "civil"]
ZONES = ["urban", "suburban", "coastal", "historic"]


def risk_probability(row: dict[str, object]) -> float:
    score = -2.8
    score += 0.65 if row["permit_type"] in {"commercial", "civil"} else 0
    score += 0.75 if row["zone"] in {"coastal", "historic"} else 0
    score += 0.42 * int(row["missing_documents"])
    score += 0.03 * int(row["reviewer_queue"])
    score += 0.55 * int(row["prior_revisions"])
    score += 0.35 if float(row["project_value_m"]) > 2.5 else 0
    score -= 0.45 if int(row["contractor_approved_count"]) > 12 else 0
    return 1 / (1 + 2.71828 ** -score)


def make_rows(count: int = 600, seed: int = 42) -> list[dict[str, object]]:
    rng = random.Random(seed)
    rows: list[dict[str, object]] = []
    for permit_id in range(1, count + 1):
        row: dict[str, object] = {
            "permit_id": permit_id,
            "permit_type": rng.choice(PERMIT_TYPES),
            "zone": rng.choice(ZONES),
            "project_value_m": round(rng.uniform(0.08, 6.5), 2),
            "missing_documents": rng.randint(0, 4),
            "reviewer_queue": rng.randint(3, 38),
            "prior_revisions": rng.randint(0, 3),
            "contractor_approved_count": rng.randint(0, 24),
        }
        row["delay_risk"] = int(rng.random() < risk_probability(row))
        rows.append(row)
    return rows


def main() -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    rows = make_rows()
    with DATA_FILE.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {DATA_FILE}")


if __name__ == "__main__":
    main()
