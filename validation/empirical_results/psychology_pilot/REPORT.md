# Exploratory empirical test: occupational psychology (pilot)

**Real data, exploratory analysis. This is not confirmatory validation of a universal formula.**

- Source: https://zenodo.org/records/21153011
- Complete sample analyzed: 140 respondents
- Sample role: pilot
- Specification: `H=-z(burnout)`, `E=z(job resources)`, `h=z(job demands)`
- Transformations fitted on training data only
- Split: [84, 28, 28] (training, validation, test)
- Baseline selected on validation: nonlinear
- Theory RMSE on test: 1.3555
- Selected-baseline RMSE on test: 1.2267
- Delta MSE, theory minus baseline: 0.3326
- Simultaneous 95% interval for delta: [-0.8792817398265672, 1.4234915325189854]
- Margin prespecified in code: 0.0500 squared standardized units
- Operational decision: `falsified_operationally`

The result concerns only the predictive extension that identifies the residual with standardized well-being; the central relation H:=E-h remains a definitional identity. Standardization makes numerical scales comparable but does not prove that the constructs share a substantive unit. The dataset is cross-sectional and does not identify causality. Because the hypothesis and margin were not preregistered before collection, this result defines a specification for prospective replication.
