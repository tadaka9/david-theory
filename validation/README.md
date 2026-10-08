# H = E − h: banco di prova riproducibile

Questa è una simulazione metodologica, NON una validazione empirica di una legge universale. Il paper completo è `PAPER.md`. Le etichette dei sei settori non implicano dati disciplinari reali.

## Esecuzione PowerShell (Windows)

Python 3.12 consigliato. Aprire PowerShell nella cartella estratta del progetto. Non è necessario attivare l’ambiente virtuale né cambiare ExecutionPolicy.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe experiment.py --out results --n 800 --seed 20261008 --bootstrap 1000 --margin 0.02
Get-Content .\results\REPORT.md
```

Per stimare meglio le code degli intervalli, usare `--bootstrap 10000`. Per studiare sensibilità allo split, eseguire semi prefissati in cartelle distinte, riportando tutti i risultati (senza selezionare il migliore):

```powershell
foreach ($seed in @(20261008, 20261009, 20261010)) {
  .\.venv\Scripts\python.exe experiment.py --out "sensitivity_$seed" --seed $seed --bootstrap 1000
  if ($LASTEXITCODE -ne 0) { throw "Esperimento fallito: $seed" }
}
```

Linux/macOS: `python3 -m venv .venv`, quindi usare `.venv/bin/python` al posto del percorso Windows. Il progetto è stato eseguito su Linux con Python 3.12 e NumPy 2.2.6; PowerShell non è stato eseguito in questo ambiente. Dipendenza bloccata per versione; piccole differenze numeriche fra piattaforme/BLAS sono possibili.

## Dati esterni

CSV con intestazione `E,h,H`, almeno 80 righe, numeri finiti. Non calcolare H dai predittori. Preparare una copia di `metadata.example.json`, sostituendo TUTTI i segnaposto e giustificando l’indipendenza dell’osservazione di H (non indipendenza statistica dalle altre variabili).

```powershell
.\.venv\Scripts\python.exe experiment.py --csv dati.csv --metadata metadata.json --out external_results --bootstrap 10000 --margin 0.02
```

La lettura dei metadata non certifica la qualità dei dati. Il metodo accetta soltanto campionamento dichiarato iid. Per serie temporali/panel serve un nuovo protocollo con blocchi/cluster; `--ordered` cambia lo split ma NON rende corretto il bootstrap iid per dati dipendenti. Conservare fonte, licenza, periodo, unità, protocolli di misura e criteri di esclusione. Non usare punteggi psicologici ordinali come unità additive senza giustificazione.

## Specifica fissata prima dell’analisi

- Train 60%, validation 20%, test 20%; semi riproducibili e indici salvati.
- Teoria fissa: E − h. Additivo: a + bE + ch. Interazione: additivo + dEh. Nonlineare: interazione + eE² + fh².
- Scelta della baseline mediante MSE validation; rifit sullo sviluppo (train + validation). Test aperto soltanto dopo la scelta.
- Tutte le tre baseline sono confronti prefissati, con CI bootstrap percentile e correzione Bonferroni per caso. Differenza: MSE teoria meno MSE baseline.
- Rigetto predittivo se limite inferiore del CI > 0.02 unità². Margine illustrativo, da ridefinire PRIMA di dati reali in base al dominio e alla precisione di misura.
- CI dei parametri additivi rispetto a (0,1,−1), diagnostica separata; non prova causale né test di equivalenza.
- Output: CSV sintetici, risultati JSON, audit degli split/previsioni e report Markdown. Una nuova esecuzione nella stessa cartella sovrascrive gli output corrispondenti.

## Fonti metodologiche

- [Scikit-learn: leakage e preprocessing](https://scikit-learn.org/1.7/common_pitfalls.html).
- [Shalizi, Carnegie Mellon: bootstrap](https://stat.cmu.edu/~cshalizi/dst/18/lectures/18/lecture-18.html).

Il codice usa NumPy, non scikit-learn. Questi riferimenti documentano i principi; non attestano H = E − h.

## Analisi empiriche esplorative incluse

Il progetto include un test su dati reali di psicologia del lavoro. Usa il campione formale de-identificato di 274 addetti alla gestione di cantieri metropolitani pubblicato su Zenodo. La relazione centrale definisce `H:=E-h`; l'estensione empirica testata è `Y=-z(burnout)=z(job resources)-z(job demands)`. Le trasformazioni sono stimate esclusivamente sul training.

```powershell
.\.venv\Scripts\python.exe empirical_psychology.py --out empirical_results\psychology --bootstrap 10000 --margin 0.05
.\.venv\Scripts\python.exe empirical_psychology.py --sample pilot --out empirical_results\psychology_pilot --bootstrap 10000 --margin 0.05
.\.venv\Scripts\python.exe empirical_economy.py --year 2022 --out empirical_results\economy
Get-Content .\empirical_results\psychology\REPORT.md
```

Lo script psicologico scarica l'archivio dalla fonte, controlla l'hash SHA-256 e non redistribuisce le risposte nel repository. Per lavorare offline, passare `--archive percorso\metro_burnout_repository_package.zip`. Il campione pilot è una replica interna parziale. Lo script economico interroga World Bank e produce un audit contabile: poiché il risparmio è definito usando reddito, consumo e trasferimenti netti, non è una validazione indipendente.

Per il lavoro futuro vedere `MATHEMATICAL_STATUS.md`, `LAB_PROTOCOL.md`, `PROSPECTIVE_PREREGISTRATION.md` e `DATASET_AUDIT.md`.
