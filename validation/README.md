# H = E - h: reproducible test harness

This is a methodological simulation, not empirical validation of a universal law. The complete paper is `PAPER.md`. The six field labels do not imply real disciplinary evidence.

## PowerShell execution on Windows

Python 3.12 is recommended. Open PowerShell in the extracted project directory. You do not need to activate the virtual environment or change the execution policy.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe experiment.py --out results --n 800 --seed 20261008 --bootstrap 1000 --margin 0.02
Get-Content .\results\REPORT.md
```

Use `--bootstrap 10000` for better tail resolution. To examine split sensitivity, run prespecified seeds in separate directories and report every result:

```powershell
foreach ($seed in @(20261008, 20261009, 20261010)) {
  .\.venv\Scripts\python.exe experiment.py --out "sensitivity_$seed" --seed $seed --bootstrap 1000
  if ($LASTEXITCODE -ne 0) { throw "Experiment failed: $seed" }
}
```

On Linux or macOS, create the environment with `python3 -m venv .venv` and use `.venv/bin/python`. GitHub Actions has verified the project with Python 3.12 on Ubuntu and Windows. Dependencies are version-pinned; small numerical differences between platforms or BLAS implementations remain possible.

## External data

Provide a CSV with the header `E,h,H`, at least 80 rows, and finite numeric values. Do not calculate H from the predictors. Copy `metadata.example.json`, replace every placeholder, and justify why H was observed independently.

```powershell
.\.venv\Scripts\python.exe experiment.py --csv data.csv --metadata metadata.json --out external_results --bootstrap 10000 --margin 0.02
```

Metadata validation does not certify data quality. The harness accepts only data declared iid. Time series, panels, clusters, and repeated measures require a suitable split and block or cluster bootstrap. Preserve source, license, period, units, measurement protocols, and exclusion criteria. Do not treat ordinal psychological scores as additive units without justification.

## Prespecified analysis

- Training 60%, validation 20%, test 20%; reproducible seeds and saved indices.
- Fixed theory: E-h. Additive: a+bE+ch. Interaction: additive+dEh. Nonlinear: interaction+eE²+fh².
- Select the baseline on validation MSE, then refit on training plus validation. Open the test set only after selection.
- Compare all three prespecified baselines with paired percentile bootstrap intervals and per-case Bonferroni correction.
- Predictive rejection occurs when a lower confidence bound exceeds the 0.02 squared-unit illustrative margin. Define a domain-specific margin before analyzing real data.
- Additive-parameter intervals against `(0,1,-1)` are diagnostic, not causal evidence or an equivalence test.
- Outputs include synthetic CSV files, JSON results, split/prediction audits, and Markdown reports.

## Method references

- [Scikit-learn: common pitfalls and data leakage](https://scikit-learn.org/1.7/common_pitfalls.html).
- [Shalizi, Carnegie Mellon: bootstrap](https://stat.cmu.edu/~cshalizi/dst/18/lectures/18/lecture-18.html).

The implementation uses NumPy, not scikit-learn. These references support methodology and do not attest to H=E-h.

## Included exploratory real-data analyses

The occupational-psychology analysis uses a de-identified formal sample of 274 metro construction managers from Zenodo. The central relation defines `H:=E-h`; the empirical extension is `Y=-z(burnout)=z(job resources)-z(job demands)`. Transformations are fitted on training data only.

```powershell
.\.venv\Scripts\python.exe empirical_psychology.py --out empirical_results\psychology --bootstrap 10000 --margin 0.05
.\.venv\Scripts\python.exe empirical_psychology.py --sample pilot --out empirical_results\psychology_pilot --bootstrap 10000 --margin 0.05
.\.venv\Scripts\python.exe empirical_economy.py --year 2022 --out empirical_results\economy
Get-Content .\empirical_results\psychology\REPORT.md
```

The psychology script downloads the source archive, verifies its SHA-256 hash, and does not redistribute individual responses. Pass `--archive path\metro_burnout_repository_package.zip` for offline use. The pilot is only a partial internal replication. The economics script queries the World Bank and performs an accounting audit; because gross savings is defined using income, consumption, and net transfers, it is not independent validation.

See `MATHEMATICAL_STATUS.md`, `LAB_PROTOCOL.md`, `PROSPECTIVE_PREREGISTRATION.md`, and `DATASET_AUDIT.md` for limitations and future work.

For a distinct claim that `h` or `H` is a numerical constant, see
`UNIVERSAL_CONSTANT_PROTOCOL.md`. Its `constant_validation.py` utility checks
finite bounded-error measurements for compatibility with one `h=E-H` value;
compatibility is not universal validation.
