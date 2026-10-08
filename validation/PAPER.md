# Plasticità della relazione H = E − h: interpretazioni interdisciplinari e protocollo riproducibile di falsificazione

**Working paper metodologico — 8 ottobre 2026.** Versione 0.3. Include test esplorativi di estensioni empiriche in psicologia del lavoro e un audit contabile economico; nessuna validazione universale e nessuna rivendicazione di nuova legge fisica. Autorialità e affiliazione da confermare prima della pubblicazione.

## Abstract

Si esamina H = E − h come schema di bilancio trasferibile fra domini, distinguendo identità definitorie, ipotesi misurabili e modelli statistici. La plasticità riguarda l’adattamento semantico delle variabili, non una universalità dimostrata. Un esperimento Python riproducibile confronta una previsione vincolata con baseline additive, con interazione e quadratiche, mediante split train/validation/test e bootstrap. Ventiquattro casi sintetici coprono sei etichette disciplinari e quattro processi generatori. Una seconda analisi usa dati reali de-identificati di 274 lavoratori e testa l'estensione esterna `Y=-z(burnout)=z(risorse)-z(richieste)`. Nel campione formale l'estensione è falsificata operativamente: RMSE 1,460 contro 0,668 della baseline selezionata, con intervallo simultaneo del vantaggio MSE [0,895; 2,773], superiore al margine 0,05. Una coorte pilot di 140 partecipanti fornisce una replica interna parziale. Un audit World Bank su 158 serie del 2022 trova uno scarto mediano del 3,55% del GNI per la formula economica ridotta, ma non è indipendente perché il risparmio è definito da reddito, consumo e trasferimenti netti. Le analisi sono esplorative e non testano l'identità `H:=E-h` in sé. Si propone un protocollo di preregistrazione e replica indipendente per future indagini.

## 1. Problema e significato della plasticità

Una formula breve può organizzare molte descrizioni se E indica una disponibilità iniziale, h una sottrazione e H un risultato residuo. Questa flessibilità può facilitare la costruzione di ipotesi, ma anche renderle immuni alla confutazione se le variabili vengono ridefinite dopo aver visto i risultati. Una versione scientificamente controllabile deve fissare dominio, unità, misura e condizioni di fallimento prima dell’osservazione.

Le lettere non possiedono qui il significato convenzionale dei simboli fisici omonimi. In particolare h non è assunto essere la costante di Planck: sottrarre un’azione, misurata in joule-secondi, da un’energia in joule sarebbe dimensionalmente incoerente. La relazione non deriva né sostituisce E = mc².

## 2. Tre statuti distinti

**Identità.** Se H è definita come E − h, la formula è vera per costruzione. Nessuna regressione ne verifica una proprietà del mondo.

**Ipotesi deterministica.** H osservata indipendentemente è uguale alla differenza entro tolleranze di misura preregistrate. È necessario un modello degli errori di misura; l’attuale harness non esegue una metrologia completa né un test di uguaglianza riga per riga.

**Ipotesi statistica operativa.** In questo esperimento si pone H = E − h + ε con media condizionale di ε nulla. È una formalizzazione aggiuntiva esplicita, non una conseguenza dimostrata della formula originale. Il programma valuta prestazioni predittive e diagnostica i vincoli del modello additivo. La mancata falsificazione non dimostra uguaglianza, equivalenza, causalità o universalità.

## 3. Mappa interdisciplinare: ipotesi da rendere misurabili

