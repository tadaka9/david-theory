# Real-data source audit

| Field | Source reviewed | Decision |
|---|---|---|
| Psychology | Zenodo 21153011: job demands, resources, and burnout | Used to test the predictive extension `Y=E-h`, not the definitional identity. Formal sample: 274; pilot: 140. |
| Economics | World Bank WDI: GNI, final consumption, gross savings | Used for a 2022 accounting audit. It is not independent because savings is defined from income and consumption plus net transfers. |
| Energy/engineering | UCI Energy Efficiency | Not used: heating/cooling loads and building characteristics do not form three homogeneous `E,h,H` measurements. |
| Energy | Eurostat CHP statistics | Candidate source, but fuel input, output, and primary-energy savings follow regulatory definitions and do not yet provide an independent residual measurement. |
| Physics | No suitable integrated source | The original theory explicitly rejects automatic identification with physical energy or Planck's constant. A defined experimental system and uncertainty budget are required first. |
| Mathematics | Not applicable | Mathematics requires a proof or counterexample, not a dataset. |

This selection is not a systematic literature review. It is a suitability audit based on common units, measurement independence, and definitions fixed before analysis.
