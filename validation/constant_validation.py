"""Compatibility checks for a prespecified constant h = E - H.

This module does not prove universality. It checks whether a finite collection of
independent measurements is compatible with one constant under declared bounded
absolute errors.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path


REQUIRED_COLUMNS = ("E", "H", "error_E", "error_H")


def constant_intersection(rows: list[dict[str, float]]) -> dict[str, object]:
    """Return the intersection of row-wise intervals for c = E - H."""
    if not rows:
        raise ValueError("At least one measurement row is required")

    intervals: list[tuple[float, float]] = []
    for row_number, row in enumerate(rows, start=1):
        try:
            e = float(row["E"])
            observed_h = float(row["H"])
            error_e = float(row["error_E"])
            error_h = float(row["error_H"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"Invalid measurement in row {row_number}") from exc
        values = (e, observed_h, error_e, error_h)
        if not all(math.isfinite(value) for value in values):
            raise ValueError(f"Non-finite measurement in row {row_number}")
        if error_e < 0 or error_h < 0:
            raise ValueError(f"Negative uncertainty in row {row_number}")

        difference = e - observed_h
        combined_error = error_e + error_h
        intervals.append((difference - combined_error, difference + combined_error))

    lower = max(interval[0] for interval in intervals)
    upper = min(interval[1] for interval in intervals)
    return {
        "candidate": "h",
        "relation": "h = E - H",
        "row_count": len(rows),
        "compatible_with_one_constant": lower <= upper,
        "intersection": [lower, upper] if lower <= upper else None,
        "maximum_lower_bound": lower,
        "minimum_upper_bound": upper,
        "intervals": [[low, high] for low, high in intervals],
        "interpretation": (
            "Finite-sample compatibility only; this is not proof of universality."
            if lower <= upper
            else "The declared bounded-error measurements reject one shared constant."
        ),
    }


def load_measurements(path: Path) -> list[dict[str, float]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None or not set(REQUIRED_COLUMNS).issubset(reader.fieldnames):
            raise ValueError(f"CSV must contain: {', '.join(REQUIRED_COLUMNS)}")
        return list(reader)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check finite measurements for compatibility with one h = E - H constant"
    )
    parser.add_argument("csv", type=Path, help="CSV containing E,H,error_E,error_H")
    parser.add_argument("--out", type=Path, default=Path("constant_validation.json"))
    args = parser.parse_args()
    result = constant_intersection(load_measurements(args.csv))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
