"""Exploratory real-data falsification in occupational psychology.

This analysis is not a confirmatory validation of a universal law. It fixes one
operationalization: standardized psychological well-being equals standardized
job resources minus standardized job demands.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import platform
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
from openpyxl import load_workbook

from experiment import analyze, split_indices


SOURCE_RECORD = "https://zenodo.org/records/21153011"
DOWNLOAD_URL = (
    "https://zenodo.org/api/records/21153011/files/"
    "metro_burnout_repository_package.zip/content"
)
EXPECTED_ZIP_SHA256 = "fe33873b7b6a847203edd5d70101f60fb9529c693ec252f10fdfbce2bfe6bec0"
WORKBOOK_MEMBER = (
    "metro_burnout_repository_package/"
    "Metro_Burnout_Deidentified_Survey_Data.xlsx"
)
SHEET = "Formal_Survey_n274"
PILOT_SHEET = "Pilot_Survey_n140"
RESOURCE_COLUMN = "工作资源"
DEMAND_COLUMN = "工作要求"
BURNOUT_COLUMN = "职业倦怠"


def fetch_bytes(url: str = DOWNLOAD_URL, timeout: float = 30.0) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "david-theory/0.2"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def verify_archive(raw: bytes) -> str:
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_ZIP_SHA256:
        raise ValueError(
            f"Unexpected archive hash: {digest}. Expected: {EXPECTED_ZIP_SHA256}"
        )
    return digest


PILOT_GROUPS = {
    "burnout": [
        [f"EX{i}" for i in range(1, 7)],
        [f"CY{i}" for i in range(1, 4)],
        [f"LP{i}" for i in range(1, 7)],
    ],
    "demands": [
        [f"WL{i}" for i in range(1, 4)],
        [f"JC{i}" for i in range(1, 6)],
        [f"GJ{i}" for i in range(1, 4)],
        [f"GF{i}" for i in range(1, 6)],
    ],
    "resources": [
        [f"SZ{i}" for i in range(1, 6)],
        [f"GZ{i}" for i in range(1, 8)],
        [f"ZF{i}" for i in range(1, 5)],
        [f"ZG{i}" for i in range(1, 6)],
    ],
}


def _mean_groups(row: tuple, positions: dict[str, int], groups: list[list[str]]) -> float:
    scale_means = []
    for group in groups:
        values = [float(row[positions[name]]) for name in group]
        scale_means.append(float(np.mean(values)))
    return float(np.mean(scale_means))


def load_raw_scores(raw_zip: bytes, sample: str = "formal") -> np.ndarray:
    if sample not in ("formal", "pilot"):
        raise ValueError("Sample must be formal or pilot")
    verify_archive(raw_zip)
    with zipfile.ZipFile(io.BytesIO(raw_zip)) as archive:
        try:
            workbook_bytes = archive.read(WORKBOOK_MEMBER)
        except KeyError as exc:
            raise ValueError("Expected workbook is missing from the archive") from exc
    workbook = load_workbook(io.BytesIO(workbook_bytes), read_only=True, data_only=True)
    sheet_name = SHEET if sample == "formal" else PILOT_SHEET
    if sheet_name not in workbook.sheetnames:
        raise ValueError(f"Missing sheet: {sheet_name}")
    sheet = workbook[sheet_name]
    rows = sheet.iter_rows(values_only=True)
    headers = next(rows, None)
    if headers is None:
        raise ValueError("Workbook is empty")
    positions = {name: i for i, name in enumerate(headers)}
    required = (
        (RESOURCE_COLUMN, DEMAND_COLUMN, BURNOUT_COLUMN)
        if sample == "formal"
        else tuple(
            name
            for construct in ("resources", "demands", "burnout")
            for group in PILOT_GROUPS[construct]
            for name in group
        )
    )
    missing = [name for name in required if name not in positions]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    values = []
    for row in rows:
        selected = [row[positions[name]] for name in required]
        if any(value is None for value in selected):
            continue
        try:
            if sample == "formal":
                values.append([float(value) for value in selected])
            else:
                values.append(
                    [
                        _mean_groups(row, positions, PILOT_GROUPS["resources"]),
                        _mean_groups(row, positions, PILOT_GROUPS["demands"]),
                        _mean_groups(row, positions, PILOT_GROUPS["burnout"]),
                    ]
                )
        except (TypeError, ValueError) as exc:
            raise ValueError("Non-numeric value in selected scales") from exc
    data = np.asarray(values, dtype=float)
    if data.ndim != 2 or data.shape[0] < 80 or data.shape[1] != 3:
        raise ValueError("Insufficient valid data")
    if not np.isfinite(data).all():
        raise ValueError("Non-finite values in selected scales")
    return data


def operationalize(raw_scores: np.ndarray, seed: int) -> tuple[np.ndarray, dict]:
    """Create E=z(resources), h=z(demands), H=-z(burnout).

    Means and standard deviations are fitted on training rows only. This avoids
    letting validation or test outcomes determine the scale.
    """
    train, _, _ = split_indices(len(raw_scores), seed)
    means = raw_scores[train].mean(axis=0)
    scales = raw_scores[train].std(axis=0, ddof=1)
    if np.any(scales <= 0):
        raise ValueError("A training scale is constant")
    standardized = (raw_scores - means) / scales
    data = np.column_stack(
        (standardized[:, 0], standardized[:, 1], -standardized[:, 2])
    )
    transform = {
        "training_means": means.tolist(),
        "training_standard_deviations": scales.tolist(),
        "columns_before_transform": [
            RESOURCE_COLUMN,
            DEMAND_COLUMN,
            BURNOUT_COLUMN,
        ],
        "columns_after_transform": [
            "E=z(job_resources)",
            "h=z(job_demands)",
            "H=-z(burnout)",
        ],
    }
    return data, transform


def run(args: argparse.Namespace) -> dict:
    raw_zip = args.archive.read_bytes() if args.archive else fetch_bytes(timeout=args.timeout)
    digest = verify_archive(raw_zip)
    raw_scores = load_raw_scores(raw_zip, args.sample)
    data, transform = operationalize(raw_scores, args.seed)
    result, audit = analyze(
        data,
        seed=args.seed,
        bootstrap=args.bootstrap,
        margin=args.margin,
        ordered=False,
    )
    payload = {
        "analysis_status": "exploratory_real_data_falsification",
        "confirmatory_validation": False,
        "reason_not_confirmatory": (
            "The operationalization was created for this project after the source data "
            "already existed; scales differ before standardization; cross-sectional "
            "associations do not establish causality or universality."
        ),
        "source_record": SOURCE_RECORD,
        "download_url": DOWNLOAD_URL,
        "archive_sha256": digest,
        "retrieved_date": "2026-10-08",
        "dataset": (
            "De-identified survey data for job demands, job resources, and burnout "
            "among metro site management personnel in China"
        ),
        "sheet": SHEET if args.sample == "formal" else PILOT_SHEET,
        "sample_role": args.sample,
        "n_complete": int(len(data)),
        "operationalization": transform,
        "hypothesis": "-z(burnout) = z(job resources) - z(job demands)",
        "margin_mse_standardized_squared": args.margin,
        "result": result,
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
        },
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "results.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False),
        encoding="utf-8",
    )
    (args.out / "audit.json").write_text(
        json.dumps(audit, indent=2, allow_nan=False), encoding="utf-8"
    )
    selected = result["selected_baseline_before_test"]
    metrics = result["test_metrics"]
    comparison = result["comparisons"][selected]
    report = f"""# Exploratory empirical test: occupational psychology ({args.sample})

