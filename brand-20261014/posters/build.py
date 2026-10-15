"""How-to posters for the 30 products: 1080x1350 feed post and 1080x1920 story/TikTok cover.

python3 posters/build.py   -> posters/html/*.html and posters/jobs.json
node tools/render.mjs posters/jobs.json -> posters/png/*.png
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from brand import BRAND, SUB, C, PRODUCTS

REPO = os.path.dirname(ROOT)
PAT = os.path.join(REPO, "diecut-leather-20261014", "svg")
STRAP = os.path.join(REPO, "diecut-leather-20261013", "assembly-01")
ICON_SRC = {"01": "01-bear-head.svg", "02": "02-pinwheel-4-lobe.svg", "03": "03-capsule-cross.svg",
            "04": "04-rounded-square-diagonal.svg", "05": "05-circle.svg", "06": "06-soft-cross.svg"}
ACCENT = {"01": "pink", "02": "pink", "03": "mint", "04": "sun", "05": "tomato", "06": "cobalt"}

def icon(code, fill, slit):
    if code.startswith("01-S"):
        f = os.path.join(STRAP, "01S-heart-strap-%s.svg" % code[-3:])
    else:
        f = os.path.join(PAT, ICON_SRC[code])
    s = open(f).read()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    cut = re.search(r'<g id="CUT"[^>]*>(.*?)</g>', s, re.S).group(1)
    sl = re.search(r'<g id="SLIT"[^>]*>(.*?)</g>', s, re.S).group(1)
    x, y, w, h = (float(v) for v in vb.split())
    rot = ""
    if code == "01":       # stand the bear upright, as in the logo
        rot = ' transform="rotate(-45 41.685 62.675)"'
        x, y, w, h = -6.355, 14.635, 96.08, 89.72
    pad = max(w, h) * .04
    return (f'<svg viewBox="{x-pad} {y-pad} {w+2*pad} {h+2*pad}"><g{rot}><g fill="{fill}" fill-rule="evenodd" stroke="none">{cut}</g>'
            f'<g stroke="{slit}" stroke-width="{max(w,h)*.022:.2f}" stroke-linecap="round" fill="none">{sl}</g></g></svg>')

def _logo(f, vb=None):
    s = re.sub(r'<title>.*?</title>', '', open(os.path.join(ROOT, "logo", "svg", f)).read())
    s = re.sub(r' width="[\d.]+" height="[\d.]+"', '', s, count=1)
    return re.sub(r'viewBox="[^"]+"', f'viewBox="{vb}"', s, count=1) if vb else s

MARK = _logo("mark.svg")
WORD = _logo("oct-wordmark.svg")
FONTS = os.path.join(ROOT, "fonts")

# Golden layout: every size is a Fibonacci number (13 21 34 55 89 144 233 377) or phi-derived.
CSS = """
@font-face{font-family:Mitr;font-weight:500;src:url(FONTS/Mitr-Medium.ttf)}
@font-face{font-family:Mitr;font-weight:600;src:url(FONTS/Mitr-SemiBold.ttf)}
@font-face{font-family:Anuphan;font-weight:500;src:url(FONTS/alt/Anuphan-Medium.ttf)}
@font-face{font-family:Jost;font-weight:500;src:url(FONTS/alt/Jost-Medium.ttf)}
@font-face{font-family:Plex;font-weight:400;src:url(FONTS/IBMPlexSansThai-Regular.ttf)}
@font-face{font-family:Plex;font-weight:600;src:url(FONTS/IBMPlexSansThai-SemiBold.ttf)}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:WPX;height:HPX;background:CREAM;color:COCOA;font-family:Plex,sans-serif;overflow:hidden}
.page{position:relative;width:WPX;height:HPX;padding:TOPpx 89px BOTpx;display:flex;flex-direction:column}
.band{position:absolute;left:0;right:0;top:0;height:13px;background:ACC}
.head{display:flex;align-items:center;justify-content:space-between;font-family:HEADF;font-weight:500;font-size:34px;height:55px}
.brand{display:flex;align-items:center;gap:13px}.brand svg{width:55px;height:55px}.brand svg.word{width:233px;height:auto}
.brand small{display:block;font-size:21px;color:CARAMEL;font-family:Jost;letter-spacing:.06em}
.tag{background:ACC;color:TAGFG;border-radius:34px;padding:8px 21px;font-size:21px;letter-spacing:.12em;font-family:Jost;font-weight:500}
h1{font-family:HEADF;font-weight:600;font-size:TITLEpx;line-height:1.236;margin-top:GAP1px}
.hook{font-size:34px;line-height:1.5;margin-top:13px;color:MUTED}
.label{font-family:HEADF;font-weight:500;font-size:21px;color:CARAMEL;margin-top:GAP2px;letter-spacing:.06em}
.row{display:flex;align-items:center;gap:34px}.row>div:first-child{flex:1}
.pieces{display:flex;gap:34px;margin-top:13px;align-items:flex-end;flex-wrap:wrap}
.pc{display:flex;flex-direction:column;align-items:center;gap:8px}
.pc svg{height:ICONpx;width:auto;max-width:233px}
.pc .q{font-family:Jost;font-weight:500;font-size:34px}
.pc .n{font-size:21px;color:MUTED}
.steps{margin-top:GAP2px;display:flex;flex-direction:column;gap:STEPGAPpx}
.st{display:flex;align-items:center;gap:21px;background:#fff;border-radius:21px;padding:21px}
.st b{flex:none;width:55px;height:55px;border-radius:50%;background:ACC;color:TAGFG;font-family:Jost;font-weight:500;
      font-size:34px;display:flex;align-items:center;justify-content:center}
.st span{font-size:34px;line-height:1.3}
.foot{margin-top:auto;display:flex;align-items:center;justify-content:space-between}
.price{flex:none;width:233px;height:233px;border-radius:50%;background:HEART;color:#fff;display:flex;flex-direction:column;
       align-items:center;justify-content:center;font-family:Jost;font-weight:500}
.price b{font-size:89px;font-weight:500;line-height:1}.price i{font-style:normal;font-size:21px;font-family:Plex}
.claims{font-family:HEADF;font-weight:500;font-size:21px;line-height:1.5;display:flex;justify-content:space-between;width:100%;border-top:2px solid LINE;padding-top:21px}
.claims small{font-family:Jost;font-weight:500;font-size:21px;color:MUTED;letter-spacing:.04em}
"""


def page(p, W, H, vertical):
    love = p["coll"] == "love"
    if love:      # ห้าหมี FIVE BEARS · Love: pink, Mitr
        T = dict(BG=C["paper"], INK=C["ink"], ACC=C["pink"], TAGFG=C["ink"],
                 CARAMEL=C["tomato"], PRICE=C["tomato"], HEADF="Mitr", MUTED="#4A4A55", LINE="#F1DCCB")
        fill = C["leather"]
        brand = f'{MARK}<span>{SUB["th"]} · {SUB["en"]}<small>{SUB["by"]}</small></span>'
        coll, shop = "LOVE", "Shopee OCT. 26 · หมวดห้าหมี"
    else:         # OCT. 26 · SOI. 02: cobalt, Anuphan
        T = dict(BG=C["paper"], INK=C["ink"], ACC=C["cobalt"], TAGFG="#fff",
                 CARAMEL=C["cobalt"], PRICE=C["tomato"], HEADF="Anuphan", MUTED="#4A4A55", LINE="#F1DCCB")
        fill = C["leather"]
        brand = WORD.replace("<svg ", '<svg class="word" ', 1)
        coll, shop = "SOI. 02", "Shopee OCT. 26"
    sub = dict(WPX=f"{W}px", HPX=f"{H}px", CREAM=T["BG"], COCOA=T["INK"], ACC=T["ACC"], TAGFG=T["TAGFG"],
               CARAMEL=T["CARAMEL"], HEART=T["PRICE"], HEADF=T["HEADF"], MUTED=T["MUTED"], LINE=T["LINE"],
               FONTS="file://" + FONTS,
               TOP="233" if vertical else "55", BOT="377" if vertical else "55",
               TITLE="89" if len(p["name"]) < 16 else "68" if len(p["name"]) < 22 else "55", GAP1="34" if vertical else "21",
               GAP2="55" if vertical else "34", ICON="144" if vertical else "89", STEPGAP="21" if vertical else "13")
    css = CSS
    for k in sorted(sub, key=len, reverse=True):
        css = css.replace(k, sub[k])
    pcs = "".join(f'<div class="pc">{icon(code, fill, T["BG"])}<div class="q">× {q}</div>'
                  f'<div class="n">แบบ {code.replace("-S", "-S ")}</div></div>' for code, q in p["parts"])
    if p["extra"]:
        pcs += f'<div class="pc"><div class="q" style="font-size:30px;max-width:260px;text-align:center">+ {p["extra"][0]}</div></div>'
    steps = "".join(f'<div class="st"><b>{i}</b><span>{s}</span></div>' for i, s in enumerate(p["steps"], 1))
    return f"""<!doctype html><html lang="th"><head><meta charset="utf-8"><style>{css}</style></head><body>
<div class="page"><div class="band"></div>
<div class="head"><div class="brand">{brand}</div><div class="tag">{coll} · HOW TO {p['n']:02d}</div></div>
<h1>{p['name']}</h1><p class="hook">{p['hook']}</p>
<div class="row"><div><div class="label">ใช้ชิ้นหนัง</div><div class="pieces">{pcs}</div></div>
<div class="price"><b>{p['price']}</b><i>บาท</i></div></div>
<div class="label">วิธีต่อ ไม่ต้องเย็บ</div><div class="steps">{steps}</div>
<div class="foot"><div class="claims"><span>หนังแท้ · ไม่เย็บ · ไม่ใช้กาว</span><small>@{BRAND['handle']} · {shop}</small></div></div>
</div></body></html>"""

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "html"), exist_ok=True); os.makedirs(os.path.join(HERE, "png"), exist_ok=True)
    jobs = []
    for p in PRODUCTS:
        for tag, W, H, v in (("post", 1080, 1350, False), ("story", 1080, 1920, True)):
            name = f"{p['n']:02d}-{tag}"
            open(os.path.join(HERE, "html", name + ".html"), "w").write(page(p, W, H, v))
            jobs.append(dict(src=os.path.join(HERE, "html", name + ".html"), out=os.path.join(HERE, "png", name + ".png"), w=W, h=H))
    json.dump(jobs, open(os.path.join(HERE, "jobs.json"), "w"), indent=0)
    print(len(jobs), "posters")
