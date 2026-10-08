#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_calcola_copertura.py
=========================

Test end-to-end di calcola_copertura.py sul file sintetico
esempio_orbis_aggregati.csv (generato da genera_esempio_orbis.py).

Verifica che:
  1. D11 e D21 restituiscano esattamente la copertura "vera" del fatturato
     usata per costruire i dati (le sezioni senza dato Eurostat - A, O, K, P,
     Q, R, S e le celle confidenziali - devono essere escluse);
  2. D22 = 0.6 x D21 (campione TFP), D23 = copertura occupazione, D31 =
     copertura del numero di imprese;
  3. in D25 le quote Orbis coincidano con quelle Eurostat;
  4. il risultato non cambi se gli importi Orbis sono forniti in migliaia di
     euro (--unita migliaia);
  5. le quote Eurostat 2006 per classe dimensionale (D25) coincidano, a meno
     dell'arrotondamento, con quelle pubblicate dagli autori (Tab. D.2.5):
     e' un controllo della correttezza del benchmark Eurostat scaricato.

Uso:  python3 test_calcola_copertura.py      (output in output_esempio/)
"""
import io
import os
import sys
import tempfile
from contextlib import redirect_stdout

import numpy as np
import pandas as pd

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import calcola_copertura as cc  # noqa: E402
import genera_esempio_orbis as gen  # noqa: E402

OUT = os.path.join(QUI, "output_esempio")
ESEMPIO = os.path.join(QUI, "esempio_orbis_aggregati.csv")


def controlla(nome, cond, dettaglio=""):
    print(f"[{'OK ' if cond else 'ERRORE'}] {nome} {dettaglio}")
    return bool(cond)


def main():
    esiti = []
    buf = io.StringIO()
    with redirect_stdout(buf):
        tab_e, d25_e = cc.main(["--orbis", ESEMPIO, "--unita", "euro", "--out", OUT,
                                "--confronta-autori", "--eurostat-dir", QUI])
    with open(os.path.join(OUT, "output_console.txt"), "w", encoding="utf-8") as f:
        f.write(buf.getvalue())

    # versione in migliaia di euro
    tmpdir = tempfile.mkdtemp()
    f_k = os.path.join(tmpdir, "orbis_migliaia.csv")
    d = pd.read_csv(ESEMPIO)
    for c in ["somma_operating_revenue", "somma_costs_of_employees"]:
        d[c] = d[c] / 1000.0
    d.to_csv(f_k, index=False)
    with redirect_stdout(io.StringIO()):
        tab_k, _ = cc.main(["--orbis", f_k, "--unita", "migliaia",
                            "--out", os.path.join(tmpdir, "out"), "--eurostat-dir", QUI])

    def attesa(tab, cop, fattore=1.0):
        t = tab.copy()
        t["attesa"] = t["paese"].map(cop) * fattore
        return float(np.nanmax(np.abs(t["copertura"] - t["attesa"])))

    for nome, cop, f in [("D11", gen.COP_TURN, 1), ("D21", gen.COP_TURN, 1),
                         ("D22", gen.COP_TURN, gen.QUOTA_TFP),
                         ("D23", gen.COP_EMPL, 1), ("D24", gen.COP_EMPL, gen.QUOTA_TFP),
                         ("D31", gen.COP_NIMP, 1), ("CP_tot", gen.COP_COST, 1),
                         ("CP_C", gen.COP_COST, 1)]:
        tab = tab_e[nome][1]
        tab = tab[tab["copertura"].notna()]
        err = attesa(tab, cop, f)
        esiti.append(controlla(f"{nome}: copertura = valore vero", err < 1e-6,
                               f"(errore massimo {err:.2e}, {len(tab)} celle paese-anno)"))

    # le sezioni senza Eurostat non devono entrare nel calcolo
    sez = set(",".join(tab_e["D11"][1]["sezioni"]).split(","))
    esiti.append(controlla("D11: sezioni A, K, O, P, Q, R, S escluse (default)",
                           not (sez & set("AKOPQRS")), f"sezioni usate: {sorted(sez)}"))

    # euro vs migliaia
    diff = max(float(np.nanmax(np.abs(tab_e[k][1]["copertura"].values -
                                      tab_k[k][1]["copertura"].values)))
               for k in ["D11", "D21", "D22", "CP_tot"])
    esiti.append(controlla("--unita euro e --unita migliaia danno lo stesso risultato",
                           diff < 1e-9, f"(differenza massima {diff:.1e})"))

    # D25: quote Orbis = quote Eurostat
    q = d25_e[d25_e["variabile"].isin(["gross_output", "occupazione"])]
    p = q.pivot_table(index=["variabile", "paese", "anno", "classe_armonizzata"],
                      columns="fonte_dati", values="quota").dropna()
    err = float((p["Orbis"] - p["Eurostat-SBS"]).abs().max())
    esiti.append(controlla("D25: quote Orbis = quote Eurostat (costruzione)", err < 1e-6,
                           f"(errore massimo {err:.1e}, {len(p)} celle)"))

    # D25: quote Eurostat 2006 vs quote Eurostat pubblicate dagli autori
    aut = pd.read_csv(os.path.join(QUI, "autori_D25.csv"))
    aut = aut[aut["fonte"] == "Eurostat-SBS"]
    aut["variabile"] = aut["pannello"]
    es = cc.Eurostat(QUI)
    tutti = es.classi["paese"].unique()
    finto = pd.DataFrame({"paese": tutti, "anno": 2006, "nace": "C", "classe": "1-19",
                          "campione": "Totale", "n_imprese": 1.0, "opre_meur": 1.0,
                          "empl": 1.0, "costi_meur": 1.0})
    d25_all = cc.distribuzione_dimensionale(finto, es, [2006], "r11")
    m = d25_all[d25_all["fonte_dati"] == "Eurostat-SBS"].merge(
        aut, left_on=["variabile", "paese", "anno", "classe_armonizzata"],
        right_on=["variabile", "paese", "anno", "classe"])
    m["diff"] = (m["quota"] - m["quota_autori"]).abs()
    print(f"\nConfronto quote Eurostat 2006 (manifattura, NACE Rev.1.1 D) con Tab. D.2.5 "
          f"degli autori: {len(m)} celle, differenza media {m['diff'].mean():.4f}, "
          f"massima {m['diff'].max():.3f}")
    print(m.sort_values("diff", ascending=False)
          [["variabile", "paese", "classe_armonizzata", "quota", "quota_autori", "diff"]]
          .head(8).round(3).to_string(index=False))
    esiti.append(controlla("D25: benchmark Eurostat 2006 = valori Eurostat degli autori",
                           (m["diff"] <= 0.025).mean() >= 0.95,
                           f"({(m['diff'] <= 0.015).mean():.0%} delle celle entro 0.015)"))

    print(f"\nRisultato: {sum(esiti)}/{len(esiti)} controlli superati")
    print(f"Output tabelle: {OUT} (console in output_console.txt)")
    return all(esiti)


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
