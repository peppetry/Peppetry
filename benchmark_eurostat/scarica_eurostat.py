#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scarica_eurostat.py
===================

Scarica dall'API di disseminazione Eurostat (JSON-stat 2.0) i totali ufficiali
necessari per misurare la copertura dei dati Orbis secondo il metodo di
Kalemli-Özcan, Sørensen, Villegas-Sanchez, Volosovych e Yeşiltaş (2024),
Online Appendix, sezioni C e D.

Produce, nella cartella dello script, tre CSV "tidy":

  eurostat_sbs_settori.csv   SBS per sezione NACE (totale classi dimensionali)
  eurostat_sbs_classi.csv    SBS per classe di addetti (manifattura e sezioni)
  eurostat_bd_imprese.csv    Business Demography: imprese attive, addetti,
                             dipendenti per classe di dipendenti (0 / totale ...)

e un file di documentazione delle query:

  eurostat_query_usate.csv   dataset, filtri (dimensioni/codici), n. righe

Colonne dei CSV tidy:
  paese            ISO2 (GB per il Regno Unito, GR per la Grecia)
  geo_eurostat     codice geo Eurostat originale (UK, EL, ...)
  anno             anno di riferimento
  fonte            codice dataset Eurostat
  classificazione  NACE_R2 oppure NACE_R11
  nace             sezione NACE Rev.2 (lettera) o aggregato; per i dati Rev.1.1
                   e' la sezione Rev.2 "equivalente" secondo la mappatura usata
                   dagli autori (D->C, C->B, E->D, H->I, I->H, K->L, J->K)
  nace_r2_estesa   mappatura estesa Rev.1.1 -> Rev.2 (es. K -> L+M+N)
  nace_originale   codice NACE originale del dataset
  classe           classe dimensionale armonizzata (TOTAL, 0-19, 20-249,
                   250+, 0, TOTAL-0, ...)
  classe_originale codice size_emp / sizeclas originale (o formula se derivata)
  variabile        turnover_eur_milioni, addetti, dipendenti, imprese,
                   imprese_attive, costi_personale_eur_milioni,
                   valore_produzione_eur_milioni, addetti_bd, dipendenti_bd
  indicatore       codice indicatore Eurostat (indic_sb / indic_sbs)
  unita            unita' di misura (milioni di euro / numero)
  valore           valore (NaN se confidenziale o mancante)
  flag             flag Eurostat (c=confidenziale, b=rottura di serie,
                   e=stima, p=provvisorio, u=bassa affidabilita', d=definizione
                   diversa, s=stima Eurostat, n=non significativo, :=mancante)
  derivato         True se la riga e' calcolata (somma di classi o TOTAL-0)

Uso:
  python3 scarica_eurostat.py            # scarica tutto (1999-ultimo anno)
  python3 scarica_eurostat.py --dal 1995

