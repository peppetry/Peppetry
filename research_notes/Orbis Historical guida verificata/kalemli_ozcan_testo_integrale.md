# Kalemli-Özcan, Sørensen, Villegas-Sanchez, Volosovych, Yeşiltaş: how the Orbis dataset is built and validated (checked against the full texts)

Documents read in full (pdftotext -layout, every page). Each has a short code used in the citations below:

- **[AEJ]**: published article, *AEJ: Macroeconomics* 16(2), April 2024, DOI 10.1257/mac.20220036. Copy hosted on the author's site: https://sebnemkalemliozcan.com/assets/publications/AEJMacro-2022-0036.pdf (22 pp., InDesign file dated 22 Feb 2024). The journal page numbers are 353–74. Pages are cited here by the printed page of this copy, where journal page = 352 + p.
- **[NBER22]**: NBER WP 21558, the version served now at https://www.nber.org/system/files/working_papers/w21558/w21558.pdf. The cover reads "September 2015, Revised January 2022" and the PDF was created on 26 Jan 2022. It has 127 pages: main text with appendices A.1–A.3 on printed pp. 2–30, then the online appendix bundled as appendix pp. 1–96. Main-text pages are cited by printed page. Appendix pages are cited as "appx p. N". The PDF page equals appx p. + 31.
- **[NBER15]** (rev0, Sept 2015, 110 pp.): https://www.nber.org/system/files/working_papers/w21558/revisions/w21558.rev0.pdf. **[NBER19]** (rev1, "Revised December 2019", 113 pp.): https://www.nber.org/system/files/working_papers/w21558/revisions/w21558.rev1.pdf. I only grepped these two to check the coverage tables. I did not read them in full.
- **[GUIDE]**: "Processing Orbis Historical Disk", by Kalemli-Ozcan, Jingting Fan and Veronika Penciakova, "in cooperation with Bureau van Dijk". It has 15 pages; PDF metadata give author V. Penciakova and a creation date of 16 Sep 2017. URL: https://www.sebnemkalemliozcan.com/assets/policy&blog/Processing%20Orbis%20Historical%20Disk%20FINAL.pdf
- **[APPX24]**: the 2024 AEA supplemental appendix, https://www.aeaweb.org/articles/materials/20572 (98 pp., created 26 Jun 2023). The coordinator has already summarised it. I used it only to check items (a)–(g) by grepping it.

## 1. Main text: sample, vintages, consolidation, duplicates, fiscal year, cleaning, and how coverage is computed

### Takeaway
The main text (AEJ 2024 and NBER 2022) says almost nothing about construction. It sends the reader to the online appendix for every rule. What it does say is a consolidation rule for the concentration application (footnote 19 in AEJ, footnote 15 in NBER22), a duplicate/switcher appendix, a country-selection rule (AEJ footnote 16, new in the published version), and validation Tables 1–4. Cleaning thresholds, vintages, the fiscal-year rule and the coverage method appear only in the appendix bundled with NBER22 (and in APPX24).

The **AEJ published Tables 1, 2, 4 and A.1 differ from NBER22**:
- The AEJ Table 1 averages cover 2001–2012. The NBER22 averages were copied from the 1999–2012 appendix table.
- AEJ Table 2 is about 8–10 points higher.
- Some country-year cells changed (GB, CZ, NO, SE and others).

### Cited Findings

