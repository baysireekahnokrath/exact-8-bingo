"""Build site/index.html (rev 20261014 summary page) from site/template.html."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from extract import load
from generate import svg_d, SRC, final_slits

SPECS = {
    "01": ("Bear head", ["หน้า R41.68 · หู R12.68 × 2", "slit 17.27 × 2 แนวตั้งและแนวนอน"]),
    "02": ("Pinwheel", ["4 กลีบ R29.37", "slot 27.0 × 4 วนแบบกังหัน"]),
    "03": ("Capsule cross", ["สี่เหลี่ยม 45 · ปีก R22.5", "slit 23.0 × 2 · slot 11.25 × 4"]),
    "04": ("Rounded square", ["มุม R5", "slit 30.5 × 2 · slot 16.8–16.9 × 4"]),
    "05": ("Circle", ["Ø90", "slit 30.5 × 2 · slot 17.7 × 2 และ 16.0 × 2"]),
    "06": ("Soft cross", ["กลีบวงรี 35.4 × 29.4 · โค้งเว้า R12.62", "slit 18.0 × 2 · slot 8.94 × 4"]),
}

IDEAS_LINK = 'ใช้แบบชุดนี้ทั้งหมด ไม่ต้องแก้แบบ · <a href="https://claude.ai/artifact/EboiyQ9wdsMx98uk7zkCZn">ดู 20 ไอเดียสินค้า</a>'

def main():
    plates = []
    for p in load(SRC):
        W, H = p["W"], p["H"]
        lines = "".join(f'<line x1="{a[0]:.2f}" y1="{H-a[1]:.2f}" x2="{b[0]:.2f}" y2="{H-b[1]:.2f}"/>' for a, b in ((s["a"], s["b"]) for s in final_slits(p)))
        svg = (f'<svg viewBox="-2 -2 {W+4:.2f} {H+4:.2f}" role="img" aria-label="Pattern {p["code"]} {p["name"]}">'
               f'<path class="cut" d="{svg_d(p["segs"], H)}"/><g class="slit">{lines}</g></svg>')
        name, bullets = SPECS[p["code"]]
        li = "".join(f"<li>{b}</li>" for b in bullets)
        plates.append(f'<article class="plate">{svg}<header><h3>{name}</h3><span class="code">{p["code"]}</span></header>'
                      f'<span class="size">{W:.2f} × {H:.2f} mm</span><ul>{li}</ul></article>')
    t = open(os.path.join(HERE, "template.html")).read().replace("__PLATES__", "\n    ".join(plates))
    t = t.replace("__IDEAS_LINK__", IDEAS_LINK)
    open(os.path.join(HERE, "index.html"), "w").write(t)
    print("ok")

if __name__ == "__main__":
    main()
