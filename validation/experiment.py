"""Synthetic falsification harness. No real empirical validation is performed."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import platform
from pathlib import Path
import numpy as np

SECTORS = ('energy', 'engineering', 'physics', 'mathematics', 'economics', 'psychology')
SCENARIOS = ('compatible', 'additive_violation', 'interaction_violation', 'nonlinear_violation')
MODELS = ('theory', 'additive', 'interaction', 'nonlinear')


def generate(n: int, seed: int, scenario: str) -> np.ndarray:
    if n < 80 or scenario not in SCENARIOS:
        raise ValueError('n >= 80 and a known scenario are required')
    rng = np.random.default_rng(seed)
    E = rng.uniform(1, 5, n)
    h = rng.uniform(0, 2, n)
    H = E - h
    if scenario == 'additive_violation':
        H = 0.8 + 0.55 * E - 0.3 * h
    elif scenario == 'interaction_violation':
        H = H + 0.65 * E * h
    elif scenario == 'nonlinear_violation':
        H = H + 0.7 * (E - 3)**2 + 0.5 * (h - 1)**2
    H = H + rng.normal(0, 0.3, n)
    return np.column_stack((E, h, H))


def validate(data: np.ndarray) -> np.ndarray:
    data = np.asarray(data, dtype=float)
    if data.ndim != 2 or data.shape[1] != 3 or len(data) < 80:
        raise ValueError('At least 80 rows and columns E,h,H are required')
    if not np.isfinite(data).all():
        raise ValueError('Missing or non-finite values are not allowed')
    if np.linalg.matrix_rank(design(data, 'additive')) < 3:
        raise ValueError('Degenerate predictors: parameters are not identifiable')
    return data


def design(data: np.ndarray, model: str) -> np.ndarray:
    E, h = data[:, 0], data[:, 1]
    cols = [np.ones(len(data)), E, h]
    if model in ('interaction', 'nonlinear'):
        cols.append(E * h)
    if model == 'nonlinear':
        cols.extend((E**2, h**2))
    return np.column_stack(cols)


def fit_predict(train: np.ndarray, test: np.ndarray, model: str) -> np.ndarray:
    if model == 'theory':
        return test[:, 0] - test[:, 1]
    if model not in MODELS:
        raise ValueError('Unknown model')
    X = design(train, model)
    if np.linalg.matrix_rank(X) < X.shape[1]:
        raise ValueError('Design is not identifiable')
    beta = np.linalg.lstsq(X, train[:, 2], rcond=None)[0]
    return design(test, model) @ beta


def split_indices(n: int, seed: int, ordered: bool = False):
    idx = np.arange(n) if ordered else np.random.default_rng(seed).permutation(n)
    a, b = int(n * .6), int(n * .8)
    return idx[:a], idx[a:b], idx[b:]


def interval(samples, alpha: float):
    return np.quantile(samples, [alpha / 2, 1 - alpha / 2]).tolist()


def analyze(data: np.ndarray, seed: int = 20261008, bootstrap: int = 1000,
            margin: float = .02, ordered: bool = False) -> tuple[dict, dict]:
    data = validate(data)
    if bootstrap < 100 or margin < 0:
        raise ValueError('bootstrap >= 100 and margin >= 0 are required')
    tr, va, te = split_indices(len(data), seed, ordered)
    train, val, test = data[tr], data[va], data[te]
    val_mse = {m: float(np.mean((val[:, 2] - fit_predict(train, val, m))**2)) for m in MODELS}
    selected = min(MODELS[1:], key=lambda m: val_mse[m])
    development = data[np.concatenate((tr, va))]
    predictions = {m: fit_predict(development, test, m) for m in MODELS}
    losses = {m: (test[:, 2] - predictions[m])**2 for m in MODELS}
    rng = np.random.default_rng(seed + 1)
    # Shared resampling indices preserve pairing across predictions.
    indices = rng.integers(0, len(test), (bootstrap, len(test)))
    comparisons = {}
    for m in MODELS[1:]:
        delta = losses['theory'] - losses[m]
        ci = interval(delta[indices].mean(axis=1), .05 / 3)
        comparisons[m] = {'delta_mse_theory_minus_baseline': float(delta.mean()),
                          'ci_simultaneous_95': ci,
                          'reject_predictive': bool(ci[0] > margin)}
    X = design(development, 'additive')
    beta = np.linalg.lstsq(X, development[:, 2], rcond=None)[0]
    boot_beta = []
    for _ in range(bootstrap):
        ix = rng.integers(0, len(development), len(development))
        boot_beta.append(np.linalg.lstsq(X[ix], development[ix, 2], rcond=None)[0])
    cis = np.quantile(boot_beta, [.05 / 6, 1 - .05 / 6], axis=0).T
    target = np.array([0, 1, -1])
    reject_parameters = bool(np.any((target < cis[:, 0]) | (target > cis[:, 1])))
    metrics = {}
    denom = np.sum((test[:, 2] - test[:, 2].mean())**2)
    for m in MODELS:
        residual = test[:, 2] - predictions[m]
        metrics[m] = {'mse': float(losses[m].mean()), 'rmse': float(np.sqrt(losses[m].mean())),
                      'mae': float(np.abs(residual).mean()),
                      'r2': float(1 - losses[m].sum() / denom) if denom > 0 else None}
    result = {'n': len(data), 'split_sizes': list(map(len, (tr, va, te))),
              'validation_mse': val_mse, 'selected_baseline_before_test': selected,
              'test_metrics': metrics, 'comparisons': comparisons,
              'additive_coefficients': beta.tolist(), 'coefficient_ci_simultaneous_95': cis.tolist(),
              'reject_additive_restrictions_diagnostic': reject_parameters,
              'predictive_decision': 'falsified_operationally' if any(c['reject_predictive'] for c in comparisons.values()) else 'not_falsified_not_validated',
              'margin_mse': margin, 'bootstrap': bootstrap}
    audit = {'train': tr.tolist(), 'validation': va.tolist(), 'test': te.tolist(),
             'test_predictions': {m: p.tolist() for m, p in predictions.items()}}
    return result, audit


def write_csv(path: Path, data: np.ndarray):
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(('E', 'h', 'H'))
        w.writerows(data)


def load_csv(path: Path) -> np.ndarray:
    with path.open(newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or not {'E', 'h', 'H'} <= set(reader.fieldnames):
            raise ValueError('CSV must contain E,h,H')
        return validate(np.array([[float(r[k]) for k in ('E', 'h', 'H')] for r in reader]))


def run(args):
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    if args.csv:
        if not args.metadata:
            raise ValueError('--metadata is required for external data')
        meta = json.loads(args.metadata.read_text(encoding='utf-8'))
        for key in ('sector', 'source', 'unit', 'H_definition', 'E_definition', 'h_definition', 'independent_H', 'sampling'):
            if key not in meta:
                raise ValueError(f'Missing metadata: {key}')
        if meta['independent_H'] is not True or meta['sampling'] != 'iid':
            raise ValueError('This harness requires independently observed H and iid sampling; time series and panels require block or cluster bootstrap')
        jobs = [(meta['sector'], 'external', args.seed, load_csv(args.csv), meta)]
    else:
        jobs = [(sector, scenario, args.seed + i * 100 + j,
                 generate(args.n, args.seed + i * 100 + j, scenario), {'synthetic': True})
                for i, sector in enumerate(SECTORS) for j, scenario in enumerate(SCENARIOS)]
    results = []
    for sector, scenario, seed, data, meta in jobs:
        # Filenames derive from enumeration, never untrusted metadata.
        folder = out / f'case_{len(results):02d}'
        folder.mkdir(exist_ok=True)
        write_csv(folder / 'data.csv', data)
        result, audit = analyze(data, seed, args.bootstrap, args.margin, args.ordered)
        result.update(sector=sector, scenario=scenario, seed=seed, metadata=meta,
                      data_sha256=hashlib.sha256((folder / 'data.csv').read_bytes()).hexdigest())
        (folder / 'audit.json').write_text(json.dumps(audit, indent=2), encoding='utf-8')
        results.append(result)
    payload = {'synthetic': not bool(args.csv), 'python': platform.python_version(),
               'numpy': np.__version__, 'config': {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()},
               'results': results}
    (out / 'results.json').write_text(json.dumps(payload, indent=2, allow_nan=False), encoding='utf-8')
    lines = ['# H = E - h results', '',
             'SYNTHETIC DATA: method verification only; no real empirical validation.' if not args.csv else 'EXTERNAL DATA: user-declared provenance; not automatically verified.', '',
             '| Field | Scenario | Theory RMSE | Selected-baseline RMSE | Operational decision |',
             '|---|---|---:|---:|---|']
    for r in results:
        m = r['test_metrics']
        lines.append(f"| {r['sector']} | {r['scenario']} | {m['theory']['rmse']:.4f} | {m[r['selected_baseline_before_test']]['rmse']:.4f} | {r['predictive_decision']} |")
    lines += ['', '## Interpretation', '',
              'Failure to falsify does not prove the formula. Each compatible scenario is generated from the formula itself and serves as a software positive control.',
              'Positive delta MSE favors the baseline. Operational falsification requires the lower confidence bound to exceed the prespecified MSE margin. The nominal simultaneous 95% interval uses Bonferroni correction across three within-case comparisons and does not globally correct all 24 cases.',
              'The iid percentile bootstrap on test rows is conditional on fitted models and excludes training variability. The development-row coefficient bootstrap is diagnostic and not evidence of equivalence.',
              'Additive restrictions are intercept 0, E coefficient 1, and h coefficient -1. If the additive model is misspecified, rejecting these restrictions alone is not structural falsification.',
              'The nonlinear model is quadratic and does not represent every nonlinear alternative. No causal inference is made. A single split does not establish sampling robustness.',
              'The six field labels use the same abstract harness with different seeds; they are not six real disciplinary experiments. Numerical results do not replace proof in mathematics.',
              'See results.json for details, intervals, and configuration; see case_*/audit.json for split indices and predictions.']
    (out / 'REPORT.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Report: {out / "REPORT.md"}')


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', type=Path, default=Path('results'))
    p.add_argument('--n', type=int, default=800)
    p.add_argument('--seed', type=int, default=20261008)
    p.add_argument('--bootstrap', type=int, default=1000)
    p.add_argument('--margin', type=float, default=.02)
    p.add_argument('--ordered', action='store_true', help='Split in row order; bootstrap remains iid')
    p.add_argument('--csv', type=Path)
    p.add_argument('--metadata', type=Path)
    return p


if __name__ == '__main__':
    p = parser()
    try:
        run(p.parse_args())
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        p.exit(2, f'Error: {exc}\n')
