# Verifica empirica esplorativa: psicologia del lavoro (formal)

**Dati reali, analisi esplorativa. Non è una validazione confermativa della formula universale.**

- Fonte: https://zenodo.org/records/21153011
- Campione completo analizzato: 274 rispondenti
- Ruolo del campione: formal
- Specifica: `H=-z(burnout)`, `E=z(job resources)`, `h=z(job demands)`
- Trasformazioni stimate soltanto sul training
- Split: [164, 55, 55] (training, validation, test)
- Baseline scelta sulla validation: interaction
- RMSE teoria sul test: 1.4598
- RMSE baseline scelta sul test: 0.6682
- Delta MSE teoria meno baseline: 1.6847
- CI simultaneo 95% del delta: [0.8945267080133462, 2.7730091358220186]
- Margine preregistrato nel codice: 0.0500 unità standardizzate²
- Esito operativo: `falsified_operationally`

L'esito riguarda esclusivamente l'estensione predittiva che identifica il residuo con il benessere standardizzato; la relazione centrale H:=E-h resta un'identità definitoria. La standardizzazione rende confrontabili le scale numeriche, ma non dimostra che i costrutti abbiano la stessa unità sostantiva. Il dataset è trasversale; non identifica causalità. Poiché l'ipotesi e il margine non furono preregistrati prima della raccolta dei dati, questo risultato genera una specifica da replicare prospetticamente.
