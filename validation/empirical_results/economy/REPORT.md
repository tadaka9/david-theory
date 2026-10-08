# Audit empirico economico: contabilità nazionale 2022

**Dati reali World Bank. Audit di coerenza contabile, non validazione indipendente.**

- Serie complete congiunte: 158
- E: GNI (current US$), `NY.GNP.MKTP.CD`
- h: final consumption expenditure (current US$), `NE.CON.TOTL.CD`
- H: gross savings (current US$), `NY.GNS.ICTR.CD`
- Mediana di `|H-(E-h)|/|E|`: 3.5473%
- 90° percentile: 18.3638%
- Quota entro 1% del GNI: 29.75%
- Quota entro 5% del GNI: 60.13%

La definizione World Bank specifica che il risparmio lordo è reddito nazionale lordo meno consumo totale **più trasferimenti netti**. La formula ridotta omette quindi un termine noto. Inoltre le serie provengono dallo stesso sistema di contabilità nazionale. Una corrispondenza misura coerenza del database; una discrepanza può rappresentare trasferimenti netti, revisioni, differenze di copertura o aggregati sovranazionali. Non è un test causale né una conferma indipendente della teoria percettiva.
