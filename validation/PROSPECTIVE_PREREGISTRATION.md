# Prospective preregistration v1

Drafted on October 8, 2026. It becomes time-verifiable when committed publicly. It applies only to data collected or first made accessible after that commit and does not retroactively preregister completed analyses.

## Primary future psychology hypothesis

In a new independent sample using the scales from Zenodo dataset 21153011, define from training data only `E=z(job resources)`, `h=z(job demands)`, and the external outcome `Y=-z(burnout)`. The central relation defines `H:=E-h`; the separate empirical prediction is `Y=H`.

Prespecified comparisons: fixed-coefficient prediction, free additive model, additive model with interaction, and quadratic model. Use a 60/20/20 split with seed 20261008. Select the baseline on validation data and open the test set once. Primary metrics are MSE and the paired difference between the theory and each baseline. Use 10,000 bootstrap repetitions and Bonferroni correction across the three comparisons. The margin is 0.05 squared standardized units.

Operationally falsify `Y=H` if the simultaneous lower confidence bound for theory MSE minus at least one baseline MSE exceeds 0.05. Failure to falsify does not establish equivalence; an equivalence test and precision threshold must be added before collection if compatibility is to be claimed.

## Future physical and engineering hypothesis

Use `LAB_PROTOCOL.md`. Determine the equivalence margin from the instrument uncertainty budget and record it in a new preregistration version before acquiring data. Without that value, the experiment must not be described as confirmatory.

## Transparency

Publish permitted data, a data dictionary, calibrations, exclusions, code, and every outcome. Label every deviation. Any new definition of `E`, `h`, `H`, or `Y` constitutes a new hypothesis.