**Countries and years**
- AEJ sample of 20 countries, with a stated selection rule: "We select the sample of countries that cover at least 50 percent of the output reported by official statistics for aggregate economy in all years over the period 2001–2012, namely Austria, Belgium, the Czech Republic, Germany, Estonia, Spain, Finland, France, the United Kingdom, Greece, Hungary, Italy, Latvia, Norway, Poland, Portugal, Romania, Sweden, Slovenia, and Slovakia" (AEJ p. 9, fn 16). This footnote is not in NBER22. — [AEJ](https://sebnemkalemliozcan.com/assets/publications/AEJMacro-2022-0036.pdf)
- The concentration application covers "the period 2001–2012" (AEJ p. 10; NBER22 p. 12). — [AEJ](https://sebnemkalemliozcan.com/assets/publications/AEJMacro-2022-0036.pdf)
- The appendix tables cover 27 countries over 1999–2012: "BvD provides firm-level information on gross output for all sectors of each European country starting 1999." Footnote 34 adds: "Data go further back in time in Orbis but the coverage is not good as the regulations for filing changed in 1999 requiring all firms to file with the registries if they are located in a EU country" (NBER22 appx p. 65). This is the only statement in these texts about which years are reliable. — [NBER22](https://www.nber.org/system/files/working_papers/w21558/w21558.pdf)
- Table C.2.1 gives "Year 1999-2012" for the Table 1 comparison (NBER22 appx p. 54), but the main-text Table 1 starts in 2001. — [NBER22](https://www.nber.org/system/files/working_papers/w21558/w21558.pdf)

**Vintages (only in the appendix bundled with NBER22)**
- "our download strategy (Method 2) for financials makes use of several vintages of BvD products: Orbis disk 2005, Orbis disk 2009, Orbis disk 2013, Amadeus online 2010 (from WRDS; accessed in May), and Amadeus disk 2014" (NBER22 appx p. 9). — [NBER22](https://www.nber.org/system/files/working_papers/w21558/w21558.pdf)
- Ownership is taken from annual Orbis disks issued as close as possible to the end of each year: "to obtain the ownership as of end of 2010, we use the Orbis disk issued in January 2011" (appx pp. 9–10). Ownership vintages are "bi-annual vintages of Amadeus Ownership since 2000 and annual vintages of Orbis Ownership since 2005" (appx p. 30). — [NBER22](https://www.nber.org/system/files/working_papers/w21558/w21558.pdf)
- The main text points to the Historical Product: "BvD has recently developed a new product, labeled the 'Historical Product,' which links several vintages/disks … as we have done 'manually.' … We provide the guide and programs to process this historical data at http://econweb.umd.edu/~kalemli/orbis.html" (AEJ p. 6; NBER22 p. 7).
- AEJ adds a sentence not in NBER22: "It is reassuring that the coverage ratios from our 'manual procedure' and those from Orbis Historical Product are similar (Diez, Fan, and Villegas-Sanchez 2021 and Gourinchas et al. 2020 use Orbis Historical, follow our cleaning procedure, and report coverage ratios…)" (AEJ p. 6). — [AEJ](https://sebnemkalemliozcan.com/assets/publications/AEJMacro-2022-0036.pdf)
- AEJ fn 12 is also new: "We have updated the comparison of three different data access methods: WRDS, Orbis Online, and Orbis Historical … Orbis Online is the most problematic due to firm attrition and download limitations. Meanwhile, WRDS provides information for the most recent eight years without download limitations, but still experiences firm attrition in the early years" (AEJ p. 5). — [AEJ](https://sebnemkalemliozcan.com/assets/publications/AEJMacro-2022-0036.pdf)
- In the NBER22 appendix the Historical solution is described as "still in the developing stage. Therefore, we focus on the steps required to work with the separate historic disks" (appx p. 2). — [NBER22](https://www.nber.org/system/files/working_papers/w21558/w21558.pdf)

**Consolidation codes: which ones are kept for which purpose. The documents contradict each other.**
1. *Concentration application (main text).* "To avoid double counting of sales, we eliminate duplicates based on BvD ID keeping the consolidated accounts when both consolidated and unconsolidated are reported (i.e., we drop the unconsolidated sales of headquarters)" (AEJ p. 10 fn 19; NBER22 p. 13 fn 15). The application uses three samples: all accounts, unconsolidated only, consolidated only (AEJ p. 10). — [AEJ](https://sebnemkalemliozcan.com/assets/publications/AEJMacro-2022-0036.pdf)
2. *Main-text Appendix A ("Dealing with Duplicates").*
   - Case 1 (same ID, different values): "we give priority to those with consolidated accounts."
   - Case 2 (same values): (i) unconsolidated if the firm always reports unconsolidated; (ii) consolidated if it always reports consolidated; (iii) if it reports both inconsistently, "we give priority to the consolidated code classification and reclassify the time series as consolidated" (AEJ pp. 17–18; NBER22 pp. 23–25).
   - The CONSCODE2 identifier is "a copy of the last letter of BvD Account Number", filled with "C" (C1/C2) or "U" (U1/U2). For LF accounts the letter is taken from the BvD Account Number (AEJ p. 17). — [AEJ](https://sebnemkalemliozcan.com/assets/publications/AEJMacro-2022-0036.pdf)
3. *Switchers.* "we decided to drop these firms to have a consistent time series" (AEJ p. 18, Appendix B). — [AEJ](https://sebnemkalemliozcan.com/assets/publications/AEJMacro-2022-0036.pdf)
4. *Online appendix bundled with NBER22: the opposite rule.*
   - "Whenever we need a unique company-year observation … For Case 1, we give preference to unconsolidated accounts to avoid double-counting." Case 2: "we either retain the accounts reporting the longer time series for a given company, or keep the unconsolidated account if it is reported the same number of years" (NBER22 appx pp. 78–79, D.4).
   - The Ford Otosan example: "we drop C1 account to avoid from double-counting" (appx p. 79).
   - Elsewhere: "We download both consolidated and unconsolidated accounts and, so far, use unconsolidated accounts in all of our applications" (appx p. 11, A.3.2).
   - D.4 also says: "We also check consolidation codes of duplicate accounts registered in 'Historical Product' and verify the accuracy of this procedure" (appx p. 79).
   - Duplicates are "607,839, constituting 0.24% of total observations". Mix of duplicate pairs: LF&U 62.52%, C1&U1 32.24% in the text but 33.25% in Fig. D.4.2 (appx pp. 78, 80). — [NBER22](https://www.nber.org/system/files/working_papers/w21558/w21558.pdf)
5. *Validation against Eurostat (C.2 step 8).* "we first drop C2 accounts to avoid double accounting … in cases where we use the Total Sample, we drop C1 accounts for all countries except Spain and Italy. In the cases where we use the TFP Sample, we drop C1 accounts for all countries except Spain, Italy, Cyprus, Denmark, the UK, Greece, Ireland, and Lithuania" (NBER22 appx pp. 52–53; the same wording is in APPX24 PDF p. 55). So in the Eurostat validation for **Italy and Spain, C1 accounts (consolidated, with no unconsolidated counterpart) are kept** alongside U1/U2. — [NBER22](https://www.nber.org/system/files/working_papers/w21558/w21558.pdf)

**Other duplicates and the fiscal-year rule (NBER22 appendix)**
- Year assignment: "If the closing date is after or on June 1st, the current year is assigned (if CLOSEDATE is 4th of August, 2003, the year is 2003). Otherwise, the previous year is assigned (if CLOSEDATE is 25th of May, 2003, the year is 2002)" (appx p. 15).
- ID-YEAR duplicates (quarterly/annual reports, change of closing month): "retain the data for the closing date closest conceptually to the end of year … we drop duplicates whose revenue are less than the maximum per firm-year. For example, in 2005 vintage, there are around 34 thousand duplicates like that out of over 18 million observations" (appx p. 15, fn 11).
- Same financial data but different industry: keep the first, which is the main industry (fn 13, appx p. 16).
- Across vintages: "retain only observations coming from the most recent vintage". Later vintages fill missing values, but "A non-missing value, however, will never be replaced with a missing" (appx p. 20). — [NBER22](https://www.nber.org/system/files/working_papers/w21558/w21558.pdf)

**Cleaning filters and thresholds (NBER22 appendix)**
- Per vintage (A.5.1):
  - drop records with only a name, or with a missing BvD ID or Account number;
  - drop ID-YEAR duplicates;
  - drop records with no financials;
  - drop records whose BvD-ID country prefix ≠ BvD country ISO code;
  - drop records with missing currency or missing closing date (appx pp. 14–17).
- UNITS check when merging (A.5.2): drop the whole firm if a switch in UNITS does not coincide with a "reasonable" move in total assets. The bounds are −99% and +19,800%. Effect: "about 3% of observations in the 2005 and 2009 Orbis vintages; less than 1% in the 2010 WRDS Amadeus vintage; and less than 0.5% in the 2014 Amadeus vintage" (appx pp. 17–18).
- Industry: NACE Rev. 1.1 is mapped to Rev. 2 by keeping the first Rev. 2 code in the Eurostat correspondence table (appx p. 19).
- After merging (A.5.3), in this order (appx pp. 20–22):
  1. keep major currencies and drop unreasonable ones;
  2. convert to **real 2005 USD**: convert to the official national currency, "deflate the series by the national GDP deflator with the 2005 base from the World Bank", then "divide by the exchange rate of the official currency to the U.S. dollar in the year 2005" (Compustat Global exchange rates; special handling for legacy euro-adopter currencies);
  3. drop firm-years with total assets, operating revenue, sales and employment all missing;
  4. drop the whole firm if total assets < 0 in any year;
  5. drop the whole firm if employment < 0 or > 2 million ("Walmart") in any year;
  6. drop the whole firm if sales < 0 (the filter is not applied to operating revenue; for Denmark it cannot be applied);
  7. drop the whole firm if employment per million of total assets > 99.9th percentile in any year;
  8. drop it if employment per million of sales > 99.9th percentile;
  9. drop it if sales/total assets > 99.9th percentile;
  10. drop it if tangible fixed assets < 0;
  11. fill static strings from lags and leads. — [NBER22](https://www.nber.org/system/files/working_papers/w21558/w21558.pdf)

**How coverage against Eurostat SBS and BD is computed (NBER22 appendix C.1–C.2 and Table C.2.1)**
- Variables: Orbis OPRE against SBS "V12110-Turnover" for gross output. Orbis EMPL against SBS V16110 for size distributions, and against BD for employment coverage. "We express these financial variables in real dollars 2005 base using original values in Eurostat SBS data (see Step 2 in Chapter A.5.3)" (appx p. 52; table at appx pp. 54–55).
- Which source when: number of enterprises and employment for "Total" or "Zero" use BD; gross output uses SBS; "For all other cases where we do comparison for SMEs, we always use the SBS data" (appx p. 49).
- BD comparison uses "AllminusZero" (Total minus self-employed), "since BvD excludes self-employed workers by construction". When comparing with BD, inactive firms are dropped using STATUS ("Inactive," "Dissolved," "In liquidation," "Bankruptcy") (appx pp. 51–52).
- Size classes: Orbis 1–19, 20–249, 250+ against SBS 0–19, 20–249, 250+ (appx p. 54).
- Sector overlap: NACE Rev. 2 Level 1. Orbis output is summed only over sectors "which have non-missing gross output in both Eurostat SBS and BvD data sets", per country-year (Table C.2.3). For size distributions a "hypothetical aggregate" economy is built from sectors with official size-class data (Table C.2.4, 2006) (appx pp. 50–51).
- Samples: "Total Sample" (positive EMPL and OPRE) and "TFP Sample" (positive EMPL or STAF, plus TFAS, OPRE and MATE) (appx p. 52).
- Winsorising: "we check distributions of the underlying economic activity measure within a given country-sector-year triplet and winsorize data if neccessary". The amount "varies between 0.01% and 0.5%" and the list of triplets is "available upon request" (appx p. 53, fn 32).
- Main text: "We proxy output by firm's operating revenue … ratio of the value of total output produced by firms in our sample relative to the value of total output from the official Eurostat-SBS data for the manufacturing sector" (AEJ p. 6). — [NBER22](https://www.nber.org/system/files/working_papers/w21558/w21558.pdf); [AEJ](https://sebnemkalemliozcan.com/assets/publications/AEJMacro-2022-0036.pdf)

**Headline numbers in the main text. AEJ values first; NBER22 in brackets where different.**
- **Table 1** (AEJ p. 7), manufacturing gross output coverage, 2001→2012:
  - **IT**: 0.65, 0.71, 0.70, 0.73, 0.77, 0.79, 0.79, 0.90, 0.86, 0.87, 0.89, 0.86. Average **0.79** [NBER22 average 0.77, same cells].
  - **DE**: 0.50, 0.51, 0.57, 0.65 [0.64], 0.90, 0.73, 0.77, 0.64, 0.60, 0.60, 0.57, 0.48. Average **0.63** [0.58].
  - **FR**: 0.79, 0.82, 0.79, 0.83, 0.82, 0.84, 0.87, 0.90, 0.89, 0.92, 0.96, 0.95. Average **0.87** [0.84].
  - **ES**: 0.78, 0.80, 0.79, 0.79, 0.78, 0.83, 0.81, 0.85, 0.87, 0.90, 0.85, 0.83. Average **0.82** [0.81].
  - FI is the low outlier at 0.36–0.51.
  - The NBER22 averages equal the 1999–2012 averages of appendix Table D.2.1. The AEJ averages are over 2001–2012 only (for AT, (0.47+…+0.76)/12 = 0.65).
  - Other cells changed between versions, for example GB 2001 = 0.60 in AEJ against 0.68 in NBER22; CZ 2006–2012 and NO/SE/RO/LV/SI also differ. — [AEJ](https://sebnemkalemliozcan.com/assets/publications/AEJMacro-2022-0036.pdf); [NBER22 p. 8](https://www.nber.org/system/files/working_papers/w21558/w21558.pdf)
- **Table 2** (AEJ p. 8), EU coverage in three versions: unweighted / GDP-weighted / EU-wide pooled.
  - AEJ: 2001 = 0.65/0.64/0.65; 2007 = 0.79/0.77/0.78; 2012 = 0.78/0.75/0.72.
  - NBER22 is much lower: 2001 = 0.56/0.58/0.57; 2007 = 0.76/0.71/0.71; 2012 = 0.68/0.65/0.62.
  - Both versions say in the introduction: "close to 60 percent of manufacturing output at the beginning of our sample and more than 70 percent at the end" (AEJ p. 2). — [AEJ](https://sebnemkalemliozcan.com/assets/publications/AEJMacro-2022-0036.pdf)
- **Table 3** (2006, manufacturing size distribution; identical in AEJ p. 8 and NBER22 p. 10).
  - IT gross output, Orbis / SBS: 1–19 = 0.12 / 0.20; 20–249 = 0.49 / 0.41; 250+ = 0.40 / 0.38.
  - IT employment, Orbis / SBS: 0.13 / 0.40; 0.55 / 0.38; 0.32 / 0.22.
  - DE gross output: 0.06/0.06; 0.23/0.22; 0.70/0.72. DE employment: 0.05/0.15; 0.32/0.32; 0.63/0.53.
  - FR gross output: 0.05/0.09; 0.23/0.27; 0.72/0.63. FR employment: 0.10/0.19; 0.34/0.34; 0.56/0.47.
  - ES gross output: 0.13/0.13; 0.40/0.38; 0.47/0.49. ES employment: 0.25/0.31; 0.49/0.43; 0.26/0.26. — [AEJ](https://sebnemkalemliozcan.com/assets/publications/AEJMacro-2022-0036.pdf)
- **Table 4** (2006, aggregate economy, Orbis only). AEJ IT gross output 0.18 / 0.40 / 0.42; IT employment 0.15 / 0.40 / 0.45 (AEJ p. 9). NBER22 has different values: IT gross output 0.21 / 0.44 / 0.35; IT employment 0.17 / 0.44 / 0.39 (NBER22 p. 11). — [AEJ](https://sebnemkalemliozcan.com/assets/publications/AEJMacro-2022-0036.pdf)
- **Table A.1** ("Missing" output in Eurostat, % of Orbis output in sectors missing from SBS / missing sector-size cells). AEJ: IT 13 / 56, DE 18 / 68, FR 9 / 65, ES 11 / 59 (AEJ p. 19). NBER22: IT 14 / 53, DE 26 / 66, FR 20 / 65, ES 16 / 57 (p. 26). In the text, Spain is "41 percent … leaving out 59 percent" in AEJ p. 8, against 43%/57% in NBER22 p. 11. — [AEJ](https://sebnemkalemliozcan.com/assets/publications/AEJMacro-2022-0036.pdf)
- Foreign-ownership validation: foreign share "at most 30 percent overall", and "in Germany or Italy is around 20 percent" (AEJ p. 3 fn 7). NBER22 appx Table B.3.3 (2003–2012, manufacturing) gives IT 21 (Orbis) against 19 (OECD), DE 22/28, FR 26/31, ES 39/32 (appx p. 46). — [NBER22](https://www.nber.org/system/files/working_papers/w21558/w21558.pdf)

### Inferences
- To check your own data against the authors' benchmarks, the applicable rules are the appendix validation rules: OPRE in real 2005 USD; manufacturing (NACE Rev. 2 C); drop C2 always; drop C1 except for IT and ES (Total Sample); light winsorising. The concentration rule (consolidated preferred) does not apply here.
- The rule used to make firm-years unique is internally contradictory across documents: the main text prefers consolidated, appendix D.4 prefers unconsolidated. This should be flagged in any replication.

### Gaps
- No main-text statement on the Historical Product vintage the authors' coverage ratios rest on. The tables come from the "manual" multi-vintage dataset (2005/2009/2013 Orbis disks, WRDS Amadeus 2010, Amadeus disk 2014), not from Orbis Historical.
- The list of winsorised triplets is "available upon request" and is not published.

## 2. The "Processing Orbis Historical Disk" guide and the replication package

### Takeaway
The guide (2017, Kalemli-Ozcan, Fan, Penciakova, with BvD) describes a December delivery on an external drive. Its financials folder contains exactly the "Industry - Global financials and ratios" / "- USD" / "- EUR" files, which match the user's `Industry-Global_financials_and_ratios-EUR.txt`. Everything is keyed on BVDID, with country taken from the first two letters of BVDID. The guide is about file handling, not cleaning: it gives no cleaning thresholds.

The openICPSR replication package (E187541V1) could not be read; it sits behind a Cloudflare 403. The AEA "Replication Package" link (materials/20573) contains only disclosure statements.

### Cited Findings
- Folder layout: "Financials Histo Dec SQL", "**Financials Histo Dec text**", "Orbis Dec text", "Ownership histo Dec SQL", "Ownership histo Dec text". Only the "text" folders are processed, because the SQL folders hold "the same information … in a different format (ie one that cannot be read into Stata)" (GUIDE p. 1). Size: "The historical disk is around 280 GB. We recommend using an 8 TB drive"; Stata MP 12+; 128 GB RAM workstation (GUIDE p. 1). — [GUIDE](https://www.sebnemkalemliozcan.com/assets/policy&blog/Processing%20Orbis%20Historical%20Disk%20FINAL.pdf)
- Financial files: "Financials Histo Dec text, which contains three files: 'Industry - Global financials and ratios', 'Industry - Global financials and ratios - USD', and 'Industry - Global financials and ratios - EUR'" (GUIDE p. 7).
  - "All three files have the same underlying data, but differ in reporting currency … In the case when EUR or USD is used, a time-varying exchange rate used to convert currency is also reported" (p. 8).
  - Scope: "all 'industrial firms' … Entities excluded from this data set are financial firms, such as banks or insurance companies" (p. 8).
  - The Orbis Dec text folder has 32 RAR files: 12 descriptive and 20 financial, which make 7 datasets. Files there with the same names as the Histo files differ in that "the files under Financials Histo Dec text are available for more financial years" (pp. 7–9). — [GUIDE](https://www.sebnemkalemliozcan.com/assets/policy&blog/Processing%20Orbis%20Historical%20Disk%20FINAL.pdf)
- Time coverage of the Historical financials: "the sample extends until 2016, with the earliest observation in the data set dates back to the 1970's … European countries, for example, are better covered since the mid to late 1990's; many other countries … do not have a significant coverage until around 2005-2007. Overall, for most countries, the sample expands over the period of 1995-2005, and becomes more or less a stable panel afterwards" (GUIDE p. 8). — [GUIDE](https://www.sebnemkalemliozcan.com/assets/policy&blog/Processing%20Orbis%20Historical%20Disk%20FINAL.pdf)
- Key and duplicates: "each observation is a firm BVDID-year observation … There are a small number of duplicates in terms of BVDID-year." The guide gives three reasons:
  1. "Some firms report both consolidated and unconsolidated accounting reports. Focusing on only on consolidated results (there is a variable indicating consolidation status) can significantly reduce the number of duplicates";
  2. a change of reporting month;
  3. two filing channels ("filing type": local registry against annual report), which can carry different values (GUIDE pp. 10–11). — [GUIDE](https://www.sebnemkalemliozcan.com/assets/policy&blog/Processing%20Orbis%20Historical%20Disk%20FINAL.pdf)
- Processing: the USD file is "around 200GB after converting to Stata data format". Split it with `chunky` into 10–20 pieces. "Correct the difference between the country of a firm, and the country code indicated by the first 2 digits of BVDID, using the table 'discrepancy'". Save by country, then append per country (GUIDE p. 11). For descriptive files, chunk to at most 2 GB, `import delimited`, force variables to string, split by the first two letters of BVDID, then append (pp. 5–6).
- The 12 descriptive files include All addresses, Contact info, Identifiers, Industry classifications (NACE Rev. 2 / NAICS 2012 / USSIC; core, primary, secondary), Legal info (status, legal form, incorporation date, entity type, size class, listed) and others (pp. 3–5).
- Ownership: Entities.txt plus Links_YEAR.txt. Relation types SHH, CTP, ISH, HQ, DUO/GUO 25/50/50C, GUO 25C. "For each country ISO code and each year 2007 through 2016", outputs are SHARE and SUB files "containing all the relevant ownership links between 2007 and the end of the sample period (2016)" (GUIDE pp. 12–15). — [GUIDE](https://www.sebnemkalemliozcan.com/assets/policy&blog/Processing%20Orbis%20Historical%20Disk%20FINAL.pdf)
- Authors' page (Wayback snapshot of 1 Dec 2023, http://econweb.umd.edu/~kalemli/orbis.html; the live URL returns 403). It has "Guide" and "Programs" links and the description "Processing Orbis Historical Disk, with Jingting Fan, and Veronika Penciakova, in cooperation with Bureau van Dijk. PDF". — [Wayback](https://web.archive.org/web/20231201130832id_/http://econweb.umd.edu/~kalemli/orbis.html)

### Inferences
- The guide describes a Dec-2016 / 2017 delivery. A December 2025 delivery will have more years and possibly renamed files: the user's file uses underscores, `Industry-Global_financials_and_ratios-EUR.txt`. The guide documents no column names or key list beyond BVDID and "a variable indicating consolidation status".
- Using the EUR file with its time-varying rate differs from the authors' real-2005-USD procedure, which converts from the original currency with the World Bank GDP deflator and the 2005 USD exchange rate. To replicate their ratios, start from the original-currency file, or undo the conversion with the reported rate.

### Gaps
- The "Programs" page (programs.html), i.e. the do-files, could not be fetched (Wayback connection reset). UNVERIFIED.
- openICPSR 187541 returned 403 (Cloudflare challenge) both via doi.org/10.3886/E187541V1 and directly. File list and README are UNVERIFIED.

## 3. Verdicts on statements (a)–(g)

### Takeaway
- (b), (c), (d), (e) are CONFIRMED, with nuances.
- (a) is CONTRADICTED by every version.
- (f) is CONFIRMED but only in APPX24 (it is not in the main text).
- (g) is only PARTIALLY confirmed, by the guide; the paper itself does not say it.

### Cited Findings
- **(a) "Italy manufacturing coverage rose from about 0.59 in 1999 to about 0.86 in 2011": CONTRADICTED.**
  - Every version gives IT manufacturing gross-output coverage (Total Sample) of **0.61 in 1999 and 0.89 in 2011**: NBER15 Table 6.5, NBER19 Table D.1.1, NBER22 appx Table D.2.1 (appx p. 70), and APPX24 Table D.2.1.
  - 0.86 is the value for 2009 and 2012. The main-text Table 1 starts at 0.65 in 2001 (AEJ p. 7).
  - Other IT series do not match either. TFP sample: 0.60 (1999) → 0.87 (2011). Aggregate economy: 0.45 → 0.71 in NBER22 Table D.1.4, and 0.56 → 0.88 in APPX24 Table D.1.1. — [NBER22](https://www.nber.org/system/files/working_papers/w21558/w21558.pdf); [NBER15](https://www.nber.org/system/files/working_papers/w21558/revisions/w21558.rev0.pdf); [AEJ](https://sebnemkalemliozcan.com/assets/publications/AEJMacro-2022-0036.pdf)
- **(b) "coverage of manufacturing gross output vs Eurostat SBS mostly 60%+ since 2001": CONFIRMED.** "With the exception of Finland, most countries show close to or above 60 percent coverage ratios, especially since 2001" (AEJ p. 6; NBER22 p. 8). — [AEJ](https://sebnemkalemliozcan.com/assets/publications/AEJMacro-2022-0036.pdf)
- **(c) "Orbis keeps firms while active in the business register; Amadeus deletes after 5 years without filings": CONFIRMED (appendix only).**
  - "Amadeus will delete a company from the database if the company did not report anything in the last 5 years, while Orbis will keep this company as long as the company is active in the business register" (NBER22 appx p. 4; same wording in APPX24 PDF p. 4).
  - Also: "Amadeus drops firms … if they did not report anything during the last 5 years while Orbis keeps the information … as long as companies are still in the business register" (appx p. 7).
  - The main text says only "certain companies are erased from the database if there is no reporting done for some time" (AEJ p. 5 fn 11) and "Orbis drops nonreporting firms from the database after a certain period of time" (AEJ p. 5). — [NBER22](https://www.nber.org/system/files/working_papers/w21558/w21558.pdf)
- **(d) "reporting lag of about 2 years": CONFIRMED.**
  - Main text: "there is a reporting lag in the BvD products of roughly two years, meaning that a firm's filing in 2017 will appear fully on the media issued/accessed in 2019" (AEJ p. 5 fn 11).
  - Appendix: "a reporting lag of about 2 years, on average … for the 2010 vintage, a company may not have the 2010 filings but the 2010 filings will appear in the 2012 vintage" (NBER22 appx p. 4); elsewhere "1–2 years" (appx p. 10). — [AEJ](https://sebnemkalemliozcan.com/assets/publications/AEJMacro-2022-0036.pdf)
- **(e) "keep consolidated accounts for some purpose" in the main text: CONFIRMED.**
  - "we eliminate duplicates based on BvD ID keeping the consolidated accounts when both consolidated and unconsolidated are reported" (AEJ p. 10 fn 19).
  - Main-text Appendix A, Case 1: "we give priority to those with consolidated accounts" (AEJ p. 18).
  - The purpose is the concentration/market-share application.
  - This conflicts with NBER22 appx D.4 ("For Case 1, we give preference to unconsolidated accounts", appx p. 78) and A.3.2 ("so far, use unconsolidated accounts in all of our applications", appx p. 11). — [AEJ](https://sebnemkalemliozcan.com/assets/publications/AEJMacro-2022-0036.pdf)
- **(f) "Table A.2.2 counts keep both consolidated and unconsolidated statements": CONFIRMED in APPX24 only.** "for completeness we keep two observations in a year for the firms which report both consolidated and unconsolidated accounts" (APPX24 PDF p. 11). The table is titled "Data coverage of the BvD products in various platforms, March 2023" (PDF p. 10). It does not exist in NBER22. — [APPX24](https://www.aeaweb.org/articles/materials/20572)
- **(g) "Orbis Historical financials back to 1995 / ownership to 2007": PARTIALLY CONFIRMED (guide only; NOT FOUND in the paper).**
  - Guide on financials: "earliest observation … dates back to the 1970's … for most countries, the sample expands over the period of 1995-2005" (GUIDE p. 8).
  - Guide on ownership: links are processed "for each year 2007 through 2016" (GUIDE p. 14).
  - The paper's only 1995 is Eurostat SBS ("Starting in 1995, the SBS data…", NBER22 appx p. 48). — [GUIDE](https://www.sebnemkalemliozcan.com/assets/policy&blog/Processing%20Orbis%20Historical%20Disk%20FINAL.pdf)

### Inferences
- Statement (a) may come from an approximate reading or from another source. Use 0.61 → 0.89 (Total Sample, appendix) or 0.65 (2001) → 0.89 (2011) (main text).

### Gaps
- I did not read NBER15 and NBER19 in full, so a stray 0.59/0.86 figure for Italy in their prose cannot be fully excluded. Their tables give 0.61 and 0.89.

## 4. Main-text statements on SME representativeness, on Italy, and on reliable years

### Takeaway
The main text says the Orbis size distribution in manufacturing (2006) is "very close" to SBS. Italy has "a slight underrepresentation of small firms", visible mostly in employment: 0.13 in Orbis against 0.40 in SBS for 1–19 employees. SMEs (20–249 employees) account for more than half of activity. The only statement about reliable years is the 1999 filing-regulation footnote in the appendix.

### Cited Findings
- "Some exceptions are Finland, the United Kingdom, and Slovakia with an underrepresentation of large firms; Greece with an overrepresentation of medium firms; and Italy and Slovenia with a slight underrepresentation of small firms" (AEJ p. 7; NBER22 p. 9). — [AEJ](https://sebnemkalemliozcan.com/assets/publications/AEJMacro-2022-0036.pdf)
- "SMEs, defined as firms with 20–250 employees (consistent with the Eurostat definition), account for more than half of aggregate employment and gross output in almost all our countries" (AEJ p. 2). "most of the gross output and employment are accounted for by SMEs in the entire economy" (AEJ p. 9). — [AEJ](https://sebnemkalemliozcan.com/assets/publications/AEJMacro-2022-0036.pdf)
- "Single-vintage data will often overrepresent larger firms and underrepresent smaller firms due to survivorship bias." AEJ adds: "Bajgar et al. (2020), using a single download from the 2017 vintage, find that Orbis is tilted toward larger, older, and more productive firms, even within each size class" (AEJ p. 5). — [AEJ](https://sebnemkalemliozcan.com/assets/publications/AEJMacro-2022-0036.pdf)
- "If our guidelines are followed, there is no need to reweigh the data" (AEJ p. 6).
- Italy elsewhere in the main text: foreign-firm output share "in Germany or Italy is around 20 percent" (AEJ p. 3 fn 7); Italy appears in the EU KLEMS concentration figure (AEJ p. 21). — [AEJ](https://sebnemkalemliozcan.com/assets/publications/AEJMacro-2022-0036.pdf)
- Appendix extras for Italy (NBER22):
  - Filing requirement: "Approximately 900,000" companies (S.p.A., S.r.l., Sapa, cooperatives, consortia, …) (appx p. 25).
  - CompNet comparison, number of firms relative to Eurostat: Italy 2008 = 58.8% (BvD) against 2.2% (CompNet) (appx p. 76).
  - Size shares by number of firms: 85.1 / 14.1 / 0.8 (BvD) against 97.4 / 2.5 / 0.1 (Eurostat) (appx p. 77).
  - The coverage pattern "improves over time for all countries until 2005 and is stable thereafter". Germany's weaker coverage is due to "the under-representation of small firms" (appx p. 66). — [NBER22](https://www.nber.org/system/files/working_papers/w21558/w21558.pdf)

### Inferences
- An Italian check should expect manufacturing gross-output coverage of about 0.65–0.79 for 2001–2007 and 0.86–0.90 for 2008–2012. It should also expect a strong deficit in micro-firm (1–19) employment against SBS.

### Gaps
- No main-text statement singles out reliable years beyond "especially since 2001".

---
**URL log**

Worked:
- NBER22 PDF (200, 1,998,729 B)
- NBER rev0 and rev1 PDFs
- https://www.nber.org/papers/w21558 (gives issue date Sept 2015, revision date Jan 2022)
- https://data.nber.org/data-appendix/w21558/ (2015 Appendix.pdf and readme.txt)
- AEA article page https://www.aeaweb.org/articles?id=10.1257/mac.20220036 (lists "Supplemental Appendix" materials/20572 and "Replication Package" materials/20573)
- materials/20572 (PDF, 98 pp.)
- materials/20573 (zip; only author disclosure statements)
- the author-hosted AEJ PDF
- the guide PDF on sebnemkalemliozcan.com
- Wayback snapshots of orbis.html and guide.html
- IDEAS: https://ideas.repec.org/a/aea/aejmac/v16y2024i2p353-74.html and https://ideas.repec.org/p/nbr/nberwo/21558.html

Failed:
- https://www.aeaweb.org/articles/pdf/doi/10.1257/mac.20220036 (returns an HTML login page)
- econweb.umd.edu (403)
- openICPSR 187541 and doi.org/10.3886/E187541V1 (403, Cloudflare)
- Wayback copies of programs.html and of the guide PDF (connection reset)
