"""Build site/index.html (project summary page) from site/template.html."""
import os, subprocess, sys, json, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import generate as g

SPECS = {
    "01": ("Bear head", ["หน้า R41.5 · หู R12.5", "slit 17 mm × 2 เอียง 45°"]),
    "02": ("Pinwheel", ["4 กลีบ R29.25", "slot 29.25 mm × 4 วนแบบกังหัน"]),
    "03": ("Capsule cross", ["สี่เหลี่ยม 45 · ปีก R22.5", "slit 30 × 2 · slot 14 × 4"]),
    "04": ("Rounded square", ["มุม R5 · พับเป็นข้าวหลามตัด", "slit 30 × 2 · slot 15 × 4"]),
    "05": ("Circle", ["Ø90 · พับเป็นสี่เหลี่ยม 63.6", "slit 30 × 2 · slot 15 × 4"]),
    "06": ("Soft cross", ["กลีบ R16 · โค้งเว้า R16", "slit 15 × 2 · slot 5 × 4"]),
}

def main():
    tmp = os.path.join(tempfile.mkdtemp(), "svgs.json")
    subprocess.run([sys.executable, os.path.join(HERE, "build_svgs.py"), tmp], check=True)
    sv = json.load(open(tmp))
    plates = []
    for p in g.P:
        name, bullets = SPECS[p["code"]]
        li = "".join(f"<li>{b}</li>" for b in bullets)
        plates.append(f'<article class="plate">{sv[p["code"]]}<header><h3>{name}</h3><span class="code">{p["code"]}</span></header>'
                      f'<span class="size">{p["W"]} × {p["H"]} mm</span><ul>{li}</ul></article>')
    t = open(os.path.join(HERE, "template.html")).read().replace("__PLATES__", "\n    ".join(plates))
    open(os.path.join(HERE, "index.html"), "w").write(t)
    print("ok")

if __name__ == "__main__":
    main()
