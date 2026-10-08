# Protocol for a universal-constant claim

## Claim to specify

`H := E-h` is an algebraic definition when `H` is constructed from `E` and `h`.
It does not imply a universal numerical constant. A constant claim must identify
the candidate explicitly:

- `h(x)=c` requires independently measured `E(x)-H(x)=c`;
- `H(x)=C` requires independently measured `E(x)-h(x)=C`.

These are different empirical hypotheses. The domain `x`, units, instruments,
calibration, uncertainty model, and meaningful equivalence tolerance must be
fixed before confirmation data are observed.

## Bounded-error compatibility check

For row `j`, let `E_hat` and `H_hat` have absolute error bounds `error_E` and
`error_H`. A candidate `c=E-H` belongs to

`[E_hat-H_hat-(error_E+error_H), E_hat-H_hat+(error_E+error_H)]`.

One constant is feasible only when all row intervals intersect. An empty
intersection rejects one shared constant under the stated assumptions. A
nonempty intersection means compatibility with the finite data; it does not
prove universality.

Prepare a CSV with `E,H,error_E,error_H`, then run:

```powershell
.\.venv\Scripts\python.exe constant_validation.py measurements.csv --out constant_result.json
```

The measurements must be independent. Calculating `H` as `E-h` and then testing
whether `E-H=h` is circular. Shared calibration errors and common data sources
must be modeled because they can create apparent constancy.

## Stochastic measurements

For repeated stochastic observations, preregister an equivalence region rather
than treating a nonsignificant heterogeneity test as proof. Estimate variation
between subjects, phenomena, times, instruments, and domains. Confidence
intervals for the relevant differences and variation components must fall
inside the justified equivalence bounds. Confirm on untouched domains and seek
an independent replication.

No finite sample proves invariance over every possible domain. Evidence can
support only the stated domain, instruments, conditions, and precision.

## Economic model and dimensions

For `h_D=expit(alpha U+beta L+gamma D-delta Q)`, the logistic output is bounded
and dimensionless. If it is to represent the `h` subtracted from `E`, the theory
must specify a measurement map or scale factor that gives both quantities a
common additive scale. Otherwise `h_D` is an index associated with the theory,
not the same measured quantity as `h`.

Because `expit` is strictly increasing, `h_D` is constant exactly when its
linear index is constant on the chosen domain. If the four predictors vary
independently over an open region, constancy requires all four slopes to be
zero. Cancellation among dependent predictors on one observed sample does not
establish universal invariance.