| Area | E proposta | h proposta | H da osservare separatamente | Condizioni e possibili confutazioni |
|---|---|---|---|---|
| Energia | Energia entrante in un dispositivo, J | Dissipazione misurata, J | Energia utile in uscita, J | Definire confini e intervallo. Accumulo e flussi omessi possono invalidare il bilancio a due termini. Misurare input, output e perdite con strumenti distinti. |
| Ingegneria | Quantità di pezzi lavorati in un lotto | Scarti contati | Pezzi conformi contati separatamente | Verificare rilavorazioni, inventario e categorie esaustive. Se H è ricavata sottraendo scarti, si tratta di contabilità e non conferma indipendente. |
| Fisica | Energia disponibile in un sistema scelto, J | Trasferimenti in canali esclusi, J | Energia del canale osservato, J | Specificare sistema e regime. Un termine di accumulo o un canale non misurato può richiedere un’equazione più ampia. Non costituisce alternativa alla relatività. |
| Matematica | Elemento E di uno spazio vettoriale | Elemento h dello stesso spazio | Elemento H definito o indipendentemente caratterizzato | Se H := E − h, è una definizione. Se H ha altra definizione, l’uguaglianza richiede una dimostrazione dagli assiomi. Esempio reale: E=3, h=1, H=4 confuta un’enunciazione universale senza vincoli. |
| Economia | Risorse monetarie disponibili nel periodo | Impieghi vincolati misurati | Risorse residue misurate indipendentemente | Stessa valuta, base nominale/reale e periodo; includere credito, risparmio, trasferimenti e valutazioni. Non equiparare automaticamente risorse residue a benessere. |
| Psicologia | Punteggio di risorsa su una scala metrica giustificata | Punteggio di carico su unità comparabili | Esito su scala validata e rilevata separatamente | La sottrazione richiede scale e calibrazione compatibili; punteggi ordinali non bastano. Interazioni, saturazione, variabilità individuale e affidabilità possono confutare la versione lineare. |

La tabella propone operazionalizzazioni, non dichiara che queste discipline adottino la formula. Energia e fisica si sovrappongono in questa mappa. La psicologia richiede una validazione delle misure prima di una prova della relazione. In matematica, la verifica numerica è una ricerca di esempi o controesempi e non sostituisce una dimostrazione generale.

## 4. Metodo computazionale

Per ogni caso si generano 800 osservazioni indipendenti, E uniforme fra 1 e 5, h uniforme fra 0 e 2 e rumore normale con deviazione standard 0.3. Le variabili sono surrogate astratte su una stessa unità numerica; non sono misure di joule, euro o costrutti psicologici. Le sei etichette condividono lo stesso schema e differiscono soltanto per il seme: questo evita di inventare evidenza disciplinare.

I generatori sono:

1. Compatibile: H = E − h + ε.
2. Violazione additiva: H = 0.8 + 0.55E − 0.3h + ε.
3. Violazione d’interazione: H = E − h + 0.65Eh + ε.
4. Violazione nonlineare: H = E − h + 0.7(E−3)² + 0.5(h−1)² + ε.

La teoria non stima parametri. Le baseline stimano rispettivamente intercetta e coefficienti liberi, un termine Eh aggiuntivo, e termini E² e h² aggiuntivi. Il polinomio quadratico è una sola famiglia nonlineare: un suo insuccesso non esclude altre funzioni.

Lo split casuale è 60% training, 20% validation, 20% test, senza sovrapposizioni. La baseline di riferimento è scelta mediante MSE validation, poi tutte le baseline prefissate sono ristimate su training più validation. Il test non determina la scelta. Non si applicano scaling o trasformazioni apprese sull’intero dataset.

Per ciascuna baseline si calcola Δ = MSE(teoria) − MSE(baseline). Un bootstrap paired delle righe di test, 1.000 repliche, mantiene gli stessi indici fra previsioni. Gli intervalli percentile usano alpha 0.05/3 per i tre confronti, con obiettivo nominale di copertura simultanea 95% entro ciascun caso. Non si assume copertura finita esatta e non si correggono globalmente i 24 casi. Mille repliche hanno risoluzione limitata nelle code: per analisi confermative si raccomandano più repliche e controlli di sensibilità.

Il criterio illustrativo di falsificazione predittiva è che almeno un limite inferiore superi 0.02 unità². Il margine deve essere scelto in funzione del dominio PRIMA di dati reali. Non è invariante al cambio di scala: moltiplicando tutte le misure per c, il margine MSE deve essere moltiplicato per c².

Un bootstrap separato delle righe di sviluppo stima intervalli per i coefficienti additivi e confronta i vincoli (0,1,−1), correggendo sui tre parametri. È diagnostico: un modello additivo mal specificato o errori di misura nei predittori possono alterare i coefficienti. Il bootstrap del test condiziona sui modelli già stimati e non misura l’intera variabilità della procedura di training.

## 5. Risultati osservati della simulazione

Configurazione: seme base 20261008, 800 righe per caso, 1.000 bootstrap, margine 0.02. Python 3.12 e NumPy 2.2.6, ambiente Linux. Le cifre seguenti provengono dall’esecuzione salvata, non da una previsione dei risultati.

