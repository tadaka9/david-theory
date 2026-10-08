# Prospective laboratory protocol

This document prepares future experiments; no physical experiment has been performed in this project.

## Experiment A: electric-motor energy balance

Objective: determine whether a balance based on independent measurements is compatible with `H=E-h` within uncertainty and identify omitted terms.

- `E`: electrical input energy, the time integral of power measured by a calibrated analyzer, in joules.
- `H`: shaft mechanical work, the integral of torque times angular velocity measured by a dynamometer and tachometer, in joules.
- `h`: heat dissipated by the motor and electronics measured calorimetrically, plus mechanical dissipation measured with a coast-down test, in joules.
- Storage term: change in kinetic and thermal energy between the beginning and end of the trial. Measure it or make it negligible under steady-state operation.

Design: at least 30 repetitions at each of five load levels selected before collection; randomized order; instruments zeroed before each block; technician calculating `H` without seeing `E-h`. Retain raw readings, calibration certificates, ambient temperature, and timestamps.

Primary outcome: `r = H-(E-h)`. The relation is compatible only if the preregistered equivalence interval contains the entire confidence interval for `r` and no systematic load dependence appears. The interval must come from the instrument uncertainty budget, not from observed results.

The same test bench covers energy, applied physics, and engineering, but it does not constitute three independent replications. Separate laboratories, operators, and instruments are required for each field.

## Experiment B: discrete engineering process

- `E`: number of units entering a production stage.
- `h`: rejected units observed and classified by an independent system.
- `H`: conforming units counted downstream by a second system.

Record rework, starting and ending inventory, and unclassified units. If `H` is calculated by subtracting `h` from `E`, the test becomes tautological. The primary criterion is balance closure with every category measured separately.

## Experiment C: causal psychology extension

Causality requires intervention. Proposed design: randomly assign participants in a 2x2 factorial design to high/low cognitive demand and support resource present/absent. Measure manipulation, performance, and fatigue with separate instruments; blind the analyst to group labels; preregister exclusions and the primary outcome.

The causal prediction concerns the effects and interaction of the manipulations on an independent outcome. It does not automatically turn the definitional residual `H:=E-h` into a psychological law. Ethical approval, informed consent, power analysis, and data collection by qualified researchers are required.
