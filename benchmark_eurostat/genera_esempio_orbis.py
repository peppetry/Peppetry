#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
genera_esempio_orbis.py
=======================

Genera un file Orbis aggregato SINTETICO (esempio_orbis_aggregati.csv) per
provare calcola_copertura.py end-to-end. NON sono dati Orbis veri.

Costruzione (cosi' i risultati attesi sono noti in anticipo):
  * per ogni paese si fissa una copertura "vera" del fatturato (COP_TURN),
    dell'occupazione (COP_EMPL), del numero di imprese (COP_NIMP) e dei costi
    del personale (COP_COST), uguale in tutte le sezioni;
  * il valore Orbis di ogni sezione = copertura x totale Eurostat della stessa
    sezione (stessa fonte che sceglie calcola_copertura.py);
  * le sezioni senza dato Eurostat (A, O, K prima del 2021, celle
    confidenziali...) ricevono comunque valori Orbis arbitrari: lo script deve
    ESCLUDERLE dal confronto;
  * il campione TFP e' il 60% del campione Totale;
  * il valore di sezione e' ripartito tra le classi 1-19 / 20-249 / 250+
    secondo le quote Eurostat per classe (se disponibili) e un 2% va alla
    classe 'mancante'.
Di conseguenza: D11 = D21 = COP_TURN, D22 = 0.6 x COP_TURN, D23 = COP_EMPL,
D31 = COP_NIMP, e in D25 le quote Orbis coincidono con quelle Eurostat.

Uso:  python3 genera_esempio_orbis.py [--unita euro|migliaia] [--out file.csv]
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calcola_copertura as cc  # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
PAESI = ["IT", "DE", "FR", "ES", "GB", "PL", "EE"]
ANNI = list(range(2005, 2011)) + list(range(2019, 2024))
SEZIONI = list("ABCDEFGHIJKLMNOPQRS")
COP_TURN = {"IT": 0.75, "DE": 0.60, "FR": 0.80, "ES": 0.85, "GB": 0.70, "PL": 0.55, "EE": 0.95}
COP_EMPL = {"IT": 0.65, "DE": 0.55, "FR": 0.60, "ES": 0.80, "GB": 0.62, "PL": 0.50, "EE": 0.90}
COP_NIMP = {"IT": 0.50, "DE": 0.40, "FR": 0.70, "ES": 0.45, "GB": 0.66, "PL": 0.20, "EE": 0.75}
COP_COST = {"IT": 0.72, "DE": 0.58, "FR": 0.77, "ES": 0.83, "GB": 0.68, "PL": 0.52, "EE": 0.93}
QUOTA_TFP = 0.6
QUOTA_MANCANTE = 0.02
QUOTE_DEFAULT = {"1-19": 0.20, "20-249": 0.35, "250+": 0.45}
QUOTE_DEFAULT_N = {"1-19": 0.85, "20-249": 0.13, "250+": 0.02}


def totali(es, variabile, bd=False):
    """Totale Eurostat per paese-anno-sezione con la stessa selezione dello script."""
    if bd:
        d = cc.eurostat_bd(es, variabile, "TOTAL-0", "r2", cc.SEZIONI_TUTTE, "autori")
    else:
        d = cc.eurostat_settori(es, variabile, "autori", "r2", cc.SEZIONI_TUTTE)
    d = d[~d["chiave"].str.contains(r"\+")]
    return d.set_index(["paese", "anno", "chiave"])["valore"].to_dict()


def quote_classi(es, variabile):
    d = es.classi[(es.classi["variabile"] == variabile) &
                  (es.classi["classe"].isin(cc.CLASSI_EUROSTAT))].copy()
    d = cc.assegna_regime(d, cc.REGIMI_CLASSI, "sbs")
    d = d[d["valore"] > 0]
    n = d.groupby(["paese", "anno", "nace", "regime"])["classe"].transform("nunique")
    d = cc.scegli_un_regime(d[n == 3], "r2", "sbs")
    d["q"] = d["valore"] / d.groupby(["paese", "anno", "nace"])["valore"].transform("sum")
    d["classe"] = d["classe"].replace({"0-19": "1-19"})
    out = {}
    for (p, a, s), g in d.groupby(["paese", "anno", "nace"]):
        out[(p, a, s)] = dict(zip(g["classe"], g["q"]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--unita", choices=["euro", "migliaia"], default="euro")
    ap.add_argument("--out", default=os.path.join(QUI, "esempio_orbis_aggregati.csv"))
    a = ap.parse_args()
    es = cc.Eurostat(QUI)
    T = totali(es, "turnover_eur_milioni")
    E = totali(es, "addetti")
    C = totali(es, "costi_personale_eur_milioni")
    N = totali(es, "imprese_attive", bd=True)
    QT = quote_classi(es, "turnover_eur_milioni")
    QE = quote_classi(es, "addetti")
    QN = quote_classi(es, "imprese")
    rng = np.random.default_rng(12345)
    fatt = 1e6 if a.unita == "euro" else 1e3  # milioni -> euro o migliaia

    righe = []
    for p in PAESI:
        for anno in ANNI:
            if p == "GB" and anno > 2020:
                continue  # Orbis ha ancora dati GB, ma qui li omettiamo
            for s in SEZIONI:
                k = (p, anno, s)
                # valori di sezione (campione Totale), in milioni / numero
                turn = COP_TURN[p] * T[k] if k in T else rng.uniform(500, 5000)
                empl = COP_EMPL[p] * E[k] if k in E else rng.uniform(1e3, 5e4)
                cost = COP_COST[p] * C[k] if k in C else rng.uniform(100, 900)
                nimp = COP_NIMP[p] * N[k] if k in N else rng.uniform(100, 5000)
                qt = QT.get(k, QUOTE_DEFAULT)
                qe = QE.get(k, QUOTE_DEFAULT)
                qn = QN.get(k, QUOTE_DEFAULT_N)
                for camp, f in [("Totale", 1.0), ("TFP", QUOTA_TFP)]:
                    for cl in ["1-19", "20-249", "250+", "mancante"]:
                        if cl == "mancante":
                            wt = we = wn = QUOTA_MANCANTE
                        else:
                            wt = (1 - QUOTA_MANCANTE) * qt[cl]
                            we = (1 - QUOTA_MANCANTE) * qe[cl]
                            wn = (1 - QUOTA_MANCANTE) * qn[cl]
                        righe.append({
                            "paese": p, "anno": anno, "settore_nace": s,
                            "classe_addetti": cl, "campione": camp,
                            "n_imprese": round(f * nimp * wn, 4),
                            "somma_operating_revenue": round(f * turn * wt * fatt, 2),
                            "somma_employees": round(f * empl * we, 4),
                            "somma_costs_of_employees": round(f * cost * wt * fatt, 2),
                        })
    df = pd.DataFrame(righe)
    df.to_csv(a.out, index=False)
    print(f"scritto {a.out}: {len(df)} righe ({a.unita})")


if __name__ == "__main__":
    main()
