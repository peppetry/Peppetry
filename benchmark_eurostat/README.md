# Benchmark Eurostat per la copertura di Orbis

Totali ufficiali Eurostat e script per misurare quanta parte dell'economia è
coperta da un estratto Orbis. Il metodo replica l'Online Appendix, sezioni C e D, di
Kalemli-Özcan, Sørensen, Villegas-Sanchez, Volosovych e Yeşiltaş (2024),
*How to Construct Nationally Representative Firm-Level Data from the Orbis
Global Database*.

**Copertura** = somma su tutte le imprese Orbis di una variabile ÷ totale Eurostat
della stessa variabile, per paese e anno. La somma comprende **solo le sezioni NACE
che hanno un valore in entrambe le fonti** per quel paese-anno (Tab. C.2.3
dell'Appendix).

Paesi: AT BE CZ DE EE ES FI FR GB GR HU IT LV NO PL PT RO SE SI SK
(nei file si usa GB per il Regno Unito e GR per la Grecia, mentre Eurostat usa UK ed EL;
il codice originale resta nella colonna `geo_eurostat`). Anni: 1999-2024.

---

## 1. File

| File | Contenuto |
|---|---|
| `scarica_eurostat.py` | Scarica i dati dall'API Eurostat (JSON-stat) e crea i tre CSV tidy |
| `eurostat_sbs_settori.csv` | SBS per sezione NACE, classe TOTAL (1999-2024) |
| `eurostat_sbs_classi.csv` | SBS per classe di addetti (sezioni Rev.2 2005-2024, manifattura Rev.1.1 1999-2007) |
| `eurostat_bd_imprese.csv` | Business Demography: imprese attive, addetti e dipendenti per classe di dipendenti (1999-2024) |
| `eurostat_query_usate.csv` | Per ogni dataset: titolo, filtri usati (codici delle dimensioni), anni, paesi e numero di righe |
| `eurostat_disponibilita.csv` | Anni disponibili per paese nelle serie chiave |
| `estrai_tabelle_autori.py` | Estrae dal PDF dell'Appendix le tabelle pubblicate dagli autori |
| `autori_D11.csv`, `autori_D21.csv`, `autori_D22.csv`, `autori_D23.csv`, `autori_D24.csv`, `autori_D25.csv`, `autori_D31.csv` | Valori pubblicati dagli autori (Tab. D.1.1 p.69, D.2.1 p.72, D.2.2 p.73, D.2.3 p.74, D.2.4 p.75, D.2.5 p.76, D.3.1 p.78) |
| `calcola_copertura.py` | **Script principale**: legge Orbis e Eurostat e produce le tabelle di copertura in CSV ed Excel |
| `genera_esempio_orbis.py` | Genera il file Orbis sintetico di prova |
| `esempio_orbis_aggregati.csv` | Orbis **sintetico** (dati inventati, non sono dati Orbis veri) usato per il test |
| `test_calcola_copertura.py` | Test end-to-end con controlli automatici |
| `output_esempio/` | Output del test: CSV, `copertura_orbis.xlsx`, `output_console.txt`, `test_output.txt` |

### Colonne dei CSV Eurostat

`paese, geo_eurostat, anno, fonte, classificazione, nace, nace_r2_estesa,
nace_originale, classe, classe_originale, variabile, indicatore, unita, valore,
flag, derivato`

- `fonte` è il codice del dataset Eurostat.
- `classificazione` vale `NACE_R2` oppure `NACE_R11`.
- `nace` è la lettera di sezione NACE Rev.2. Per i dati Rev.1.1 è la sezione Rev.2
  equivalente secondo la mappatura degli autori (vedi §4).
- `nace_r2_estesa` è la mappatura alternativa, per esempio `L+M+N`.
- `nace_originale` è il codice del dataset (lettera Rev.1.1, oppure aggregati come
  `B-N_S95_X_K`).
- `classe` è la classe armonizzata: `TOTAL`, `0-19`, `20-249`, `250+`, le classi fini
  (`0-9`, `10-19`, …) e, solo per la BD, `0` e `TOTAL-0`.
- `derivato = True` indica una riga calcolata, cioè la somma di classi fini (ad es.
  `0-9+10-19`) oppure `TOTAL-0` nella BD.
- `flag` è il flag Eurostat:
  - `c` confidenziale (valore assente);
  - `b` rottura di serie;
  - `e` stima;
  - `p` provvisorio;
  - `u` bassa affidabilità;
  - `d` definizione diversa;
  - `:` dato mancante.
- Le celle confidenziali restano nel file con `valore` vuoto.

### Variabili e unità (unità originali Eurostat)

| `variabile` | SBS 1995-2020 (`indic_sb`) | SBS dal 2021 (`indic_sbs`) | Unità |
|---|---|---|---|
| `turnover_eur_milioni` | V12110 Turnover or gross premiums written | NETTUR_MEUR Net turnover | **milioni di euro** |
| `addetti` | V16110 Persons employed | EMP_NR Persons employed | numero di persone |
| `dipendenti` | V16130 Employees | SAL_NR Employees | numero |
| `imprese` | V11110 Enterprises | ENT_NR Enterprises | numero |
| `costi_personale_eur_milioni` | V13310 Personnel costs | EXPN_SAL_BEN_MEUR Employee benefits expense | milioni di euro |
| `valore_produzione_eur_milioni` | V12120 Production value | VAL_OUT_MEUR Value of output | milioni di euro |

| `variabile` (BD) | fino al 2020 (`indic_sb`) | `bd_size` (`indic_sbs`) | Unità |
|---|---|---|---|
| `imprese_attive` | V11910 Population of active enterprises in t | ENT_NR | numero |
| `addetti_bd` | V16910 Persons employed in the population of active enterprises | EMP_NR | numero |
| `dipendenti_bd` | V16911 Employees in the population of active enterprises | SAL_NR | numero |

Per i paesi fuori dall'euro (CZ, HU, PL, RO, SE, NO, GB) Eurostat converte in euro al
cambio medio annuo. Prima del 1999 gli importi sono in ECU.

---

## 2. Dataset Eurostat usati (codici verificati interrogando l'API)

API JSON-stat: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{dataset}?format=JSON&lang=EN&sinceTimePeriod=1999&geo=...&...`

| Uso | Dataset | Periodo | Filtri (dimensione = codici) |
|---|---|---|---|
| (a) SBS per sezione, NACE Rev.2 | **`sbs_na_sca_r2`** | 2005-2020 (2005-07 solo SE) | `nace_r2` = B C D E F G H I J L M N S95 B-N_S95_X_K; `indic_sb` = V12110 V12120 V16110 V16130 V11110 V13310 |
| (b) SBS per classe di addetti, Rev.2 | **`sbs_sc_sca_r2`** | 2005-2020 | stessi `nace_r2` e `indic_sb`; `size_emp` = TOTAL 0-9 10-19 20-49 50-249 GE250 |
| (c) SBS dal 2021 (regolamento EBS) | **`sbs_ovw_act`** | 2021-2024 | `nace_r2` = B…N, K, P, Q, R, S95, B-S_X_O_S94; `indic_sbs` = NETTUR_MEUR VAL_OUT_MEUR EMP_NR SAL_NR ENT_NR EXPN_SAL_BEN_MEUR |
| (c) SBS per classe dal 2021 | **`sbs_sc_ovw`** | 2021-2024 | come sopra; `size_emp` = TOTAL 0_1 2-9 0-9 10-19 20-49 50-249 GE250 |
| (d) SBS NACE Rev.1.1, per sezione | `sbs_na_2a_mi` (C estrattive), **`sbs_na_2a_dade`** (D manifattura totale), `sbs_na_2a_el` (E energia), `sbs_na_4a_co` (F costruzioni), `sbs_na_3b_tr` (G commercio), `sbs_na_1a_se` (H, I, K servizi) | 1995-2008 | `nace_r1` = C / D / E / F / G / H I K; stessi `indic_sb` |
| (d) SBS Rev.1.1, manifattura per classe | **`sbs_sc_2d_dade02`** (2002-07), `sbs_sc_2d_dade95` (1995-2001) | 1999-2007 | `nace_r1` = D; `size_emp` = TOTAL 1-9 1-19 10-19 20-49 50-249 GE20 GE250 (95: 50-99 100-249 250-499 500-999 GE1000) |
| (e) BD per classe e NACE Rev.2 | **`bd_9bd_sz_cl_r2`** | 2004-2020 | `nace_r2` = B…J, K_X_K642, L…S, B-N_X_K642, B-S_X_K642; `indic_sb` = V11910 V16910 V16911; `sizeclas` = TOTAL 0 1-4 5-9 GE10 |
| (e) BD attuale | **`bd_size`** | 2015-2024 per questi paesi | `nace_r2` = B…S, B-S_X_O_S94; `indic_sbs` = ENT_NR EMP_NR SAL_NR; `sizeclas` come sopra; `age` = TOTAL |
| (e) BD Rev.1.1 | `bd_9b_size_cl` | 1999-2007 | `nace_r1` = C D E F G H I J K_X_K7415 C-K_X_K7415; stessi indicatori |

Codici che **non esistono** o non sono più diffusi (l'API risponde 404): `sbs_na_ind`,
`sbs_sc_ind`, `sbs_sc_1b_se`, `sbs_sc_2d_dadn02`, `bd_9b_sz_cl`.
- `sbs_na_ind_r2` e `sbs_sc_ind_r2` esistono (B-E) ma non servono, perché contengono
  gli stessi valori di `*_sca_r2` per la sezione C.
- `bd_9ac_l_form_r2` e `bd_l_form` (per forma giuridica) esistono ma non servono:
  gli autori usano il totale delle forme giuridiche, e quel totale è già nei
  dataset per classe.

**Classi "0-19", "20-249", "250+"**
- **SBS Rev.2 ed EBS**: `0-19` = `0-9` + `10-19` e `20-249` = `20-49` + `50-249`.
  Sono righe derivate, calcolate solo se entrambe le componenti hanno un valore.
  `250+` = `GE250`.
- **SBS Rev.1.1**: la classe `1-19` è usata come `0-19`, perché le tabelle per classe
  Rev.1.1 partono da 1 addetto. Gli autori confrontano Eurostat 0-19 con Orbis 1-19.
- **BD**: `TOTAL-0` = classe `TOTAL` − classe `0` (zero **dipendenti**). È "all size
  classes minus zero employees" e serve a escludere gli autonomi.

---

## 3. Come Orbis viene confrontato con Eurostat (`calcola_copertura.py`)

| Tabella | Numeratore Orbis | Denominatore Eurostat | Sezioni |
|---|---|---|---|
| **D11** economia aggregata | Operating revenue, campione Totale, tutte le classi (anche `mancante`) | SBS turnover, classe TOTAL | sezioni comuni (default B-N senza K) |
| **D21 / D22** manifattura, gross output | Operating revenue, Totale / TFP | SBS turnover C (Rev.1.1: D) | C |
| **D23 / D24** manifattura, occupazione | Number of employees, Totale / TFP | SBS persons employed C | C |
| ↳ colonne extra di D23/D24 | come sopra | BD `addetti_bd` TOTAL-0 e BD `dipendenti_bd` | C |
| **D25** distribuzione dimensionale (default 2006) | quote di Operating revenue, Employees e n. imprese nelle classi 1-19 / 20-249 / 250+ (`mancante` esclusa) | quote SBS 0-19 / 20-249 / 250+ (`copertura_classe` = Orbis/Eurostat per classe) | C |
| **D31** numero di imprese | n_imprese, campione Totale | BD imprese attive, classe **TOTAL-0** (colonna extra: vs TOTAL) | sezioni comuni |
| **CP_tot / CP_C** (extra) | Costs of employees | SBS personnel costs (EBS: employee benefits expense) | sezioni comuni / C |

Regole:
1. In ogni paese-anno una sezione entra nel calcolo solo se ha **valore > 0 sia in
   Orbis sia in Eurostat**. Le celle Eurostat confidenziali (`c`) sono quindi escluse.
   La colonna `sezioni` dice quali sezioni sono state usate.
2. In ogni paese-anno si usa **una sola fonte (un solo "regime")**, per non mescolare
   classificazioni:
   - dal 2021: EBS (`sbs_ovw_act` / `sbs_sc_ovw`);
   - 2008-2020: SBS Rev.2;
   - prima del 2008: Rev.2 retropolata se esiste (`--preferenza-pre2008 r2`, il
     default), altrimenti Rev.1.1. Con `r11` si usa Rev.1.1 come gli autori.
   - Per la BD: prima `bd_size`, poi `bd_9bd_sz_cl_r2` (Rev.2 dal 2004), poi
     `bd_9b_size_cl`.

   La colonna `fonte_eurostat` dice quale dataset è stato usato.
3. Gli autori winsorizzano le celle paese-settore-anno con rapporto > 1. Lo script
   **non winsorizza**: segnala queste celle (colonna `n_sezioni_sopra_1` e file
   `dettaglio_sezioni.csv`), così si possono controllare a mano.
4. La riga "Media" delle tabelle larghe è la media degli anni mostrati. Per gli
   autori è la media 1999-2012.

---

## 4. Rotture di serie e avvertenze

- **2008, da NACE Rev.1.1 a Rev.2.** Fino al 2007 la manifattura è la sezione **D**
  (Rev.1.1); dal 2008 è la sezione **C**. Mappatura usata (`--mappa-rev11 autori`,
  come la Tab. C.2.3):

  | Rev.1.1 | Rev.2 |
  |---|---|
  | C (estrattive) | B |
  | D (manifattura) | C |
  | E (energia) | D |
  | F | F |
  | G | G |
  | H (alberghi) | I |
  | I (trasporti e comunicazioni) | H |
  | K (immobiliare e servizi alle imprese) | L |

  La mappatura non è esatta: la Rev.1.1 K comprende anche le attuali M, N e J62-63.
  Con `--mappa-rev11 estesa` si usano i gruppi D+E, H+J e L+M+N, e il numeratore Orbis
  somma le sezioni Rev.2 corrispondenti. Prima del 2008 l'SBS non pubblica E, J, M e
  N come sezioni Rev.2, quindi le coperture totali prima e dopo il 2008 si basano su
  insiemi diversi di sezioni. Per la manifattura le serie D e C sono quasi uguali:
  IT 2008 = 1.005 mld € (D) contro 978 mld € (C).
- **2021, regolamento EBS (UE 2019/2152).** Con l'EBS arrivano nuovi dataset
  (`sbs_ovw_act`, `sbs_sc_ovw`, `bd_size`) e nuovi codici degli indicatori:
  - il fatturato diventa *Net turnover* (NETTUR) invece di *Turnover or gross premiums
    written*;
  - i costi del personale diventano *Employee benefits expense*;
  - la copertura si estende a K, P, Q, R (e S95-S96);
  - le nuove classi 0_1 e 2-9 si aggiungono alla 0-9;
  - l'unità "impresa" è applicata in modo più rigoroso (profiling).

  Alcune celle 2021 hanno flag `b`, per esempio FR e PT nella manifattura. Il default
  `--sezioni default` (B-N senza K) rende il totale confrontabile prima e dopo il 2021.
  `--sezioni tutte` aggiunge K, P, Q, R dove Eurostat le pubblica. In Orbis la sezione
  K comprende le holding, che la BD esclude.
- **SBS e sezioni escluse.** Fino al 2020 l'SBS copre le sezioni B-N senza K (la
  finanza è solo parziale e non è nei dataset usati) più S95. Non coprono A, O, P-S.
  S95 si confronta solo se il file Orbis contiene il codice `S95`: con la sola sezione
  S il confronto gonfierebbe il numeratore.
- **BD.** La BD esclude le holding (K64.2, nella Rev.1.1 K74.15) e copre B-S senza O;
  P-S sono su base volontaria. La classe di dimensione della BD è per **dipendenti**,
  non per addetti. Per GR mancano gli anni 2008-2014 (TOTAL-0) e per BE gli anni
  precedenti il 2006.
- **Regno Unito (GB).** I dati SBS e BD finiscono nel **2018**: il Regno Unito non ha
  trasmesso i dati 2019-2020 per via della Brexit (uscita il 31.1.2020) e dal 2021 non
  rientra nell'EBS.
- **Lavoratori autonomi.** SBS turnover e SBS persons employed comprendono le imprese
  senza dipendenti e i titolari che lavorano nell'impresa. Orbis no. Per questo le
  coperture dell'occupazione su base SBS sono più basse; la BD TOTAL-0 le esclude.
  Le note della Tab. D.2.3 citano la BD, mentre la Tab. C.2.1 cita SBS V16110: lo
  script le calcola tutte e due.
- **Unità e cambi.** Gli importi Orbis vanno indicati in euro (`--unita euro`) o in
  migliaia di euro (`--unita migliaia`). Lo script li converte in milioni di euro.
  - Per i paesi fuori dall'euro Orbis converte al cambio della data di chiusura del
    bilancio, Eurostat al cambio medio annuo. Ne nasce un piccolo scarto.
  - Gli autori esprimono tutto in USD 2005. Il rapporto non cambia se numeratore e
    denominatore sono deflazionati allo stesso modo.
- **Bilanci consolidati.** Per evitare doppi conteggi gli aggregati Orbis vanno
  costruiti come fanno gli autori (Appendix C.2, punto 8): si escludono i bilanci
  C2 e, salvo eccezioni, anche i C1.
- **Anno.** Orbis usa l'anno di chiusura del bilancio, Eurostat l'anno solare.

### Disponibilità (anni con valore; dettagli in `eurostat_disponibilita.csv`)

| Paese | SBS manif. turnover | SBS manif. addetti | SBS manif. 3 classi | BD imprese attive (senza 0) |
|---|---|---|---|---|
| AT | 1999-2024 | 1999-2024 | 1999-2024 | 2004-2024 |
| BE | 1999-2001, 2003-2024 | 1999-2001, 2003-2024 | 1999-2001, 2003-08, 2010-24 | 2006-2024 |
| CZ | 1999-2004, 2006-2024 | 1999-2024 | 1999-2024 | 2000-2024 |
| DE | 1999-2024 | 1999-2024 | 1999-2024 | 2004-2024 |
| EE | 1999-2024 | 2000-2024 | 1999-2024 | 2000-2024 |
| ES | 1999-2024 | 1999-2024 | 1999-2024 | 1999-2024 |
| FI | 1999-2024 | 1999-2024 | 1999-2024 | 1999-2024 |
| FR | 1999-2024 | 1999-2007, 2010-2024 | 1999-2008, 2010-2024 | 1999-2001, 2003-2024 |
| GB | 1999-2018 | 1999-2018 | 1999-2018 | 1999-2018 |
| GR | 2003-2024 | 2003-2024 | 1999-2000, 2003-2024 | 2004-07, 2015-2024 |
| HU | 1999-2024 | 1999-2024 | 2000-2024 | 2000-2024 |
| IT | 1999-2024 | 1999-2024 | 1999-2024 | 1999-2024 |
| LV | 1999-2024 | 1999-2024 | 1999-2024 | 2000-2024 |
| NO | 1999-2001, 2003-2024 | 1999-2001, 2003-2024 | 1999-2000, 2002-2024 | 2003-2024 |
| PL | 1999-2024 | 2002-2024 | 1999-2001, 2003-2024 | 2004-2024 |
| PT | 1999-2024 | 1999-2024 | 1999-2024 | 1999-2024 |
| RO | 1999-2024 | 1999-2024 | 2000-2024 | 2000-2024 |
| SE | 1999-2024 | 1999-2024 | 1999-2024 | 1999-2024 |
| SI | 1999-2024 | 2002-2024 | 1999-2024 | 2000-2024 |
| SK | 1999-2024 | 2000-2024 | 1999-2024 | 2000-2024 |

Per il totale dell'economia il numero di sezioni con turnover cambia per paese e
anno:
- 1999-2007: di solito 8 sezioni (B C D F G H I L);
- 2008-2020: fino a 12 sezioni (B-N senza K) più S95. Nell'edizione attuale il
  turnover delle costruzioni (F) per il **2009** manca in 18 paesi su 20 e quello del
  2008 manca per DE. La Tab. C.2.3 degli autori mostra lacune simili per F e G;
- 2021-2024: fino a 16 sezioni.

### Verifica del benchmark

Il test confronta le quote Eurostat per classe dimensionale della manifattura nel 2006,
ricalcolate da `sbs_sc_2d_dade02`, con le quote "Eurostat-SBS" pubblicate dagli autori
(Tab. D.2.5): su 120 celle (20 paesi × 3 classi × 2 variabili) la differenza media è
0.004 e la massima 0.016, cioè lo scarto da arrotondamento. Gli autori hanno quindi
usato gli stessi dati che si scaricano oggi.

---

## 5. Come si usa

```bash
pip install pandas requests openpyxl xlsxwriter pdfplumber

# 1) (ri)scaricare i dati Eurostat (circa 1 minuto)
python3 scarica_eurostat.py            # opzione: --dal 1995

# 2) (facoltativo) ri-estrarre le tabelle degli autori dal PDF
python3 estrai_tabelle_autori.py /percorso/Appendix.pdf

# 3) calcolare la copertura dei propri dati Orbis
python3 calcola_copertura.py --orbis miei_aggregati_orbis.csv --unita migliaia \
        --out output_copertura --confronta-autori

# opzioni utili
#   --anni-dimensioni 2006,2015,2022   anni per D25
#   --sezioni default|tutte|B,C,F,G    sezioni ammesse nel totale economia
#   --mappa-rev11 autori|estesa        mappatura Rev.1.1 -> Rev.2 prima del 2008
#   --preferenza-pre2008 r2|r11        fonte preferita per gli anni < 2008
#   --anno-min / --anno-max

# 4) test end-to-end sul file sintetico
python3 genera_esempio_orbis.py        # ricrea esempio_orbis_aggregati.csv
python3 test_calcola_copertura.py      # 12 controlli automatici
```

### Formato del file Orbis aggregato

Una riga per `paese × anno × settore_nace × classe_addetti × campione`:

```
paese,anno,settore_nace,classe_addetti,campione,n_imprese,somma_operating_revenue,somma_employees,somma_costs_of_employees
IT,2006,C,1-19,Totale,61234,48211000000,301200,9100000000
IT,2006,C,20-249,Totale,...
IT,2006,C,mancante,Totale,...
IT,2006,C,1-19,TFP,...
```

- `settore_nace`: lettera di sezione NACE Rev.2 (A-U). `S95` è accettato.
- `classe_addetti`: `1-19`, `20-249`, `250+`, `mancante`. Sono riconosciuti anche
  `0-19`, `GE250`, `>=250`, `missing` e vuoto.
- `campione`: `Totale` (imprese con il valore positivo della variabile) oppure `TFP`
  (imprese che riportano anche employees o costs of employees, tangible fixed assets
  e material costs).
- UK ed EL sono accettati e convertiti in GB e GR. Il separatore può essere `,` o `;`.
- Le righe duplicate vengono sommate, con un avviso.

Schema indicativo per costruirlo dai microdati, in Python o in Stata con `collapse (sum)`:
```python
agg = (firm.assign(classe=pd.cut(firm.employees, [0, 19, 249, np.inf],
                                 labels=["1-19", "20-249", "250+"]).astype(str)
                          .replace("nan", "mancante"))
           .groupby(["paese", "anno", "settore_nace", "classe", "campione"])
           .agg(n_imprese=("bvd_id", "nunique"),
                somma_operating_revenue=("operating_revenue", "sum"),
                somma_employees=("employees", "sum"),
                somma_costs_of_employees=("costs_of_employees", "sum")))
```
(Per D31 contare solo le imprese **attive**: gli autori escludono Inactive, Dissolved,
In liquidation e Bankruptcy.)

### Output

- `copertura_<tab>.csv`, in formato lungo: `paese, anno, orbis, eurostat, n_sezioni,
  sezioni, fonte_eurostat, flag_eurostat, n_sezioni_sopra_1, copertura` più le colonne
  extra. Con `--confronta-autori` si aggiungono `copertura_autori` e `differenza`.
- `copertura_orbis.xlsx`: un foglio per tabella, con la tabella anno × paese calcolata,
  i valori degli autori, la differenza e il dettaglio in formato lungo. Ci sono anche
  un foglio LEGGIMI con i parametri della corsa, il foglio D25 e il foglio
  `dettaglio_sezioni`.
- A console ogni cella è stampata come `valore calcolato[valore autori]`.

### Risultato del test (file sintetico)

Vedi `output_esempio/test_output.txt`. Il file sintetico è costruito con coperture
note, uguali in ogni sezione. Esempio: IT con fatturato al 75%, occupazione al 65% e
imprese al 50%; campione TFP pari al 60% del campione Totale. Le sezioni senza
Eurostat ricevono valori Orbis casuali, che lo script deve escludere. Risultato:
12/12 controlli superati.
- D11, D21, D22, D23, D24, D31 e CP restituiscono le coperture vere, con errore
  inferiore a 1e-8.
- Le sezioni A, K, O, P, Q, R, S sono escluse.
- `--unita euro` e `--unita migliaia` danno lo stesso risultato.
- In D25 le quote Orbis coincidono con quelle Eurostat.
- Il benchmark Eurostat 2006 coincide con i valori pubblicati dagli autori.
