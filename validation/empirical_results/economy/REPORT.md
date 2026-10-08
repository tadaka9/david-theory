# Empirical economics audit: national accounts 2022

**Real World Bank data. Accounting consistency audit, not independent validation.**

- Complete joined series: 158
- E: GNI (current US$), `NY.GNP.MKTP.CD`
- h: final consumption expenditure (current US$), `NE.CON.TOTL.CD`
- H: gross savings (current US$), `NY.GNS.ICTR.CD`
- Median `|H-(E-h)|/|E|`: 3.5473%
- 90th percentile: 18.3638%
- Share within 1% of GNI: 29.75%
- Share within 5% of GNI: 60.13%

World Bank metadata defines gross savings as gross national income minus total consumption **plus net transfers**. The reduced formula therefore omits a known term. The series also come from the same national-accounts system. Agreement measures database consistency; a discrepancy may represent net transfers, revisions, coverage differences, or supranational aggregates. This is neither a causal test nor independent confirmation of the perceptual theory.
