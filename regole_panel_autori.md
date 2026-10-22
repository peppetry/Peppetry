# Cosa tagliano e cosa verificano gli autori per costruire il panel dei bilanci

Fonte: Kalemli-Özcan, Sørensen, Villegas-Sanchez, Volosovych, Yeşiltaş, *How to Construct Nationally Representative Firm-Level Data from the Orbis Global Database*. Letti per intero:

- l'articolo pubblicato su AEJ: Macroeconomics nel 2024;
- la revisione NBER del gennaio 2022, con l'appendice online;
- l'appendice 2024;
- la guida "Processing Orbis Historical Disk" del 2017.

Le pagine indicate come "appendice" sono quelle dell'appendice NBER 2022.

Per ogni regola, la nota **"Nel tuo disco"** dice come si applica a una consegna Orbis Historical del 2025, che è già un unico file con tutta la storia. Gli autori invece univano più dischi annuali.

**Controllo di completezza.** La lista è stata ricontrollata cercando nei testi integrali ogni punto in cui gli autori tolgono, tengono, sostituiscono o verificano qualcosa. Le regole trovate in questo secondo passaggio sono nella Fase 4.

Restano fuori, di proposito:

- le regole sui dati di proprietà, appendice B, perché non riguardano i bilanci;
- i consigli su come scaricare dal software BvD, perché non servono con una consegna bulk. Sono riassunti al punto 55.

---

## Fase 1. Lettura del file e prima pulizia di ogni riga

Appendice A.5.1, pagine 14-17.

1. **Righe con solo il nome dell'impresa.** Togliere.
   - **Nel tuo disco:** sono righe senza nessun numero di bilancio.
2. **Righe senza BvD ID** o senza numero di conto BvD. Togliere.
3. **Righe senza nessun dato finanziario.** Togliere.
   - Gli autori hanno verificato che di solito sono righe vuote senza data di chiusura.
4. **Paese incoerente.** Togliere le righe in cui il paese ricavato dalle prime due lettere del BvD ID è diverso dal codice ISO del paese indicato da Moody's.
   - Gli autori lo trattano come un errore o una possibile società di comodo a fini fiscali.
   - **Nel tuo disco:** confronta le due lettere con `Country ISO code` del file `All_addresses`.
5. **Valuta mancante.** Togliere.
   - **Nel tuo disco:** colonna `Original currency`.
6. **Data di chiusura mancante.** Togliere.
7. **Anno.** Si ricava dalla `Closing date`:
   - chiusura dal 1° giugno in poi: anno della data;
   - chiusura prima del 1° giugno: anno della data meno uno.

   Esempi degli autori: 4 agosto 2003 vale per il 2003, 25 maggio 2003 vale per il 2002.
8. **Due bilanci della stessa impresa nello stesso anno.** Succede con bilanci trimestrali accanto a quello annuale, o quando l'impresa cambia mese di chiusura. Si risolve in due passi:
   1. tenere il bilancio con la data di chiusura più vicina alla fine dell'anno;
   2. se restano doppioni, togliere quelli con fatturato più basso del massimo di quell'impresa in quell'anno, perché un bilancio trimestrale ha fatturato molto più basso.

   Nel disco 2005 erano circa 34 mila su 18 milioni di righe.
   - **Nel tuo disco:** tenere solo `Number of months` uguale a 12 risolve quasi tutto.
9. **Unità di misura sbagliate.** Gli autori tolgono l'intera impresa se, nell'anno in cui cambia l'unità dichiarata (euro, migliaia, milioni), il totale attivo cresce più del 19.800% o scende più del 99%: è il segno di un errore di unità. Hanno perso così il 3% delle righe nei dischi del 2005 e del 2009.
   - **Nel tuo disco:** i file EUR sono già in euro pieni, verificato su Walmart. Resta utile un controllo simile: segnalare le imprese il cui totale attivo si moltiplica o si divide per circa mille da un anno all'altro.
10. **Codici di settore.** Convertire i vecchi codici NACE Rev. 1.1 in Rev. 2, tenendo il primo codice della tabella di corrispondenza Eurostat.
    - **Nel tuo disco:** non serve. Il file `Industry_classifications` ha già il NACE Rev. 2, ma è quello attuale, applicato a tutti gli anni.

---

## Fase 2. Pulizia del panel

Appendice A.5.3, pagine 20-22.

11. **Valute strane.** Tenere i bilanci nelle valute principali (euro, dollaro, sterlina) e togliere quelli in valute senza senso per il paese, ad esempio rand sudafricano o dollaro canadese per un'impresa europea.
    - **Nel tuo disco:** controllare la distribuzione di `Original currency` per paese.
