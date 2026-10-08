# Plasticity of H = E - h: interdisciplinary interpretations and a reproducible falsification protocol

**Methodological working paper - October 8, 2026. Version 0.4.** Includes exploratory tests of empirical extensions in occupational psychology and a real-data economics audit. It does not claim universal validation or a new physical law. Authorship and affiliation should be confirmed before formal publication.

## Abstract

This paper examines `H = E-h` as a transferable balance schema while separating definitional identities, measurable hypotheses, and statistical models. Plasticity means that the variables can receive domain-specific interpretations; it does not establish universality. A reproducible Python experiment compares a fixed prediction with additive, interaction, and quadratic baselines using training/validation/test splits and bootstrap inference. Twenty-four synthetic controls cover six disciplinary labels and four data-generating processes. A real-data analysis tests the external prediction `Y=-z(burnout)=z(job resources)-z(job demands)` in a formal sample of 274 workers. The extension is operationally falsified in that sample: RMSE 1.460 versus 0.668 for the selected baseline, with a simultaneous MSE-improvement interval of [0.895, 2.773], above the 0.05 margin. A 140-person pilot provides only a partial internal replication. A World Bank audit of 158 complete 2022 series finds a median discrepancy of 3.55% of GNI for the reduced economics relation, but gross savings is defined from income, consumption, and net transfers, so the audit is not independent validation. These analyses do not test the identity `H:=E-h` itself.

## 1. Plasticity and scientific content

A short formula can organize different descriptions when `E` denotes an initial magnitude, `h` a subtractive term, and `H` the residual. This flexibility can help formulate hypotheses, but it can also make a claim immune to falsification if variables are redefined after observing results. A testable version must fix the domain, units, measurement procedures, and failure conditions before observation.

The symbols do not inherit the conventional meanings of similarly named physical quantities. In particular, `h` is not Planck's constant: subtracting action measured in joule-seconds from energy measured in joules would be dimensionally invalid. The relation neither follows from nor replaces `E=mc²`.

## 2. Three distinct statuses

**Identity.** If `H` is defined as `E-h`, the formula is true by construction. Regression cannot verify a separate property of the world.

**Deterministic hypothesis.** An independently observed `H` may be predicted to equal the difference within preregistered measurement tolerances. This requires an error model and independent measurements.

**Statistical extension.** A project may posit an external outcome `Y=E-h+epsilon`, with a zero conditional mean for the error. This is an additional empirical hypothesis, not a consequence of subtraction. Failure to falsify it would not establish equality, equivalence, causality, or universality.

## 3. Interdisciplinary map

| Field | Proposed E | Proposed h | Independently observed quantity | Main qualification |
|---|---|---|---|---|
| Energy | Device input energy, J | Measured dissipation, J | Useful output energy, J | Define boundaries and storage; omitted flows break a two-term balance. |
| Engineering | Units entering a process | Independently counted rejects | Independently counted conforming units | Rework, inventory, and unclassified units must be recorded. |
| Physics | Available energy in a defined system, J | Transfer through excluded channels, J | Energy in the observed channel, J | Specify system, regime, storage, and all channels. This is not an alternative to relativity. |
| Mathematics | Element `E` of an additive group | Element `h` of the same group | Defined or independently characterized `H` | A definition is proved algebraically; an independent universal equality needs axioms. |
| Economics | Monetary resources in a fixed period | Measured uses or constraints | Independently observed residual resources | Use the same currency, price basis, and period; include transfers and valuation effects. |
| Psychology | Resource score on a justified metric scale | Demand score on a compatible scale | Separate validated outcome | Standardization does not by itself create substantively identical units. |

These are candidate operationalizations, not claims that the disciplines have adopted the formula.

## 4. Synthetic method

Each synthetic case contains 800 iid observations. `E` is uniform on [1,5], `h` is uniform on [0,2], and the noise standard deviation is 0.3. The variables are abstract surrogates, not measurements in joules, dollars, or psychological units. The four generators are:

1. compatible: `H=E-h+epsilon`;
2. additive violation: `H=0.8+0.55E-0.3h+epsilon`;
3. interaction violation: `H=E-h+0.65Eh+epsilon`;
4. nonlinear violation: `H=E-h+0.7(E-3)^2+0.5(h-1)^2+epsilon`.

The fixed theory estimates no parameters. Baselines estimate a free additive model, an additional `Eh` interaction, and additional `E²,h²` terms. The random split is 60% training, 20% validation, and 20% test. Baseline selection uses validation MSE; models are then refitted on training plus validation. The test set does not determine model selection.

For each baseline, `delta=MSE(theory)-MSE(baseline)`. A paired test-row bootstrap uses 1,000 repetitions and Bonferroni correction across the three prespecified comparisons. Operational falsification requires a simultaneous lower bound above the illustrative 0.02 squared-unit margin. A domain-specific margin must be fixed before real-data analysis.

