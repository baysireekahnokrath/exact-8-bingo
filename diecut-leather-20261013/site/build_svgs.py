"""Emit inline <svg> snippets (theme-aware strokes) for the summary page."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import generate as g

out = {}
for p in g.P:
    W, H = p["W"], p["H"]
    lines = "".join(f'<line x1="{s[1][0]:.2f}" y1="{H-s[1][1]:.2f}" x2="{s[2][0]:.2f}" y2="{H-s[2][1]:.2f}"/>' for s in p["slits"])
    out[p["code"]] = (f'<svg viewBox="-2 -2 {W+4} {H+4}" role="img" aria-label="Pattern {p["code"]} {p["name"]}">'
                      f'<path class="cut" d="{g.svg_path(p["cut"], H)}"/><g class="slit">{lines}</g></svg>')
json.dump(out, open(sys.argv[1], "w"))
