#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calcola_copertura.py
====================

Calcola la copertura dei dati Orbis rispetto ai totali ufficiali Eurostat,
replicando il metodo dell'Online Appendix (sezioni C e D) di
Kalemli-Özcan, Sørensen, Villegas-Sanchez, Volosovych, Yeşiltaş (2024),
"How to Construct Nationally Representative Firm-Level Data from the Orbis
Global Database".

Tabelle prodotte (stessa numerazione dell'Appendix):

  D11  Economia aggregata, gross output: somma Operating revenue Orbis /
       Turnover SBS, solo sulle sezioni NACE presenti in ENTRAMBE le fonti
       per quel paese-anno (Tab. C.2.3 degli autori).
  D21  Manifattura (sez. C), gross output, campione Totale
  D22  Manifattura, gross output, campione TFP
  D23  Manifattura, occupazione (Number of employees / Persons employed SBS),
       campione Totale; in colonne aggiuntive anche il confronto con la
       Business Demography (addetti e dipendenti delle imprese attive con
       almeno un dipendente, "tutte le classi meno zero")
  D24  Manifattura, occupazione, campione TFP
  D25  Distribuzione dimensionale della manifattura (default 2006):
       quote di gross output e occupazione per classe 1-19 / 20-249 / 250+
       (Orbis) e 0-19 / 20-249 / 250+ (Eurostat SBS)
  D31  Numero di imprese Orbis / imprese attive Eurostat BD (V11910),
       "tutte le classi meno zero dipendenti" per escludere gli autonomi
  CP   (extra) Costi del personale Orbis / Personnel costs SBS (V13310),
       manifattura ed economia aggregata, campione Totale

INPUT ORBIS (--orbis): CSV con colonne
  paese              ISO2 (UK/EL accettati e convertiti in GB/GR)
  anno               anno contabile (closing date)
  settore_nace       lettera di sezione NACE Rev.2 (A..U); 'S95' accettato
  classe_addetti     1-19, 20-249, 250+, mancante
  campione           Totale oppure TFP
  n_imprese          numero di imprese
  somma_operating_revenue, somma_employees, somma_costs_of_employees

  Gli importi monetari Orbis sono in euro (--unita euro) o migliaia di euro
  (--unita migliaia); Eurostat e' in MILIONI di euro: la conversione e'
  fatta dallo script.

INPUT EUROSTAT (cartella --eurostat-dir, default quella dello script):
  eurostat_sbs_settori.csv, eurostat_sbs_classi.csv, eurostat_bd_imprese.csv
  (prodotti da scarica_eurostat.py) e, facoltativi, autori_D*.csv
  (prodotti da estrai_tabelle_autori.py).

OUTPUT (cartella --out, default ./output_copertura):
  copertura_D11.csv ... copertura_D31.csv, copertura_CP.csv  (formato lungo)
  dettaglio_sezioni.csv   rapporto Orbis/Eurostat per ogni sezione usata
  copertura_orbis.xlsx    cartella Excel leggibile (tabelle anno x paese)

ESEMPI:
  python3 calcola_copertura.py --orbis esempio_orbis_aggregati.csv --unita euro
  python3 calcola_copertura.py --orbis mio.csv --unita migliaia \
          --confronta-autori --anni-dimensioni 2006,2019 --sezioni tutte

Note di metodo (vedi README.md):
  * Una sezione entra nel calcolo di un paese-anno solo se ha valore > 0 sia
    in Orbis sia in Eurostat (celle Eurostat confidenziali = escluse).
  * Per ogni paese-anno si usa UN solo "regime" Eurostat: NACE Rev.2 SBS
    2005-2020 (sbs_na_sca_r2), EBS dal 2021 (sbs_ovw_act), NACE Rev.1.1 prima
    del 2008 (tabelle sbs_na_*), convertite in sezioni Rev.2 con la mappatura
    degli autori (D->C, C->B, E->D, H->I, I->H, K->L) o con quella estesa
    (--mappa-rev11 estesa: E->D+E, I->H+J, K->L+M+N), nel qual caso il
    numeratore Orbis somma le sezioni Rev.2 corrispondenti.
  * Gli autori winsorizzano le celle paese-settore-anno con rapporto > 1;
    qui non si winsorizza ma si segnalano le sezioni con rapporto > 1
    (colonna 'n_sezioni_sopra_1' e file dettaglio_sezioni.csv).
"""
import argparse
import os
import re
import sys
import warnings

import numpy as np
import pandas as pd

QUI = os.path.dirname(os.path.abspath(__file__))

# Sezioni di default: economia d'impresa SBS 2008-2020 (B-N senza K) +
# S95 (usata solo se presente anche in Orbis). E' l'insieme comparabile su
# tutto il periodo, anche dopo la rottura EBS del 2021.
SEZIONI_DEFAULT = list("BCDEFGHIJLMN") + ["S95"]
# --sezioni tutte: tutte le sezioni che Eurostat pubblica in qualche periodo
SEZIONI_TUTTE = list("BCDEFGHIJKLMNPQRS") + ["S95"]

PAESI_ALIAS = {"UK": "GB", "EL": "GR"}

# Gruppi di dataset ("regimi") per scegliere UNA fonte per paese-anno
REGIMI_SETTORI = {"EBS": {"sbs_ovw_act"}, "R2": {"sbs_na_sca_r2"}}
REGIMI_CLASSI = {"EBS": {"sbs_sc_ovw"}, "R2": {"sbs_sc_sca_r2"},
                 "R11": {"sbs_sc_2d_dade02", "sbs_sc_2d_dade95"}}
REGIMI_BD = {"BDNEW": {"bd_size"}, "R2": {"bd_9bd_sz_cl_r2"},
             "R11": {"bd_9b_size_cl"}}

CLASSI_ORBIS = ["1-19", "20-249", "250+"]
CLASSI_EUROSTAT = ["0-19", "20-249", "250+"]

RE_CHIAVE_SEZIONI = re.compile(r"^([A-U]|S95)(\+([A-U]|S95))*$")


# ---------------------------------------------------------------------------
# Utilita'
# ---------------------------------------------------------------------------
def avviso(msg):
    print(f"[avviso] {msg}", file=sys.stderr)


def info(msg):
    print(msg, file=sys.stderr)


def normalizza_paese(s):
    s = s.astype(str).str.strip().str.upper()
    return s.replace(PAESI_ALIAS)


def normalizza_classe(s):
    """Uniforma le etichette di classe Orbis a 1-19 / 20-249 / 250+ / mancante."""
    t = s.astype(str).str.strip().str.lower().str.replace(" ", "", regex=False)
    mappa = {
        "1-19": "1-19", "0-19": "1-19", "1to19": "1-19", "0": "1-19",
        "20-249": "20-249", "20to249": "20-249",
        "250+": "250+", ">=250": "250+", "ge250": "250+", "250ormore": "250+",
        "mancante": "mancante", "missing": "mancante", "nan": "mancante",
        "": "mancante", "na": "mancante", "n.d.": "mancante", "nd": "mancante",
    }
    out = t.map(mappa)
    ignote = sorted(set(s[out.isna()].astype(str)))
    if ignote:
        avviso(f"classi_addetti non riconosciute trattate come 'mancante': {ignote}")
    return out.fillna("mancante")


def normalizza_campione(s):
    t = s.astype(str).str.strip().str.lower()
    out = t.map({"totale": "Totale", "total": "Totale", "tot": "Totale",
                 "tfp": "TFP"})
    ignote = sorted(set(s[out.isna()].astype(str)))
    if ignote:
        raise SystemExit(f"Valori di 'campione' non riconosciuti: {ignote} "
                         "(attesi: Totale, TFP)")
    return out


# ---------------------------------------------------------------------------
# Lettura Orbis
# ---------------------------------------------------------------------------
COLONNE_ORBIS = ["paese", "anno", "settore_nace", "classe_addetti", "campione",
                 "n_imprese", "somma_operating_revenue", "somma_employees",
                 "somma_costs_of_employees"]


def leggi_orbis(percorso, unita):
    """Legge e valida il CSV aggregato Orbis. Restituisce un DataFrame con
    importi monetari convertiti in MILIONI di euro (come Eurostat)."""
    sep = None  # autodetect , oppure ;
    df = pd.read_csv(percorso, sep=sep, engine="python", dtype=str)
    df.columns = [c.strip().lower() for c in df.columns]
    mancanti = [c for c in COLONNE_ORBIS if c not in df.columns]
    if mancanti:
        raise SystemExit(f"Colonne mancanti nel CSV Orbis: {mancanti}")
    df["paese"] = normalizza_paese(df["paese"])
    df["anno"] = pd.to_numeric(df["anno"], errors="coerce")
    if df["anno"].isna().any():
        avviso(f"{df['anno'].isna().sum()} righe Orbis con anno non numerico scartate")
        df = df[df["anno"].notna()]
    df["anno"] = df["anno"].astype(int)
    df["nace"] = df["settore_nace"].astype(str).str.strip().str.upper()
    df["classe"] = normalizza_classe(df["classe_addetti"])
    df["campione"] = normalizza_campione(df["campione"])
    for c in ["n_imprese", "somma_operating_revenue", "somma_employees",
              "somma_costs_of_employees"]:
        # accetta anche la virgola decimale
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(",", ".", regex=False)
                              .replace({"": np.nan, "nan": np.nan}),
                              errors="coerce")
    fattore = {"euro": 1e-6, "migliaia": 1e-3}[unita]
    df["opre_meur"] = df["somma_operating_revenue"] * fattore
    df["costi_meur"] = df["somma_costs_of_employees"] * fattore
    df["empl"] = df["somma_employees"]
    chiavi = ["paese", "anno", "nace", "classe", "campione"]
    dup = df.duplicated(chiavi, keep=False)
    if dup.any():
        avviso(f"{dup.sum()} righe Orbis duplicate sulle chiavi {chiavi}: "
               "vengono sommate")
    df = (df.groupby(chiavi, as_index=False)
          [["n_imprese", "opre_meur", "empl", "costi_meur"]]
          .sum(min_count=1))
    sezioni_ignote = sorted(set(df["nace"]) - set("ABCDEFGHIJKLMNOPQRSTU") - {"S95"})
    if sezioni_ignote:
        avviso(f"settore_nace non riconosciuti (ignorati nei confronti): {sezioni_ignote}")
    if not (df["campione"] == "TFP").any():
        avviso("nessuna riga con campione=TFP: le tabelle D22/D24 saranno vuote")
    return df


# ---------------------------------------------------------------------------
# Lettura Eurostat
# ---------------------------------------------------------------------------
class Eurostat:
    def __init__(self, cartella):
        def leggi(nome):
            p = os.path.join(cartella, nome)
            if not os.path.exists(p):
                raise SystemExit(f"File Eurostat mancante: {p} "
                                 "(eseguire prima scarica_eurostat.py)")
            d = pd.read_csv(p, dtype={"flag": str}, low_memory=False)
            d["flag"] = d["flag"].fillna("")
            return d
        self.settori = leggi("eurostat_sbs_settori.csv")
        self.classi = leggi("eurostat_sbs_classi.csv")
        self.bd = leggi("eurostat_bd_imprese.csv")
        self.cartella = cartella


def priorita_regimi(anno, pref, tipo):
    """Ordine di preferenza dei regimi per un anno.
    pref='r2'  : NACE Rev.2 quando esiste (anche 2005-2007), poi Rev.1.1
    pref='r11' : prima del 2008 Rev.1.1 (come gli autori), poi Rev.2."""
    if tipo == "bd":
        if anno <= 2007 and pref == "r11":
            return ["R11", "R2", "BDNEW"]
        return ["BDNEW", "R2", "R11"]
    if anno >= 2021:
        return ["EBS", "R2", "R11"]
    if anno >= 2008 or pref == "r2":
        return ["R2", "R11", "EBS"]
    return ["R11", "R2", "EBS"]


def assegna_regime(df, regimi, tipo):
    """Aggiunge la colonna 'regime' a partire dal dataset di origine."""
    m = {}
    for r, fonti in regimi.items():
        for f in fonti:
            m[f] = r
    # tutto cio' che non e' elencato (tabelle sbs_na_* Rev.1.1) e' R11
    df = df.copy()
    df["regime"] = df["fonte"].map(m).fillna("R11")
    return df


def scegli_un_regime(df, pref, tipo):
    """Per ogni paese-anno tiene solo le righe del regime preferito che ha
    almeno un valore positivo (evita di mescolare Rev.1.1, Rev.2 ed EBS)."""
    if df.empty:
        return df
    df = df[df["valore"] > 0]
    disp = df.groupby(["paese", "anno"])["regime"].agg(set)
    scelto = {}
    for (p, a), insieme in disp.items():
        for r in priorita_regimi(a, pref, tipo):
            if r in insieme:
                scelto[(p, a)] = r
                break
    chiave = list(zip(df["paese"], df["anno"]))
    mask = [scelto.get(k) == r for k, r in zip(chiave, df["regime"])]
    return df[mask]


def eurostat_settori(es, variabile, mappa, pref, sezioni):
    """Totali SBS per sezione (classe TOTAL) per la variabile richiesta."""
    d = es.settori[(es.settori["variabile"] == variabile) &
                   (es.settori["classe"] == "TOTAL")].copy()
    d["chiave"] = d["nace"] if mappa == "autori" else d["nace_r2_estesa"]
    d = d[d["chiave"].astype(str).str.match(RE_CHIAVE_SEZIONI)]
    d = d[d["chiave"].map(lambda k: all(c in sezioni for c in k.split("+")))]
    d = assegna_regime(d, REGIMI_SETTORI, "sbs")
    return scegli_un_regime(d, pref, "sbs")


def eurostat_bd(es, variabile, classe, pref, sezioni, mappa):
    d = es.bd[(es.bd["variabile"] == variabile) & (es.bd["classe"] == classe)].copy()
    d["chiave"] = d["nace"] if mappa == "autori" else d["nace_r2_estesa"]
    d = d[d["chiave"].astype(str).str.match(RE_CHIAVE_SEZIONI)]
    d = d[d["chiave"].map(lambda k: all(c in sezioni for c in k.split("+")))]
    d = assegna_regime(d, REGIMI_BD, "bd")
    return scegli_un_regime(d, pref, "bd")


# ---------------------------------------------------------------------------
# Calcolo della copertura per sezioni comuni
# ---------------------------------------------------------------------------
def copertura(orb, campione, col_orbis, eur, etichetta):
    """Rapporto Orbis/Eurostat per paese-anno sommando solo le sezioni con
    valore > 0 in entrambe le fonti.

    orb : dati Orbis (tutte le classi di addetti, compresa 'mancante')
    eur : righe Eurostat gia' filtrate (colonne paese, anno, chiave, valore)
    Restituisce (tabella paese-anno, dettaglio per sezione)."""
    o = (orb[orb["campione"] == campione]
         .groupby(["paese", "anno", "nace"])[col_orbis].sum(min_count=1))
    o = o[o > 0].rename("orbis").reset_index()
    if eur.empty or o.empty:
        return pd.DataFrame(), pd.DataFrame()
    e = eur[["paese", "anno", "chiave", "valore", "fonte", "flag"]].copy()
    e = e.reset_index(drop=True)
    e["id"] = np.arange(len(e))
    e["n_comp"] = e["chiave"].str.count(r"\+") + 1
    ex = e.assign(nace=e["chiave"].str.split("+")).explode("nace")
    ex = ex.merge(o, on=["paese", "anno", "nace"], how="inner")
    g = ex.groupby("id").agg(orbis=("orbis", "sum"), n=("orbis", "size"))
    g = g[g["n"] == e.set_index("id").loc[g.index, "n_comp"]]
    det = e.set_index("id").loc[g.index].assign(orbis=g["orbis"])
    det = det.rename(columns={"valore": "eurostat"}).reset_index(drop=True)
    det["rapporto_sezione"] = det["orbis"] / det["eurostat"]
    det["tabella"] = etichetta
    det["campione"] = campione
    tab = det.groupby(["paese", "anno"]).agg(
        orbis=("orbis", "sum"), eurostat=("eurostat", "sum"),
        n_sezioni=("chiave", "size"),
        sezioni=("chiave", lambda s: ",".join(sorted(s))),
        fonte_eurostat=("fonte", lambda s: ",".join(sorted(set(s)))),
        flag_eurostat=("flag", lambda s: "".join(sorted(set("".join(s))))),
        n_sezioni_sopra_1=("rapporto_sezione", lambda s: int((s > 1).sum())),
    ).reset_index()
    tab["copertura"] = tab["orbis"] / tab["eurostat"]
    tab.insert(0, "tabella", etichetta)
    tab.insert(1, "campione", campione)
    return tab, det


# ---------------------------------------------------------------------------
# Distribuzione dimensionale (D25)
# ---------------------------------------------------------------------------
def distribuzione_dimensionale(orb, es, anni, pref):
    righe = []
    for var_orb, var_eur, nome in [("opre_meur", "turnover_eur_milioni", "gross_output"),
                                   ("empl", "addetti", "occupazione"),
                                   ("n_imprese", "imprese", "numero_imprese")]:
        # --- Orbis: manifattura, campione Totale, classi note
        o = orb[(orb["campione"] == "Totale") & (orb["nace"] == "C") &
                (orb["anno"].isin(anni)) & (orb["classe"].isin(CLASSI_ORBIS))]
        o = o.groupby(["paese", "anno", "classe"])[var_orb].sum(min_count=1).reset_index()
        o["totale"] = o.groupby(["paese", "anno"])[var_orb].transform("sum")
        o["quota"] = o[var_orb] / o["totale"]
        o["classe_armonizzata"] = o["classe"].replace({"1-19": "0-19"})
        o = o.rename(columns={var_orb: "valore"})
        o["fonte_dati"] = "Orbis"
        o["fonte"] = "orbis"
        # --- Eurostat SBS per classe di addetti, sezione C
        e = es.classi[(es.classi["nace"] == "C") & (es.classi["variabile"] == var_eur) &
                      (es.classi["anno"].isin(anni)) &
                      (es.classi["paese"].isin(orb["paese"].unique())) &
                      (es.classi["classe"].isin(CLASSI_EUROSTAT))].copy()
        e = assegna_regime(e, REGIMI_CLASSI, "sbs")
        # il regime si sceglie solo tra le combinazioni con tutte e 3 le classi
        compl = e[e["valore"] > 0].groupby(["paese", "anno", "regime"])["classe"].transform("nunique")
        e = e[e["valore"] > 0][compl == 3]
        e = scegli_un_regime(e, pref, "sbs")
        e["totale"] = e.groupby(["paese", "anno"])["valore"].transform("sum")
        e["quota"] = e["valore"] / e["totale"]
        e["classe_armonizzata"] = e["classe"]
        e["fonte_dati"] = "Eurostat-SBS"
        for d in (o, e):
            d["variabile"] = nome
        cols = ["variabile", "fonte_dati", "paese", "anno", "classe",
                "classe_armonizzata", "valore", "totale", "quota", "fonte"]
        righe += [o[cols], e[cols]]
    out = pd.concat(righe, ignore_index=True)
    # copertura per classe: Orbis / Eurostat nella stessa classe
    piv = out.pivot_table(index=["variabile", "paese", "anno", "classe_armonizzata"],
                          columns="fonte_dati", values="valore", aggfunc="first")
    if {"Orbis", "Eurostat-SBS"} <= set(piv.columns):
        cop = (piv["Orbis"] / piv["Eurostat-SBS"]).rename("copertura_classe").reset_index()
        out = out.merge(cop, on=["variabile", "paese", "anno", "classe_armonizzata"],
                        how="left")
        out.loc[out["fonte_dati"] != "Orbis", "copertura_classe"] = np.nan
    out.insert(0, "tabella", "D25")
    return out.sort_values(["variabile", "paese", "anno", "fonte_dati", "classe"])


# ---------------------------------------------------------------------------
# Valori pubblicati dagli autori
# ---------------------------------------------------------------------------
def carica_autori(cartella):
    aut = {}
    for tab in ["D11", "D21", "D22", "D23", "D24"]:
        p = os.path.join(cartella, f"autori_{tab}.csv")
        if os.path.exists(p):
            d = pd.read_csv(p, dtype={"anno": str})
            d = d[d["anno"].str.fullmatch(r"\d{4}")]
            d["anno"] = d["anno"].astype(int)
            aut[tab] = d[["paese", "anno", "copertura_autori"]]
    p = os.path.join(cartella, "autori_D25.csv")
    if os.path.exists(p):
        d = pd.read_csv(p)
        d["fonte_dati"] = d["fonte"].replace({"Orbis-Amadeus": "Orbis"})
        d["variabile"] = d["pannello"]
        d["classe_armonizzata"] = d["classe"].replace({"1-19": "0-19"})
        aut["D25"] = d[["variabile", "fonte_dati", "paese", "anno",
                        "classe_armonizzata", "quota_autori"]]
    p = os.path.join(cartella, "autori_D31.csv")
    if os.path.exists(p):
        d = pd.read_csv(p)
        d["copertura_autori"] = d["bvd_orbis_pct"] / 100.0
        aut["D31"] = d[["paese", "anno", "copertura_autori"]]
    return aut


def aggiungi_autori(tab, aut, nome):
    if tab.empty or nome not in aut:
        return tab
    t = tab.merge(aut[nome], on=["paese", "anno"], how="left")
    t["differenza"] = t["copertura"] - t["copertura_autori"]
    return t


# ---------------------------------------------------------------------------
# Presentazione
# ---------------------------------------------------------------------------
def larga(tab, col="copertura"):
    if tab.empty or col not in tab.columns:
        return pd.DataFrame()
    w = tab.pivot_table(index="anno", columns="paese", values=col, aggfunc="first")
    if not w.empty:
        w.loc["Media"] = w.mean()
    return w


def stampa(titolo, tab, confronta):
    print("\n" + "=" * 100)
    print(titolo)
    print("=" * 100)
    if tab.empty:
        print("(nessun dato in comune tra Orbis ed Eurostat)")
        return
    w = larga(tab)
    if confronta and "copertura_autori" in tab.columns:
        a = larga(tab, "copertura_autori").reindex(index=w.index, columns=w.columns)
        testo = w.copy().astype(object)
        for r in w.index:
            for c in w.columns:
                v, va = w.loc[r, c], a.loc[r, c]
                s = "" if pd.isna(v) else f"{v:.2f}"
                if pd.notna(va):
                    s += f"[{va:.2f}]"
                testo.loc[r, c] = s
        print("valore calcolato [valore pubblicato dagli autori]")
        print(testo.to_string())
    else:
        print(w.round(2).astype(object).where(w.notna(), "").to_string())


def stampa_d25(d25, confronta):
    print("\n" + "=" * 100)
    print("D25 - Distribuzione dimensionale manifattura (quote), Orbis 1-19 vs Eurostat 0-19")
    print("=" * 100)
    if d25.empty:
        print("(nessun dato)")
        return
    for var in ["gross_output", "occupazione"]:
        s = d25[d25["variabile"] == var]
        if s.empty:
            continue
        idx = ["anno", "fonte_dati", "classe_armonizzata"]
        w = s.pivot_table(index=idx, columns="paese", values="quota", aggfunc="first")
        if confronta and "quota_autori" in s.columns:
            a = s.pivot_table(index=idx, columns="paese", values="quota_autori",
                              aggfunc="first").reindex(index=w.index, columns=w.columns)
            t = w.copy().astype(object)
            for r in w.index:
                for c in w.columns:
                    v, va = w.loc[r, c], a.loc[r, c]
                    t.loc[r, c] = ("" if pd.isna(v) else f"{v:.2f}") + \
                        ("" if pd.isna(va) else f"[{va:.2f}]")
            w = t
        else:
            w = w.round(2).astype(object).where(w.notna(), "")
        print(f"\n-- {var}")
        print(w.to_string())


def scrivi_excel(percorso, tabelle, d25, dettaglio, parametri, confronta):
    try:
        import xlsxwriter  # noqa: F401
        motore = "xlsxwriter"
    except ImportError:
        motore = "openpyxl"
    with pd.ExcelWriter(percorso, engine=motore) as xw:
        leggimi = pd.DataFrame({"voce": list(parametri.keys()),
                                "valore": [str(v) for v in parametri.values()]})
        leggimi.to_excel(xw, sheet_name="LEGGIMI", index=False)
        for nome, (titolo, tab) in tabelle.items():
            r = 0
            pd.DataFrame({titolo: []}).to_excel(xw, sheet_name=nome, startrow=r, index=False)
            r += 2
            w = larga(tab)
            if w.empty:
                pd.DataFrame({"nessun dato": []}).to_excel(xw, sheet_name=nome, startrow=r)
                continue
            pd.DataFrame({"Copertura calcolata (Orbis / Eurostat)": []}).to_excel(
                xw, sheet_name=nome, startrow=r, index=False)
            w.round(3).to_excel(xw, sheet_name=nome, startrow=r + 1)
            r += len(w) + 4
            if confronta and "copertura_autori" in tab.columns and \
                    tab["copertura_autori"].notna().any():
                a = larga(tab, "copertura_autori")
                pd.DataFrame({"Valori pubblicati dagli autori (Appendix)": []}).to_excel(
                    xw, sheet_name=nome, startrow=r, index=False)
                a.round(3).to_excel(xw, sheet_name=nome, startrow=r + 1)
                r += len(a) + 4
                dif = larga(tab, "differenza")
                pd.DataFrame({"Differenza (calcolato - autori)": []}).to_excel(
                    xw, sheet_name=nome, startrow=r, index=False)
                dif.round(3).to_excel(xw, sheet_name=nome, startrow=r + 1)
                r += len(dif) + 4
            pd.DataFrame({"Dettaglio (formato lungo)": []}).to_excel(
                xw, sheet_name=nome, startrow=r, index=False)
            tab.to_excel(xw, sheet_name=nome, startrow=r + 1, index=False)
        if not d25.empty:
            d25.to_excel(xw, sheet_name="D25", index=False)
        if not dettaglio.empty:
            dettaglio.to_excel(xw, sheet_name="dettaglio_sezioni", index=False)
        if motore == "xlsxwriter":  # larghezze di colonna leggibili
            for nome_foglio, ws in xw.sheets.items():
                ws.set_column(0, 0, 14 if nome_foglio != "LEGGIMI" else 28)
                ws.set_column(1, 60, 11 if nome_foglio != "LEGGIMI" else 110)


# ---------------------------------------------------------------------------
# Programma principale
# ---------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Copertura Orbis vs Eurostat (metodo Kalemli-Özcan et al. 2024)",
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    ap.add_argument("--orbis", required=True, help="CSV aggregato Orbis")
    ap.add_argument("--unita", choices=["euro", "migliaia"], required=True,
                    help="unita' degli importi Orbis (euro o migliaia di euro)")
    ap.add_argument("--eurostat-dir", default=QUI,
                    help="cartella con i CSV Eurostat e autori_*.csv")
    ap.add_argument("--out", default="output_copertura", help="cartella di output")
    ap.add_argument("--anni-dimensioni", default="2006",
                    help="anno/i per D25, separati da virgola (default 2006)")
    ap.add_argument("--sezioni", default="default",
                    help="'default' (B-N senza K, + S95), 'tutte' (B-S, comprese K,P,Q,R "
                         "quando Eurostat le pubblica) o elenco es. 'B,C,D,F,G'")
    ap.add_argument("--mappa-rev11", choices=["autori", "estesa"], default="autori",
                    help="corrispondenza sezioni NACE Rev.1.1 -> Rev.2 prima del 2008")
    ap.add_argument("--preferenza-pre2008", choices=["r2", "r11"], default="r2",
                    help="per anni <2008 usa prima i dati NACE Rev.2 (retropolati, "
                         "default) oppure Rev.1.1 come gli autori")
    ap.add_argument("--confronta-autori", action="store_true",
                    help="affianca i valori pubblicati nell'Appendix (autori_*.csv)")
    ap.add_argument("--anno-min", type=int, default=None)
    ap.add_argument("--anno-max", type=int, default=None)
    a = ap.parse_args(argv)

    if a.sezioni == "default":
        sezioni = SEZIONI_DEFAULT
    elif a.sezioni == "tutte":
        sezioni = SEZIONI_TUTTE
    else:
        sezioni = [s.strip().upper() for s in a.sezioni.split(",") if s.strip()]
    anni_dim = [int(x) for x in a.anni_dimensioni.split(",") if x.strip()]

    orb = leggi_orbis(a.orbis, a.unita)
    if a.anno_min:
        orb = orb[orb["anno"] >= a.anno_min]
    if a.anno_max:
        orb = orb[orb["anno"] <= a.anno_max]
    es = Eurostat(a.eurostat_dir)
    aut = carica_autori(a.eurostat_dir) if a.confronta_autori else {}
    os.makedirs(a.out, exist_ok=True)
    info(f"Orbis: {len(orb)} righe, paesi {sorted(orb['paese'].unique())}, "
         f"anni {orb['anno'].min()}-{orb['anno'].max()}")

    pref, mappa = a.preferenza_pre2008, a.mappa_rev11
    tabelle, dettagli = {}, []

    def registra(nome, titolo, tab, det):
        tab = aggiungi_autori(tab, aut, nome) if a.confronta_autori else tab
        tabelle[nome] = (titolo, tab)
        if not det.empty:
            dettagli.append(det)

    # ---- D11: economia aggregata, gross output
    e_turn = eurostat_settori(es, "turnover_eur_milioni", mappa, pref, sezioni)
    t, d = copertura(orb, "Totale", "opre_meur", e_turn, "D11")
    registra("D11", "D.1.1 Economia aggregata - gross output (Operating revenue / SBS Turnover), "
             "sezioni comuni", t, d)

    # ---- D21 / D22: manifattura, gross output
    e_turn_c = eurostat_settori(es, "turnover_eur_milioni", mappa, pref, ["C"])
    for nome, camp in [("D21", "Totale"), ("D22", "TFP")]:
        t, d = copertura(orb, camp, "opre_meur", e_turn_c, nome)
        registra(nome, f"{nome[0]}.{nome[1]}.{nome[2]} Manifattura - gross output, campione {camp}",
                 t, d)

    # ---- D23 / D24: manifattura, occupazione (SBS + confronto BD)
    e_occ_c = eurostat_settori(es, "addetti", mappa, pref, ["C"])
    e_bd_add = eurostat_bd(es, "addetti_bd", "TOTAL-0", pref, ["C"], mappa)
    e_bd_dip = eurostat_bd(es, "dipendenti_bd", "TOTAL", pref, ["C"], mappa)
    for nome, camp in [("D23", "Totale"), ("D24", "TFP")]:
        t, d = copertura(orb, camp, "empl", e_occ_c, nome)
        for e_alt, col in [(e_bd_add, "copertura_bd_addetti_senza0"),
                           (e_bd_dip, "copertura_bd_dipendenti")]:
            t2, _ = copertura(orb, camp, "empl", e_alt, nome)
            if not t2.empty:
                t2 = t2[["paese", "anno", "copertura"]].rename(columns={"copertura": col})
                t = t2 if t.empty else t.merge(t2, on=["paese", "anno"], how="outer")
        if not t.empty:
            t["tabella"] = nome
            t["campione"] = camp
        registra(nome, f"{nome[0]}.{nome[1]}.{nome[2]} Manifattura - occupazione "
                 f"(Number of employees / SBS Persons employed), campione {camp}", t, d)

    # ---- D31: numero di imprese vs BD imprese attive (tutte meno zero)
    e_bd_imp = eurostat_bd(es, "imprese_attive", "TOTAL-0", pref, sezioni, mappa)
    t, d = copertura(orb, "Totale", "n_imprese", e_bd_imp, "D31")
    e_bd_tot = eurostat_bd(es, "imprese_attive", "TOTAL", pref, sezioni, mappa)
    t2, _ = copertura(orb, "Totale", "n_imprese", e_bd_tot, "D31")
    if not t2.empty and not t.empty:
        t = t.merge(t2[["paese", "anno", "copertura"]]
                    .rename(columns={"copertura": "copertura_vs_tutte_le_imprese"}),
                    on=["paese", "anno"], how="left")
    registra("D31", "D.3.1 Numero di imprese Orbis / imprese attive BD (tutte le classi meno 0 dipendenti)",
             t, d)

    # ---- CP: costi del personale (extra)
    e_cp = eurostat_settori(es, "costi_personale_eur_milioni", mappa, pref, sezioni)
    t, d = copertura(orb, "Totale", "costi_meur", e_cp, "CP_tot")
    tabelle["CP_tot"] = ("Extra - Costi del personale, economia aggregata (sezioni comuni)", t)
    if not d.empty:
        dettagli.append(d)
    e_cp_c = eurostat_settori(es, "costi_personale_eur_milioni", mappa, pref, ["C"])
    t, d = copertura(orb, "Totale", "costi_meur", e_cp_c, "CP_C")
    tabelle["CP_C"] = ("Extra - Costi del personale, manifattura", t)
    if not d.empty:
        dettagli.append(d)

    # ---- D25: distribuzione dimensionale
    d25 = distribuzione_dimensionale(orb, es, anni_dim, pref)
    if a.confronta_autori and "D25" in aut and not d25.empty:
        d25 = d25.merge(aut["D25"], on=["variabile", "fonte_dati", "paese", "anno",
                                        "classe_armonizzata"], how="left")

    # ---- scrittura output
    for nome, (titolo, tab) in tabelle.items():
        tab.to_csv(os.path.join(a.out, f"copertura_{nome}.csv"), index=False)
        stampa(f"{nome} - {titolo}", tab, a.confronta_autori)
    d25.to_csv(os.path.join(a.out, "copertura_D25.csv"), index=False)
    stampa_d25(d25, a.confronta_autori)
    dettaglio = pd.concat(dettagli, ignore_index=True) if dettagli else pd.DataFrame()
    dettaglio.to_csv(os.path.join(a.out, "dettaglio_sezioni.csv"), index=False)

    parametri = {
        "file Orbis": os.path.abspath(a.orbis),
        "unita Orbis": a.unita + " (convertiti in milioni di euro)",
        "cartella Eurostat": os.path.abspath(a.eurostat_dir),
        "sezioni ammesse": ",".join(sezioni),
        "mappatura Rev.1.1->Rev.2": mappa,
        "preferenza anni <2008": pref,
        "anni D25": ",".join(map(str, anni_dim)),
        "unita Eurostat": "turnover e costi: milioni di euro; addetti/imprese: numero",
        "metodo": "copertura = somma Orbis / somma Eurostat sulle sole sezioni con valore >0 "
                  "in entrambe le fonti per paese-anno; un solo regime Eurostat per paese-anno",
        "D23 colonne extra": "copertura_bd_addetti_senza0 = vs BD persone occupate imprese "
                             "con >=1 dipendente; copertura_bd_dipendenti = vs BD dipendenti",
        "D31 colonna extra": "copertura_vs_tutte_le_imprese = vs BD tutte le imprese attive",
        "fonti": "vedi README.md ed eurostat_query_usate.csv",
    }
    xlsx = os.path.join(a.out, "copertura_orbis.xlsx")
    try:
        scrivi_excel(xlsx, tabelle, d25, dettaglio, parametri, a.confronta_autori)
        info(f"\nScritto {xlsx}")
    except Exception as e:  # noqa: BLE001
        avviso(f"impossibile scrivere l'Excel ({e}); i CSV sono comunque in {a.out}")
    n_sopra = int((dettaglio["rapporto_sezione"] > 1).sum()) if not dettaglio.empty else 0
    if n_sopra:
        avviso(f"{n_sopra} celle paese-sezione-anno con rapporto Orbis/Eurostat > 1 "
               "(gli autori le winsorizzano): vedi dettaglio_sezioni.csv")
    info(f"Output in {os.path.abspath(a.out)}")
    return tabelle, d25


if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=FutureWarning)
        main()
