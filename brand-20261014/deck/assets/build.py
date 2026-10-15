"""Deck-only drawings in the brand's geometric letters. python3 deck/assets/build.py -> deck/assets/*.svg (+ PNG via tools/render.mjs)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "logolab"))
import geometry as G
from brand import C

def plate(text, ink, dot, cap, name):
    s, w = G.word(text, ink, dot, name)
    k = cap / G.H; pad = cap / G.PHI ** 2
    W, H = round(w * k + 2 * pad), round(cap + 2 * pad)
    open(os.path.join(HERE, name + ".svg"), "w").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><title>{text}</title>'
        f'<g transform="translate({pad:.2f},{pad + cap:.2f}) scale({k:.5f})">{s}</g></svg>')
    return {"src": f"deck/assets/{name}.svg", "out": f"deck/assets/{name}.png", "w": W, "h": H, "transparent": True}

jobs = [plate("26.10", C["paper"], C["tomato"], 233, "date-2610"),        # cap 233 px on a 1080 slide (Fibonacci)
        plate("OCT. 26", C["ink"], C["tomato"], 144, "name-oct26")]
json.dump(jobs, open(os.path.join(HERE, "jobs.json"), "w"), indent=1)
print(len(jobs), "plates")
