# Cosa caricare in david-theory

Copiare il CONTENUTO di questa cartella nella radice di `david-theory`, inclusa la cartella nascosta `.github`. Prima di sostituire file esistenti confrontarli e integrare i contenuti. Nessun caricamento è stato effettuato da questa chat.

Caricare:

- PAPER.md: paper unico, ipotesi settoriali e risultati con limiti espliciti.
- README.md, experiment.py, empirical_psychology.py, empirical_economy.py, requirements.txt e tests/: replica eseguibile.
- results/: 24 CSV sintetici, audit, report e risultati numerici originali.
- empirical_results/: risultati psicologici esplorativi e audit economico, senza redistribuire le risposte individuali.
- MATHEMATICAL_STATUS.md, LAB_PROTOCOL.md, PROSPECTIVE_PREREGISTRATION.md e DATASET_AUDIT.md: stato dei limiti e lavoro futuro verificabile.
- metadata.example.json, PREREGISTRATION.md e CONTRIBUTING.md: percorso per misure reali e verifica indipendente.
- .github/: CI Linux/Windows e modulo per repliche/confutazioni.
- .gitignore: esclusione di ambienti e risultati locali non revisionati.

Scegliere autore e licenza di codice/paper prima della pubblicazione. Non presentare i dati sintetici come osservazioni disciplinari. Titolo suggerito del repository: «David Theory — H = E − h: falsification and reproducibility harness».

Procedura PowerShell, per chi usa Git e ha già accesso al repository:

```powershell
# All’interno del clone david-theory, dopo aver copiato e confrontato i file:
git switch -c add-reproducible-heh-experiment
git status
# Eseguire i comandi di verifica del README prima del commit.
git add README.md PAPER.md experiment.py empirical_psychology.py empirical_economy.py requirements.txt tests results empirical_results metadata.example.json PREREGISTRATION.md PROSPECTIVE_PREREGISTRATION.md LAB_PROTOCOL.md MATHEMATICAL_STATUS.md DATASET_AUDIT.md CONTRIBUTING.md GITHUB_UPLOAD.md .github .gitignore
git diff --cached --stat
git commit -m "Add reproducible synthetic falsification harness and interdisciplinary paper"
git push -u origin add-reproducible-heh-experiment
```

Aprire poi una pull request dalla pagina GitHub e controllare la CI. La CI inclusa produrrà artefatti di replica: non è stata ancora eseguita su GitHub. Non sovrascrivere una workflow omonima senza confronto. Una issue con risultati completi permette ai revisori di distinguere errori del codice, limiti dell’inferenza e confutazioni di una specifica ipotesi scientifica.
