# Confronto Orbis contro statistiche ufficiali: manifattura

Due tabelle, costruite come Kalemli-Özcan et al. (2024), appendice sezioni C.2 e D.2:

- **Tabella 1, produzione**: quanta parte del fatturato manifatturiero del paese è coperta dalle imprese in Orbis.
- **Tabella 2, occupazione**: quanta parte degli addetti manifatturieri del paese è coperta dalle imprese in Orbis.

Paesi: Italia, Germania, Francia, Spagna, Portogallo, Stati Uniti. Anni: 1999-2024.

Il lavoro si divide così:

- **Dai dati Orbis** si producono solo **due somme per paese e anno**: il fatturato totale e i dipendenti totali delle imprese selezionate.
- **I totali ufficiali** (Eurostat per l'Europa, Census per gli Stati Uniti) e la divisione finale li aggiungo io.

Il risultato finale è una tabella con un paese per colonna, un anno per riga e dentro la percentuale coperta.

---

## Prima di tutto: due controlli sul file

**Controllo 1, le unità degli importi.** Non esiste una dichiarazione ufficiale che dica se i file `-EUR` sono in euro o in migliaia di euro. Tre verifiche indipendenti indicano euro pieni, ma va controllato. Il modo più semplice: prendi il fatturato più alto tra le imprese italiane nel 2019. Deve essere dell'ordine delle decine di miliardi di euro.

- Se il numero ha **11 cifre** o giù di lì, gli importi sono in **euro**.
- Se ha **8 cifre** o giù di lì, sono in **migliaia di euro**.

Scrivi il risultato nel CSV finale o nella mail: senza questo dato la percentuale può sbagliare di mille volte.

**Controllo 2, il formato della data.** Guarda alcune righe della colonna `Closing date`. Di solito è scritta come `20061231`, cioè anno, mese, giorno attaccati. Se è scritta in un altro modo, ad esempio `2006/12/31`, va adattato il passo che ricava l'anno.

---

## Tabella 1: produzione

**Obiettivo.** Per ogni paese e anno, la somma dell'`Operating revenue (Turnover)` delle imprese manifatturiere in Orbis, e quante imprese sono state sommate.

**Formula finale**, che calcolo io:

```
copertura produzione (%) = somma Operating revenue Orbis / fatturato manifattura ufficiale × 100
```

### Passo 1. Leggi il file dei bilanci

- **Cosa fare:** apri `Industry-Global_financials_and_ratios-EUR.txt`. È separato da tabulazioni e molto grande: va letto a pezzi o con DuckDB, non aperto tutto in memoria.
- **Perché:** è il file con i bilanci, già convertiti in euro.
- **Da sapere:** ogni riga è **un bilancio depositato**, non un'impresa. La stessa impresa può comparire più volte nello stesso anno. I passi seguenti servono anche a sistemare questo.

### Passo 2. Tieni solo i sei paesi

- **Cosa fare:** tieni le righe in cui le prime due lettere di `BvD ID number` sono `IT`, `DE`, `FR`, `ES`, `PT` o `US`.
- **Perché:** il BvD ID inizia con il codice del paese.
- **Da sapere:** in pochi casi le due lettere non corrispondono al paese reale dell'impresa. Se nel file `Contact_info` c'è una colonna con il codice ISO del paese, è più precisa. Per un primo giro le due lettere vanno bene.

### Passo 3. Tieni solo i bilanci di 12 mesi

- **Cosa fare:** tieni le righe con `Number of months` uguale a 12.
- **Perché:** un bilancio di 6 mesi ha circa metà del fatturato di un anno, uno di 18 mesi una volta e mezza. Sommati agli altri falsano il totale. Capitano nel primo anno di vita di un'impresa o quando cambia la data di chiusura.

### Passo 4. Assegna l'anno

- **Cosa fare:** guarda il mese della `Closing date`.
  - Se il bilancio chiude **da giugno a dicembre**, l'anno è quello della data.
  - Se chiude **da gennaio a maggio**, l'anno è quello della data **meno uno**.

| Closing date | Anno da assegnare |
|---|---|
| 31/12/2006 | 2006 |
| 30/09/2006 | 2006 |
| 30/06/2006 | 2006 |
| 31/05/2007 | 2006 |
| 31/03/2007 | 2006 |

- **Perché:** le statistiche ufficiali sono per anno solare. Un esercizio da aprile 2006 a marzo 2007 cade per nove mesi su dodici nel 2006. Per i nostri paesi cambia poco, perché quasi tutte le imprese chiudono il 31 dicembre, ma è la regola degli autori.

### Passo 5. Scegli il tipo di bilancio

La colonna `Consolidation code` dice che tipo di bilancio è:

| Codice | Che cos'è | Cosa fare |
|---|---|---|
| U1 | bilancio della singola impresa, che non ha un consolidato | **tenere** |
| U2 | bilancio della singola impresa, che ha anche un consolidato | **tenere** |
| C1 | bilancio consolidato di un gruppo che non deposita quello della singola capogruppo | **tenere solo per Italia e Spagna** |
| C2 | bilancio consolidato di un gruppo che deposita anche quello della capogruppo | **scartare sempre** |
| LF | scheda con dati minimi o stimati | **scartare sempre** |

- **Perché:** il bilancio consolidato somma il fatturato della capogruppo e di tutte le controllate, anche quelle all'estero. Le statistiche ufficiali contano invece le singole imprese residenti nel paese. Sommare un consolidato vuol dire contare due volte le controllate italiane, che hanno già il loro bilancio in Orbis, e aggiungere fatturato prodotto all'estero.
- **Perché l'eccezione per Italia e Spagna:** lì molti gruppi depositano solo il consolidato. Toglierlo farebbe sparire grandi imprese. Gli autori accettano un po' di doppio conteggio pur di non perderle.

### Passo 6. Un solo bilancio per impresa e anno

- **Cosa fare:** se dopo i passi precedenti la stessa impresa ha ancora più righe nello stesso anno, tienine una sola, scegliendo in quest'ordine:
  1. il bilancio non consolidato (U) rispetto al consolidato (C);
  2. il `Filing type` "Annual report" rispetto a "Local registry filing";
  3. la `Closing date` più recente.
- **Perché:** altrimenti la stessa impresa viene sommata due volte. La regola 1 è degli autori. Le regole 2 e 3 sono nostre: gli autori lavoravano su dischi vecchi dove questo caso non era descritto.

### Passo 7. Togli le imprese con dati impossibili

- **Cosa fare:** togli **l'impresa intera, in tutti i suoi anni**, se in almeno un anno ha:
  - `Total assets` negativo;
  - `Number of employees` negativo o maggiore di 2 milioni;
  - `Sales` negativo;
  - `Tangible fixed assets` negativo.
- **Perché:** sono errori nei dati. Gli autori trattano l'impresa intera come inaffidabile.
- **Passo aggiuntivo degli autori:** togliere anche le imprese che in almeno un anno hanno un rapporto anomalo, cioè sopra il 99,9° percentile, di:
  - dipendenti per milione di attivo;
  - dipendenti per milione di vendite;
  - vendite su attivo.

  Calcola il percentile su tutte le osservazioni del paese. L'effetto sui totali è piccolo, ma serve per essere fedeli al metodo.

### Passo 8. Tieni solo la manifattura

- **Cosa fare:** dal file `Industry_classifications.txt`, collegando con il `BvD ID number`, prendi il codice **NACE Rev. 2 principale** dell'impresa, la colonna "core code". Tieni le imprese il cui codice inizia con un numero **da 10 a 33**.
- **Perché:** la manifattura è il settore che le statistiche ufficiali coprono in tutti gli anni e in tutti i paesi. Il confronto è pulito.
- **Da sapere:**
  - il codice NACE nel file è quello di oggi, applicato a tutti gli anni passati;
  - se il file ha più righe per la stessa impresa, usa solo il codice principale, altrimenti l'impresa viene contata più volte nel collegamento.

### Passo 9. Tieni gli anni 1999-2024

- **Cosa fare:** tieni solo gli anni assegnati al passo 4 compresi tra 1999 e 2024.
- **Perché:** questo passo viene dopo il passo 7, perché il controllo dei dati impossibili guarda tutti gli anni dell'impresa.

### Passo 10. Definisci il campione degli autori

- **Cosa fare:** tieni le righe con `Operating revenue (Turnover)` **maggiore di zero** e, in più, almeno uno tra `Number of employees` **maggiore di zero** e `Costs of employees` **maggiore di zero**.
- **Perché:** è il "campione totale" degli autori. Un'impresa senza fatturato non aggiunge nulla al numeratore. Chiedere dipendenti o costo del personale esclude le scatole vuote, cioè società senza attività reale.

### Passo 11. Somma

- **Cosa fare:** per ogni paese e anno calcola il **numero di imprese** e la **somma di `Operating revenue (Turnover)`**.

**Risultato da consegnare**, file `tabella_produzione.csv`:

| paese | anno | n_imprese | somma_operating_revenue |
|---|---|---|---|
| IT | 1999 | … | … |
| IT | 2000 | … | … |
| … | … | … | … |
| US | 2024 | … | … |

---

## Tabella 2: occupazione

**Obiettivo.** Per ogni paese e anno, la somma del `Number of employees` delle imprese manifatturiere in Orbis, e quante imprese sono state sommate.

**Formula finale**, che calcolo io:

```
copertura occupazione (%) = somma Number of employees Orbis / addetti manifattura ufficiali × 100
```

### Passi da 1 a 10

**Identici alla Tabella 1**, nello stesso ordine:

1. leggi il file dei bilanci;
2. tieni i sei paesi;
3. tieni solo i bilanci di 12 mesi;
4. assegna l'anno con la regola del 1° giugno;
5. tieni U1 e U2, C1 solo per Italia e Spagna, scarta C2 e LF;
6. un solo bilancio per impresa e anno;
7. togli le imprese con dati impossibili;
8. tieni solo la manifattura, NACE da 10 a 33;
9. tieni gli anni 1999-2024;
10. tieni le righe con fatturato maggiore di zero e con dipendenti o costo del personale maggiori di zero.

Si parte dallo **stesso campione** della produzione: è così che fanno gli autori.

### Passo 11. Tieni solo chi ha i dipendenti

- **Cosa fare:** dal campione del passo 10, tieni le righe con `Number of employees` **maggiore di zero**.
- **Perché:** un'impresa con il numero di dipendenti vuoto non aggiunge nulla alla somma. Nel campione del passo 10 può esserci un'impresa con il solo costo del personale: per la produzione conta, per l'occupazione no.

### Passo 12. Somma

- **Cosa fare:** per ogni paese e anno calcola il **numero di imprese** e la **somma di `Number of employees`**.

**Risultato da consegnare**, file `tabella_occupazione.csv`:

| paese | anno | n_imprese | somma_dipendenti |
|---|---|---|---|
| IT | 1999 | … | … |
| … | … | … | … |

**Da sapere sul denominatore.** L'appendice degli autori si contraddice:

- la nota della Table D.2.3 dice che confrontano con gli addetti delle imprese attive **esclusi i lavoratori autonomi**, dalla Business Demography di Eurostat;
- la Table C.2.1 indica invece gli addetti delle Structural Business Statistics, **autonomi inclusi**.

Calcolo entrambe le versioni e vediamo quale si avvicina ai loro numeri. In ogni caso Orbis conta solo i dipendenti, quindi la copertura dell'occupazione esce un po' più bassa di quella della produzione, soprattutto dove ci sono molte micro imprese.

---

## Come leggere il risultato

- **Confronto con gli autori.** Le loro tabelle coprono il 1999-2012:
  - produzione: Table D.2.1 dell'appendice;
  - occupazione: Table D.2.3 dell'appendice.

  Per l'Italia, produzione manifatturiera: 61% nel 1999, 89% nel 2011, media 79% sul 2001-2012. I nostri numeri non devono coincidere al decimale. Gli autori hanno unito dischi Orbis del 2005, 2009 e 2013 e dati Amadeus, non Orbis Historical. Devono però avere lo stesso ordine di grandezza e lo stesso andamento.
- **Quali anni usare.** Il criterio pubblicato dagli autori è che il paese superi il 50% della produzione ufficiale in tutti gli anni del periodo di analisi. Gli anni in cui la percentuale è sotto il 50%, o salta molto da un anno all'altro, sono da usare con cautela.
- **Stati Uniti.**
  - Gli autori non li hanno validati, quindi non c'è un loro numero di confronto.
  - Il fatturato manifatturiero ufficiale americano è completo solo negli anni del censimento economico: 2007, 2012, 2017, 2022.
  - In Orbis le imprese private americane non depositano bilanci, e per molte il fatturato e i dipendenti sono stime di Moody's. Il file ha le colonne `Estimated operating revenue` ed `Estimated employees`: conviene contare quante righe americane sono stimate. Se sono la maggioranza, la copertura misura le stime, non dati reali.