Richiede: pandas, requests.
"""
import argparse
import os
import sys
import time

import numpy as np
import pandas as pd
import requests

BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
QUI = os.path.dirname(os.path.abspath(__file__))

# Paesi richiesti (ISO2 "di lavoro") e relativo codice geo Eurostat
PAESI = ["AT", "BE", "CZ", "DE", "EE", "ES", "FI", "FR", "GB", "GR",
         "HU", "IT", "LV", "NO", "PL", "PT", "RO", "SE", "SI", "SK"]
ISO2_A_GEO = {"GB": "UK", "GR": "EL"}
GEO_A_ISO2 = {v: k for k, v in ISO2_A_GEO.items()}

# Sezioni NACE Rev.2 di interesse
SEZ_R2_SBS = ["B", "C", "D", "E", "F", "G", "H", "I", "J", "L", "M", "N", "S95"]
SEZ_R2_EBS = ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
              "P", "Q", "R", "S95"]  # dal 2021 (regolamento EBS)
SEZ_R2_BD = ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
             "P", "Q", "R", "S"]

# Mappatura NACE Rev.1.1 -> Rev.2 (livello sezione).
#  "autori": come in Appendix C.2 / Tabella C.2.3 (D->C ecc., K->L)
#  "estesa": raggruppamento piu' fedele (la Rev.1.1 K comprende L, M, N e J62-63)
R11_A_R2_AUTORI = {"C": "B", "D": "C", "E": "D", "F": "F", "G": "G",
                   "H": "I", "I": "H", "J": "K", "K": "L", "K_X_K7415": "L",
                   "M": "P", "N": "Q", "O": "S"}
R11_A_R2_ESTESA = {"C": "B", "D": "C", "E": "D+E", "F": "F", "G": "G",
                   "H": "I", "I": "H+J", "J": "K", "K": "L+M+N",
                   "K_X_K7415": "L+M+N", "M": "P", "N": "Q", "O": "R+S"}

# Indicatori -> nome variabile e unita'
VAR_SBS = {  # dataset SBS 1995-2020 (indic_sb)
    "V12110": ("turnover_eur_milioni", "milioni di euro"),
    "V12120": ("valore_produzione_eur_milioni", "milioni di euro"),
    "V16110": ("addetti", "numero (persone occupate)"),
    "V16130": ("dipendenti", "numero"),
    "V11110": ("imprese", "numero"),
    "V13310": ("costi_personale_eur_milioni", "milioni di euro"),
}
VAR_EBS = {  # dataset SBS dal 2021 (indic_sbs)
    "NETTUR_MEUR": ("turnover_eur_milioni", "milioni di euro (net turnover)"),
    "VAL_OUT_MEUR": ("valore_produzione_eur_milioni", "milioni di euro"),
    "EMP_NR": ("addetti", "numero (persone occupate)"),
    "SAL_NR": ("dipendenti", "numero"),
    "ENT_NR": ("imprese", "numero"),
    "EXPN_SAL_BEN_MEUR": ("costi_personale_eur_milioni",
                          "milioni di euro (employee benefits expense)"),
}
VAR_BD_OLD = {
    "V11910": ("imprese_attive", "numero"),
    "V16910": ("addetti_bd", "numero (persone occupate imprese attive)"),
    "V16911": ("dipendenti_bd", "numero (dipendenti imprese attive)"),
}
VAR_BD_NEW = {
    "ENT_NR": ("imprese_attive", "numero"),
    "EMP_NR": ("addetti_bd", "numero (persone occupate imprese attive)"),
    "SAL_NR": ("dipendenti_bd", "numero (dipendenti imprese attive)"),
}

# Definizione delle query: (dataset, gruppo di output, filtri, dimensione nace,
#                            dimensione indicatore, dizionario variabili)
QUERY = [
    # ---- SBS per sezione ----
    ("sbs_na_sca_r2", "settori",
     {"nace_r2": SEZ_R2_SBS + ["B-N_S95_X_K"]}, "nace_r2", "indic_sb", VAR_SBS),
    ("sbs_ovw_act", "settori",
     {"nace_r2": SEZ_R2_EBS + ["B-S_X_O_S94"]}, "nace_r2", "indic_sbs", VAR_EBS),
    # Rev.1.1 1995-2008, una tabella per sezione
    ("sbs_na_2a_mi", "settori", {"nace_r1": ["C"]}, "nace_r1", "indic_sb", VAR_SBS),
    ("sbs_na_2a_dade", "settori", {"nace_r1": ["D"]}, "nace_r1", "indic_sb", VAR_SBS),
    ("sbs_na_2a_el", "settori", {"nace_r1": ["E"]}, "nace_r1", "indic_sb", VAR_SBS),
    ("sbs_na_4a_co", "settori", {"nace_r1": ["F"]}, "nace_r1", "indic_sb", VAR_SBS),
    ("sbs_na_3b_tr", "settori", {"nace_r1": ["G"]}, "nace_r1", "indic_sb", VAR_SBS),
    ("sbs_na_1a_se", "settori", {"nace_r1": ["H", "I", "K"]}, "nace_r1", "indic_sb", VAR_SBS),
    # ---- SBS per classe di addetti ----
    ("sbs_sc_sca_r2", "classi",
     {"nace_r2": SEZ_R2_SBS + ["B-N_S95_X_K"]}, "nace_r2", "indic_sb", VAR_SBS),
    ("sbs_sc_ovw", "classi",
     {"nace_r2": SEZ_R2_EBS + ["B-S_X_O_S94"]}, "nace_r2", "indic_sbs", VAR_EBS),
    ("sbs_sc_2d_dade02", "classi", {"nace_r1": ["D"]}, "nace_r1", "indic_sb", VAR_SBS),
    ("sbs_sc_2d_dade95", "classi", {"nace_r1": ["D"]}, "nace_r1", "indic_sb", VAR_SBS),
    # ---- Business Demography ----
    ("bd_size", "bd",
     {"nace_r2": SEZ_R2_BD + ["B-S_X_O_S94"], "age": ["TOTAL"]},
     "nace_r2", "indic_sbs", VAR_BD_NEW),
    ("bd_9bd_sz_cl_r2", "bd",
     {"nace_r2": SEZ_R2_BD[:9] + ["K_X_K642"] + SEZ_R2_BD[10:] +
      ["B-N_X_K642", "B-S_X_K642"]},
     "nace_r2", "indic_sb", VAR_BD_OLD),
    ("bd_9b_size_cl", "bd",
     {"nace_r1": ["C", "D", "E", "F", "G", "H", "I", "J", "K_X_K7415",
                  "C-K_X_K7415"]},
     "nace_r1", "indic_sb", VAR_BD_OLD),
]


def scarica_json(dataset, params, tentativi=4):
    """Esegue una GET all'API JSON-stat con ritentativi."""
    url = BASE + dataset
    for t in range(tentativi):
        try:
            r = requests.get(url, params=params, timeout=180)
            if r.status_code == 200:
                d = r.json()
                if "error" in d:
                    raise RuntimeError(str(d["error"]))
                if "value" not in d:  # risposta asincrona / messaggio
                    raise RuntimeError("risposta senza 'value': " + r.text[:200])
                return d
            raise RuntimeError(f"HTTP {r.status_code}: {r.text[:200]}")
        except Exception as e:  # noqa: BLE001
            if t == tentativi - 1:
                raise
            print(f"   ritento {dataset} ({e})", file=sys.stderr)
            time.sleep(5 * (t + 1))