| Area | Generatore | RMSE teoria | Baseline scelta su validation | RMSE baseline | CI Δ MSE baseline scelta | Esito operativo |
|---|---|---:|---|---:|---|---|
| energia | compatible | 0.287 | additive | 0.288 | [-0.002, 0.001] | not_falsified_not_validated |
| energia | additive_violation | 0.758 | interaction | 0.300 | [0.352, 0.616] | falsified_operationally |
| energia | interaction_violation | 2.392 | nonlinear | 0.292 | [4.310, 6.875] | falsified_operationally |
| energia | nonlinear_violation | 1.475 | nonlinear | 0.295 | [1.601, 2.651] | falsified_operationally |
| ingegneria | compatible | 0.287 | interaction | 0.287 | [-0.001, 0.000] | not_falsified_not_validated |
| ingegneria | additive_violation | 0.746 | additive | 0.305 | [0.348, 0.585] | falsified_operationally |
| ingegneria | interaction_violation | 2.507 | interaction | 0.285 | [4.926, 7.833] | falsified_operationally |
| ingegneria | nonlinear_violation | 1.321 | nonlinear | 0.299 | [1.268, 2.069] | falsified_operationally |
| fisica | compatible | 0.300 | nonlinear | 0.301 | [-0.005, 0.003] | not_falsified_not_validated |
| fisica | additive_violation | 0.757 | additive | 0.304 | [0.359, 0.607] | falsified_operationally |
| fisica | interaction_violation | 2.406 | interaction | 0.314 | [4.427, 7.321] | falsified_operationally |
| fisica | nonlinear_violation | 1.380 | nonlinear | 0.306 | [1.382, 2.293] | falsified_operationally |
| matematica | compatible | 0.287 | interaction | 0.286 | [-0.002, 0.003] | not_falsified_not_validated |
| matematica | additive_violation | 0.719 | interaction | 0.321 | [0.292, 0.523] | falsified_operationally |
| matematica | interaction_violation | 2.511 | interaction | 0.314 | [4.643, 7.786] | falsified_operationally |
| matematica | nonlinear_violation | 1.404 | nonlinear | 0.314 | [1.457, 2.293] | falsified_operationally |
| economia | compatible | 0.288 | nonlinear | 0.287 | [-0.003, 0.004] | not_falsified_not_validated |
| economia | additive_violation | 0.721 | interaction | 0.321 | [0.306, 0.543] | falsified_operationally |
| economia | interaction_violation | 2.460 | interaction | 0.295 | [4.565, 7.733] | falsified_operationally |
| economia | nonlinear_violation | 1.432 | nonlinear | 0.289 | [1.458, 2.467] | falsified_operationally |
| psicologia | compatible | 0.294 | interaction | 0.299 | [-0.006, 0.000] | not_falsified_not_validated |
| psicologia | additive_violation | 0.651 | nonlinear | 0.278 | [0.237, 0.459] | falsified_operationally |
| psicologia | interaction_violation | 2.663 | interaction | 0.342 | [5.335, 8.572] | falsified_operationally |
| psicologia | nonlinear_violation | 1.454 | nonlinear | 0.304 | [1.555, 2.496] | falsified_operationally |

Gli esiti operativi considerano tutti i tre confronti prefissati; la tabella mostra l’intervallo della sola baseline scelta in validation. Gli intervalli completi, i coefficienti e le metriche sono nel file results/results.json.

- compatible: 0/6 casi con falsificazione predittiva.
- additive_violation: 6/6 casi con falsificazione predittiva.
- interaction_violation: 6/6 casi con falsificazione predittiva.
- nonlinear_violation: 6/6 casi con falsificazione predittiva.

Queste frequenze non stimano potenza o errore di primo tipo: sei etichette e sei semi non costituiscono uno studio Monte Carlo adeguato. Il successo nel generatore compatibile verifica il controllo positivo. Il rigetto negli altri generatori verifica la sensibilità a violazioni costruite, non la falsità della formula in una disciplina reale.

## 6. Test empirico esplorativo di un'estensione psicologica

