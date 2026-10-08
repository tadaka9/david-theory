# Risultati H = E − h

DATI SINTETICI: verifica del metodo, nessuna validazione empirica reale.

| Settore | Scenario | RMSE teoria | RMSE baseline scelta | Esito operativo |
|---|---|---:|---:|---|
| energia | compatible | 0.2870 | 0.2885 | not_falsified_not_validated |
| energia | additive_violation | 0.7584 | 0.3000 | falsified_operationally |
| energia | interaction_violation | 2.3924 | 0.2919 | falsified_operationally |
| energia | nonlinear_violation | 1.4748 | 0.2955 | falsified_operationally |
| ingegneria | compatible | 0.2865 | 0.2868 | not_falsified_not_validated |
| ingegneria | additive_violation | 0.7456 | 0.3046 | falsified_operationally |
| ingegneria | interaction_violation | 2.5070 | 0.2848 | falsified_operationally |
| ingegneria | nonlinear_violation | 1.3209 | 0.2994 | falsified_operationally |
| fisica | compatible | 0.3000 | 0.3015 | not_falsified_not_validated |
| fisica | additive_violation | 0.7571 | 0.3039 | falsified_operationally |
| fisica | interaction_violation | 2.4061 | 0.3139 | falsified_operationally |
| fisica | nonlinear_violation | 1.3802 | 0.3059 | falsified_operationally |
| matematica | compatible | 0.2869 | 0.2860 | not_falsified_not_validated |
| matematica | additive_violation | 0.7195 | 0.3208 | falsified_operationally |
| matematica | interaction_violation | 2.5107 | 0.3140 | falsified_operationally |
| matematica | nonlinear_violation | 1.4039 | 0.3144 | falsified_operationally |
| economia | compatible | 0.2882 | 0.2872 | not_falsified_not_validated |
| economia | additive_violation | 0.7210 | 0.3205 | falsified_operationally |
| economia | interaction_violation | 2.4596 | 0.2953 | falsified_operationally |
| economia | nonlinear_violation | 1.4323 | 0.2893 | falsified_operationally |
| psicologia | compatible | 0.2943 | 0.2989 | not_falsified_not_validated |
| psicologia | additive_violation | 0.6509 | 0.2779 | falsified_operationally |
| psicologia | interaction_violation | 2.6626 | 0.3420 | falsified_operationally |
| psicologia | nonlinear_violation | 1.4541 | 0.3037 | falsified_operationally |

## Interpretazione

La mancata falsificazione non prova la formula. Ogni scenario compatibile è generato dalla formula stessa: il successo è un controllo positivo del software.
Delta MSE positivo favorisce la baseline. Falsificazione operativa: limite inferiore del CI maggiore del margine MSE prefissato. Il CI nominale simultaneo 95% usa Bonferroni sui tre confronti all’interno di ogni caso; non corregge globalmente i 24 casi.
Bootstrap percentile iid del test: incertezza condizionata ai modelli stimati, non include la variabilità di training. Bootstrap delle righe di sviluppo: CI dei coefficienti additivi, diagnostico e non prova di equivalenza.
Restrizioni additive: intercetta 0, coefficiente E 1, coefficiente h −1. Se il modello additivo è mal specificato, il loro rigetto non costituisce da solo una falsificazione strutturale.
Modello nonlineare: polinomio quadratico, non rappresenta tutte le alternative nonlineari. Nessuna inferenza causale. Un solo split non dimostra robustezza rispetto al campionamento.
Le sei etichette settoriali usano lo stesso banco di prova astratto con semi diversi: non sono sei esperimenti disciplinari reali. In matematica i risultati numerici non sostituiscono una dimostrazione.
Dettagli, intervalli e configurazione: results.json. Indici dello split e previsioni: case_*/audit.json.