## 5. Synthetic results

Across all six labels, none of the six compatible controls was rejected. All 18 constructed additive, interaction, and nonlinear violations were detected. This confirms that the software responds to known positive and negative controls; it does not estimate power, type-I error, or evidence in any discipline.

Complete metrics, intervals, coefficients, configuration, split indices, and predictions are stored under `results/`.

## 6. Exploratory occupational-psychology extension

The source is the formal sample from *De-identified survey data for job demands, job resources, and burnout among metro site management personnel in China*, Zenodo record 21153011. The archive is accepted only when its SHA-256 hash matches the pinned value. Individual responses are not redistributed.

The central identity defines `H:=E-h`. The separate empirical extension sets `E=z(job resources)`, `h=z(job demands)`, and `Y=-z(burnout)`, then predicts `Y=H`. Means and standard deviations are fitted on 164 training rows and applied to 55 validation and 55 test rows. The operational MSE margin is 0.05 squared standardized units, with 10,000 paired bootstrap repetitions.

The interaction baseline was selected on validation data. On test data, the fixed extension has RMSE 1.4598, MAE 1.1234, and R² -1.6941. The selected baseline has RMSE 0.6682, MAE 0.4616, and R² 0.4356. The MSE difference is 1.6847 with simultaneous 95% interval [0.8945, 2.7730]. All three prespecified baselines outperform the fixed prediction. The external extension `Y=H` is operationally falsified in this sample; the identity `H:=E-h` remains true by definition.

The pilot sheet contains 140 different participants and the initial scale items. On its test split, the fixed prediction has RMSE 1.3555. The quadratic model selected on validation has RMSE 1.2267, but its MSE-difference interval [-0.8793, 1.4235] is inconclusive. The prespecified additive and interaction comparisons have lower bounds 0.1430 and 0.1484, above the 0.05 margin. This is a partial internal replication, not an independent external replication.

The analysis is exploratory: the operationalization postdates data collection, original scales differ, the design is cross-sectional, and no causal conclusion is available.

## 7. World Bank accounting audit

For 2022, the audit joins GNI as `E`, final consumption as `h`, and gross savings as `H`, all in current US dollars. Among 158 complete country or aggregate series, median `|H-(E-h)|/|E|` is 3.5473%, the 90th percentile is 18.3638%, and 60.13% lie within 5% of GNI.

World Bank metadata defines gross savings as national income minus consumption plus net transfers. The reduced formula omits that known term, and all three series belong to the same national-accounts system. The result documents database consistency and an omitted component; it is not independent confirmation or a causal test of the perceptual theory.

## 8. Reproducibility

The project contains version-pinned dependencies, command-line programs, synthetic CSV files, split indices, test predictions, source hashes, reports, and 13 automated tests. The test suite and synthetic reproduction passed through GitHub Actions on Ubuntu and Windows. A manual GitHub workflow also reproduced both psychology samples and the World Bank audit from the published sources.

The tests verify covered software behavior. They do not certify a scientific model or exact finite-sample confidence coverage.

## 9. Prospective research program

Before collection, choose one domain interpretation; document units, boundaries, independent measurements, uncertainty, margin, sampling design, exclusions, alternatives, and multiplicity correction. Preregister the protocol and reserve confirmation data that are untouched by model selection. Time series, panels, clusters, and repeated measures need appropriate splits and block or cluster inference.

Separate exploration from independent confirmation. Redefining variables after a failure creates a new hypothesis that must be tested on new data. In mathematics, replace statistical testing with a precise statement, assumptions, proof, and counterexample search.

## 10. Conclusion

`H=E-h` is mathematically valid as a definition when subtraction, units, and the domain are specified. Its plasticity does not produce a universal empirical law. The fixed-weight psychology extension is rejected in the formal sample and receives mixed but unfavorable evidence in the pilot. The economics audit exposes a known omitted term. Energy, engineering, and physics still require independent laboratory measurements under a preregistered uncertainty budget.

## References

1. Scikit-learn, *Common pitfalls and recommended practices*: https://scikit-learn.org/1.7/common_pitfalls.html
2. C. R. Shalizi, Carnegie Mellon University, *Simulation for Inference I - The Bootstrap*: https://stat.cmu.edu/~cshalizi/dst/18/lectures/18/lecture-18.html
3. Zhao, C., Qi, J., and Chen, Y., *De-identified survey data for job demands, job resources, and burnout among metro site management personnel in China*, Zenodo record 21153011: https://zenodo.org/records/21153011
4. World Bank, *World Development Indicators API* and gross-savings metadata: https://datahelpdesk.worldbank.org/knowledgebase/articles/898599-indicator-api-queries
