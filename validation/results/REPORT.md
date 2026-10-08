# H = E - h results

SYNTHETIC DATA: method verification only; no real empirical validation.

| Field | Scenario | Theory RMSE | Selected-baseline RMSE | Operational decision |
|---|---|---:|---:|---|
| energy | compatible | 0.2870 | 0.2885 | not_falsified_not_validated |
| energy | additive_violation | 0.7584 | 0.3000 | falsified_operationally |
| energy | interaction_violation | 2.3924 | 0.2919 | falsified_operationally |
| energy | nonlinear_violation | 1.4748 | 0.2955 | falsified_operationally |
| engineering | compatible | 0.2865 | 0.2868 | not_falsified_not_validated |
| engineering | additive_violation | 0.7456 | 0.3046 | falsified_operationally |
| engineering | interaction_violation | 2.5070 | 0.2848 | falsified_operationally |
| engineering | nonlinear_violation | 1.3209 | 0.2994 | falsified_operationally |
| physics | compatible | 0.3000 | 0.3015 | not_falsified_not_validated |
| physics | additive_violation | 0.7571 | 0.3039 | falsified_operationally |
| physics | interaction_violation | 2.4061 | 0.3139 | falsified_operationally |
| physics | nonlinear_violation | 1.3802 | 0.3059 | falsified_operationally |
| mathematics | compatible | 0.2869 | 0.2860 | not_falsified_not_validated |
| mathematics | additive_violation | 0.7195 | 0.3208 | falsified_operationally |
| mathematics | interaction_violation | 2.5107 | 0.3140 | falsified_operationally |
| mathematics | nonlinear_violation | 1.4039 | 0.3144 | falsified_operationally |
| economics | compatible | 0.2882 | 0.2872 | not_falsified_not_validated |
| economics | additive_violation | 0.7210 | 0.3205 | falsified_operationally |
| economics | interaction_violation | 2.4596 | 0.2953 | falsified_operationally |
| economics | nonlinear_violation | 1.4323 | 0.2893 | falsified_operationally |
| psychology | compatible | 0.2943 | 0.2989 | not_falsified_not_validated |
| psychology | additive_violation | 0.6509 | 0.2779 | falsified_operationally |
| psychology | interaction_violation | 2.6626 | 0.3420 | falsified_operationally |
| psychology | nonlinear_violation | 1.4541 | 0.3037 | falsified_operationally |

## Interpretation

Failure to falsify does not prove the formula. Each compatible scenario is generated from the formula itself and serves as a software positive control.
Positive delta MSE favors the baseline. Operational falsification requires the lower confidence bound to exceed the prespecified MSE margin. The nominal simultaneous 95% interval uses Bonferroni correction across three within-case comparisons and does not globally correct all 24 cases.
The iid percentile bootstrap on test rows is conditional on fitted models and excludes training variability. The development-row coefficient bootstrap is diagnostic and not evidence of equivalence.
Additive restrictions are intercept 0, E coefficient 1, and h coefficient -1. If the additive model is misspecified, rejecting these restrictions alone is not structural falsification.
The nonlinear model is quadratic and does not represent every nonlinear alternative. No causal inference is made. A single split does not establish sampling robustness.
The six field labels use the same abstract harness with different seeds; they are not six real disciplinary experiments. Numerical results do not replace proof in mathematics.
See results.json for details, intervals, and configuration; see case_*/audit.json for split indices and predictions.
