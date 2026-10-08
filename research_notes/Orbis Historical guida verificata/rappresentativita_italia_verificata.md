# Rappresentatività di Orbis rispetto alle statistiche ufficiali, con focus sull'Italia: verifica sui testi integrali

> **Metodo e affidabilità (da leggere prima).** Questa nota sostituisce le note basate sui soli snippet (`Guida Orbis Historical analisi economica/rappresentativita_e_italia.md` e `letteratura_metodologica.md`). Tutti i documenti citati sotto come "testo integrale" sono stati scaricati con curl in `/tmp/claude-0/-home-user-Peppetry/e076315a-2555-515f-b864-91b965e0091a/scratchpad/pdf_repr/` e letti con pdftotext. Le figure senza dati tabellari sono state convertite in immagine e lette a vista.
> - **Citazioni**: sono riportate alla lettera nella lingua originale (inglese per OCSE, NBER, AEJ, FMI, CompNet e Banca d'Italia; italiano per Istat e codice civile).
> - **Pagine**: "p." indica la pagina stampata del documento; dove differisce dalla pagina del PDF lo segnalo come "PDF p.". Per Bajgar et al. e AEJ le due numerazioni coincidono; per Gal (2013), Kalemli-Özcan rev1 e Díez et al. la pagina stampata è quella del PDF meno 1; per QEF 308 è quella del PDF meno 2.
> - **Numeri letti dai grafici**: sono marcati **[lettura grafica, ±5 p.p.]**.
> - **Fonti non lette per intero**: sono marcate **UNVERIFIED**. Restano bloccati con 403: oecd.org (pagine HTML e one.oecd.org; i PDF in `/content/dam/` invece si scaricano), imf.org (il WP 19/82 è stato letto da una copia Wayback), SSRN, CEPR e JRC (publications.jrc.ec.europa.eu, "Request Rejected").
> - **Verdetti** sulle affermazioni precedenti: CONFIRMED / CORRECTED / NOT FOUND / NOT CHECKED. Il riepilogo completo è nella KQ7.

---

## KQ1. Bajgar, Berlingieri, Calligaris, Criscuolo, Timmis (2020), OECD STI WP 2020/06: copertura per paese (Italia) e per classe dimensionale, "preferred sample", raccomandazioni, pulizia

### Takeaway
Con il vintage OECD-Orbis di **febbraio 2017** (non Orbis Historical), confrontato con STAN e MultiProd, il campione 2002-2015 di 20 paesi cattura in media circa il 60% di occupazione e output e circa il 40% del valore aggiunto. L'Italia è vicina alla media sul piano aggregato, ma in numero di imprese (con occupazione non mancante) ne copre solo circa il 35% di quelle MultiProd, e appena il 15-17% se si richiedono anche output o valore aggiunto. L'Italia è comunque **uno dei sette paesi del "preferred sample"**, con il periodo 2002-2015 interamente incluso in entrambi i campioni ristretti. Il "preferred sample" combina tre scelte: (1) imputazione interna del valore aggiunto (costo del personale + EBITDA); (2) country-year "hand-picked", cioè periodi continui con copertura superiore a circa il 20% e stabile; (3) solo imprese con almeno 10 addetti. Il re-weighting per classe dimensionale **non** risolve il problema di rappresentatività.

### Cited Findings
**Dati e confronto**
- Vintage usato: "This paper focuses on the OECD Orbis vintage from February 2017" (p. 11). Paesi: Austria, Belgio, Danimarca, Estonia, Finlandia, Francia, Germania, Grecia, Ungheria, **Italia**, Giappone, Corea, Paesi Bassi, Norvegia, Portogallo, Slovenia, Spagna, Svezia, Regno Unito, Stati Uniti; periodo "2002-2015" (p. 12). Repubblica Ceca, Polonia e Slovacchia sono escluse perché "lose most observations once rounded values are dropped" (p. 12) — [Bajgar et al. 2020, PDF OCSE](https://www.oecd.org/content/dam/oecd/en/publications/reports/2020/05/coverage-and-representativeness-of-orbis-data_9628c322/c7bdaa03-en.pdf)
- **Caveat per l'Italia sul benchmark**: in MultiProd "in some countries (e.g. Italy and the Netherlands) such data sources are not available and surveys based on a sample of firms have to be used", poi riponderati con il registro (p. 13). Inoltre "The underlying microdata for Italy and the Netherlands are a sample rather than a population and account for only about 50% of the aggregate output, value added and employment; however, they are made representative and comparable through re-weighting based on business registers information" (p. 13) — [Bajgar et al. 2020](https://www.oecd.org/content/dam/oecd/en/publications/reports/2020/05/coverage-and-representativeness-of-orbis-data_9628c322/c7bdaa03-en.pdf)
- Soglie del benchmark: MultiProd copre di norma le imprese con almeno 1 dipendente. Fanno eccezione Austria e Paesi Bassi (≥10 dipendenti), Germania (≥20), Finlandia (escluse le imprese con meno di 1 FTE) e Giappone (solo manifattura). "For these countries, we apply the corresponding thresholds also to the Orbis data" (p. 13). **CORRECTED** rispetto a "firms with at least 10 employees for most countries": la soglia 10 vale solo per AUT e NLD, e in seguito per il "preferred sample".
- Tutte le statistiche sono condizionate all'occupazione non mancante: "the coverage and distribution statistics are calculated over firms with non-missing employment variable" (p. 9); il codice MultiProd "drops observations with missing employment information" (p. 16).

**Pulizia (p. 11, verbatim)**
- "we keep accounts that refer to entire calendar years, dropping observations with missing information on key variables as well as outliers identified as implausible changes or ratios and firms that are inactive. We also (i) set operating revenues and the number of employees to missing when a large number of firms in a country and year have the same value of a given variable, suggesting rounded or imputed values, and (ii) we drop duplicate accounts of the same firm in the same year" (p. 11). **CONFIRMED.**
- Arrotondamenti: il problema è grave per CZE, POL, SVK e USA e "Rounding also plays a smaller, but non-negligible, role for Finland, Japan, Sweden and Italy" (p. 49, Fig. 6.1 p. 50).
- Regola di consolidamento: gli autori usano principalmente i conti non consolidati. Scartano i conti consolidati quando esiste il non consolidato (C2) o quando il non consolidato è osservato per lo stesso ID (alcuni C1). Se restano duplicati e uno è U2, scartano gli altri. Infine scartano i LF (pp. 51-52). Per i LF: "they almost never have information on value added, capital or wages" (p. 51).
- Variabili: l'output è approssimato dall'operating revenue (p. 14). I consumi intermedi sono calcolati come operating revenue meno valore aggiunto; il materials cost di Orbis non viene usato perché "material costs represent only a part of intermediate inputs" (nota 10, p. 56). Il capitale è il valore contabile delle immobilizzazioni materiali (p. 15).

**Copertura aggregata vs STAN (Fig. 3.1, p. 18; media 2002-2015; manifattura, utilities, costruzioni e servizi non finanziari)**
- Testo: "Orbis data in the sample ... typically capture around 60% of aggregate employment and output and around 40% of aggregate value added" (p. 17). **CONFIRMED.** Variazione: output da "over 100% in the Netherlands and the United Kingdom" a "just 30-40% in Austria, Norway and all three non-European countries"; "just 10% of value added or less captured for Japan and the United States" (p. 17).
- **Italia** (Fig. 3.1): occupazione circa 62%, output circa 56%, valore aggiunto circa 40% di STAN **[lettura grafica, ±5 p.p.]**.
- **Italia nel tempo** (Fig. A.1, p. 62): l'asse del pannello ITA va da 30 a 94. L'occupazione Orbis/STAN sale da circa il 45% (2002) a circa il 90% (2013-2015); output intorno al 45-60%; valore aggiunto intorno al 30-40% **[lettura grafica]**. Esempio testuale di discontinuità: per il Portogallo la copertura "increases in 2006 from less than 5% to more than 80%" (p. 18).

**Copertura in numero di imprese vs MultiProd (manifattura e servizi non finanziari)**
- Testo: "about half the countries in the sample have coverage in the 10-30% range"; "Sweden and Portugal ... at 40-60%" (p. 20). "A substantial share of firms in several countries lack information on output (Belgium, the Netherlands, Austria, Denmark, Italy and Germany)" (p. 21). **CONFIRMED.**
- Senza condizionare all'occupazione (Fig. A.2), "the availability of the output variable is significantly higher than the availability of the employment variable for Finland, France, Hungary, the earlier years in Germany and Italy and the later years in Norway" (p. 21).
- **Italia** (Fig. 3.4, p. 21; media sugli anni): con occupazione disponibile circa 0,35; con output circa 0,17; con valore aggiunto circa 0,15; con capitale circa 0,16; con salari circa 0,17 **[lettura grafica]**.
- **Italia nel tempo** (Fig. 3.5, p. 22): copertura bassa (circa 0,1-0,25) dal 2002 al 2012 circa; poi il numero di osservazioni con occupazione salta a circa 1,1-1,2 nel 2013-2015, mentre output, valore aggiunto e capitale restano intorno a 0,25 **[lettura grafica]**. Il salto indica che in quel vintage il campo "employees" diventa disponibile per molte più società negli anni recenti. È un'inferenza mia: gli autori non commentano il caso italiano.
- **Per classe dimensionale** (Fig. 3.6, p. 22; mediane su country-industry-year): "The median coverage in terms of employment, output and value added is, respectively, only 43%, 29% and 7% for micro-firms with less than 10 employees but 83%, 79% and 50% for large firms with at least 250 employees" (p. 21). Distribuzione dell'occupazione: le imprese con 250+ addetti pesano "about 40% all employment according to the MultiProd data but for about 60% in Orbis"; quelle con meno di 10 addetti "17% ... in MultiProd but just 7% in Orbis" (pp. 23-24).
- Selezione: "the average firm in Orbis is two-and-half times larger in terms of employment"; "35% greater labour productivity, 16% greater total factor productivity and pays 20% higher wages" (p. 24). Differenza di produttività entro classe: "just 3% for large firms above 250 employees but 23% for small firms with 10-19 employees and 60% for micro-firms" (p. 25).
- Entrata e uscita: correlazione mediana nel tempo con DynEmp "about 0.2 for entry rates and close to zero for exit rates" (p. 30).

**Campioni ristretti e "preferred sample"**
- Definizioni (p. 35): il campione "5000+" "includes only country-years with at least 5000 observations for which value added is available"; il campione "hand-picked" "represents, broadly speaking, continuous country-periods with coverage that is north of 20% and reasonably stable over time".
- **Tabella 4.1 (p. 36)**, nel formato 5000+ / hand-picked:

  | Paese | 5000+ | hand-picked |
  |---|---|---|
  | BEL | 2002-2014 | 2002-2014 |
  | DNK | 2002-2003 | — |
  | FIN | 2002-2013 | 2004-2013 |
  | FRA | 2002-2015 | 2002-2015 |
  | DEU | 2005-2013 | 2006-2013 |
  | HUN | 2007, 2009, 2010, 2012 | — |
  | **ITA** | **2002-2015** | **2002-2015** |
  | JPN | 2002-2004 | — |
  | NOR | 2002-2004 | — |
  | PRT | 2006-2012 | 2006-2012 |
  | SWE | 2002-2012 | 2004-2012 |

  Nota alla tabella: sono elencati solo i country-year coperti anche da MultiProd. "Some other countries in Orbis, such as Spain, could also fit in the restricted samples but are not shown here" (p. 36 e nota 23).
- Effetto sulla copertura: la copertura mediana per country-industry-year passa da 14% (campione completo) a 25% (5000+) e 26% (hand-picked); il 25° percentile da meno del 3% a 13-14% (p. 36).
- "Preferred sample": "it relies on the internal imputation of value added, on the 'hand-picked' country sample and on firms with at least 10 employees. The sample consists of seven countries: Belgium, Finland, France, Germany, Italy, Portugal and Sweden" (p. 44). Copertura: "from over 70% for Belgium ..., Portugal and Finland to about 40% for France, Italy and Germany ... a dip for Italy in 2010" (p. 44).
  - **Italia** (Fig. 5.1, p. 45): circa 0,48 nel 2002, circa 0,25-0,40 nel 2003-2009, circa 0,1 nel 2010, circa 0,30-0,35 nel 2011-2015 **[lettura grafica]**.
  - Risultato: le imprese 250+ fanno "50% of the total employment captured by Orbis, as compared to 47% in MultiProd"; rispetto a MultiProd le imprese Orbis hanno "21% greater employment, 15% higher age, 5% greater labour productivity, 13% greater multi-factor productivity and 5% higher wages" (p. 45).
- I tre passi, alla lettera: "restricting the sample to periods of stable and high coverage within the best-covered European countries; imputing value added, using firm wage bill and earnings information; and focusing on firms with more than 10 employees" (p. 9). **CORRECTED** rispetto alla nota precedente: il terzo passo è la soglia dei 10 addetti. "Fewer than 10 countries" è la dimensione del campione di paesi (abstract, p. 3), non un passo separato.
- Imputazione del valore aggiunto: quella interna è "a sensible choice"; quella esterna (salari medi STAN × addetti) "dramatically reduces variation" e va usata "only for analyses specifically focusing on countries where neither unimputed nor internally imputed value added is available" (p. 33). Il VA imputato va usato per tutte le imprese, non solo per quelle con VA mancante (p. 32, nota 21).
- Soglia dei 10 addetti: "excluding this group is a sensible choice" (p. 40). Nota 24, rilevante per l'Italia: "by excluding firms with less than 20 employees, one drops about 97% (55% of employment) of employing firms in Italy service sector and 89% of firms (35% of employment) in the Norwegian service sector" (p. 57).
- Pesi: "Surprisingly, weighting does not improve representativeness of Orbis data beyond the mechanic effect on the firm size distribution" (p. 41); "reweighting based on firm size does not solve the problem at hand" (p. 42).
- Ownership: "There are ownership linkages since the early 1990s, but coverage is better from 2007 onwards. Furthermore, the global ultimate owner data only begins in 2007"; "around 5-10% of firms enter the Orbis ownership data each year and up to 4% leave each year" (p. 53).
- Raccomandazioni finali (p. 55): Orbis è più adatto ad analisi su "large and high-performing firms", a statistiche "at a global level", ai "best covered country-years", alla "mean performance" e alle "within-firm responses"; serve cautela per la metà inferiore della distribuzione, i confronti tra paesi, la dispersione, l'entrata e l'uscita. **CONFIRMED.**

### Inferences
- L'Italia è l'unico grande paese mediterraneo presente in entrambi i campioni ristretti per tutti gli anni 2002-2015. Il limite italiano non è la presenza delle imprese ma la **disponibilità delle variabili** per riga: occupazione, output e VA mancano per molte società e l'output manca più spesso che altrove. Per la consegna Orbis Historical conviene quindi misurare la copertura **per variabile** (addetti, ricavi, VA, costo del personale, immobilizzazioni) e non solo per numero di BvD ID.
- Il "dip" italiano del 2010 e il salto dell'occupazione nel 2013-2015 (vintage 2017) sono fenomeni del singolo vintage. In Orbis Historical (consegna dic. 2025) possono essere diversi, perché i bilanci sono raccolti nel tempo: va verificato direttamente sui dati.
- Il benchmark italiano di Bajgar et al. è esso stesso un campione riponderato (circa il 50% dell'output). Le correlazioni Orbis-MultiProd per l'Italia sono quindi un confronto campione-contro-campione.

### Gaps
- Gli autori non pubblicano valori numerici per paese-anno: "Coverage data at the country-industry-year level is available from the authors upon request" (nota 16, p. 57). I valori italiani sopra sono letture grafiche.
- Non si sa se Orbis Historical riproduca le stesse discontinuità italiane (2010, 2013): nessuno studio letto lo documenta.

---

## KQ2. Gal (2013), OECD ECO WP 1049: pulizia e metodo di ri-pesatura (OECD-ORBIS)

### Takeaway
Gal costruisce pesi di **ricampionamento interi ≥1** per cella paese × industria × classe dimensionale × anno, in modo che l'occupazione Orbis eguagli quella SDBS. Non applica filtri sugli outlier di default. Nel 1999-2009 l'Italia è il paese con la migliore disponibilità di variabili per la TFP. Il peso medio italiano nel 2005 (9,4) è però alto per le micro-imprese (17,7), molto superiore a Spagna e Francia (circa 2) e inferiore a Germania (46,6) e Regno Unito (18,2).

### Cited Findings
- Campione: "the years 1999-2009 ... derived from filtering out accounts referring to less than complete calendar years and consolidated accounts, using indicator variables prepared Gonnard and Ragoussis (2013)" (nota 5, p. 7 = PDF p. 8). Settore: "non-farm business sector (NACE Rev 1.1 codes 15-74)" — [Gal 2013, PDF OCSE](https://www.oecd.org/content/dam/oecd/en/publications/reports/2013/05/measuring-total-factor-productivity-at-the-firm-level-using-oecd-orbis_g17a22d0/5k46dsb25ls6-en.pdf)
- **Tabella 1 (p. 8 = PDF p. 9), Italia, 1999-2009**: 2.010.555 osservazioni con produttività del lavoro su turnover; 1.748.028 con TFP non imputata (86,9%); 1.843.820 con imputazione interna (91,7%); 1.944.699 con imputazione esterna (96,7%). L'Italia è prima nella graduatoria (ESP 83,8%, GBR 56,7%, FRA 38,6%, DEU 18,7%, USA 0,0%). "most large European countries, such as Spain, Italy, and Great Britain ... have data which are almost equally well suited for obtaining measures of either labour productivity or TFP" (p. 8).
- Imputazione interna: "VA = wL + rK" con controparti "COSTS_EMPLOYEES and EBITDA"; correlazioni con il VA osservato "0.98 for an average country and year" nei livelli e "around 0.8" nelle crescite (p. 9 = PDF p. 10). Imputazione esterna: costo medio del lavoro STAN per paese, anno e industria a 2 cifre × addetti Orbis (p. 9; Tab. 2 p. 11).
- **Pesi, testo (p. 10 = PDF p. 11)**: "sampling weights are introduced, using information on the number of employees in a country*industry*sizeclass*year cell from the OECD SDBS database ... a time-varying resampling weight is assigned to each firm, which is always greater or equal to one, making sure we do not lose firms which are already in ORBIS, but we only replicate them up to the point where the true size- and sectoral structure is achieved". Si usa l'occupazione e non il numero di imprese, perché alcuni paesi (Giappone, Corea) riportano stabilimenti (nota 17).
- **Formula (p. 12 = PDF p. 13)**: E(w_jt) = L^SDBS_cist / L^ORBIS_cist. In pratica w̃_jt = 1 + ⌊(L^SDBS − L^ORBIS)/L^ORBIS⌋ + z_jt, con z_jt ~ Bernoulli di probabilità pari al resto frazionario. Esempio dell'autore: "if the ratio ... is 1.3 ... the 30% 'extra' employment is obtained by drawing firms randomly from the pool of ORBIS firms"; con rapporto 2,3 "all firms are taken at least twice and only the remaining extra 30% will be drawn randomly" (nota 18). Pesi distinti per ogni misura di produttività (nota 19). **CONFIRMED**: la nota precedente descriveva correttamente il metodo e la formula implicita ora è verificata.
- **Tabella 3 (p. 13 = PDF p. 14), peso medio 2005 per classe 1-9 / 10-19 / 20-49 / 50-249 / 250+ / media**:
  - **ITA**: 17,7 / 6,0 / 2,3 / 1,3 / 1,2 / 9,4
  - DEU: 333,6 / 126,8 / 26,5 / 5,1 / 1,9 / 46,6
  - ESP: 2,4 / 1,7 / 1,5 / 1,4 / 1,2 / 2,1
  - FRA: 2,1 / 2,0 / 1,7 / 1,6 / 1,6 / 2,0
  - GBR: 46,6 / 24,2 / 6,2 / 1,9 / 1,1 / 18,2

  Commento dell'autore: "Differences in coverage mainly reflect differences in the nature of data providers"; "concentrating on the set of firms with more than 20 employees helps in getting a better coverage"; i servizi hanno pesi "2-3 times higher" della manifattura (p. 12).
- Assunzione critica: il ricampionamento "implicitly assumes that firms in ORBIS within a specific country * industry * size-class ... are representative" (p. 15 = PDF p. 16).
- Outlier: "By default, no outlier-filtering is implemented" (§3.1.4, p. 20 = PDF p. 21). Le due opzioni proposte sono filtri ex ante su rapporti (K/L, M/Y) e salti (dVA, dL), oppure filtri ex post su livelli e variazioni di produttività, "by country and industry". La nota 29 cita un'eccezione: un filtro applicato solo agli indici superlativi.
- Caveat temporale: "in cases where resampling weights are high, typically, in the early years (up to 2004), and in countries with generally poor coverage (see Table 3), results need to be treated with more caution. Further, the measurement of entry and especially exit is noisy" (p. 38 = PDF p. 39).

### Inferences
- Per l'Italia un peso medio di 17,7 per le micro (2005) vuol dire che in Orbis compare circa 1 addetto su 18 delle micro-imprese SDBS. Ripesare le micro italiane significa replicare circa 18 volte imprese già selezionate positivamente. Bajgar et al. (2020) mostrano che questo non corregge la produttività; la soglia ≥10 o ≥20 addetti è la strada più difendibile.
- I pesi di Gal derivano da OECD-ORBIS 2010-2012 circa. Per Orbis Historical 2025 vanno ricalcolati con SBS/Frame-SBS correnti.

### Gaps
- Non ho estratto la Tabella E.5 (pesi per macro-settore) né la Tabella E.1 completa: sono disponibili nel PDF alle pp. 46-47 se servono.

---

## KQ3. Banca d'Italia (QEF 308, De Socio e Finaldi Russo 2016) e confronti Cerved/Orbis/Istat: copertura italiana

### Takeaway
QEF 308 usa Orbis per i paesi dell'area euro (2004-2013) e Cerved per l'Italia. Per l'Italia nel 2013 Orbis supera il 50% del numero di imprese Eurostat nelle classi piccole, medie e grandi, ma non nelle micro. Cerved copre circa il 15% delle micro-imprese Istat, il 33% delle piccole e quasi il 99% delle classi maggiori, oltre all'80% circa del debito finanziario dei conti finanziari. Non ho trovato altri lavori Banca d'Italia con un confronto quantitativo Orbis/AIDA vs Istat.

### Cited Findings
- Dati Orbis: "The database includes firms' data from 2004 to 2013 for the 18 countries belonging to the euro area in 2014. Sample coverage is frequently above 50 per cent (see Tab. A8 in the Appendix); it is generally lower for micro firms and, among the largest countries, for Germany" (p. 9 = PDF p. 11) — [QEF 308](https://www.bancaditalia.it/pubblicazioni/qef/2016-0308/QEF_308_16.pdf)
- Cerved: "in the Cerved database (which includes virtually all Italian limited liability companies) around 40 per cent of firms without financial debt report a positive amount of total debt but not the specific values for financial debt or other kind of debt (fig. A7)" (nota 10, p. 9). **CONFIRMED.** Formulazione più precisa nell'Appendice: "according to Cerved data, around 40 per cent of Italian firms with zero leverage ... report a positive amount of total debt but not the specific values" (p. 34 = PDF p. 36).
- **Copertura Cerved vs Istat (nota 22, p. 18 = PDF p. 20)**: "Cerved's better coverage of larger firms emerges clearly from a comparison with Istat data ('Business size and competitiveness' database): in terms of number of firms, the coverage ratio increases from about 15 per cent among micro firms, to 33 per cent among small firms and to nearly 99 per cent for the larger size classes." **NUOVO** (prima non presente).
- Copertura Cerved vs conti finanziari (2013): "the amount of financial debt based on Cerved (about 1,000 billion euros) represents about 80 per cent of the aggregate financial debt derived from financial accounts" (p. 18). Totale dei conti finanziari: 1.273 miliardi (Tab. 3).
- **Tab. A8 (p. 32 = PDF p. 34), Orbis 2013, Italia**: micro 130.841, piccole 60.274, medie 14.176, grandi 3.947, totale 209.238 imprese. Le celle verdi, cioè "estimated coverage of the Orbis dataset is above 50 per cent" rispetto al numero di imprese Eurostat, sono **piccole, medie e grandi; le micro no** (verificato sull'immagine della tabella). Caveat degli autori: le classi usano anche fatturato e attivo e "the comparison must be viewed with caution" (p. 31). Il campione è già filtrato (attivo, fatturato e debito non nulli, almeno tre osservazioni consecutive, outlier esclusi; p. 31).
- Orbis, imprese senza debito finanziario: "around 35 per cent; among the largest countries Italy has the highest percentage (43 per cent; Fig. A5)" (p. 34).

### Inferences
- I due rapporti di copertura di QEF 308 (Cerved/Istat circa 15% per le micro, circa 99% per le grandi; Orbis/Eurostat sopra il 50% tranne le micro) misurano la stessa realtà: le micro italiane sono in gran parte ditte individuali e società di persone che non depositano bilancio (vedi KQ4). Il tetto di copertura per numero di imprese è quindi strutturalmente basso.

### Gaps
- Non trovato (e non cercato in modo esaustivo per limiti di tempo) un Tema di discussione o QEF Banca d'Italia che confronti sistematicamente Orbis/AIDA con Cerved o Istat per anno. L'affermazione precedente su QEF 313 ("only 32 patenting firms ... not in Cerved") resta **NOT CHECKED**.

---

## KQ4. Istat: Frame-SBS, chi deposita il bilancio, quota di unità/addetti/VA delle società di capitali; bilancio abbreviato e micro (voci omesse)

### Takeaway
I bilanci civilistici coprono circa **800 mila società di capitali**, pari al **21% delle unità, 59% dell'occupazione e 75% del VA del Frame SBS** (Istat, Oropallo et al. 2015, anno di riferimento circa 2012). Le imprese individuali (circa 37% delle unità, meno del 6-7% del VA) e le società di persone (18-20% delle unità, 6-9% del VA) restano fuori. Il bilancio abbreviato (art. 2435-bis c.c.) **non** raggruppa materie prime (B6) e servizi (B7) e mantiene salari (B9a) e oneri sociali (B9b). Il bilancio delle micro-imprese (art. 2435-ter) può omettere la nota integrativa, e con essa il numero medio dei dipendenti.

### Cited Findings
**Frame-SBS e fonti amministrative**
- Nota metodologica Istat sui risultati economici delle imprese (anno 2012): "Il nuovo sistema Frame per le imprese con meno di 100 addetti (4.340.464 unità) è basato sul trattamento statistico delle informazioni provenienti dalle seguenti fonti amministrative: Bilanci civilistici (16,2%), Studi di settore (67,2%), Modello Unico (12,3%), Modello Irap (1,8%). Una quota di imprese (2,5%) non risulta coperto dalle fonti amministrative" (p. 1) — [Istat, Nota metodologica](https://www.istat.it/it/files//2014/11/Nota-metodologica7.pdf). Il costo del lavoro usa come ausiliaria "Racli ... ottenuto sulla base della fonte Inps-Emens" (p. 1).
  - Verdetto sulla nota precedente ("16% delle unità (700 mila società)" e "<250 addetti (4.361.922 unità): bilanci 18%-19,3%, studi di settore 55,5%"): **CORRECTED**. Il valore corretto è 16,2% per le imprese con meno di 100 addetti (4.340.464 unità), con studi di settore 67,2%. I numeri 18-19,3% e 55,5% **NOT FOUND**: il PDF indicato (`2020/03/Principali-risultati-nota-metodologica.pdf`) riguarda l'integrazione Frame SBS-ICT e non contiene quei dati. "700000" era un'etichetta d'asse nelle slide di Oropallo.
- **Quota delle società di capitali**: "Circa 800 mila bilanci associati alle imprese società di capitali di Asia (21% unità, 59% occupazione e 75% VA del Frame SBS)" (slide 9) — [Istat, Oropallo, Boselli, Causo, workshop 21/09/2015](https://www.istat.it/wp-content/uploads/2015/07/F.-Oropallo_C.-Boselli_M.S.-Causo.pdf). Nella stessa presentazione: ASIA "4,4 milioni di unità statistiche (circa la metà del VA nazionale ai prezzi base)" (slide 6), con periodo di riferimento del panel 2001-2012 (slide 5). **NUOVO**: è il dato chiave per il "tetto" di copertura di Orbis in Italia.
- Forme giuridiche escluse (Istat, Sanzo 2022, slide 7): le imprese individuali, "pur rappresentando circa il 37% dell'universo di riferimento, rappresentano meno del 6-7% in termini di valore aggiunto"; le società di persone, "pur rappresentando nel sistema italiano circa il 18-20% in termini di unità, rappresenta solo il 6-9% in termini di valore aggiunto" — [Istat, Sanzo, Frame anticipato](https://www.istat.it/it/files//2022/11/Sanzo_La-Metodologia-del-Frame-Anticipato.pdf). Verdetto sulla nota precedente ("società di persone circa 20% unità e circa 9% VA", attribuita a Monducci): **CORRECTED** nell'attribuzione e nella forbice, perché la fonte è Sanzo (2022) con 18-20% e 6-9%.
- Tabella di Sanzo (slide 6, anno 2020): le società di capitali sono 622.118 unità in Asia Anticipato; i "Bilanci provvisori" ne coprono il **62,73%** delle unità (65,37% dei dipendenti, 62,52% del VA). Verdetto: **CORRECTED** nell'interpretazione. È la copertura dei bilanci *provvisori* disponibili a 10 mesi, non la copertura definitiva. Inoltre Asia Anticipato comprende solo le unità con dipendenti ("35-36% delle unità presenti nel Frame SBS", slide 7).
- Monducci (1/12/2014, slide 5, dati 2012): "Le imprese con dipendenti realizzano 609 mld di valore aggiunto (l'88,3% del totale). Le imprese con un solo addetto (2,4 mln di unità) producono 70 mld di valore aggiunto (il 10% del totale)" — [Istat, Monducci](https://www.istat.it/it/files//2014/11/Monducci-Aumento-di-qualità-dei-dati-economici.pdf). **CONFIRMED** il "10%"; il dato sulle società di persone non è in questa fonte.
- Report 2014 (p. 8 = PDF p. 9): "le imprese appartenenti a gruppi generano oltre 376 miliardi di valore aggiunto, il 54,7% del totale delle imprese dell'industria e dei servizi e il 70% del valore aggiunto delle società di capitali (374 miliardi)". Il VA totale 2014 è "circa 688 miliardi di euro" (p. 1). La nota 6 precisa che "società di capitali" comprende Spa, Srl, Sapa, cooperative, consorzi, branch estere, enti pubblici economici e aziende speciali — [Istat, Risultati economici delle imprese 2014](https://www.istat.it/it/files//2016/10/Report-Risultati-economici-imprese-2014.pdf). **CONFIRMED.** Ne segue una quota delle società di capitali sul VA di circa 76-78% (54,7/0,70), coerente con il 75% di Oropallo per il 2012.
- 2022: le imprese in gruppi generano "il 66,7% del fatturato totale e il 57,3% del valore aggiunto" (p. 1) — [Istat, Conti economici imprese e gruppi 2022](https://www.istat.it/wp-content/uploads/2024/10/Report-Conti-economici-imprese-e-gruppi-2022.pdf). **CONFIRMED** (altri numeri 2021-2022 della nota precedente **NOT CHECKED**).
- Panel Istat bilanci: "copre annualmente circa il 12% della popolazione del Registro Asia. Esso rappresenta l'86% delle società di capitali con dipendenti e il 90% della relativa occupazione" — [Istat, Panel bilanci società di capitali con dipendenti 2001-2012](https://www.istat.it/microdati-integrati/panel-bilanci-societa-di-capitali-con-dipendenti-anni-2001-2012/). **CONFIRMED.**

**Chi deposita il bilancio (fonte BvD citata da Kalemli-Özcan et al.)**
- Tabella A.6.1, riga IT: sono soggette S.p.A., S.r.l., Sapa, società cooperative, società consortili, "G.e.i.e, Società di persone (only consolidated accounts)", consorzi con qualifica di Confidi, e Srl e Spa a socio unico; "Approximately 900,000". Fonte delle regole: "Orbis Online Manual on February 3d, 2014" (Appendice A.6, p. 40 = PDF p. 41) — [Kalemli-Özcan et al., NBER WP 21558 rev. dic. 2019](https://www.nber.org/system/files/working_papers/w21558/revisions/w21558.rev1.pdf)

**Bilancio abbreviato e micro-imprese (testo vigente del codice civile)**
- Art. 2435-bis, soglie vigenti: "1) totale dell'attivo dello stato patrimoniale: 5.500.000 euro; 2) ricavi delle vendite e delle prestazioni: 11.000.000 euro; 3) dipendenti occupati in media durante l'esercizio: 50 unità". Le soglie sono state modificate dal D.Lgs. 125/2024; le precedenti erano 4,4 e 8,8 milioni — [Brocardi, art. 2435-bis c.c.](https://www.brocardi.it/codice-civile/libro-quinto/titolo-v/capo-v/sezione-ix/art2435bis.html). Verdetto: **CORRECTED** (la nota precedente riportava solo le soglie pre-2024 come se fossero vigenti).
- **Conto economico abbreviato**, alla lettera: "le seguenti voci previste dall'articolo 2425 possono essere tra loro raggruppate: voci A2 e A3; voci B9(c), B9(d), B9(e); voci B10(a), B10(b), B10(c); voci C16(b) e C16(c); voci D18(a)...(d); voci D19(a)...(d)" (art. 2435-bis, c. 3). Stato patrimoniale: solo le voci con lettere maiuscole e numeri romani. Rendiconto finanziario: esonero. Verdetto sulla nota precedente ("le voci per materie prime e servizi possono essere raggruppate"): **CORRECTED**. B6 (materie prime) e B7 (servizi) **non** sono tra le voci raggruppabili; B9(a) salari e stipendi e B9(b) oneri sociali restano separati, e si accorpano solo TFR, quiescenza e altri costi (B9c-e).
- Nota integrativa abbreviata: deve comunque riportare l'art. 2427 n. 15, cioè il numero medio dei dipendenti, "anche omettendo la ripartizione per categoria" (art. 2435-bis).
- Art. 2435-ter, micro-imprese, soglie vigenti: "totale dell'attivo ...: 220.000 euro; ricavi ...: 440.000 euro; dipendenti occupati in media ...: 5 unità". Le micro sono esonerate dal rendiconto finanziario, "della nota integrativa quando in calce allo stato patrimoniale risultino le informazioni previste dal primo comma dell'articolo 2427, numeri 9) e 16)", e dalla relazione sulla gestione — [Brocardi, art. 2435-ter c.c.](https://www.brocardi.it/codice-civile/libro-quinto/titolo-v/capo-v/sezione-ix/art2435ter.html). **CONFIRMED** (le soglie 220/440 mila sono vigenti).

### Inferences
- Il **tetto teorico** di copertura di Orbis Historical per l'Italia è circa 21% delle imprese, 59% degli addetti e 75% del VA del perimetro Frame SBS (circa 2012). Ne seguono due indicazioni:
  - **Confronto corretto**: Orbis Italia va confrontato con il sottoinsieme Frame-SBS/ASIA delle *società di capitali*, o in alternativa con le imprese ≥10 addetti, non con l'universo.
  - **Rapporti attesi**: Orbis/totale SBS intorno al 60% per gli addetti (Bajgar, Fig. 3.1) è vicino al tetto del 59%, cioè una copertura quasi completa delle società di capitali con addetti noti.
- Le variabili di conto economico italiane sono strutturalmente disponibili anche per le società in forma abbreviata: B6, B7 e B9 totale esistono nello schema. Il materials cost e il costo del personale dovrebbero quindi essere presenti per quasi tutte le società di capitali con bilancio depositato. Le lacune di "employees" dipendono invece dalla fonte del dato (nota integrativa, assente per le micro; oppure stime INPS/InfoCamere). Quest'ultimo punto della nota precedente resta da fonti secondarie, **NOT CHECKED**.

### Gaps
- Non ho trovato una tavola Istat recente (2018-2022) con la ripartizione per forma giuridica di unità, addetti e VA da usare come denominatore anno per anno: va estratta dal datawarehouse Istat (Frame-SBS per forma giuridica).
- Non ho trovato statistiche ufficiali sulla quota di bilanci abbreviati o micro sul totale dei depositi.

---

## KQ5. CompNet sull'Italia; regole di pulizia di Díez-Fan-Villegas-Sánchez (IMF WP 19/82); copertura italiana di Orbis per anno

### Takeaway
I numeri di copertura italiana per anno verificati vengono da Kalemli-Özcan et al.:
- **manifattura, output lordo vs Eurostat-SBS** (AEJ 2024): 0,65 nel 2001 → 0,89 nel 2011 (media 0,79);
- **economia aggregata, output lordo** (NBER rev. 2019): 0,45 nel 1999 → 0,71 nel 2011 (media 0,59);
- **manifattura, monte salari** (slide NBER luglio 2015): 0,59 nel 1999 → 0,86 nel 2011.

CompNet (6° vintage, 2011) copre solo l'11% delle imprese italiane e il 39% degli addetti rispetto a Eurostat. Díez et al. (2019) usano Orbis Historical con l'Italia nel campione base 2000-2015, una soglia di copertura paese ≥40% dell'output ufficiale e imprese con almeno 20 addetti medi.

### Cited Findings
**Kalemli-Özcan, Sørensen, Villegas-Sanchez, Volosovych, Yeşiltaş**
- **AEJ: Macro 16(2), 2024, Tabella 1 (p. 7), "Coverage of the Manufacturing Sector Based on Gross Output"**, Italia 2001-2012: 0,65; 0,71; 0,70; 0,73; 0,77; 0,79; 0,79; 0,90; 0,86; 0,87; 0,89; 0,86; media 0,79.
  - Confronti (medie): DE 0,63 (0,50 nel 2001, 0,90 nel 2005, 0,48 nel 2012); ES 0,82; FR 0,87; GB 0,72; FI 0,44.
  - Testo: "With the exception of Finland, most countries show close to or above 60 percent coverage ratios, especially since 2001" (p. 6). Distribuzione dimensionale: "Italy and Slovenia with a slight underrepresentation of small firms" (p. 7).
  - Tabella 2 (p. 8): copertura UE-wide della manifattura 0,65 (2001), 0,79 (2005), 0,76 (2011) — [AEJ PDF](https://sebnemkalemliozcan.com/assets/publications/AEJMacro-2022-0036.pdf)
- **NBER WP 21558 rev. dicembre 2019, Tabella 1 (p. 7 = PDF p. 8), "Coverage of the Aggregate Economy Based on Gross Output"**, Italia 1999-2012: 0,45; 0,50; 0,50; 0,54; 0,53; 0,57; 0,57; 0,58; 0,60; 0,72; 0,68; 0,64; 0,71; 0,61; media 0,59. Germania: 0,29 (1999) → 0,81 (2005) → 0,47 (2012), media 0,60. Spagna: media 0,72. Francia: media 0,70 — [rev1](https://www.nber.org/system/files/working_papers/w21558/revisions/w21558.rev1.pdf)
- **Slide "Firm Level Data from ORBIS/AMADEUS Database", NBER Data Group, luglio 2015, "Coverage Relative to Eurostat (Manufacturing Wage Bill)"** (slide 2), Italia: 1999 0,59; 2000 0,63; 2001 0,62; 2002 0,69; 2003 0,68; 2004 0,71; 2005 0,72; 2006 0,73; 2007 0,73; 2008 0,84; 2009 0,81; 2010 0,83; 2011 0,86; 2012 0,85. Spagna 0,69-0,75; Francia 0,70-0,75; **Germania 0,34 (2006-2007) → 0,25 (2012)**, serie che parte dal 2006 — [Slide Kalemli-Özcan](https://data.nber.org/international-finance//Sebnem.pdf)
  - Verdetti sulla nota precedente:
    - "Italia 0,59 (1999) → 0,86 (2011) monte salari manifatturiero": **CONFIRMED** nei numeri, ma **CORRECTED** nella fonte (slide 2015, non rev1).
    - "Germania circa 0,28-0,34 nei primi anni 2000": **CORRECTED**. Nelle slide sono gli anni 2006-2012; nelle tabelle a output lordo la Germania nei primi anni 2000 è 0,29-0,58 (aggregato) e 0,50-0,65 (manifattura).
    - "Italia 0,62-0,73 nel 2000-2005": **CONFIRMED** con precisazione: 0,62-0,72 nel 2000-2005 e 0,73 nel 2006-2007.
- Pre-1999: "Data go further back in time in Orbis but the coverage is not good as the regulations for filing changed in 1999 requiring all firms to file with the registries if they are located in a EU country" (nota 8, rev1 p. 5 = PDF p. 6). **CONFIRMED** come affermazione degli autori (fonte: rev1, non le slide). Non ho verificato il fondamento giuridico per l'Italia.
- Ritardo e finestre:
  - "a reporting lag in the BvD products of roughly two years, meaning that a firm's filing in 2017 will appear fully on the media issued/accessed in 2019" (nota 4, rev1 p. 4 = PDF p. 5);
  - "Orbis de facto reports only the most recent 5 years of a given company, with a reporting lag of 1–2 years" (rev1, PDF p. 28);
  - slide 11: "AMADEUS provide most recent 10 years ... ORBIS provides 5 most recent years"; "AMADEUS drops the firm if firm did not report anything in the last 5 years where ORBIS keeps the firm as long as firm is active".

  **CONFIRMED.**
- Anno contabile: "If the closing date is after or on June 1st, the current year is assigned ... Otherwise, the previous year is assigned" (rev1 p. 32 = PDF p. 33). **CONFIRMED.**
- Regola C1 specifica per l'Italia: "in cases where we use the Total Sample, we drop C1 accounts for all countries except Spain and Italy. In the cases where we use the TFP Sample, we drop C1 accounts for all countries except Spain, Italy, Cyprus, Denmark, the UK, Greece, Ireland, and Lithuania" (rev1 p. 70 = PDF p. 71). **NUOVO.** Conteggi 2006 per la manifattura italiana: 111.200 imprese con conti non consolidati, 803 con consolidati (rev1 p. 9 = PDF p. 10).
- Orbis Historical vs procedura manuale: "It is reassuring that the coverage ratios from our 'manual procedure' and those from Orbis Historical Product are similar (Diez, Fan, and Villegas-Sanchez 2021 and Gourinchas et al. 2020 use Orbis Historical, follow our cleaning procedure ...)" (AEJ p. 6).

**Díez, Fan, Villegas-Sánchez (2019), IMF WP 19/82, letto dalla copia Wayback** ([link](https://web.archive.org/web/2020/https://www.imf.org/-/media/Files/Publications/WP/2019/WPIEA2019082.ashx))
- Fonte e campione: "Our data were obtained through the 'Orbis Historical' product that provides the longest available coverage" (p. 11 = PDF p. 12). Campione base: 20 paesi, Italia inclusa, "2000-2015"; campione alternativo di 28 paesi per il 2004-2013 (Tab. 1, p. 13).
- **Soglie**: "we focus on the sample of firms with average employment greater or equal to 20 employees"; "we initially selected the set of countries for which aggregate Orbis data represented at least 40% of the total output reported in official sources" (nota 17, p. 12).
- **Duplicati (App. A.1, p. 35 = PDF p. 36), alla lettera**: "(1) We kept company accounts that are unconsolidated (U1 or U2 in Orbis) or unknown (LF, stands for limited financials). (2) We removed accounts that are duplicates and not 'annual report' types. (3) We removed accounts that are duplicates for firms reporting data that refers to less than 12 months of operations. (4) We kept accounts that are duplicates but have the closest reporting date to Dec. 31st in the corresponding year. (5) If there were still duplicates found, we kept those accounts that have more non-missing variables to calculate TFP."
  - Verdetto sulla nota precedente ("priorità a unconsolidated per chi riporta continuativamente unconsolidated, a consolidated per chi riporta consolidated"): **NOT FOUND** nel WP 19/82. Probabilmente viene dalla versione JIE 2021, non letta.
- **Pulizia (App. A.2, pp. 35-37)**:
  - eliminazione dell'impresa con totale attivo, addetti, vendite o immobilizzazioni materiali negativi in qualsiasi anno, o con più di 2 milioni di addetti;
  - eliminazione delle osservazioni con materials cost, operating revenue o total assets mancanti, nulli o negativi;
  - eliminazione delle imprese senza codice NACE;
  - trimming 0,1% in alto e in basso di addetti per milione di attivo, di ricavi e di ricavi/attivo;
  - età non positiva;
  - passività non positive; due misure di passività con rapporto >1,1 o <0,9;
  - immobilizzazioni immateriali negative; immobilizzazioni nulle o negative;
  - costo del personale e addetti mancanti, o costo del personale non positivo;
  - valori negativi di passività correnti e non correnti, attivo circolante, prestiti, creditori, patrimonio netto, valore aggiunto, ammortamenti;
  - rapporto debiti bancari a breve/lungo >1,1;
  - trimming 0,1% di sei rapporti;
  - **filtri di crescita annua degli addetti**: >1000% (0-10 addetti), >500% (11-20), >300% (21-50), >200% (50-100), >100% (100+); soglie doppie per vendite e ricavi; per le imprese senza addetti ritardati, crescita dei ricavi >2000%.

  **CONFIRMED** le regole già elencate nella nota precedente; il resto è **NUOVO** e più esteso.
- Verdetto su "Spagna: Eurostat-SBS fornisce dettaglio solo per il 41% dell'output": **NOT FOUND** nel WP 19/82.

**CompNet**
- Rapporto "Assessing the reliability of the CompNet micro-aggregated dataset" (CompNet 2018; working group presieduto da Marc Melitz; fornitore italiano: Filippo Oropallo, ISTAT, p. 2): "CompNet covers about 58% of the corresponding population of firms although with large cross-country variation, ranging from 11% of firms in Italy to about 90% in Slovakia" (§4.1, p. 43).
  - Tab. 14, Italia (anno 2011): **occupazione 39%, numero di imprese 11%** (p. 43).
  - Tab. 15, copertura degli addetti per macro-settore, Italia: manifattura 60,7%, costruzioni 35,3%, servizi 53,6% (p. 44).
  - Ri-pesatura: "inverse probability weights: using data available from Eurostat, the number of firms in a given size class and NACE Rev. 2 macro-sector is gathered ... This reweighing procedure hinges on the assumption that there is no selection into reporting within these bins" (pp. 45-46) — [CompNet Cross-Country Comparability Report](https://www.comp-net.org/fileadmin/_compnet/user_upload/Documents/Cross-Country_Comparability_Report.pdf).

  **CONFIRMED** l'11%; il fornitore è Istat. **CORRECTED** la frase sulle "imprese con più di 20 addetti pesate": il rapporto descrive pesi per classe dimensionale × macro-settore basati su Eurostat.
- 8th Vintage User Guide (31/10/2023): Italia coperta "2006–2018" sia nel campione completo sia in quello 20e (p. 9). Popolazione target: "non-financial corporations with at least one employee ... (excluding sole proprietors)" (p. 9). Pesi: "inverse probability weighting within the strata" (p. 15); "variables ending on '_sw', standing for 'summed_weights'" per riportare le statistiche ai totali di popolazione (p. 30). Outlier: "we eliminate capital, turnover, intermediate input expenditure, labour cost, and labour values for the top two and bottom three percent values in the distribution of the ratios" (p. 98) — [CompNet 8th Vintage User Guide](https://www.comp-net.org/fileadmin/_compnet/user_upload/2023-10-31%208th%20Vintage%20User%20Guide%20Final.pdf). Verdetti:
  - "Italia 2006-2018": **CONFIRMED**.
  - "pesi compresi tra 1 e 6": **NOT FOUND**.
  - "fonti italiane: Chamber of Commerce + Istat": **NOT FOUND**. La Tabella 20 (p. 101), nella riga Italia, riporta in estrazione solo "microBACH ... ECCBSO", probabilmente per un errore di impaginazione.
  - "top/bottom 1% nel rapporto con capitale/lavoro": **CORRECTED**, perché nel testo letto la regola è "top two and bottom three percent" (p. 98).

**Altri studi per anno**
- Guntin e Kochen (online appendix): "The firms in our sample represent 54% of aggregate revenue in 1995 and 92% by 2018. On average, across all years, Orbis Historical covers 78% of total revenue" (Spagna, vs OECD STAN) — [GK Online Appendix](https://www.rguntin.com/research/GK_TopFirms_OnlineAppendix.pdf). **CONFIRMED.**

### Inferences
- **Serie italiana di riferimento** per la copertura di Orbis/Amadeus:
  - manifattura: circa 0,6-0,7 nel 1999-2003, circa 0,75-0,80 nel 2004-2007, circa 0,85-0,90 nel 2008-2012;
  - economia aggregata: circa 0,45-0,55 prima del 2004, circa 0,6-0,7 dopo il 2008.

  Il salto del 2008 compare in tutte e tre le serie.
- Non ho trovato serie verificate per l'Italia dopo il 2015 (fino al 2020) basate su Orbis Historical. Bajgar et al. arrivano al 2015 con un vintage 2017; Kalemli-Özcan et al. al 2012.

### Gaps
- Copertura italiana 2013-2023 in Orbis Historical: nessuna fonte primaria letta. Va calcolata direttamente sulla consegna di dicembre 2025, confrontandola con Eurostat SBS (`sbs_ovw_act`, `sbs_sc_ovw`) e con Istat Frame-SBS.
- Il "Processing Orbis Historical Disk" e il Data Description 2015 non sono stati riletti in questa sessione. Il "75-80%" della versione 2015 resta **NOT CHECKED**.

---

## KQ6. Quale soglia di copertura usano gli autori per dichiarare utilizzabile un paese-anno?

### Takeaway
Non esiste una soglia unica. Le regole esplicite verificate sono:
- Bajgar et al.: almeno 5000 imprese con VA per paese-anno, oppure periodi continui con copertura (numero di imprese vs popolazione) superiore a circa il 20% e stabile; in più la soglia ≥10 addetti.
- Díez et al.: output Orbis aggregato almeno pari al 40% dell'output ufficiale, imprese con ≥20 addetti medi.
- QEF 308: oltre il 50% del numero di imprese Eurostat per classe dimensionale (criterio descrittivo).
- Kalemli-Özcan et al.: "close to or above 60 percent" dell'output manifatturiero (descrittivo, nessun cut-off formale).
- Gal: cautela quando i pesi di ricampionamento sono alti, tipicamente fino al 2004.

### Cited Findings
- "5000+": "country-years with at least 5000 observations for which value added is available"; "hand-picked": "continuous country-periods with coverage that is north of 20% and reasonably stable over time". Avvertenza: "blindly applying a simple rule such as the 5000 threshold may keep in countries for which the included period is very short or has gaps" (pp. 35, 37) — [Bajgar et al. 2020](https://www.oecd.org/content/dam/oecd/en/publications/reports/2020/05/coverage-and-representativeness-of-orbis-data_9628c322/c7bdaa03-en.pdf)
- "at least 40% of the total output reported in official sources"; soglia di 20 addetti medi (nota 17, p. 12) — [Díez et al. 2019, WP 19/82](https://web.archive.org/web/2020/https://www.imf.org/-/media/Files/Publications/WP/2019/WPIEA2019082.ashx)
- "green cells identify size classes in each country where the estimated coverage of the Orbis dataset is above 50 per cent" (Tab. A8, p. 32) — [QEF 308](https://www.bancaditalia.it/pubblicazioni/qef/2016-0308/QEF_308_16.pdf)
- "most countries show close to or above 60 percent coverage ratios, especially since 2001" (p. 6) — [AEJ 2024](https://sebnemkalemliozcan.com/assets/publications/AEJMacro-2022-0036.pdf); nel rev1: "our data account for more than 50 percent of the aggregate output in all countries and close to 80-90 percent in most countries" (p. 6 = PDF p. 7) — [rev1](https://www.nber.org/system/files/working_papers/w21558/revisions/w21558.rev1.pdf)
- "in cases where resampling weights are high, typically, in the early years (up to 2004) ... results need to be treated with more caution" (p. 38) — [Gal 2013](https://www.oecd.org/content/dam/oecd/en/publications/reports/2013/05/measuring-total-factor-productivity-at-the-firm-level-using-oecd-orbis_g17a22d0/5k46dsb25ls6-en.pdf)

### Inferences
- Una regola operativa difendibile per Orbis Historical, sintesi mia e non di un singolo autore, richiede che un paese-anno soddisfi tre condizioni:
  - (a) output o ricavi Orbis (U1/U2/LF, deduplicati) almeno pari al 40-60% dell'output SBS, con la manifattura come controllo;
  - (b) almeno 5000 imprese con le variabili richieste (VA o costo del personale + EBITDA);
  - (c) per le imprese con almeno 10 addetti, copertura in numero di imprese superiore al 20% e senza salti superiori a circa 10 p.p. da un anno all'altro.
- Per l'Italia queste condizioni risultano soddisfatte: dal 2002 in Bajgar et al. (hand-picked 2002-2015), dal 2001 nella manifattura in Kalemli-Özcan et al. (0,65 o più) e dal 2000 in Díez et al. Il 1999-2001 è marginale nell'economia aggregata (0,45-0,50).

### Gaps
- Nessuna fonte giustifica statisticamente una soglia specifica: sono tutte scelte pragmatiche.

---

## KQ7. Riepilogo dei verdetti sulle affermazioni precedenti (snippet-based)

### Takeaway
Sul complesso delle affermazioni numeriche controllate: le cifre di Bajgar et al., Gal, QEF 308, Istat (gruppi 2014, panel 86/90%), CompNet 11% e Guntin-Kochen sono **confermate**. Vanno corrette:
- l'attribuzione e gli anni dei numeri di Kalemli-Özcan;
- le quote Frame-SBS (16,2% delle unità <100 addetti, non "16%/700 mila");
- la quota delle società di capitali, ora verificata: 21% unità, 59% addetti, 75% VA;
- la regola sul bilancio abbreviato: B6 e B7 non sono raggruppabili;
- le soglie dell'abbreviato, ora 5,5 e 11 milioni;
- la regola di consolidamento attribuita a Díez et al.;
- l'attribuzione di una frase a ECB WP 2651.

### Cited Findings

| # | Affermazione precedente | Verdetto | Fonte verificata (pagina) |
|---|---|---|---|
| 1 | Bajgar: circa 60% occupazione/output, circa 40% VA | CONFIRMED | Bajgar p. 17, Fig. 3.1 p. 18 |
| 2 | Bajgar: 20 paesi, 2002-2015, vintage 2017 | CONFIRMED (vintage feb. 2017) | pp. 11-12 |
| 3 | Bajgar: "≥10 addetti per la maggior parte dei paesi; DEU ≥20; JPN solo manifattura" | CORRECTED: MultiProd ≥1 dipendente; ≥10 solo AUT e NLD; DEU ≥20; JPN manifattura | p. 13 |
| 4 | Bajgar: output mancante per molte imprese in BEL, NLD, AUT, DNK, ITA, DEU | CONFIRMED | p. 21 |
| 5 | Bajgar: rounding → ricavi e addetti a missing | CONFIRMED; l'Italia ha un problema "smaller, but non-negligible" | pp. 11, 49 |
| 6 | Bajgar: tre passi = periodi stabili, meno di 10 paesi, imputazione VA | CORRECTED: periodi stabili e alti nei paesi meglio coperti + VA imputato + ≥10 addetti | p. 9, p. 54 |
| 7 | Bajgar: "copertura da oltre il 50% delle imprese a pochissime osservazioni" | CONFIRMED | p. 7 |
| 8 | Bajgar: il re-weighting non funziona | CONFIRMED | pp. 41-42 |
| 9 | Gal: pesi SDBS per paese × industria × classe × anno, esempio 1,3 | CONFIRMED (formula esatta) | Gal pp. 10-12 |
| 10 | Gal: 18 paesi OCSE | CONFIRMED (abstract) | p. 2 (PDF 3) |
| 11 | Kalemli: Italia monte salari manifatturiero 0,59 (1999) → 0,86 (2011) | CONFIRMED nei numeri; CORRECTED nella fonte (slide luglio 2015, non rev1) | Slide p. 2 |
| 12 | Kalemli: DEU 0,28-0,34 nei primi anni 2000; ES/FR 0,70-0,75; IT 0,62-0,73 | DEU CORRECTED (2006-2012, monte salari); ES/FR/IT CONFIRMED | Slide p. 2; AEJ Tab. 1 p. 7; rev1 Tab. 1 |
| 13 | Kalemli: circa 60% di output manifatturiero, specie dal 2001 | CONFIRMED | AEJ p. 6 |
| 14 | Kalemli: regole di deposito cambiate nel 1999 | CONFIRMED (rev1, nota 8) | rev1 p. 5 |
| 15 | Kalemli: Orbis "de facto" 5 anni; lag di circa 2 anni | CONFIRMED | rev1 PDF p. 5, 28; slide 11 |
| 16 | Kalemli: 75-80% dell'attività Eurostat (Data Description 2015) | NOT CHECKED | — |
| 17 | Díez: U1/U2/LF; drop negativi; >2 mln addetti; passività 0,9-1,1 | CONFIRMED | WP 19/82 App. A, pp. 35-37 |
| 18 | Díez: priorità per continuità consolidated/unconsolidated | NOT FOUND nel WP 19/82 (probabilmente JIE 2021) | App. A.1 |
| 19 | Díez: Spagna, SBS solo 41% dell'output | NOT FOUND nel WP 19/82 | — |
| 20 | QEF 308: Cerved "virtually all" + circa 40% di imprese con debito totale ma non finanziario | CONFIRMED | QEF 308 p. 9 nota 10; p. 34 |
| 21 | QEF 308: copertura Cerved più alta per le classi maggiori | CONFIRMED + numeri: 15% / 33% / circa 99% | QEF 308 p. 18 nota 22 |
| 22 | Istat Frame-SBS: 16% delle unità (700 mila) da bilanci; 18-19,3% e 55,5% | CORRECTED: 16,2% delle imprese <100 addetti (4.340.464); studi di settore 67,2%; 18-19,3% e 55,5% NOT FOUND | Nota metodologica p. 1 |
| 23 | Società di persone circa 20% unità e circa 9% VA (Monducci) | CORRECTED: 18-20% unità, 6-9% VA, fonte Sanzo 2022 | Sanzo slide 7 |
| 24 | Imprese con 1 addetto: 2,4 mln, 70 mld, 10% del VA | CONFIRMED (dati 2012) | Monducci slide 5 |
| 25 | Società di capitali 622.118, copertura 62,73% | CORRECTED nell'interpretazione: copertura dei bilanci *provvisori*, anno 2020 | Sanzo slide 6 |
| 26 | Istat 2014: gruppi 54,7% del VA = 70% del VA delle società di capitali | CONFIRMED | Report 2014 p. 8 |
| 27 | Inferenza: società di capitali circa 78% del VA | CONFIRMED in ordine di grandezza: 75% (2012, Oropallo); circa 77-78% (2014, derivato) | Oropallo slide 9 |
| 28 | Panel Istat: 86% società con dipendenti, 90% occupazione, 12% di ASIA | CONFIRMED | Pagina Istat panel |
| 29 | Abbreviato: soglie 4,4/8,8 mln/50 | CORRECTED: vigenti 5,5/11 mln/50 (D.Lgs. 125/2024) | art. 2435-bis |
| 30 | Abbreviato: materie prime e servizi raggruppabili | CORRECTED: non raggruppabili; raggruppabili solo A2-A3, B9c-e, B10a-c, C16b-c, D18, D19 | art. 2435-bis c. 3 |
| 31 | Micro: 220/440 mila, 5 dipendenti, esonero nota integrativa | CONFIRMED | art. 2435-ter |
| 32 | CompNet: circa 11% delle imprese italiane, fornitore Istat | CONFIRMED (2011; occupazione 39%) | CCR p. 43 |
| 33 | CompNet 8th: Italia 2006-2018 | CONFIRMED | Guide p. 9 |
| 34 | CompNet 8th: pesi tra 1 e 6; fonti Chamber of Commerce + Istat | NOT FOUND | Guide |
| 35 | CompNet 8th: outlier top/bottom 1% | CORRECTED: "top two and bottom three percent" dei rapporti | Guide p. 98 |
| 36 | Guntin-Kochen: Spagna 54% (1995) → 92% (2018), media 78% | CONFIRMED | GK appendix |
| 37 | ECB WP 2651: copertura Orbis verificata con SBS e CompNet | CORRECTED: il WP 2651 (Abbritti e Consolo, mercato del lavoro) non usa Orbis; attribuzione errata | ECB WP 2651 |
| 38 | JRC 121476: 80-90% dell'output Eurostat | NOT CHECKED (sito JRC bloccato) | — |
| 39 | ESRI/CE mid-cap, World Bank 10261, Arndt 2023, Ribeiro et al. 2010, guide di biblioteca | NOT CHECKED in questa sessione | — |

### Inferences
- **Implicazioni pratiche per la consegna Orbis Historical dicembre 2025 sull'Italia**:
  - **Anni**: anni affidabili dal 2002 circa (manifattura dal 2001); il 1999-2001 è utilizzabile con cautela; prima del 1999 la copertura è debole secondo gli autori.
  - **Discontinuità da controllare**: salti tra 2007 e 2008 (serie Kalemli) e calo nel 2010 (Bajgar).
  - **Perimetro**: lavorare sulle sole società di capitali con almeno 10 addetti, con VA imputato internamente (costo del personale + EBITDA), conti U1/U2 (C1 ammessi per l'Italia secondo Kalemli-Özcan) e deduplicazione per closing date e filing type.
  - **Benchmark**: Istat Frame-SBS per forma giuridica, non l'universo ASIA.
- Il problema italiano più serio non è la copertura per output o VA, che si avvicina al tetto del 75% del VA, ma la **disponibilità della variabile addetti**. Bajgar et al. mostrano coperture italiane in numero di imprese molto più alte senza il condizionamento sugli addetti (Fig. A.2) e un salto dopo il 2012. Va verificato quanto `employees` manca per anno nella consegna e se va imputato, ad esempio dal costo del personale diviso per il salario medio di settore.

### Gaps
- Le voci NOT CHECKED (16, 38, 39) richiedono una sessione dedicata o l'accesso ai siti bloccati (JRC, SSRN, imf.org diretto).
- Le letture grafiche di Bajgar et al. (Italia) potrebbero essere sostituite da numeri esatti solo chiedendo i dati agli autori (nota 16 del paper).
