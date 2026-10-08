# Orbis Historical (Moody's / Bureau van Dijk): full-text verification of the official and library documentation, and of the structure of the bulk flat files

**How this note was made (read first).** All sources below were downloaded on **2026-10-08** and read in full (HTML converted to text; PDFs extracted with `pdftotext`). This note re-checks the snippet-based claims in `research_notes/Guida Orbis Historical analisi economica/documentazione_ufficiale.md` and `variabili_e_missing.md` one by one. Each claim gets a verdict:
- **CONFIRMED**: the claim is in the full text, quoted verbatim.
- **CORRECTED**: the full text says something different, or the claim was pinned to the wrong page.
- **NOT FOUND**: the page could not be opened, or the text is not on it.

Each finding is also labelled **[vendor]** (Moody's/BvD's own text, e.g. a brochure or press release), **[library reproducing vendor]**, **[third-party, with BvD cooperation]** or **[third-party]**. Note that **no Moody's web page dedicated to "Orbis Historical" exists at a guessable moodys.com URL**, and none was returned by search. Vendor wording therefore comes from BvD brochures, a Moody's press release and library pages.

**Access log (2026-10-08).**

Worked (HTTP 200, read in full):
- library.hbs.edu
- kresgeguides.bus.umich.edu
- gsb-research-help.stanford.edu
- faq.library.princeton.edu (11030 and 11082)
- libguides.cbs.dk (DataHub newsletter and Orbis guide)
- manchester-uk.libanswers.com
- library.fuqua.duke.edu
- moodys.com Orbis product page
- wrds-www.wharton.upenn.edu vendor page
- nber.org/research/orbis
- sebnemkalemliozcan.com "Processing Orbis Historical Disk" PDF. The fanjt.weebly.com mirror is byte-identical (same MD5).
- econ.umd.edu Kalemli-Özcan et al. data description (2015, 110 pp.)
- back.nber.org w21558 Appendix
- papers.tinbergen.nl 15-110 (rev. Jan 2022)
- documents1.worldbank.org PRWP 10261 (Dec 2022)
- nuffieldfoundation.org IFS Deaton appendices
- amlinsight.lexisnexis.com and riskmanagement.lexisnexis.com help pages
- andaf.it BvD Orbis brochure (Sept 2022)
- creditreform.de BvD Orbis brochure (2015)
- s203.q4cdn.com Moody's DataHub press release (28 Jan 2021)
- anderson.ucla.edu BvD "Filing Requirements for Companies Globally" (Jan 2016)
- appexchange.salesforce.com Moody's Orbis connector release notes (Oct 2025)
- conference.nber.org NBER-ORBIS slides (July 2019)
- unisg.ch
- datahub.aalto.fi
- biblioteca.luiss.it
- raw.githubusercontent.com (Tax-Justice-Network, agostinognasso, jakob-ra)

Did **not** work:
- **WRDS "BvD data retention"**: login wall ("You must be logged-in to access that page."). The Wayback snapshot of 2024-07-20 also redirects to login.
- **Yale guides.library.yale.edu/BVDORBIS/Historic**: 404, "not currently available due to visibility settings". WebFetch is egress-blocked.
- **edesiderata.crl.edu**: curl TLS name mismatch; WebFetch egress-blocked.
- **dsrs.illinois.edu**: login page only ("Sign in to your account").
- **nber.org/research/data/orbis-company-data**: 403.
- **aeaweb.org appendix**: 403.
- **UWE page**: JavaScript-rendered, no text.
- **matchplat.com**: no code definitions in the static HTML.
- **library.fa.ru**: 403.
- **bf.uzh.ch**: connection failed.
- **web.archive.org**: 429 / connection reset.
- **Guessed moodys.com URLs**: 404 for `/company-reference-data/orbis-historical.html`, `/capabilities/data-hub.html` and `/capabilities/datahub.html`.

---

## 1. What Moody's/BvD officially say Orbis Historical is: time span, ownership history, update frequency, delivery format, dead firms, and whether descriptive data are a current snapshot

### Takeaway
Vendor text (BvD brochures, 2015 and 2022) sells Orbis Historical as history "beyond the 10 years covered in Orbis's reports", "going back 15-20 years", keyed on the same BvD ID numbers as current Orbis and "treated" to be compatible with current data. Library pages that reproduce vendor text agree on **financials from 1995** and **ownership (Links) from 2007**. They also agree on **bulk tab-delimited TXT (or SQL)** delivery outside the web interface, **twice a year**, with each delivery replacing the prior one.

The **update months differ by source**:
- April/October (HBS)
- June/December (Michigan Kresge, 2025 cut-off "June 2025")
- "twice yearly" with a June 2024 cut-off (Duke)

All full-text sources agree that the **descriptive files are a single static snapshot without a time dimension**. Only industrial financials and ownership are "cumulatively historical". No vendor text explicitly says that dissolved or dead firms are retained. The flat files do, however, carry a "historical record flag" in `Legal info`, which points that way.