def jsonstat_a_df(d):
    """Converte un JSON-stat 2.0 in DataFrame (una riga per cella con valore o flag)."""
    ids, sizes = d["id"], d["size"]
    cats = []
    for dim in ids:
        idx = d["dimension"][dim]["category"]["index"]
        cats.append(sorted(idx, key=lambda k: idx[k]))
    valori = {int(k): v for k, v in d.get("value", {}).items()}
    stati = {int(k): v for k, v in (d.get("status") or {}).items()}
    pos = sorted(set(valori) | set(stati))
    if not pos:
        return pd.DataFrame(columns=ids + ["valore", "flag"])
    pos = np.array(pos)
    righe = {}
    resto = pos.copy()
    for dim, n, cat in zip(reversed(ids), reversed(sizes), reversed(cats)):
        righe[dim] = np.array(cat)[resto % n]
        resto = resto // n
    df = pd.DataFrame({dim: righe[dim] for dim in ids})
    df["valore"] = [valori.get(int(p), np.nan) for p in pos]
    df["flag"] = [stati.get(int(p), "") for p in pos]
    df.attrs["label"] = d.get("label", "")
    return df


def scarica_dataset(dataset, filtri, dal):
    """Scarica un dataset per tutti i paesi; se la richiesta e' troppo grande
    la spezza per paese."""
    base = {"format": "JSON", "lang": "EN", "sinceTimePeriod": str(dal)}
    geos = [ISO2_A_GEO.get(p, p) for p in PAESI]

    def params_per(geo_list):
        p = list(base.items())
        p += [("geo", g) for g in geo_list]
        for dim, codici in filtri.items():
            p += [(dim, c) for c in codici]
        return p

    try:
        return jsonstat_a_df(scarica_json(dataset, params_per(geos)))
    except Exception as e:  # noqa: BLE001
        print(f"   {dataset}: richiesta unica fallita ({e}); scarico per paese",
              file=sys.stderr)
        parti = []
        for g in geos:
            try:
                parti.append(jsonstat_a_df(scarica_json(dataset, params_per([g]))))
            except Exception as e2:  # noqa: BLE001
                print(f"   {dataset} {g}: nessun dato ({e2})", file=sys.stderr)
        if not parti:
            return pd.DataFrame()
        out = pd.concat(parti, ignore_index=True)
        out.attrs["label"] = parti[0].attrs.get("label", "")
        return out


