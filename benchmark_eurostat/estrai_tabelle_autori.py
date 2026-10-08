#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
estrai_tabelle_autori.py
========================

Trascrive dalle pagine (ruotate di 90 gradi) dell'Online Appendix di
Kalemli-Özcan et al. (2024) le tabelle di copertura pubblicate dagli autori:

  autori_D11.csv  Tab. D.1.1  copertura economia aggregata, gross output (p. 69)
  autori_D21.csv  Tab. D.2.1  manifattura, gross output, Total sample  (p. 72)
  autori_D22.csv  Tab. D.2.2  manifattura, gross output, TFP sample    (p. 73)
  autori_D23.csv  Tab. D.2.3  manifattura, occupazione, Total sample   (p. 74)
  autori_D24.csv  Tab. D.2.4  manifattura, occupazione, TFP sample     (p. 75)
  autori_D25.csv  Tab. D.2.5  distribuzione dimensionale manifattura 2006 (p. 76)
  autori_D31.csv  Tab. D.3.1  numero di imprese vs Eurostat-BD (p. 78, trascritta
                  a mano: la pagina non e' ruotata e ha solo 10 righe)

Metodo: pdfplumber legge i caratteri ruotati; ogni riga della tabella ha la
stessa coordinata x; i numeri vengono assegnati alla colonna-paese la cui
intestazione ha il centro piu' vicino (tolleranza 9 pt). Le celle vuote nella
tabella pubblicata NON compaiono nel CSV (oppure hanno valore vuoto se nel PDF
c'e' un '.'). I valori sono stati controllati a campione rendendo le pagine in
PNG (pdftoppm) e confrontandole visivamente.

Uso:
  python3 estrai_tabelle_autori.py PERCORSO_APPENDIX.pdf
"""
import csv
import os
import sys

import pdfplumber

QUI = os.path.dirname(os.path.abspath(__file__))


def righe_ruotate(pagina):
    """Raggruppa i caratteri ruotati per riga (stessa x) e li unisce in token
    (inizio, fine, testo) lungo la direzione di lettura."""
    chars = [c for c in pagina.chars if not c.get("upright")]
    righe = {}
    for c in chars:
        x = round(c["x0"] * 2) / 2
        k = next((kk for kk in righe if abs(kk - x) <= 1.5), None)
        if k is None:
            k = x
            righe[k] = []
        righe[k].append(c)
    out = []
    H = pagina.height
    for k in sorted(righe):
        cs = sorted(righe[k], key=lambda c: -c["top"])
        toks, cur, inizio, fine = [], "", None, None
        for c in cs:
            s, e = H - c["bottom"], H - c["top"]
            if cur and s - fine > 1.5:
                toks.append((inizio, fine, cur))
                cur = ""
            if not cur:
                inizio = s
            cur += c["text"]
            fine = e
        if cur:
            toks.append((inizio, fine, cur))
        out.append(toks)
    return out


def centro(t):
    return (t[0] + t[1]) / 2


def tabella_anni(pdf, pagina, tabella, descr):
    """Tabelle con righe = anni (piu' 'Average') e colonne = paesi."""
    out = []
    intest = None
    for toks in righe_ruotate(pdf.pages[pagina - 1]):
        if not toks:
            continue
        primo = toks[0][2]
        if primo == "Year":
            intest = [(centro(t), t[2]) for t in toks[1:]]
            continue
        if intest and ((primo.isdigit() and len(primo) == 4) or primo == "Average"):
            for t in toks[1:]:
                c = centro(t)
                best = min(intest, key=lambda h: abs(h[0] - c))
                if abs(best[0] - c) > 9:
                    raise ValueError(f"p.{pagina}: token non assegnabile {t}")
                out.append({"tabella": tabella, "descrizione": descr,
                            "paese": best[1],
                            "anno": primo if primo != "Average" else "Media",
                            "copertura_autori": "" if t[2] == "." else t[2],
                            "pagina": pagina})
    return out


def tabella_d25(pdf, pagina=76):
    out = []
    intest, pannello, fonte = None, None, None
    for toks in righe_ruotate(pdf.pages[pagina - 1]):
        if not toks:
            continue
        testo = " ".join(t[2] for t in toks)
        if testo.startswith("Panel A"):
            pannello = "gross_output"
            continue
        if testo.startswith("Panel B"):
            pannello = "occupazione"
            continue
        if toks[0][2] == "AT":
            intest = [(centro(t), t[2]) for t in toks]
            continue
        if testo.startswith("Orbis-Amadeus"):
            fonte = "Orbis-Amadeus"
            continue
        if testo.startswith("Eurostat-SBS"):
            fonte = "Eurostat-SBS"
            continue
        if intest and "employees" in testo:
            etich = []
            valori = []
            for t in toks:
                if t[2][0].isdigit() and "." in t[2]:
                    valori.append(t)
                else:
                    etich.append(t[2])
            classe = {"1 to 19 employees": "1-19", "0 to 19 employees": "0-19",
                      "20 to 249 employees": "20-249",
                      "250 + employees": "250+"}[" ".join(etich)]
            for t in valori:
                c = centro(t)
                best = min(intest, key=lambda h: abs(h[0] - c))
                if abs(best[0] - c) > 9:
                    raise ValueError(f"p.{pagina}: token non assegnabile {t}")
                out.append({"tabella": "D.2.5", "pannello": pannello,
                            "fonte": fonte, "paese": best[1], "anno": 2006,
                            "classe": classe, "quota_autori": t[2],
                            "pagina": pagina})
    return out


# Tabella D.3.1 (p. 78): trascrizione manuale, valori in percentuale
D31 = [
    ("BE", "Belgium", 2008, 26.5, 59.9),
    ("EE", "Estonia", 2007, 65.9, 73.4),
    ("FR", "France", 2009, 30.6, 83.5),
    ("DE", "Germany", 2008, 3.1, 66.6),
    ("HU", "Hungary", 2007, 3.6, 52.2),
    ("IT", "Italy", 2008, 2.2, 60.5),
    ("PL", "Poland", 2007, 1.2, 15.6),
    ("SK", "Slovakia", 2008, 12.8, 41.6),
    ("SI", "Slovenia", 2007, 28.4, 25.3),
    ("ES", "Spain", 2008, 23.6, 42.9),
]


def scrivi(nome, righe, campi):
    with open(os.path.join(QUI, nome), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campi)
        w.writeheader()
        for r in righe:
            w.writerow(r)
    print(f"{nome}: {len(righe)} righe")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    pdf = pdfplumber.open(sys.argv[1])
    campi = ["tabella", "descrizione", "paese", "anno", "copertura_autori", "pagina"]
    spec = [
        ("autori_D11.csv", 69, "D.1.1", "Economia aggregata, gross output (OPRE / SBS V12110), settori comuni"),
        ("autori_D21.csv", 72, "D.2.1", "Manifattura, gross output, Total sample"),
        ("autori_D22.csv", 73, "D.2.2", "Manifattura, gross output, TFP sample"),
        ("autori_D23.csv", 74, "D.2.3", "Manifattura, occupazione, Total sample"),
        ("autori_D24.csv", 75, "D.2.4", "Manifattura, occupazione, TFP sample"),
    ]
    for nome, pag, tab, descr in spec:
        scrivi(nome, tabella_anni(pdf, pag, tab, descr), campi)
    scrivi("autori_D25.csv", tabella_d25(pdf),
           ["tabella", "pannello", "fonte", "paese", "anno", "classe",
            "quota_autori", "pagina"])
    scrivi("autori_D31.csv",
           [{"tabella": "D.3.1", "paese": p, "nome_paese": n, "anno": a,
             "compnet_pct": c, "bvd_orbis_pct": b, "pagina": 78}
            for p, n, a, c, b in D31],
           ["tabella", "paese", "nome_paese", "anno", "compnet_pct",
            "bvd_orbis_pct", "pagina"])


if __name__ == "__main__":
    main()