12. **Conversione in dollari reali del 2005.** Tre passaggi:
    1. portare tutto nella valuta ufficiale del paese, gestendo le vecchie valute prima dell'euro;
    2. deflazionare con il deflatore del PIL della Banca Mondiale, base 2005;
    3. dividere per il cambio col dollaro del 2005.

    Gli autori non usano il cambio fornito da Moody's.
    - **Nel tuo disco:** per i rapporti di copertura non serve, basta che dati Orbis e Eurostat siano nella stessa valuta e nello stesso anno. Serve se si confrontano livelli tra anni o tra paesi.
13. **Impresa-anno vuota.** Togliere le righe in cui mancano tutti e quattro: totale attivo, fatturato, vendite e dipendenti.
14. **Totale attivo negativo** in qualsiasi anno. Togliere l'impresa intera.
15. **Dipendenti negativi, o più di 2 milioni**, in qualsiasi anno. Togliere l'impresa intera.
    - La soglia era pensata come "più di Walmart".
    - **Nel tuo disco:** Walmart oggi dichiara tra 2,1 e 2,3 milioni di dipendenti e verrebbe tolta. Per l'intera economia conviene alzare la soglia, ad esempio a 3 milioni.
16. **Vendite negative** in qualsiasi anno. Togliere l'impresa intera.
    - Il filtro non si applica al fatturato operativo, che può essere negativo per perdite finanziarie.
    - Per la Danimarca non si può applicare, perché le imprese danesi non riportano le vendite.
17. **Troppi dipendenti per milione di attivo**, sopra il 99,9° percentile, in qualsiasi anno. Togliere l'impresa intera.
18. **Troppi dipendenti per milione di vendite**, sopra il 99,9° percentile, in qualsiasi anno. Togliere l'impresa intera.
19. **Vendite su attivo troppo alte**, sopra il 99,9° percentile, in qualsiasi anno. Togliere l'impresa intera.
    - Gli autori non dicono se il percentile è calcolato per paese o su tutto il campione. Per paese è la scelta più prudente.
20. **Immobilizzazioni materiali negative** in qualsiasi anno. Togliere l'impresa intera.
21. **Dati anagrafici mancanti in alcuni anni.** Riempire paese, nome, città, regione, codice postale, forma giuridica e data di costituzione con i valori degli altri anni della stessa impresa.
    - **Nel tuo disco:** l'anagrafica è già una sola, quella di dicembre 2025, per tutti gli anni.

---

## Fase 3. Doppioni, consolidamento, scelta del campione e verifiche

Appendice C.2, D.2, D.4 e articolo pubblicato, appendici A e B.

### Doppioni e tipo di bilancio

22. **I tipi di bilancio.**

    | Codice | Che cos'è |
    |---|---|
    | C1 | consolidato di un gruppo senza bilancio della singola capogruppo |
    | C2 | consolidato di un gruppo che ha anche il bilancio della singola capogruppo |
    | U1 | singola impresa senza consolidato |
    | U2 | singola impresa che ha anche un consolidato |
    | LF | dati limitati |

23. **C2 si toglie sempre**, per non contare due volte il gruppo e la sua capogruppo.
24. **C1 si toglie tranne in alcuni paesi**:
    - nel campione completo, tranne Spagna e Italia;
    - nel campione per la produttività, tranne Spagna, Italia, Cipro, Danimarca, Regno Unito, Grecia, Irlanda e Lituania.

    Sono i paesi dove molti gruppi depositano solo il consolidato.
25. **Stessa impresa, stesso anno, bilanci con valori diversi.** Qui i testi si contraddicono:
    - l'appendice dà la preferenza al non consolidato, e dice che in tutte le applicazioni usano i non consolidati;
    - l'articolo pubblicato, per lo studio sulla concentrazione, dà la preferenza al consolidato.

    Per il confronto con Eurostat vale l'appendice.
26. **Stessa impresa, stesso anno, bilanci con valori uguali.** Anche qui ci sono due versioni.
    - **Appendice D.4:** tenere il tipo di bilancio che ha la serie storica più lunga. A parità di lunghezza, tenere il non consolidato.
    - **Articolo pubblicato, appendice A:**
      - se l'impresa presenta sempre il non consolidato, tenere il non consolidato;
      - se presenta sempre il consolidato, tenere il consolidato;
      - se alterna i due senza regolarità, tenere il consolidato e trattare tutta la serie come consolidata.
27. **Imprese che passano avanti e indietro tra consolidato e non consolidato.** Nell'articolo pubblicato le tolgono, per avere serie storiche coerenti. Il motivo indicato è il cambio di norme contabili tra il 2005 e il 2007, quando molte imprese sono passate al consolidato secondo i principi internazionali: tenerle creerebbe salti artificiali nelle vendite.
28. **Quanti doppioni aspettarsi.** Gli autori ne trovano 607.839, lo 0,24% delle righe:
    - nel 62,5% dei casi la coppia è un LF con un U;
    - in circa un terzo dei casi è un C1 con un U1.