# ---------------------------------------------------------------------------
# Armonizzazione delle classi dimensionali
# ---------------------------------------------------------------------------
CLASSI_DIRETTE = {
    "TOTAL": "TOTAL", "GE250": "250+", "0": "0", "GE10": "10+",
    "0-9": "0-9", "10-19": "10-19", "20-49": "20-49", "50-249": "50-249",
    "0_1": "0-1", "2-9": "2-9", "1-9": "1-9", "1-4": "1-4", "5-9": "5-9",
    "LE4": "0-4", "GE20": "20+", "50-99": "50-99", "100-249": "100-249",
    "250-499": "250-499", "500-999": "500-999", "GE1000": "1000+",
}
# Rev.1.1: la classe 1-19 e' usata come "0-19" (gli autori confrontano
# Eurostat 0-19 con Orbis 1-19)
CLASSI_DIRETTE_R11 = dict(CLASSI_DIRETTE, **{"1-19": "0-19"})

# Classi derivate come somma di classi originali (si prova in ordine)
DERIVATE = {
    "0-19": [["0-9", "10-19"]],
    "20-249": [["20-49", "50-249"], ["20-49", "50-99", "100-249"]],
    "250+": [["250-499", "500-999", "GE1000"]],
}


def aggiungi_classi_derivate(df, col_classe):
    """Aggiunge righe derivate (0-19, 20-249, 250+) sommando le classi fini.
    Una classe derivata e' calcolata solo se TUTTE le componenti hanno valore."""
    chiavi = [c for c in df.columns if c not in
              (col_classe, "valore", "flag")]
    out = []
    presenti = set(df[col_classe].unique())
    for nuova, alternative in DERIVATE.items():
        if nuova in presenti or (nuova == "250+" and "GE250" in presenti) \
                or (nuova == "0-19" and "1-19" in presenti):
            # la classe esiste gia' nel dataset come codice originale
            continue
        for comp in alternative:
            if not set(comp) <= presenti:
                continue
            sub = df[df[col_classe].isin(comp)]
            g = sub.groupby(chiavi, dropna=False)
            agg = g.agg(n=("valore", "count"), valore=("valore", "sum"),
                        flag=("flag", lambda s: "".join(sorted(set("".join(s))))))
            agg = agg[agg["n"] == len(comp)].drop(columns="n").reset_index()
            agg[col_classe] = "+".join(comp)
            agg["_classe_arm"] = nuova
            out.append(agg)
            break
    return out