È stato usato il campione formale del dataset pubblico *De-identified survey data for job demands, job resources, and burnout among metro site management personnel in China*, disponibile su Zenodo, record 21153011. Il file contiene 274 rispondenti e scale composite per risorse lavorative, richieste lavorative e burnout. L’archivio viene scaricato dalla fonte e accettato soltanto se corrisponde allo SHA-256 registrato; le risposte individuali non sono redistribuite nel repository.

La specifica è stata fissata nel codice prima di eseguire il test: `E=z(risorse)`, `h=z(richieste)` e `Y=-z(burnout)`. La relazione centrale definisce `H:=E-h`; l'ipotesi empirica aggiuntiva è `Y=H`. Medie e deviazioni standard sono stimate esclusivamente sulle 164 righe di training, poi applicate alle 55 righe di validation e alle 55 righe di test. Il margine operativo è 0,05 unità standardizzate²; il bootstrap paired usa 10.000 repliche e la stessa correzione sui tre confronti adottata nell’esperimento sintetico.

La baseline con interazione è stata selezionata sulla validation. Sul test, l'estensione ha RMSE 1,4598, MAE 1,1234 e R² −1,6941; la baseline selezionata ha RMSE 0,6682, MAE 0,4616 e R² 0,4356. La differenza MSE è 1,6847 e il suo intervallo simultaneo 95% è [0,8945; 2,7730], interamente sopra il margine. Anche le baseline additiva e quadratica superano la previsione con intervalli interamente positivi. L'estensione `Y=H` è quindi **falsificata operativamente in questo campione**. L'identità `H:=E-h` resta vera per definizione.

Nel modello additivo libero, i coefficienti stimati sono intercetta 0,0019, risorse 0,4283 e richieste −0,3380. Gli intervalli simultanei dei due coefficienti escludono rispettivamente 1 e −1. Il segno è coerente con l’idea qualitativa che maggiori risorse e minori richieste si associno a minore burnout; i pesi unitari imposti dalla formula non sono sostenuti da questo test.

Questa non è una prova confermativa: l’operazionalizzazione è stata formulata dopo che il dataset era già stato raccolto, le scale originali hanno intervalli diversi e la standardizzazione non crea automaticamente una comune unità sostantiva. Il disegno è trasversale e non identifica causalità.

Il foglio pilot contiene 140 partecipanti distinti e gli item iniziali delle stesse famiglie di scale. I compositi sono stati ricostruiti come media delle sottoscale. Sul test pilot, la previsione ha RMSE 1,3555. La baseline quadratica scelta sulla validation ha RMSE 1,2267, ma il CI della differenza MSE è [−0,8793; 1,4235] e non consente una conclusione. Le baseline additiva e con interazione, entrambe prefissate, hanno invece limiti inferiori 0,1430 e 0,1484, superiori al margine 0,05. È una replica interna parziale: i partecipanti sono diversi, ma provengono dallo stesso programma di studio e il pilot servì alla selezione degli item.

| Area | Stato empirico nel progetto | Motivo |
|---|---|---|
| Psicologia | Estensione predittiva falsificata nel campione formale; replica interna parziale | Dati reali pubblici, tre scale separate; specifica post-raccolta e trasversale. |
| Energia | Non ancora testata | Manca una specifica preregistrata con input, perdita e output misurati separatamente nella stessa unità. |
| Ingegneria | Non ancora testata | Serve un processo e un protocollo di misura indipendente; un conteggio residuo sarebbe tautologico. |
| Fisica | Non ancora testata | Occorre fissare sistema, confini, regime e canali energetici; h non può essere la costante di Planck in questa sottrazione. |
| Economia | Audit contabile reale completato, non indipendente | 158 serie World Bank 2022; il risparmio include trasferimenti netti, termine omesso dalla formula ridotta. |
| Matematica | Non applicabile come validazione empirica | Una relazione universale richiede ipotesi e dimostrazione oppure viene confutata da un controesempio. |

### 6.1 Audit economico reale

Per il 2022 sono state unite tre serie World Development Indicators in dollari correnti: GNI come `E`, consumo finale come `h` e risparmio lordo come `H`. Le 158 serie complete mostrano una mediana di `|H-(E-h)|/|E|` pari al 3,5473% e un 90° percentile del 18,3638%; il 60,13% è entro il 5% del GNI. La definizione World Bank del risparmio include però i trasferimenti netti, e le tre serie appartengono allo stesso sistema di contabilità nazionale. Il risultato documenta un termine omesso e la coerenza interna dei dati; non è una conferma indipendente né un test causale della teoria percettiva.

