# Exploratory empirical test: occupational psychology (formal)

**Real data, exploratory analysis. This is not confirmatory validation of a universal formula.**

- Source: https://zenodo.org/records/21153011
- Complete sample analyzed: 274 respondents
- Sample role: formal
- Specification: `H=-z(burnout)`, `E=z(job resources)`, `h=z(job demands)`
- Transformations fitted on training data only
- Split: [164, 55, 55] (training, validation, test)
- Baseline selected on validation: interaction
- Theory RMSE on test: 1.4598
- Selected-baseline RMSE on test: 0.6682
- Delta MSE, theory minus baseline: 1.6847
- Simultaneous 95% interval for delta: [0.8945267080133462, 2.7730091358220186]
- Margin prespecified in code: 0.0500 squared standardized units
- Operational decision: `falsified_operationally`

The result concerns only the predictive extension that identifies the residual with standardized well-being; the central relation H:=E-h remains a definitional identity. Standardization makes numerical scales comparable but does not prove that the constructs share a substantive unit. The dataset is cross-sectional and does not identify causality. Because the hypothesis and margin were not preregistered before collection, this result defines a specification for prospective replication.
