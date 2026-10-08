# Protocollo prospettico di laboratorio

Questo documento prepara esperimenti futuri; nessun esperimento fisico è stato eseguito in questo progetto.

## Esperimento A: bilancio energetico di un motore elettrico

Obiettivo: verificare se un bilancio con misure indipendenti è compatibile con `H=E-h` entro l'incertezza, e identificare termini omessi.

- `E`: energia elettrica in ingresso, integrale temporale della potenza misurata con analizzatore calibrato, joule.
- `H`: lavoro meccanico all'albero, integrale di coppia per velocità angolare misurate da dinamometro e tachimetro, joule.
- `h`: calore disperso nel motore e nell'elettronica misurato calorimetricamente, più energia meccanica dissipata misurata con una prova di coast-down, joule.
- Termine di accumulo: variazione di energia cinetica e termica fra inizio e fine prova. Deve essere misurato o reso trascurabile con regime stazionario.

Disegno: almeno 30 ripetizioni per ciascuno di cinque livelli di carico scelti prima della raccolta; ordine casuale; strumenti azzerati prima di ogni blocco; tecnico che calcola `H` senza vedere `E-h`. Conservare letture grezze, certificati di calibrazione, temperatura ambiente e timestamp.

Esito primario: `r = H-(E-h)`. La relazione è compatibile soltanto se l'intervallo di equivalenza preregistrato contiene l'intero intervallo di confidenza di `r` e se non emerge una dipendenza sistematica dal carico. L'intervallo deve derivare dal budget di incertezza degli strumenti, non dai risultati osservati.

Questo stesso banco copre energia, fisica applicata e ingegneria, ma non tre repliche indipendenti: per ciascun campo servono laboratori, operatori e strumenti separati.

## Esperimento B: processo ingegneristico discreto

- `E`: numero di unità entrate in una fase produttiva.
- `h`: scarti osservati e classificati da un sistema indipendente.
- `H`: unità conformi contate a valle da un secondo sistema.

Registrare anche rilavorazioni, inventario iniziale/finale e unità non classificate. Se `H` viene calcolato sottraendo `h` da `E`, il test diventa tautologico. Il criterio primario è la chiusura del bilancio con tutte le categorie misurate separatamente.

## Esperimento C: estensione causale psicologica

La causalità richiede un intervento. Proposta: partecipanti assegnati casualmente in schema fattoriale 2x2 a richiesta cognitiva alta/bassa e risorsa di supporto presente/assente. Misurare manipolazione, prestazione e affaticamento con strumenti distinti; analista cieco alle etichette dei gruppi; esclusioni e outcome primario preregistrati.

La previsione causale riguarda effetti e interazione delle manipolazioni su un esito indipendente. Non trasforma automaticamente il residuo definitorio `H:=E-h` in una legge psicologica. Servono approvazione etica, consenso informato, calcolo di potenza e raccolta da parte di ricercatori qualificati.