29. **Unione dei dischi.** Gli autori uniscono i dischi di anni diversi:
    - a parità di impresa e anno vince il disco più recente;
    - un valore presente non viene mai sostituito con un valore mancante.
    - **Nel tuo disco:** non serve, è già un unico file.
30. **Cambi del BvD ID.** Prima di unire i dati, sostituire i vecchi codici con quelli nuovi usando la tabella di corrispondenza di Moody's, conservando il vecchio codice. Il codice cambia per trasferimenti di sede, cambi di forma giuridica e fusioni.
    - **Nel tuo disco:** chiedere a Moody's se la tabella di corrispondenza è inclusa nella consegna.

### Quali imprese entrano

31. **Solo imprese industriali e commerciali.** Banche e assicurazioni hanno schemi di bilancio diversi e file separati.
    - **Nel tuo disco:** usare `Industry-Global_financials_and_ratios`, non i file `Banks` o `Insurance`.
32. **Campione completo.** Fatturato operativo positivo, e dipendenti oppure costo del personale positivi.
33. **Campione per la produttività.** In più, immobilizzazioni materiali e costi dei materiali positivi.
    - È il campione per stimare la produttività totale dei fattori.
    - In Danimarca e nel Regno Unito è molto più piccolo, perché le imprese non riportano i costi dei materiali.

### Verifiche sui dati

34. **Copertura della produzione.** Somma del fatturato operativo Orbis diviso il fatturato Eurostat, per paese e anno.
    - Per la manifattura si confronta la sola sezione C.
    - Per l'intera economia si sommano solo le sezioni presenti in entrambe le fonti in quell'anno.
35. **Copertura dell'occupazione.** Somma dei dipendenti Orbis diviso gli addetti ufficiali, esclusi i lavoratori autonomi, che Orbis non contiene.
36. **Distribuzione per dimensione.** Nel 2006, quota di fatturato e di occupazione delle imprese con 1-19, 20-249 e 250 o più addetti, confrontata con Eurostat.
    - Per l'Italia gli autori segnalano poche piccole imprese: il 13% dell'occupazione manifatturiera nella classe 1-19, contro il 40% di Eurostat.
37. **Numero di imprese.** Imprese Orbis attive diviso imprese attive Eurostat, togliendo le imprese con status inattivo, sciolto, in liquidazione o in fallimento.
    - Per l'Italia nel 2008 il rapporto è 60,5%.
    - **Nel tuo disco:** lo status è quello di oggi. Per gli anni passati considera attiva un'impresa che ha depositato un bilancio in quell'anno.
38. **Celle con copertura sopra il 100%.** In quelle combinazioni di paese, settore e anno si correggono i valori estremi, dallo 0,01% allo 0,5% delle osservazioni. Riguarda meno dell'1% delle celle, salvo il settore minerario.
39. **Quali paesi tenere.** Nell'articolo pubblicato, un paese entra se le imprese Orbis coprono almeno il 50% della produzione ufficiale in tutti gli anni dal 2001 al 2012.
40. **Quali anni tenere.** I dati prima del 1999 sono poveri, perché solo dal 1999 le norme europee obbligano tutte le società a depositare i bilanci. La copertura migliora fino al 2005 e poi è stabile.
41. **Valori di riferimento per la manifattura**, copertura della produzione, media 2001-2012 nell'articolo pubblicato:

    | Paese | Media | Andamento |
    |---|---|---|
    | Italia | 79% | dal 65% nel 2001 all'86% nel 2012 |
    | Germania | 63% | |
    | Francia | 87% | |
    | Spagna | 82% | |

    I tuoi numeri non devono coincidere al decimale, perché gli autori non usavano Orbis Historical. Devono avere lo stesso ordine di grandezza e lo stesso andamento.

---

## Fase 4. Regole trovate nel secondo controllo

Nella prima versione della lista non c'erano. Sono in ordine di importanza per il tuo lavoro.

### Tipo di bilancio e doppioni

42. **Cosa sono davvero i bilanci LF.** Sono bilanci con dati limitati: tutte le variabili sono vuote tranne vendite e totale attivo (articolo pubblicato, appendice A). Gli autori non li buttano a priori: ricavano se sono consolidati o no dall'ultima lettera del numero di conto BvD.
    - Nei loro dati, il 62,5% dei doppioni è proprio una coppia LF più un bilancio U.
    - **Nel tuo disco:** per i conti di copertura scartarli va bene, perché non hanno né fatturato operativo né dipendenti.