def elabora(dataset, gruppo, filtri, dim_nace, dim_ind, varmap, dal):
    print(f"-> {dataset}", file=sys.stderr)
    filtri = dict(filtri)
    filtri[dim_ind] = list(varmap)
    raw = scarica_dataset(dataset, filtri, dal)
    if raw.empty:
        return pd.DataFrame(), {"dataset": dataset, "righe": 0}
    titolo = raw.attrs.get("label", "")
    raw = raw.rename(columns={"time": "anno", "geo": "geo_eurostat"})
    raw = raw.drop(columns=[c for c in ("freq", "age") if c in raw.columns])
    col_classe = "size_emp" if "size_emp" in raw.columns else (
        "sizeclas" if "sizeclas" in raw.columns else None)
    rev11 = dim_nace == "nace_r1"

    righe = [raw.assign(_classe_arm=None)]
    if col_classe:
        righe += aggiungi_classi_derivate(raw, col_classe)
    df = pd.concat(righe, ignore_index=True)
    df["derivato"] = df["_classe_arm"].notna()
    if col_classe:
        mappa = CLASSI_DIRETTE_R11 if rev11 else CLASSI_DIRETTE
        df["classe_originale"] = df[col_classe]
        df["classe"] = df["_classe_arm"].fillna(df[col_classe].map(mappa))
        df["classe"] = df["classe"].fillna(df[col_classe])
    else:
        df["classe_originale"] = "TOTAL"
        df["classe"] = "TOTAL"

    # Business Demography: "tutte le classi meno zero dipendenti"
    if gruppo == "bd":
        chiavi = ["geo_eurostat", "anno", dim_nace, dim_ind]
        tot = df[df["classe"] == "TOTAL"].set_index(chiavi)
        zero = df[df["classe"] == "0"].set_index(chiavi)
        comune = tot.index.intersection(zero.index)
        diff = tot.loc[comune].copy()
        diff["valore"] = tot.loc[comune, "valore"] - zero.loc[comune, "valore"]
        diff["flag"] = (tot.loc[comune, "flag"].astype(str) +
                        zero.loc[comune, "flag"].astype(str)).map(
            lambda s: "".join(sorted(set(s))))
        diff["classe"] = "TOTAL-0"
        diff["classe_originale"] = "TOTAL - 0"
        diff["derivato"] = True
        df = pd.concat([df, diff.reset_index()], ignore_index=True)

    df["paese"] = df["geo_eurostat"].map(lambda g: GEO_A_ISO2.get(g, g))
    df["anno"] = df["anno"].astype(int)
    df["fonte"] = dataset
    df["classificazione"] = "NACE_R11" if rev11 else "NACE_R2"
    df["nace_originale"] = df[dim_nace]
    if rev11:
        df["nace"] = df[dim_nace].map(R11_A_R2_AUTORI).fillna(df[dim_nace])
        df["nace_r2_estesa"] = df[dim_nace].map(R11_A_R2_ESTESA).fillna(df[dim_nace])
    else:
        df["nace"] = df[dim_nace].replace({"K_X_K642": "K"})
        df["nace_r2_estesa"] = df["nace"]
    df["indicatore"] = df[dim_ind]
    df["variabile"] = df[dim_ind].map(lambda k: varmap[k][0])
    df["unita"] = df[dim_ind].map(lambda k: varmap[k][1])
    df["flag"] = df["flag"].fillna("").astype(str)
    df.loc[df["valore"].isna() & (df["flag"] == ""), "flag"] = ":"
    cols = ["paese", "geo_eurostat", "anno", "fonte", "classificazione", "nace",
            "nace_r2_estesa", "nace_originale", "classe", "classe_originale",
            "variabile", "indicatore", "unita", "valore", "flag", "derivato"]
    df = df[cols].sort_values(["paese", "anno", "nace", "classe", "variabile"])
    info = {
        "dataset": dataset,
        "titolo": titolo,
        "gruppo": gruppo,
        "filtro_nace": f"{dim_nace}=" + "+".join(filtri[dim_nace]),
        "filtro_indicatori": f"{dim_ind}=" + "+".join(varmap),
        "altri_filtri": ";".join(f"{k}={'+'.join(v)}" for k, v in filtri.items()
                                 if k not in (dim_nace, dim_ind)),
        "classi_originali": "+".join(sorted(raw[col_classe].unique())) if col_classe else "",
        "anni": f"{df['anno'].min()}-{df['anno'].max()}",
        "paesi": " ".join(sorted(df["paese"].unique())),
        "righe": len(df),
        "righe_con_valore": int(df["valore"].notna().sum()),
    }
    return df, info


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dal", type=int, default=1999, help="primo anno (default 1999)")
    ap.add_argument("--out", default=QUI, help="cartella di output")
    a = ap.parse_args()

    risultati = {"settori": [], "classi": [], "bd": []}
    infos = []
    for (ds, gruppo, filtri, dn, di, vm) in QUERY:
        df, info = elabora(ds, gruppo, filtri, dn, di, vm, a.dal)
        infos.append(info)
        if not df.empty:
            risultati[gruppo].append(df)

    nomi = {"settori": "eurostat_sbs_settori.csv",
            "classi": "eurostat_sbs_classi.csv",
            "bd": "eurostat_bd_imprese.csv"}
    for g, parti in risultati.items():
        out = pd.concat(parti, ignore_index=True)
        out.to_csv(os.path.join(a.out, nomi[g]), index=False)
        print(f"scritto {nomi[g]}: {len(out)} righe", file=sys.stderr)
    pd.DataFrame(infos).to_csv(os.path.join(a.out, "eurostat_query_usate.csv"),
                               index=False)


if __name__ == "__main__":
    main()
