# Verifica empirica esplorativa: psicologia del lavoro (pilot)

**Dati reali, analisi esplorativa. Non è una validazione confermativa della formula universale.**

- Fonte: https://zenodo.org/records/21153011
- Campione completo analizzato: 140 rispondenti
- Ruolo del campione: pilot
- Specifica: `H=-z(burnout)`, `E=z(job resources)`, `h=z(job demands)`
- Trasformazioni stimate soltanto sul training
- Split: [84, 28, 28] (training, validation, test)
- Baseline scelta sulla validation: nonlinear
- RMSE teoria sul test: 1.3555
- RMSE baseline scelta sul test: 1.2267
- Delta MSE teoria meno baseline: 0.3326
- CI simultaneo 95% del delta: [-0.8792817398265672, 1.4234915325189854]
- Margine preregistrato nel codice: 0.0500 unità standardizzate²
- Esito operativo: `falsified_operationally`

L'esito riguarda esclusivamente l'estensione predittiva che identifica il residuo con il benessere standardizzato; la relazione centrale H:=E-h resta un'identità definitoria. La standardizzazione rende confrontabili le scale numeriche, ma non dimostra che i costrutti abbiano la stessa unità sostantiva. Il dataset è trasversale; non identifica causalità. Poiché l'ipotesi e il margine non furono preregistrati prima della raccolta dei dati, questo risultato genera una specifica da replicare prospetticamente.
