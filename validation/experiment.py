"""Synthetic falsification harness. No real empirical validation is performed."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import platform
from pathlib import Path
import numpy as np

SECTORS = ('energia', 'ingegneria', 'fisica', 'matematica', 'economia', 'psicologia')
SCENARIOS = ('compatible', 'additive_violation', 'interaction_violation', 'nonlinear_violation')
MODELS = ('theory', 'additive', 'interaction', 'nonlinear')


def generate(n: int, seed: int, scenario: str) -> np.ndarray:
    if n < 80 or scenario not in SCENARIOS:
        raise ValueError('n >= 80 e scenario conosciuto richiesti')
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
        raise ValueError('Servono almeno 80 righe e colonne E,h,H')
    if not np.isfinite(data).all():
        raise ValueError('Valori mancanti/non finiti non ammessi')
    if np.linalg.matrix_rank(design(data, 'additive')) < 3:
        raise ValueError('Predittori degeneri: parametri non identificabili')
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
        raise ValueError('Modello sconosciuto')
    X = design(train, model)
    if np.linalg.matrix_rank(X) < X.shape[1]:
        raise ValueError('Design non identificabile')
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
        raise ValueError('bootstrap >= 100 e margin >= 0 richiesti')
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
            raise ValueError('CSV deve contenere E,h,H')
        return validate(np.array([[float(r[k]) for k in ('E', 'h', 'H')] for r in reader]))


def run(args):
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    if args.csv:
        if not args.metadata:
            raise ValueError('--metadata necessario per dati esterni')
        meta = json.loads(args.metadata.read_text(encoding='utf-8'))
        for key in ('sector', 'source', 'unit', 'H_definition', 'E_definition', 'h_definition', 'independent_H', 'sampling'):
            if key not in meta:
                raise ValueError(f'Metadata mancante: {key}')
        if meta['independent_H'] is not True or meta['sampling'] != 'iid':
            raise ValueError('Questo harness richiede H indipendente e campionamento iid; per serie/panel serve bootstrap a blocchi/cluster')
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
    lines = ['# Risultati H = E − h', '',
             'DATI SINTETICI: verifica del metodo, nessuna validazione empirica reale.' if not args.csv else 'DATI ESTERNI: provenienza dichiarata dall’utente, non verificata automaticamente.', '',
             '| Settore | Scenario | RMSE teoria | RMSE baseline scelta | Esito operativo |',
             '|---|---|---:|---:|---|']
    for r in results:
        m = r['test_metrics']
        lines.append(f"| {r['sector']} | {r['scenario']} | {m['theory']['rmse']:.4f} | {m[r['selected_baseline_before_test']]['rmse']:.4f} | {r['predictive_decision']} |")
    lines += ['', '## Interpretazione', '',
              'La mancata falsificazione non prova la formula. Ogni scenario compatibile è generato dalla formula stessa: il successo è un controllo positivo del software.',
              'Delta MSE positivo favorisce la baseline. Falsificazione operativa: limite inferiore del CI maggiore del margine MSE prefissato. Il CI nominale simultaneo 95% usa Bonferroni sui tre confronti all’interno di ogni caso; non corregge globalmente i 24 casi.',
              'Bootstrap percentile iid del test: incertezza condizionata ai modelli stimati, non include la variabilità di training. Bootstrap delle righe di sviluppo: CI dei coefficienti additivi, diagnostico e non prova di equivalenza.',
              'Restrizioni additive: intercetta 0, coefficiente E 1, coefficiente h −1. Se il modello additivo è mal specificato, il loro rigetto non costituisce da solo una falsificazione strutturale.',
              'Modello nonlineare: polinomio quadratico, non rappresenta tutte le alternative nonlineari. Nessuna inferenza causale. Un solo split non dimostra robustezza rispetto al campionamento.',
              'Le sei etichette settoriali usano lo stesso banco di prova astratto con semi diversi: non sono sei esperimenti disciplinari reali. In matematica i risultati numerici non sostituiscono una dimostrazione.',
              'Dettagli, intervalli e configurazione: results.json. Indici dello split e previsioni: case_*/audit.json.']
    (out / 'REPORT.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Report: {out / "REPORT.md"}')


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', type=Path, default=Path('results'))
    p.add_argument('--n', type=int, default=800)
    p.add_argument('--seed', type=int, default=20261008)
    p.add_argument('--bootstrap', type=int, default=1000)
    p.add_argument('--margin', type=float, default=.02)
    p.add_argument('--ordered', action='store_true', help='Split per ordine righe; bootstrap resta iid')
    p.add_argument('--csv', type=Path)
    p.add_argument('--metadata', type=Path)
    return p


if __name__ == '__main__':
    p = parser()
    try:
        run(p.parse_args())
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        p.exit(2, f'Errore: {exc}\n')
