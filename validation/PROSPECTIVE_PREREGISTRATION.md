# Preregistrazione prospettica v1

Data di redazione: 8 ottobre 2026. Diventa temporalmente verificabile quando il commit viene pubblicato. Vale soltanto per dati raccolti o resi accessibili dopo quel commit; non retrodata le analisi già svolte.

## Ipotesi primaria psicologica futura

In un nuovo campione indipendente, con le stesse scale del dataset Zenodo 21153011, si definiscono sul solo training `E=z(risorse lavorative)`, `h=z(richieste lavorative)` e l'estensione esterna `Y=-z(burnout)`. La relazione centrale definisce `H:=E-h`; la previsione empirica separata è `Y=H`.

Confronti prefissati: previsione a coefficienti fissi; modello additivo libero; additivo con interazione; quadratico. Split 60/20/20 con seme 20261008. Baseline scelta sulla validation, test aperto una sola volta. Metriche primarie: MSE e differenza paired fra teoria e ciascuna baseline. Bootstrap 10.000 repliche, correzione Bonferroni sui tre confronti. Margine: 0,05 unità standardizzate al quadrato.

La previsione `Y=H` è falsificata operativamente se il limite inferiore simultaneo della differenza MSE teoria meno almeno una baseline supera 0,05. La mancata falsificazione non dimostra equivalenza: un test di equivalenza e una soglia di precisione devono essere aggiunti prima della raccolta se si vuole sostenere compatibilità.

## Ipotesi fisico-ingegneristica futura

Usare il protocollo in `LAB_PROTOCOL.md`. Il margine di equivalenza sarà determinato dal budget di incertezza strumentale e inserito in una nuova versione della preregistrazione prima di acquisire dati. Senza questa quantità l'esperimento non deve essere presentato come confermativo.

## Trasparenza

Pubblicare dati consentiti, dizionario, calibrazioni, esclusioni, codice e tutti gli esiti. Ogni deviazione sarà etichettata e ogni nuova definizione di `E`, `h`, `H` o `Y` costituirà una nuova ipotesi.