## 7. Riproducibilità e controlli software

Il progetto comprende script CLI, dipendenze bloccate, CSV sintetici, indici delle partizioni, previsioni sul test, hash SHA-256 e report. Tredici test automatici locali sono passati: determinismo, split completo e disgiunto, controlli positivi/negativi, previsioni senza uso dell’esito di test, rifiuto di input invalidi, generazione degli output, metadata esterni, controllo dell’archivio psicologico, standardizzazione limitata al training e join economico. La verifica Windows/PowerShell è demandata alla CI GitHub inclusa.

I test confermano proprietà software entro i casi coperti. Non certificano un modello scientifico né una copertura statistica esatta. Una replica deve mantenere configurazione e dati originali, riportare modifiche e conservare anche risultati sfavorevoli.

## 8. Protocollo per una verifica reale e indipendente

Prima della raccolta, scegliere UNA interpretazione settoriale, stabilire se l’uguaglianza è identità o previsione, documentare unità, confini del sistema e misure indipendenti. Fissare rumore, tolleranza, margine, disegno di campionamento, esclusioni, alternative e correzione per confronti multipli. La numerosità va motivata mediante analisi di precisione/potenza specifica, non prendendo 800 come numero scientificamente ottimale.

Preregistrare il protocollo con un riferimento versionato e un timestamp indipendente quando disponibile. Lasciare una porzione di dati fuori dalla stima e dalla scelta del modello, idealmente raccolta da un gruppo indipendente. Documentare provenienza, consenso o autorizzazioni pertinenti e licenza dei dati. Non pubblicare dati personali senza una base adeguata.

Per dati iid il comando CSV del progetto è un punto di partenza. Per serie temporali, panel o misure ripetute è necessario adattare split e bootstrap a blocchi/cluster; il programma attuale rifiuta metadata che dichiarano un altro campionamento. Predisporre analisi degli errori di misura, stabilità fra campioni e controllo delle variabili omesse. La relazione osservazionale non identifica un effetto causale.

Separare l’analisi esplorativa dalla conferma indipendente. Se si cambiano definizioni per rispondere a un fallimento, si sta proponendo una nuova ipotesi: va preregistrata e verificata su nuovi dati. In matematica sostituire il protocollo statistico con enunciato, ipotesi, dimostrazione e verifica di eventuali controesempi.

## 9. Discussione e conclusione

La plasticità di H = E − h è sostenibile come schema descrittivo quando sottrazione, unità e confini sono definiti. Il costo della flessibilità è una riduzione del contenuto empirico se ogni residuo può essere rinominato h. Una teoria controllabile deve vietare questa ridefinizione retrospettiva e accettare esiti che la contraddicano.

Il contributo attuale è un banco di prova riproducibile, una mappa di ipotesi, un test esplorativo di un'estensione psicologica e un audit economico, non una legge universale. L'estensione psicologica a pesi unitari è respinta nel campione formale e riceve evidenza mista ma sfavorevole nel pilot; l'audit economico rivela un termine noto omesso. Nessuna area è convalidata universalmente. L’avanzamento successivo richiede una replica psicologica preregistrata e misure reali indipendenti negli altri settori; in matematica la formula è un'identità sotto la definizione data e non una legge empirica.

## Riferimenti metodologici

1. Scikit-learn, *Common pitfalls and recommended practices*: https://scikit-learn.org/1.7/common_pitfalls.html — separazione fra dati di sviluppo e test e prevenzione del leakage.
2. C. R. Shalizi, Carnegie Mellon University, *Simulation for Inference I — The Bootstrap*: https://stat.cmu.edu/~cshalizi/dst/18/lectures/18/lecture-18.html — principio e interpretazione del ricampionamento.
3. Zhao, C., Qi, J. e Chen, Y., *De-identified survey data for job demands, job resources, and burnout among metro site management personnel in China*, Zenodo record 21153011: https://zenodo.org/records/21153011 — dati empirici della verifica psicologica esplorativa.

I riferimenti supportano la metodologia generale, non la formula né le sue interpretazioni settoriali.