### Cited Findings
**Moody's / BvD vendor text**
- **NOT FOUND**: no moodys.com page for "Orbis Historical". The Moody's Orbis product page (retrieved 2026-10-08) never mentions Orbis Historical. Relevant vendor statements on it:
  - "With information on more than 635 million companies across the globe, Orbis captures and blends data from more than 170 different sources"
  - "Our data includes over 2B ownership links, 1.8B+ historic ownership links and with over 193M active ownership links."
  - Delivery: "via our Orbis web interface, through our Catalysts, APIs or industry connectors, or prefer to have it pushed to your existing infrastructure via our bulk feed, cloud, or real-time delivery"
  - [vendor] — [Moody's, Orbis](https://www.moodys.com/web/en/us/capabilities/company-reference-data/orbis.html)
- **CONFIRMED (new vendor source)**: BvD Orbis brochure (InDesign PDF created 2022-09-12) [vendor] — [BvD Orbis brochure Sept 2022, hosted by ANDAF](https://www.andaf.it/media/379416/orbis-brochure-sept2022.pdf)
  - "Orbis Historical — If you'd like to research a company's history, beyond the 10 years covered in Orbis's reports, a subscription to Orbis Historical gives you access to historical data going back 15-20 years. To show you historical information in the context of current company data, we: • use the same Orbis ID numbers for Orbis Historical and the current version of Orbis • 'treat' the historical data to make it compatible with current data"
  - Academic section: "The 10-year history function offers a major benefit for your academic research, and we can also supply more extensive historical information if required."
- **CONFIRMED (older vendor wording)**: BvD/Creditreform Orbis brochure (PDF created 2015-08-10) [vendor] — [Creditreform Orbis brochure](https://www.creditreform.de/fileadmin/user_upload/central_files/docs/produkte/marktanalyse-kundendaten/kundenbindung-akquise/orbis/creditreform-orbis-broschuere.pdf)
  - "Orbis reports cover up to ten years' history. But with Orbis Historical you can access historical data going back 15-20 years that's linked to current live firms."
  - "Ten years of history is offered per report with a longer history available on request via Orbis Historical."
  - The same box says BvD "used the same BvD ID numbers for Orbis Historical" and "'treated' the historical data to make it compatible".
- **Moody's DataHub (official press release, New York, 28 January 2021)** [vendor] — [Moody's press release PDF](https://s203.q4cdn.com/694693571/files/doc_news/archive/4673bec4-6fc2-4af4-a6e4-192145aacf07.pdf)
  - "Moody's Corporation (NYSE:MCO) today announced the launch of Moody's DataHub, a new cloud-based analytical platform that integrates data from across Moody's"
  - Coverage includes "Nearly 400 million private and public entities from Bureau van Dijk's Orbis database"
  - "Easily accessible data previews, along with a readily available data dictionary and documentation, allow users to explore and efficiently interact with Moody's datasets."
  - It does **not** mention Orbis Historical or 1995/2007.

**Library pages reproducing vendor text (full text)**
- **CONFIRMED verbatim, with additions**: Harvard Business School Baker Library [library reproducing vendor] — [HBS, Orbis Historical](https://www.library.hbs.edu/databases-cases-and-more/datasets/orbis-historical)
  - "Orbis Historical Data is a point-in-time snapshot of the Orbis entity database."
  - "-Financial data on the web platform reflects a rolling ten years."
  - "-Orbis Historical is delivered outside of the Orbis web interface via FTP in structured sets of tab delimited TXT or SQL table files, and updated twice yearly, in April and October."
  - "-Each new delivery replaces the prior files."
  - "-Orbis Historical has all company financials that Bureau van Dijk has collected back to 1995 as well as ownership changes back to 2007."
  - Licence block: "Vendor: Moody's Analytics. Start Date: 2023, Expires: 2026"; "Coverage Start Date: 1995".
- **CONFIRMED verbatim, but the extra text attributed earlier is CORRECTED**: Michigan Kresge [library reproducing vendor] — [Kresge, Orbis Historical Data Files](https://kresgeguides.bus.umich.edu/az/orbis-historical-data-files)
  - The page says only: "ORBIS Historical Data Files contain a point-in-time snapshot of the ORBIS database. Financials are available from 1995 to June 2025. Ownership data is available from 2007 to June 2025. Data is available in structured sets of tab-delimited TXT files, and are updated twice yearly in June and December."
  - Plus: "Data is stored on the UM Great Lakes computing cluster at Turbo location: /nfs/turbo/bus-kbaldata/Orbis/."
  - **CORRECTED**: the passages the earlier notes attributed to Kresge are **not on the Kresge page**. They come from **World Bank PRWP 10261 (Dec 2022), p. 12** (see below). The affected passages are:
    - "The financial module contains both the consolidated and unconsolidated balance sheets…"
    - "…one Links table for each year from 2007 to 2020"
    - "The Entities file contains the list of all entities…"
    - the entity-type list
  - **CORRECTED**: "The Links data contains the BVDID of the target company…" comes from **Kalemli-Özcan, Fan & Penciakova, "Processing Orbis Historical Disk", pp. 12-13**.
  - **NOT FOUND on Kresge**: "What is called 'Orbis Historical' data is a dataset that contains financials earlier than just the last 10 years…" (similar wording is on CBS, see next item).
- **CONFIRMED (date pinned) / CORRECTED attribution**: Copenhagen Business School, newsletter post dated **02/20/2024** [library] — [CBS, Smooth access to historical company data with Moody's DataHub](https://libguides.cbs.dk/newsletter/5426/smooth-access-to-historical-company-data-with-moody-s-datahub)
  - "Moody's DataHub is the brand new home of ORBIS historical company data … you no longer need to work offline with the data."
  - "'Orbis Historical' data refers to a dataset of financials older than the past five to ten years as well as historical ownership data from 2007 onwards. Financials are available from the 1990s onwards."
  - "In the Exports section, data can be exported using various export methods (SFTP, AWS S3, etc.) and file formats (CSV, Avro, Parquet, and ORC)."
  - "ORBIS – Data Dictionary: an overview of the available datasets, tables, and the frequency of updates" (held on internal CBSshare, not public).
  - The earlier notes attributed the "five to ten years… 1990s" sentence to **St. Gallen; that is CORRECTED**. It is CBS text.
- **St. Gallen (actual content)** [library] — [HSG Library, Orbis](https://www.unisg.ch/en/university/library/search-and-use/databases/orbis/)
  - "Orbis Web Access allows for exports up to 1 million datapoints … If that is not possible, please apply for a Orbis DataHub Access."
  - "The Orbis DataHub allows you to perform bigger data downloads … The setup will take around 2-3 days. You will receive a welcome E-Mail … directly from Moody's."
- **CONFIRMED and pinned**: Duke Fuqua "ORBIS Data Extract" [library reproducing vendor] — [Duke Ford Library, ORBIS Data Extract](https://library.fuqua.duke.edu/databases/orbis-extract.htm)
  - "The ORBIS Data Extract is a point-in-time snapshot of the data tables that make up the ORBIS Web database. Financials for industrial companies and ownership data are cumulatively historical. Industrial company financials are available from 1995 to June 2024. Ownership data is available from 2007 to June 2024."
  - "**Financials for non-industrial companies (banks & insurance companies) and non-financial data for all companies are available for the most recent 10-year period only.** The Data are available as tab delimited TXT files and are updated twice yearly."
  - "The data files are very large - TXT >= 159GB compressed - so you'll need at least 2TB of space."
  - This is the "cumulatively historical" page that the earlier notes could not pin (it is Duke, not CRL).
- **CONFIRMED and pinned to Princeton**: Princeton FAQ 11030 and 11082 (Bobray Bordelon, "Last Updated: May 12, 2026") [library] — [Princeton FAQ 11030](https://faq.library.princeton.edu/econ/faq/11030); [Princeton FAQ 11082](https://faq.library.princeton.edu/econ/faq/11082)
  - 11030: "ORBIS Historical (point in time snapshots of ORBIS back to 2020). Ownership files go back to 2007. Each delivery of data includes all the years; however, descriptive data is not cumulative or historical. It is a snapshot of each period and therefore is header data that cannot be used for historical industry or geography. Detailed cash flow and interim data is not cumulative or historical and is a snapshot of each period. Global format including histories are cumulative files with data back to 1997 with the exception of finance and industry that is current only. Coverage for each country begins at different points in time. Each instance is approximately 250 GB highly compressed. One should have at least 3TB of space to work with each snapshot."
  - 11082 adds: "Our oldest is 2020." It also says "finance and industry that is not cumulative and current only".
- **CORRECTED**: Stanford GSB FAQ 341892 does **not** reproduce the HBS wording. It is a comparison chart "Establishment-Level Company Data" (answered by Alice Kalinowski, Oct 06, 2026). For Orbis Historical it says [library] — [Stanford GSB FAQ 341892](https://gsb-research-help.stanford.edu/library/faq/341892):
  - "Dates Covered (coverage gets better over time): 1980s-2024 (countries are added in different years)"
  - "Data Frequency: ~Annual snapshots (exact month the snapshot is taken varies slightly)"
  - "# of Establishments Covered in the Most Recent Year: 547M"
  - "Historical Ownership Data: A subset (~135M active entities) have LINKS files since 2007. Coverage is better for larger companies + multi-nationals."
  - Availability: "Orbis Historical in Redivis. Also in WRDS, but the data is not identical; WRDS staff believes it has less data that what we have on Redivis."
  - Linking identifiers: "BvD ID, National ID, VAT/Tax Number, LEI, Ticker, ISIN".
- **NOT FOUND (could not open)**:
  - [Yale ORBIS Historic](https://guides.library.yale.edu/BVDORBIS/Historic): 404, "visibility settings".
  - [CRL eDesiderata node 549](https://edesiderata.crl.edu/node/549): TLS/egress.
  - [Illinois DSRS](https://dsrs.illinois.edu/internal/datahub/category/bvd-historicals/data-overview): login.
  - [UWE Bristol](https://www.uwe.ac.uk/study/library/databases/a-z/orbis): JavaScript-only.
  - The snippet-based quotes from these pages stay **unverified**.
- **CORRECTED**: the NBER ORBIS project page (retrieved 2026-10-08) **no longer contains** "BvD has developed a 'Historical Product'…" or the list of BvD documentation ("ownership files (pdf), variable list (xlsx), and Global Format Definitions"). It now lists "Orbis 2025-2026 (limited to internal information for NBER restricted users)" and "Data Management: Carla Tokman and Daniel Feenberg" — [NBER ORBIS Project](https://www.nber.org/research/orbis). The data page returns 403.
  - The "Historical Product" concept **is CONFIRMED** in NBER IFM slides (July 2019): "To build a panel of maximum coverage over time one has to use Historical Product of ORBIS (Historical Database) that takes care of these issues and creates a panel incorporating sector and ID changes"; "Historical product is very expensive (hundreds of $/year)" [sic] [third-party] — [Gourinchas & Kalemli-Özcan, NBER-ORBIS Firm Level Data Initiative, slides](https://conference.nber.org/conf_papers/f129854.slides.pdf)

**The best full-text description of a physical delivery** [third-party, with BvD cooperation] — [Kalemli-Özcan, Fan & Penciakova, "Processing Orbis Historical Disk" (PDF, created 2017-09-16), subtitle "in cooperation with Bureau van Dijk"](https://sebnemkalemliozcan.com/assets/workingpapers/Processing%20Orbis%20Historical%20Disk%20FINAL2.pdf)
- Disk folders: "Financials Histo Dec SQL", "Financials Histo Dec text", "Orbis Dec text", "Ownership histo Dec SQL", "Ownership histo Dec text". "The 'SQL' folders contain the same information as those in the 'text' folders". "The historical disk is around 280 GB."
- **Descriptive files are static**: "Each of the 12 descriptive files discussed in this section are static, contain the latest year for which information is available, and therefore do not have a time dimension. All of these files contain the firm ID (or BVDID) in the first column and can be linked by merging on this identifier."
  - The 12 files: All addresses, Contact info, Identifiers, Industry classifications, Legal info, Auditors – current, Bankers – current, DMC – current only, DMC – previous, Other advisors – current, Overviews, Trade description.
- **Historical depth**: "the sample extends until 2016, with the earliest observation in the data set dates back to the 1970's … European countries … better covered since the mid to late 1990's; many other countries … do not have a significant coverage until around 2005-2007."
- **Only industrial financials are deep-history**: the "Financials Histo Dec text" folder holds "Industry - Global financials and ratios" in three currency versions, "information on industrial firms, which, by BvD definition, exclude financial companies".
  - The "Orbis Dec text" folder has banks, insurance, detailed format, cash flow and Key financials. Its same-named industrial files differ in that "the files under folder Financials Histo Dec text are available for more financial years" ("According to BVD representatives").
  - This matches Duke's "non-industrial … most recent 10-year period only".
- Ownership: "Links_YEAR.txt files contain information on the links between a target firm and its owner(s) … in a given vintage year"; the folder "also contains a PDF that describes the type of entities covered and types of linkages."

**World Bank PRWP 10261, Dec 2022** [third-party] — [Dall'Olio, Goodwin, Martinez Licetti, "Using ORBIS to Build a Global Database of Firms with State Participation"](https://documents1.worldbank.org/curated/en/099800112132221252/pdf/IDU03d9586040b28504839081120922e33694f65.pdf)
- "ORBIS provides the option to access their historical vintage files, which are structured in different modules and years."
- "there is one Links table for each year from 2007 to 2020. The Links table for 2019 has about 1.9 billion ownership links."
- "the ownership links are provided for each year in a separate module from the annual financial indicators and from the entity type (atemporal file)."
- "data in the order of 200Gb when compressed".

### Inferences
- The **update calendar moved over time**:
  - December disk (2017 guide)
  - April/October (HBS text, licence from 2023)
  - June/December (Kresge 2025)
  - The user's "December 2025" delivery fits the June/December cycle. Each delivery is a **full replacement** (HBS), not an increment.
- "Point-in-time snapshot" in vendor text means the whole package is cut at one date. Inside it, industrial financials and ownership Links carry history, while every descriptive table (Legal_info, Industry_classifications, Contact_info…) reflects the delivery date only. This is stated by HBS/Princeton/Duke/Kalemli. Status, NACE code, legal form, size category and listed flag in the user's Dec-2025 files are therefore **December-2025 values applied to all past years**.
- **Start year**: "1995" is the vendor's headline; Princeton says 1997; the 2017 disk had observations back to the 1970s; Stanford says "1980s". Treat 1995 as a marketing floor, not a hard bound, and expect thin coverage before ~2000 outside Europe.
- Bank and insurance financials, and non-industrial data generally, are **not** deep-history in the Historical product (Duke; Kalemli 2017). `Key_financials` covers industrials, banks and insurers together (Kalemli 2017: "includes industry firm, banks, and insurance company data worldwide").

### Gaps
- No moodys.com product or help page specific to Orbis Historical or the DataHub "ORBIS Data Dictionary" is publicly reachable. The DataHub dictionary stays behind a login (CBSshare/DataHub).
- No vendor sentence explicitly says inactive/dissolved firms are retained in Orbis Historical (see Section 5 for indirect evidence).

---

## 2. University library guides: what each says in full (verification table)

### Takeaway
Of the eight guides named in the brief:
- **Full text read and confirmed**: HBS, Michigan Kresge, Princeton, Duke, Manchester, CBS.
- **Stanford** was mis-described in the earlier notes.
- **Yale, CRL and Illinois** stay unverifiable from this network.
- **Princeton** is the only guide that says outright that descriptive data "cannot be used for historical industry or geography".

### Cited Findings
- HBS — CONFIRMED (see §1) — [HBS](https://www.library.hbs.edu/databases-cases-and-more/datasets/orbis-historical)
- Michigan Kresge — CONFIRMED for the description; extra module text CORRECTED to the World Bank source (see §1) — [Kresge](https://kresgeguides.bus.umich.edu/az/orbis-historical-data-files)
- Princeton 11030/11082 — CONFIRMED; the "dropped after roughly 10 years" sentence is pinned here: "ORBIS is survivor biased. The current database contains header data and companies are dropped after roughly 10 years if not active." — [Princeton 11030](https://faq.library.princeton.edu/econ/faq/11030)
- Duke — CONFIRMED (the "cumulatively historical" text) — [Duke](https://library.fuqua.duke.edu/databases/orbis-extract.htm)
- Stanford GSB 341892 — CORRECTED (comparison chart, not HBS wording) — [Stanford](https://gsb-research-help.stanford.edu/library/faq/341892)
- University of Manchester (Last Updated 27 Jul 2023) — CONFIRMED: "Fame has 20 years of financial history whereas Orbis has 10 … companies in Amadeus were deleted if inactive for 4-6 years, creating survivorship bias; this is not the case with Fame and Orbis." Also "As of 30 November 2022, Amadeus was retired." — [Manchester FAQ 259496](https://manchester-uk.libanswers.com/teaching-and-learning/faq/259496)
- CBS — CONFIRMED (DataHub post 02/20/2024). The current CBS Orbis guide **does not contain** the earlier-cited "10-year window for listed companies and a 5-year window for all other companies" (NOT FOUND on the current page) — [CBS Orbis guide](https://libguides.cbs.dk/orbis)
- Aalto DataHub (Orbis web): "Time period coverage: Up to 10 years of history per company" — [Aalto](https://datahub.aalto.fi/en/data-sources/orbis)
- Yale / CRL / Illinois — NOT FOUND (inaccessible; see access log).

### Inferences
- The library sources do not contradict each other on substance. Their differences are about vintage (cut-off month and year) and about what the local library holds (e.g. Princeton's "oldest is 2020").

### Gaps
- Yale's 2021 text and CRL's evaluation could not be re-read; quotes from them in earlier notes remain snippet-based.

---

## 3. WRDS BvD support articles (data retention; Orbis variable documentation without login)

### Takeaway
The WRDS "BvD data retention" article is **login-only** (live and in the Wayback snapshot of 2024-07-20), so its content is **NOT FOUND**. The public WRDS vendor page only gives product status: Amadeus is legacy; Orbis products are updated annually. Column labels for WRDS Orbis tables remain available only via third-party GitHub notebooks.

### Cited Findings
- **NOT FOUND**: [WRDS, BvD data retention](https://wrds-www.wharton.upenn.edu/pages/support/support-articles/bvd/bvd-data-retention/) returns "Please Login — You must be logged-in to access that page." (2026-10-08). The Wayback copy (2024-07-20) redirects to `/login/?next=…`.
- WRDS vendor page (public, 2026-10-08) [WRDS] — [WRDS, Bureau van Dijk (Moody's)](https://wrds-www.wharton.upenn.edu/pages/about/data-vendors/bureau-van-dijk-bvd/)
  - "BvD Amadeus Large Companies — Last updated June 7th, 2025. Legacy data is no longer updated."
  - "BvD Orbis Medium Companies — Last updated September 26th, 2026. Data updated annually … Total Size: 435.05 GiB"
  - "BvD Orbis Bank Focus — Last updated September 29th, 2026."
- WRDS column labels (`conscode` "CONSOLIDATION CODE", `nr_months` "NUMBER OF MONTHS", `orig_units` VARCHAR(25) "ORIGINAL UNITS", `orig_currency`, `exchrate` DOUBLE PRECISION "EXCHANGE RATE FROM ORIGINAL CURRENCY") — CONFIRMED via GitHub code search hit [third-party] — [rs-kellogg/wrds_workshop_public, docs/explore.ipynb](https://github.com/rs-kellogg/wrds_workshop_public)
- Stanford: WRDS Orbis "is not identical" to the Orbis Historical delivery held on Redivis — [Stanford](https://gsb-research-help.stanford.edu/library/faq/341892)

### Inferences
- WRDS Orbis (annual, size-split L/M/S tables) is a different product from the Orbis Historical flat files. WRDS retention rules, whatever they are, do not describe the user's December-2025 delivery.

### Gaps
- The WRDS retention article text and the WRDS Orbis "Data Dictionary"/"WRDS Overview" need a WRDS login; the user (or a colleague with WRDS access) should copy them.

---

## 4. Field semantics in the flat files

### Takeaway
- **Consolidation codes**: verbatim vendor-derived definitions now exist for C1, C2, U1, U2, NRF, NRLF and NF (LexisNexis AML help). LF is defined by Kalemli-Özcan et al. NRF/NRLF/NF are company-level labels. The **NRF threshold conflicts**: ">48 months" (LexisNexis) vs "last 3 years" (Kalemli-Özcan 2022).
- **Filing type** values "Annual report" / "Local registry filing" are confirmed.
- **Currency files**: the -EUR/-USD files are conversions of the same data as the original-currency file, with a time-varying exchange rate column.
- **Units**: **no vendor text states the units of the flat files**. Three independent empirical checks point to **absolute units (not thousands)** for monetary items. The per-employee ratio columns are explicitly in thousands "(th)".
- **Item definitions** (OPRE, EMPL, STAF, TFAS, MATE) are available verbatim only as BvD definitions reproduced by Kalemli-Özcan et al.

### Cited Findings
**Consolidation code: full text**
- **CONFIRMED (and extended to NRF/NRLF/NF)**: LexisNexis AML Insight help, "Orbis Report (Global Company Coverage) Results" [third-party reproducing BvD codes] — [LexisNexis AML Insight help](https://amlinsight.lexisnexis.com/bps/web20_help/AML/bsp_results_orbisreport_r.html)
  - "Each company is associated with one or more statements. The statements are assigned a consolidation code that indicates the type of statement that is available. The following consolidation codes and descriptions may be included:"
  - "C1:Statement of a mother company integrating the statements of its controlled subsidaries or branches with no unconsolidated companion."
  - "C2:Statement of a mother company integrating the statements of its controlled subsidaries or branches with an unconsolidated companion."
  - "U1:Statement not integrating the statements of the possible controlled subsidaries or branches of the concerned company with no unconsolidated companion."
  - "U2:Statement not integrating the statements of the possible controlled subsidaries or branches of the concerned company with a unconsolidated companion." [sic; the meaning is "with a consolidated companion"]
  - "NRF: No recent financials. This code is assigned to companies where the last available accounts are more than 48 months old."
  - "NRLF: No recent limited financials. This code is attached to companies with limited financial items where the last available accounts are more than 48 months old."
  - "NF: Companies with no financials available have the code NF associated to their statement."
- **CORRECTED**:
  - The RiskManagement version of the same help page ([riskmanagement.lexisnexis.com](https://riskmanagement.lexisnexis.com/bps/web20_help/RSKM/bsp_results_orbisreport_r.html)) **no longer contains** the code list. The AML version does.
  - The LF sentence quoted earlier ("LF are quite often made of median value of turnover range…") is **NOT FOUND** on either LexisNexis page.
  - MatchPlat and VU pages showed no code text in their static HTML (NOT VERIFIED).
- **LF / NF / NRF / NRLF** (Tinbergen DP 15-110, revision Jan 2022) [third-party] — [Kalemli-Özcan et al., Tinbergen DP 15-110](https://papers.tinbergen.nl/15110.pdf)
  - "Orbis contains companies with the account type LF with limited financial information, and NF with no financial items at all. Also, there are entities with 'no recent accounts' (NRF) or 'no recent limited financials' (NRLF), where 'no recent' refers to last 3 years. By default, the Orbis media gives preference to the consolidated accounts".
  - "C1: indicates that BvD has information on the firm's consolidated accounts only; U1: … unconsolidated accounts only; C2: … both … and the associated to C2 are the consolidated ones; U2: … both … and the associated to U2 are the unconsolidated ones; LF: indicates the firm reports limited financial information."
  - "for these companies [LF] all financial variables except sales and total assets are missing".
  - "The variable BvD Account Number is composed of three parts: the first two letters … country code …, the last character of the string refers to the type of consolidation code".
- **CORRECTED**: the IFS Deaton Review appendix does **not** contain the LF sentence attributed to it earlier (no "LF" in the full text). It does confirm duplicates by filing type and by the U2/C2 codes (next item).
- **Additional definitions (2015 data description, footnote)** [third-party] — [Kalemli-Özcan et al. 2015 data description, p. 82](https://www.econ.umd.edu/sites/www.econ.umd.edu/files/pubs/Data_Description_2015_09_final.pdf)
  - "C1: account of a company-headquarter of a group, aggregating all companies belonging to the group (affiliates, subsidiaries, etc.), where the company headquarter has no unconsolidated account, C2: … where the company headquarter also presents an unconsolidated account, U1: account of a company with no consolidated account, and U2: account of a company with a consolidated account."
  - The same text is in the [NBER w21558 Appendix](https://back.nber.org/appendix/w21558/Appendix.pdf).

**Filing type**
- **CONFIRMED**: "Some firms have both an observation stemming from the 'Annual Report' and one from 'Local Registry Filing'. In these cases, the Annual Report typically contains more information on the key variables … revenue, COGS, the wage bill and employment." The appendix also states:
  - "HO contains some seemingly identical observations, which only differ in a few variables … particularly the case in the early years of the sample (pre-2002)"
  - "some firms submit both a consolidated account and an unconsolidated account, as can be identified via the consolidation codes ('U2' and 'C2')"
  - [third-party, about "Historical Orbis"] — [IFS Deaton Review, Firms and inequality online appendices, March 2022](https://www.nuffieldfoundation.org/wp-content/uploads/2022/03/Firms-and-inequalities-online-appendices-IFS-Deaton-Review.pdf)
- **CONFIRMED**: Trade description.txt holds "the type of filing (mainly annual report and local registry filing)". On duplicates: "A very small number of firms file their reports through two different channels (such as through local registry or in annual reports, indicated by the variable 'filing type' in the data). It is important to note that, due to different reporting rules, the same financial variables delivered by different channels could have different values. In addition, when the data comes from the annual reports, detailed financials are provided." — [Processing Orbis Historical Disk, pp. 5, 10-11](https://sebnemkalemliozcan.com/assets/workingpapers/Processing%20Orbis%20Historical%20Disk%20FINAL2.pdf)
- The same guide lists three reasons for duplicates per BvD ID and year:
  - "1. Some firms report both consolidated and unconsolidated accounting reports"
  - "2. Some firms change reporting month in a given year. Reports might be given for both months during the year of the change."
  - "3. … two different channels".

**Number of months / Original units / Original currency / Exchange rate**
- **CONFIRMED (vendor field names)**: column headers `Number of months`, `Original units`, `Original currency`, `Exchange rate from original currency` in the text files — [YiLulululu/EquityOwnershipStructure, bvdColumns.py](https://github.com/YiLulululu/EquityOwnershipStructure/blob/main/bvdColumns.py)
  - A 2023 delivery loaded into AWS Athena (KOF) has the column order `bvdid, consolidation_code, filing_type, closing_date, number_of_months, audit_status, accounting_practice, source_for_publicly_quoted_companies, original_units, original_currency, …`
  - In that schema `Key_financials` also has `exchange_rate_from_original_currency`, while the non-suffixed `Industry-Global_financials_and_ratios` table goes straight from `original_currency` to `fixed_assets`.
  - [third-party] — [jakob-ra/firm-level-web-indicator, orbis_athena_queries](https://github.com/jakob-ra/firm-level-web-indicator/blob/main/orbis_athena_queries)
- **CONFIRMED (three currency versions; exchange rate column)**: "All three files have the same underlying data, but differ in reporting currency: the first file reports in original currency in which the companies file financial information or that is available at BvD data providers, the second in USD, and the third in EUR. In the case when EUR or USD is used, a time-varying exchange rate used to convert currency is also reported, so it is straightforward to convert USD or EUR into the original currency unit. Our understanding is the files in common currency are provided for user convenience." — [Processing Orbis Historical Disk, p. 8](https://sebnemkalemliozcan.com/assets/workingpapers/Processing%20Orbis%20Historical%20Disk%20FINAL2.pdf)
- **Exchange-rate semantics** (about disk/web exports, not the flat file specifically): "the variable 'Exchange Rate' does not contain the rate to, say, US dollar … but has the exchange rate of the currency of an account to the currency chosen by the person downloading the data"; "once we choose to download the data in 'local currency' the values of the variable 'Exchange Rate' are always set to 1." — [Kalemli-Özcan et al. 2015, pp. 20-21](https://www.econ.umd.edu/sites/www.econ.umd.edu/files/pubs/Data_Description_2015_09_final.pdf)
- **Original units** (about BvD disk exports, 2015): "By default, the formatted export from BvD disks will result in the units and currency in which a particular company originally filed its financials. This means that a given company may report in thousands in some years, and then millions … In case the default was chosen, the variable UNITS contains the reference to what units a given observation corresponds to (the values are textual in ORBIS and numeric powers of 10 in AMADEUS) … But note that the UNITS variable might have errors in certain disks". Footnote: "By errors we mean the cases when the value of the UNITS switches from, say, thousands to millions but the corresponding financial variables do not show the 1000x decrease in the order of magnitude." — [Kalemli-Özcan et al. 2015, p. 20](https://www.econ.umd.edu/sites/www.econ.umd.edu/files/pubs/Data_Description_2015_09_final.pdf)
- `Number of months`: no vendor definition found beyond the field name. WRDS stores it as VARCHAR(2) (Kellogg notebook); the 2023 Athena schema types it `integer`.

**Units of the -EUR / -USD flat files**
- **NOT FOUND in any vendor or library text.**
- **CONFIRMED (third-party empirical, re-read in full)**: "Streams the local Orbis flatfile Key_financials-EUR.txt (~49 GB, long format…)"; "Operating-revenue values in this file are absolute EUR (verified: Walmart US710415188 ~ EUR 563bn), NOT thousands."; `THRESHOLD_EUR = 750_000_000.0 # EUR 750M, absolute units`. The file path is `…\Financials - Global format incl histo for industries June text\Key_financials-EUR.txt` — [Tax-Justice-Network/unitary-taxation, src/1b_orbis_universe/1b_1_financials.py](https://github.com/Tax-Justice-Network/unitary-taxation/blob/main/src/1b_orbis_universe/1b_1_financials.py)
- **No contradiction**: panel-e2tree's "revenue per employee in thousands" is the vendor's ratio column, not a rescaled total. Its DATA_REPORT shows:
  - `rev_per_emp` "Ricavi operativi per addetto (migliaia)" with median 155,80
  - `ln_assets` "log(total assets)" with median 14,30
  - `rev_per_emp` is extracted as column 90 of `Industry-Global_financials_and_ratios-EUR.txt` (awk `$90` in `00_extract_orbis.sh`), which in the vendor header is "Operating revenue per employee (th)".
  - [third-party] — [agostinognasso/panel-e2tree, reports/DATA_REPORT.md](https://github.com/agostinognasso/panel-e2tree/blob/main/reports/DATA_REPORT.md); [code/00_extract_orbis.sh](https://github.com/agostinognasso/panel-e2tree/blob/main/code/00_extract_orbis.sh)
- The vendor's own headers label ratio columns with units: "Profit per employee (th)", "Operating revenue per employee (th)", "Average cost of employee (th)", "Shareholders funds per employee (th)", "Working capital per employee (th)", "Total assets per employee (th)"; and in Key_financials "Market capitalisation (mil)" — [YiLulululu bvdColumns.py](https://github.com/YiLulululu/EquityOwnershipStructure/blob/main/bvdColumns.py); [jakob-ra Athena schema](https://github.com/jakob-ra/firm-level-web-indicator/blob/main/orbis_athena_queries)
- In the 2023 Key_financials Athena schema, `operating_revenue_turnover`, `cash_flow`, `total_assets` and `shareholders_funds` are typed **bigint** while P/L items are `integer` — [jakob-ra Athena schema](https://github.com/jakob-ra/firm-level-web-indicator/blob/main/orbis_athena_queries)

**Missing-value tokens**
- **CONFIRMED (ownership fields only)**: "'-' (not significant) or 'n.a.' (not available)". This passage also lists the ownership tokens "WO" (wholly owned), "MO" (majority owned), "CQP1" (50% plus 1 share), "NG" (negligible), "BR" (branch, ORBIS Ownership only) and "JO" (jointly owned, AMADEUS only) — [Kalemli-Özcan et al. 2015, §8 ownership cleaning](https://www.econ.umd.edu/sites/www.econ.umd.edu/files/pubs/Data_Description_2015_09_final.pdf)
- **CORRECTED/NOT FOUND**: no full-text source documents `n.s.` or `n.a.` strings inside the numeric financial columns of the flat files.
  - The industry file contains the literal strings `NULL`, `NUL`, `JHB` in USSIC code fields: "Replace primary codes with missing value if the current value is 'NULL' … secondary codes … 'NULL' or 'JHB' … core codes … 'NUL'" — [Processing Orbis Historical Disk, p. 6](https://sebnemkalemliozcan.com/assets/workingpapers/Processing%20Orbis%20Historical%20Disk%20FINAL2.pdf)
  - "n.a." also marks subsidiaries whose figures sit in the parent's consolidated account: "Those firms are flagged as n.a., to indicate their information is captured by the parent" (the authors' own database construction, from the web interface) — [World Bank PRWP 10261](https://documents1.worldbank.org/curated/en/099800112132221252/pdf/IDU03d9586040b28504839081120922e33694f65.pdf)

**Item definitions** (BvD definitions reproduced by researchers; no vendor definitions document reachable)
- **CONFIRMED** [third-party reproducing BvD] — [Kalemli-Özcan et al. 2015, Table B.1 notes, p. 84](https://www.econ.umd.edu/sites/www.econ.umd.edu/files/pubs/Data_Description_2015_09_final.pdf); identical in [NBER w21558 Appendix](https://back.nber.org/appendix/w21558/Appendix.pdf):
  - "OPRE: Total operating revenues (Net sales + Other operating revenues+ Stock variations). The figures do not include VAT. Local differences may occur regarding excises taxes and similar obligatory payments for specific market of tobacco and alcoholic beverage industries"
  - "EMPL: Total number of employees included in the company's payroll"
  - "STAF: All the employees costs of the company (including pension costs)"
  - "TFAS: Book value of tangible fixed assets i.e. plant, equipment and machinery"
  - "MATE: Material Costs."
- Granularity: "total assets item is decomposed into fixed and current assets. The former is further decomposed into tangible and intangible fixed assets, but no additional details on the composition of tangible fixed assets (such as plant, property, and equipment) are provided." — [Processing Orbis Historical Disk, pp. 8-9](https://sebnemkalemliozcan.com/assets/workingpapers/Processing%20Orbis%20Historical%20Disk%20FINAL2.pdf)
- "Certain variables, such as employment, will not be on the balance sheet but rather in memorandum items." — [Kalemli-Özcan et al. 2015, p. 12](https://www.econ.umd.edu/sites/www.econ.umd.edu/files/pubs/Data_Description_2015_09_final.pdf)

**Italy (filing rules that drive missingness)** [vendor] — [BvD, "Filing Requirements for Companies Globally, as of January 2016", Italy section](https://www.anderson.ucla.edu/documents/areas/adm/acis/library/FilingRequirementsForCompaniesGloballyBureauVanDijk.pdf)
- Filers: "S.p.A., S.r.l., Sapa, Società Cooperative, Società Consortili, G.e.i.e, Società di persone (only consolidated accounts)…"; "Approximately 900,000".
- Abbreviated form: "The financial statements in abbreviated form is not an obligation but a right for smaller companies". Limits: total assets €4,400,000; revenues €8,800,000; 50 employees.
- "Accounts are filed at the Chamber of Commerce"; "maximum time the deposit is 180 days from the end of 'year, with an additional 30 days"; "average time of filing accounts … 5 months".

### Inferences
- Treat **monetary columns in the -EUR files as absolute euros**:
  - Walmart check (TJN): Walmart's reported revenue is of the order of US$600bn, so "EUR 563bn" fits absolute units. This is the analyst's own sanity check, not vendor text.
  - bigint typing for revenue and assets (KOF): values above 2.1bn fit absolute units, not thousands.
  - panel-e2tree's median ln(total assets) of 14.30 ≈ €1.6 m, plausible for a balanced panel of mostly Italian/Spanish/Portuguese firms; in thousands it would be €1.6 bn.
  - Ratio columns tagged "(th)" are in thousands of euros per employee.
  - The user should still confirm on one well-known Italian company (e.g. compare `Operating revenue (Turnover)` with the published bilancio).
- `Original units` and `Exchange rate from original currency` are provenance fields. Dividing a converted value by the exchange rate gives back the original-currency amount (Kalemli 2017).
  - Whether the -EUR values are already scaled by `Original units` is implied by the absolute-units evidence but not stated anywhere.
  - Kalemli 2015 warns that UNITS can be wrong in some disks: screen for ×1000 jumps around changes in `Original units`.
- NRF/NRLF/NF are **company-level flags**. Kalemli 2017 lists a "no recent financials flag" among `Legal info` variables, so in the flat files they most likely appear in `Legal_info`, not as `Consolidation code` values of statement rows. Expect `Consolidation code` ∈ {C1, C2, U1, U2, LF} in the financial files.

### Gaps
- No vendor definition document (BvD "Global Standard Format" definitions, variable list xlsx) is publicly reachable. The NBER page that mentioned them has been rewritten.
- The value domain of `Original units`, `Audit status`, `Accounting practice` and `Source` was not found in any full-text source.
- The NRF threshold conflicts (48 months vs 3 years); it may have changed over time.

---

## 5. Retention: standard Orbis vs Orbis Historical

### Takeaway
- **Standard Orbis**: the web platform shows a **rolling ten years** of financials (HBS; vendor brochures "up to ten years' history"; Aalto). Disks/media historically gave fewer years in practice: "de facto … only up to 5 recent reporting years" in 2015.
- **Company removal**: sources conflict.
  - Kalemli-Özcan et al. (2015) and Manchester: Orbis keeps a company "as long as the company is active in the business register" / no deletion, unlike Amadeus (deleted after 4-6 years).
  - Princeton's librarian: "companies are dropped after roughly 10 years if not active".
- **Orbis Historical**: the vendor's answer is "historical data going back 15-20 years" on the same IDs. Descriptive tables are a current snapshot. No vendor text explicitly guarantees retention of dead firms.

### Cited Findings
- "Financial data on the web platform reflects a rolling ten years." — [HBS](https://www.library.hbs.edu/databases-cases-and-more/datasets/orbis-historical) [library reproducing vendor]
- "Orbis reports cover up to ten years' history. But with Orbis Historical you can access historical data going back 15-20 years that's linked to current live firms." — [Creditreform/BvD brochure 2015](https://www.creditreform.de/fileadmin/user_upload/central_files/docs/produkte/marktanalyse-kundendaten/kundenbindung-akquise/orbis/creditreform-orbis-broschuere.pdf) [vendor]; same idea in [BvD brochure Sept 2022](https://www.andaf.it/media/379416/orbis-brochure-sept2022.pdf) [vendor]
- "AMADEUS provides at most 10 recent reporting years of data for the same company while ORBIS de facto reports data for only up to 5 recent reporting years. AMADEUS will also delete the company from the database if the company did not report anything in the last 5 years, ORBIS will keep this company as long as the company is active in the business register." — [Kalemli-Özcan et al. 2015, p. 12](https://www.econ.umd.edu/sites/www.econ.umd.edu/files/pubs/Data_Description_2015_09_final.pdf) [third-party, citing BvD]. On p. 16 BvD's justification: "the information included in a given vintage had to be limited because of the media capacity".
- "AMADEUS drops the firm if firm did not report anything in the last 6 years where ORBIS keeps the firm and if firm exits, turn status to inactive"; "Reporting lag of 2 years"; "Update: For the same firm, same variable that is missing in 2012, can be there in 2018 since info is updated constantly." — [NBER-ORBIS slides, July 2019](https://conference.nber.org/conf_papers/f129854.slides.pdf) [third-party]
- "companies are dropped after roughly 10 years if not active" — [Princeton FAQ 11030](https://faq.library.princeton.edu/econ/faq/11030) [library; source of the rule not given]
- Manchester (2023): Amadeus deleted firms inactive 4-6 years; "this is not the case with Fame and Orbis" — [Manchester](https://manchester-uk.libanswers.com/teaching-and-learning/faq/259496)
- Orbis Historical package: "Financials for non-industrial companies (banks & insurance companies) and non-financial data for all companies are available for the most recent 10-year period only." — [Duke](https://library.fuqua.duke.edu/databases/orbis-extract.htm)
- `Legal info.txt` "contains one observation per BVDID" with status, status date, standardized/national legal form, date of incorporation, type of entity, "BvD firm size classification, listed status, and identity of the information provider". Variables the authors drop include "no recent financials flag (this will be apparent in the financial data), historical record flag, historical record since". — [Processing Orbis Historical Disk, pp. 4, 6](https://sebnemkalemliozcan.com/assets/workingpapers/Processing%20Orbis%20Historical%20Disk%20FINAL2.pdf)
- "Each new delivery replaces the prior files." — [HBS](https://www.library.hbs.edu/databases-cases-and-more/datasets/orbis-historical)
- WRDS retention article: NOT FOUND (login).

### Inferences
- The presence of a `Historical record flag` / `Historical record since` in `Legal_info` is the best documentary hint that Orbis Historical carries entities that are no longer "live" in current Orbis. Check in the user's Dec-2025 `Legal_info.txt` whether such columns exist and how many rows are flagged.
- Because each delivery replaces the previous one and the vendor "treat[s] the historical data to make it compatible with current data", **old statements may be restated or re-keyed between deliveries**. The Dec-2025 delivery is BvD's current version of history, not "as originally published". Kalemli-Özcan's team relied on stacking separate vintages for this reason.

### Gaps
- No vendor text on how long dissolved companies are kept in Orbis or Orbis Historical. The library statements conflict (keep vs drop after ~10 years).
- WRDS retention rules not accessible.

---

## 6. BvD ID changes: official description, and whether a correspondence table ships with Orbis Historical

### Takeaway
BvD IDs change for these reasons:
- national ID change
- information-provider switch
- address change (DE/AT/IT)
- legal-form change (ES)
- M&A (target's ID "blocked")
- BvD harmonisation

A "BvD ID changes" file **was listed among the raw vintage-disk files** by the World Bank team (2022). That is the only full-text evidence that a correspondence table is part of the historical delivery. Kalemli-Özcan et al. advise requesting the "correspondence table" from BvD. Vendor brochures say Orbis Historical uses the same ID numbers as current Orbis. Separately, the **BvD ID prefix is not always the firm's country**: the 2017 processing guide corrects it with a "discrepancy" table.

### Cited Findings
- **CONFIRMED (full text)**: "a researcher merging the time-series financial information coming from several BvD historic disks or the online downloads done at various points of time may encounter occasional BvD ID changes over time. The BvD ID number incorporates either the national ID number or the ID provided by their information providers (IP). According to BvD, the ID numbers may change when the national ID numbers change in the official data sources or the BvD IPs decide to switch their ID numbers. The ID changes are related to changes of address, legal form, or M&A activity. In acquisitions, acquiring company will keep its ID and the target's ID is blocked. BvD mentions that Spanish companies encounter a BvD ID change if they change legal form while companies incorporated in Germany, Austria or Italy may in some cases see their BvD ID change if the company changes address. Finally, BvD itself can initiate the ID change when an entity is available on more than one product, or is provided by more than one IP and BvD harmonizes the IDs across databases using a set of priority rules. As long as BvD does not know that a certain company is the same entity, it will have several different BvD ID numbers on ORBIS. Because it is hard to keep track of all these idiosyncracies, the researcher should request the 'correspondence table' of BvD IDs from their BvD representative. BvD ID changes can also be obtained by subscribing institutions via the dedicated BvD ID Change Lookup tool at idchanges.bvdinfo.com." — [Kalemli-Özcan et al. 2015, p. 13](https://www.econ.umd.edu/sites/www.econ.umd.edu/files/pubs/Data_Description_2015_09_final.pdf) [third-party, relaying BvD]
- **NEW, CONFIRMED (full text)**: "The following files are available in the raw disks: Entities, Links per year, Industry classifications, Identifiers, Contact info, Additional company information, Legal information, Controlling shareholders, Basic shareholders, Headquarters, Overviews, Cash flow, **BvD ID changes**, Banks' financials, Insurances' financials, Industry's financials, and Key financials." (footnote 22) — [World Bank PRWP 10261, Dec 2022, p. 12](https://documents1.worldbank.org/curated/en/099800112132221252/pdf/IDU03d9586040b28504839081120922e33694f65.pdf) [third-party]
- **CONFIRMED (vendor)**: "use the same Orbis ID numbers for Orbis Historical and the current version of Orbis" — [BvD brochure 2022](https://www.andaf.it/media/379416/orbis-brochure-sept2022.pdf); "used the same BvD ID numbers for Orbis Historical" — [BvD/Creditreform brochure 2015](https://www.creditreform.de/fileadmin/user_upload/central_files/docs/produkte/marktanalyse-kundendaten/kundenbindung-akquise/orbis/creditreform-orbis-broschuere.pdf)
- **CONFIRMED (vendor, connector context)**: Moody's Orbis–Salesforce connector "What's New – Version 3.44": "BvD ID Change Lookup Process — Ensures changes/removals of BvD IDs in Orbis are reflected in Salesforce for linked accounts. Includes steps to run lookup and download results." Use case: "Users can identify changed/removed BvD IDs and unlink/relink records to updated IDs." (PDF created 2025-10-31) — [AppExchange PDF](https://appexchange.salesforce.com/image_host/14fa5c88-3f7d-4622-9aef-74af3e713c06.pdf)
- "Historical Product of ORBIS … creates a panel incorporating sector and ID changes" — [NBER-ORBIS slides 2019](https://conference.nber.org/conf_papers/f129854.slides.pdf)
- **BvD ID prefix ≠ country (new)**: "Correct the difference between the country of a firm, and the country code indicated by the first 2 digits of BVDID, using the table 'discrepancy'." And: "BvD does not provide a comprehensive list of country codes covered in the data." — [Processing Orbis Historical Disk, pp. 7, 11](https://sebnemkalemliozcan.com/assets/workingpapers/Processing%20Orbis%20Historical%20Disk%20FINAL2.pdf)
- Entity types in `Entities.txt` (full list, 2017 disk), which **corrects** the earlier partial code list: "Bank (B), Financial company (F), Insurance company (A), Industrial company (C), Mutual & Pension Fund/Nominee/Trust/Trustee (E), Foundation/Research Institute (J), Public authorities (S), One or more known individuals or families (I), Employees/managers/directors (M), Self-ownership (H), Private equity firm (P), Listed (Z), Unnamed private shareholder, aggregated (D), Other unnamed shareholders, aggregated (L), Hedge fund (Y), Branch (Q), Marine vessels (W)"; "In 99.99% of cases this file only has one row for each BVDID." — [Processing Orbis Historical Disk, p. 12](https://sebnemkalemliozcan.com/assets/workingpapers/Processing%20Orbis%20Historical%20Disk%20FINAL2.pdf)
- Links relation types: "SHH: single shareholder of first level; CTP: first level shareholder identified via the Calculated Total Percentage; ISH: … immediate shareholder; HQ: when the target company is a branch or foreign company, its single shareholder is its headquarter; DUO 25; GUO 25; DUO 50; GUO 50; DUO 50C … only with owner (shareholder) types B, C, A and F; GUO 50C; GUO 25C" — [Processing Orbis Historical Disk, p. 13](https://sebnemkalemliozcan.com/assets/workingpapers/Processing%20Orbis%20Historical%20Disk%20FINAL2.pdf)

### Inferences
- If the user's December-2025 delivery contains a file such as `BvD_ID_changes.txt` (the WB list suggests a table with that name in the raw disks), apply it before linking to external data or older extracts. If it is absent, request it from Moody's client services, as Kalemli-Özcan et al. advise.
- Within a single delivery, IDs are harmonised to current numbering (vendor: same IDs; "treated" data). ID changes matter mainly when merging with **other vintages or external Orbis extracts**.
- Do not derive country solely from `substr(BvD ID,1,2)` (as panel-e2tree does). Use `Contact_info` country ISO, or at least check the discrepancy rate.

### Gaps
- The layout (column names) of the "BvD ID changes" file and whether it is in every Orbis Historical delivery (vs. only some disks or products) is not documented in any accessible source.
- idchanges.bvdinfo.com was not tested (the earlier notes record that bvdinfo.com hosts were egress-blocked).
