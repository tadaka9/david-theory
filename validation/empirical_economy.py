"""World Bank accounting audit for the reduced relation H = E - h.

This is a real-data consistency audit, not an independent validation: gross savings
is itself defined from national-accounts components and also includes net transfers.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import statistics
import urllib.request
from pathlib import Path


API = "https://api.worldbank.org/v2"
INDICATORS = {
    "E": "NY.GNP.MKTP.CD",      # GNI, current US$
    "h": "NE.CON.TOTL.CD",     # Final consumption, current US$
    "H": "NY.GNS.ICTR.CD",     # Gross savings, current US$
}


def fetch_json(url: str, timeout: float) -> tuple[object, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "david-theory/0.2"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read()
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def values_by_country(payload: object) -> dict[str, dict]:
    if not isinstance(payload, list) or len(payload) < 2 or not isinstance(payload[1], list):
        raise ValueError("Risposta World Bank inattesa")
    return {
        row["countryiso3code"]: row
        for row in payload[1]
        if row.get("countryiso3code") and row.get("value") is not None
    }


def join_indicators(payloads: dict[str, object]) -> list[dict]:
    mapped = {key: values_by_country(payload) for key, payload in payloads.items()}
    common = sorted(set.intersection(*(set(rows) for rows in mapped.values())))
    output = []
    for code in common:
        E = float(mapped["E"][code]["value"])
        h = float(mapped["h"][code]["value"])
        H = float(mapped["H"][code]["value"])
        predicted = E - h
        discrepancy = H - predicted
        relative = discrepancy / max(abs(E), 1.0)
        output.append(
            {
                "country_code": code,
                "country": mapped["H"][code]["country"]["value"],
                "E_gni_current_usd": E,
                "h_consumption_current_usd": h,
                "H_gross_savings_current_usd": H,
                "predicted_E_minus_h": predicted,
                "discrepancy_H_minus_prediction": discrepancy,
                "relative_discrepancy_to_abs_E": relative,
            }
        )
    return output


def run(args: argparse.Namespace) -> dict:
    payloads = {}
    hashes = {}
    for key, indicator in INDICATORS.items():
        url = (
            f"{API}/country/all/indicator/{indicator}"
            f"?date={args.year}&format=json&per_page=400"
        )
        payloads[key], hashes[key] = fetch_json(url, args.timeout)
    rows = join_indicators(payloads)
    if len(rows) < 80:
        raise ValueError(f"Solo {len(rows)} osservazioni complete; audit non eseguito")
    absolute_relative = sorted(abs(row["relative_discrepancy_to_abs_E"]) for row in rows)
    p90_index = min(len(absolute_relative) - 1, int(0.90 * len(absolute_relative)))
    summary = {
        "analysis_status": "real_data_accounting_consistency_audit",
        "independent_validation": False,
        "reason_not_independent": (
            "World Bank gross savings is defined from national income and consumption "
            "plus net transfers; the three indicators share a national-accounts system."
        ),
        "year": args.year,
        "retrieved_date": "2026-10-08",
        "source": "World Bank World Development Indicators API",
        "api": API,
        "indicators": INDICATORS,
        "raw_response_sha256": hashes,
        "n_complete_country_or_aggregate_series": len(rows),
        "median_absolute_relative_discrepancy": statistics.median(absolute_relative),
        "p90_absolute_relative_discrepancy": absolute_relative[p90_index],
        "share_within_1_percent_of_gni": sum(x <= 0.01 for x in absolute_relative) / len(rows),
        "share_within_5_percent_of_gni": sum(x <= 0.05 for x in absolute_relative) / len(rows),
        "interpretation": (
            "The discrepancy combines net transfers, revisions, coverage differences, "
            "and aggregation effects. Agreement is database consistency, not an "
            "independent empirical confirmation of H = E - h."
        ),
    }
    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / "country_year_audit.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (args.out / "results.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    report = f"""# Audit empirico economico: contabilità nazionale {args.year}

**Dati reali World Bank. Audit di coerenza contabile, non validazione indipendente.**

- Serie complete congiunte: {len(rows)}
- E: GNI (current US$), `{INDICATORS['E']}`
- h: final consumption expenditure (current US$), `{INDICATORS['h']}`
- H: gross savings (current US$), `{INDICATORS['H']}`
- Mediana di `|H-(E-h)|/|E|`: {summary['median_absolute_relative_discrepancy']:.4%}
- 90° percentile: {summary['p90_absolute_relative_discrepancy']:.4%}
- Quota entro 1% del GNI: {summary['share_within_1_percent_of_gni']:.2%}
- Quota entro 5% del GNI: {summary['share_within_5_percent_of_gni']:.2%}

La definizione World Bank specifica che il risparmio lordo è reddito nazionale lordo meno consumo totale **più trasferimenti netti**. La formula ridotta omette quindi un termine noto. Inoltre le serie provengono dallo stesso sistema di contabilità nazionale. Una corrispondenza misura coerenza del database; una discrepanza può rappresentare trasferimenti netti, revisioni, differenze di copertura o aggregati sovranazionali. Non è un test causale né una conferma indipendente della teoria percettiva.
"""
    (args.out / "REPORT.md").write_text(report, encoding="utf-8")
    return summary


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--year", type=int, default=2022)
    p.add_argument("--out", type=Path, default=Path("empirical_results/economy"))
    p.add_argument("--timeout", type=float, default=30.0)
    return p


if __name__ == "__main__":
    try:
        run(parser().parse_args())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Errore: {exc}") from exc