**Real data, exploratory analysis. This is not confirmatory validation of a universal formula.**

- Source: {SOURCE_RECORD}
- Complete sample analyzed: {len(data)} respondents
- Sample role: {args.sample}
- Specification: `H=-z(burnout)`, `E=z(job resources)`, `h=z(job demands)`
- Transformations fitted on training data only
- Split: {result['split_sizes']} (training, validation, test)
- Baseline selected on validation: {selected}
- Theory RMSE on test: {metrics['theory']['rmse']:.4f}
- Selected-baseline RMSE on test: {metrics[selected]['rmse']:.4f}
- Delta MSE, theory minus baseline: {comparison['delta_mse_theory_minus_baseline']:.4f}
- Simultaneous 95% interval for delta: {comparison['ci_simultaneous_95']}
- Margin prespecified in code: {args.margin:.4f} squared standardized units
- Operational decision: `{result['predictive_decision']}`

The result concerns only the predictive extension that identifies the residual with standardized well-being; the central relation H:=E-h remains a definitional identity. Standardization makes numerical scales comparable but does not prove that the constructs share a substantive unit. The dataset is cross-sectional and does not identify causality. Because the hypothesis and margin were not preregistered before collection, this result defines a specification for prospective replication.
"""
    (args.out / "REPORT.md").write_text(report, encoding="utf-8")
    return payload


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, default=Path("empirical_results/psychology"))
    p.add_argument("--archive", type=Path, help="Archivio Zenodo già scaricato")
    p.add_argument("--sample", choices=("formal", "pilot"), default="formal")
    p.add_argument("--seed", type=int, default=20261008)
    p.add_argument("--bootstrap", type=int, default=10000)
    p.add_argument("--margin", type=float, default=0.05)
    p.add_argument("--timeout", type=float, default=30.0)
    return p


if __name__ == "__main__":
    arguments = parser().parse_args()
    try:
        run(arguments)
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        raise SystemExit(f"Error: {exc}") from exc