43. **Codice di consolidamento mancante.** Si ricava dall'ultima lettera del numero di conto BvD: C per consolidato, U per non consolidato. Se manca il numero di conto, lo si costruisce unendo il BvD ID e la prima lettera del codice di consolidamento (appendice A.5.1, passo 5).
44. **Doppioni con codici di settore diversi.** Alcuni doppioni impresa-anno hanno gli stessi dati di bilancio ma codici di settore diversi. In Orbis la prima riga è il settore principale: gli autori tengono quella (appendice, nota 13).
45. **Doppioni che non si sanno risolvere.** Dopo le regole del punto 8 restano pochi casi in cui non si capisce se il bilancio è annuale o mensile. Gli autori li tolgono.
46. **Lo stesso bilancio depositato due volte.** Alcune imprese depositano lo stesso bilancio sia come "Annual report" sia come "Local registry filing". Le stesse voci possono avere valori diversi, perché le regole di deposito sono diverse. Il bilancio annuale ha in più il dettaglio delle voci (guida 2017, pagina 10).
    - Gli autori non danno una regola di scelta.
    - **Nel tuo disco:** preferire "Annual report" è una scelta nostra coerente con questo.

### Unità e identificativi

47. **Eccezione al controllo delle unità.** Nel controllo del punto 9 si possono tenere le imprese che Moody's indica come inattive: il loro attivo può davvero scendere quasi a zero da un anno all'altro, senza che sia un errore di unità (appendice A.5.2).
48. **Paese reale dell'impresa.** Le prime due lettere del BvD ID non sono sempre il paese dell'impresa. La guida corregge con una tabella di discrepanze prima di dividere i dati per paese (guida 2017, pagina 10).
    - **Nel tuo disco:** usare `Country ISO code` di `Contact_info` o `All_addresses`.
49. **Ex Jugoslavia.** I codici delle imprese passano da YU a CS e poi a RS o ME: gli autori li riassegnano a Serbia o Montenegro usando la parte numerica del codice. Non riguarda i paesi che ti interessano.
50. **Valute dei nuovi paesi dell'euro.** Slovenia, Estonia, Slovacchia e Malta:
    - prima dell'adozione dell'euro i dati vanno riportati nella vecchia valuta nazionale, perché il deflatore della Banca Mondiale è in quella valuta;
    - i tassi di cambio vengono da Compustat Global, integrati con quelli delle banche centrali.

    Non riguarda Italia, Germania, Francia, Spagna e Portogallo.

### File anagrafici

51. **File con più righe per impresa.** Sono `All addresses`, `Industry classifications` e `Identifiers`.
    - **Indirizzi:** tenere l'indirizzo di costituzione. Se manca, togliere gli indirizzi precedenti. Tra quelli rimasti, tenere l'indirizzo dell'ufficio.
    - **Settore:** tenere solo il codice "core", cioè 4 cifre per NACE e NAICS.
    - **Identificativi:** sistemare caso per caso, perché ogni paese ha identificativi principali diversi.

    Se non si fa, il collegamento con i bilanci moltiplica le righe (guida 2017, pagine 2-3).
52. **Valori speciali nei codici di settore.** Nei codici americani SIC, "NULL", "NUL" e "JHB" vanno trattati come valori mancanti (guida 2017, pagina 6).
53. **Due copie degli stessi file di bilancio.** Nella consegna descritta dalla guida, i file `Industry - Global financials and ratios` compaiono in due cartelle. Quella con "Histo" nel nome ha più anni di bilancio; l'altra ha solo gli anni recenti.
    - **Nel tuo disco:** verificare da quale cartella vengono i file usati.
    - Nella stessa consegna, `Key financials` mette insieme imprese industriali, banche e assicurazioni, con poche variabili.

### Confronti e download

54. **Come gli autori hanno costruito la Table A.2.2**, quella che hai replicato all'inizio (appendice 2024, pagina 11):
    - imprese con totale attivo compilato in quell'anno;
    - tolti i doppioni dovuti a più bilanci nello stesso anno, ad esempio primo trimestre e fine anno;
    - tenuti due bilanci nello stesso anno per le imprese che hanno sia il consolidato sia il non consolidato.
55. **Consigli di download**, che non servono con una consegna bulk ma spiegano le differenze con i dati degli autori:
    - scaricare per "anni relativi", cioè gli ultimi 5 anni disponibili per ogni impresa, invece che per anni di calendario;
    - ricostruire l'anno dalla data di chiusura, perché BvD non tiene conto dei buchi nella serie;
    - forzare un'unità fissa, ad esempio migliaia, invece di quella originale;
    - non usare la variabile "Exchange rate" di BvD, che cambia significato tra prodotti;
    - scegliere solo imprese industriali, nel formato globale.
56. **Regole valide solo per lo studio sulla concentrazione.** Gli autori tolgono:
    - elettricità, gas e acqua, NACE da 35 a 39;
    - finanza e assicurazioni, da 64 a 66;
    - attività immobiliari, 68;
    - pubblica amministrazione, 84;
    - organismi extraterritoriali, 99.

    Per i confronti di copertura non si applicano.
