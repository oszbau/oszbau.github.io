"""Erzeugt die Übersichtsseiten (/, /grs/, /grs/lf2/ …) aus seiten.json.
Aufruf im Wurzelordner des Repos: python3 werkzeug/baue_uebersicht.py"""
import json, os, html
D = json.load(open("seiten.json", encoding="utf-8"))
S = [s for s in D["seiten"] if s["status"] == "online" and s.get("gelistet", True)]
NAMEN = D.get("namen", {})
CSS = ("body{font:18px/1.5 Arial,sans-serif;max-width:40em;margin:1.5em auto;padding:0 1em}"
       "a{display:block;padding:.6em 0;border-bottom:1px solid #ccc;color:#000}small{color:#555}")
def schreibe(ordner, titel, zeilen):
    os.makedirs(ordner or ".", exist_ok=True)
    k = "".join(f'<a href="/{p}/">{html.escape(t)}<br><small>{html.escape(u)}</small></a>' for p, t, u in zeilen)
    with open(os.path.join(ordner, "index.html"), "w", encoding="utf-8") as f:
        f.write('<!doctype html><html lang="de"><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1">'
                f'<title>{html.escape(titel)}</title><style>{CSS}</style><h1>{html.escape(titel)}</h1>{k}</html>')
alle = {s["pfad"].strip("/") for s in D["seiten"]}
kinder = {}
for s in S:
    t = s["pfad"].strip("/").split("/")
    for i in range(len(t)):
        kinder.setdefault("/".join(t[:i]), set()).add("/".join(t[:i + 1]))
for ordner, ks in kinder.items():
    if ordner in alle:
        continue                                   # nie eine Lernseite überschreiben
    zeilen = []
    for k in sorted(ks):
        e = next((s for s in S if s["pfad"].strip("/") == k), None)
        zeilen.append((k, e["titel"] if e else NAMEN.get(k, k.split("/")[-1].upper()),
                       ("Stand " + e["stand"]) if e else ""))
    schreibe(ordner, NAMEN.get(ordner, "Lernseiten") if ordner else D.get("titel", "Lernseiten"), zeilen)
