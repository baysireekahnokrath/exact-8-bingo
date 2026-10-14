"""Logo boards and hang-tag mockups for the five alternative directions (outlined SVG)."""
import math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, "logo"))
from options import OPTIONS
from textpath import text_path

OUT = os.path.join(HERE, "svg"); os.makedirs(OUT, exist_ok=True)
DIE03 = os.path.join(ROOT, "..", "diecut-leather-20261014", "svg", "03-capsule-cross.svg")

def text(t, size, x, y, fill, font, tracking=0.0, anchor="middle"):
    d, w, (x0, y0, x1, y1) = text_path(t, size, font, tracking)
    if anchor == "middle":
        x -= (x0 + x1) / 2
    return f'<path transform="translate({x:.2f},{y:.2f})" d="{d}" fill="{fill}"/>'

# Marks are drawn in a 100 x 100 box centred on 0,0.
def mark_remnant(o):
    scrap = "M-38,-30 L22,-42 Q34,-44 38,-32 L44,18 Q46,32 32,36 L-24,44 Q-40,46 -42,30 L-46,-18 Q-47,-28 -38,-30 Z"
    return (f'<path d="{scrap}" fill="none" stroke="{o["fg"]}" stroke-width="3"/>'
            f'<line x1="-18" y1="2" x2="18" y2="-2" stroke="{o["acc"]}" stroke-width="4" stroke-linecap="round"/>')

def mark_unsewn(o):
    return (f'<path d="M-20,46 L-20,-12 Q-20,-34 0,-34 Q20,-34 20,-12 L20,46" fill="none" stroke="{o["fg"]}" stroke-width="3.2"/>'
            f'<line x1="-36" y1="4" x2="36" y2="4" stroke="{o["acc"]}" stroke-width="4" stroke-linecap="round"/>'
            f'<line x1="-46" y1="46" x2="46" y2="46" stroke="{o["fg"]}" stroke-width="3.2" stroke-linecap="round"/>')

def mark_interlock(o):
    s = open(DIE03).read()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    cut = re.search(r'<g id="CUT"[^>]*>(.*?)</g>', s, re.S).group(1)
    sl = re.search(r'<g id="SLIT"[^>]*>(.*?)</g>', s, re.S).group(1)
    return (f'<svg x="-48" y="-48" width="96" height="96" viewBox="{vb}">'
            f'<g fill="none" stroke="{o["fg"]}" stroke-width="2.4">{cut}</g>'
            f'<g stroke="{o["acc"]}" stroke-width="3.4" stroke-linecap="round">{sl}</g></svg>')

def mark_aftercut(o):
    return (f'<path d="M0,-48 C34,-26 34,24 0,48 C-34,24 -34,-26 0,-48 Z" fill="{o["acc"]}"/>'
            f'<line x1="0" y1="-26" x2="0" y2="26" stroke="{o["bg"]}" stroke-width="4" stroke-linecap="round"/>')

def mark_quint(o):
    g = [f'<circle r="46" fill="none" stroke="{o["acc"]}" stroke-width="2.4"/>']
    for k in range(5):
        a = math.radians(-90 + 72 * k)
        g.append(f'<line x1="{16*math.cos(a):.2f}" y1="{16*math.sin(a):.2f}" x2="{34*math.cos(a):.2f}" y2="{34*math.sin(a):.2f}" '
                 f'stroke="{o["fg"]}" stroke-width="4" stroke-linecap="round"/>')
    return "".join(g)

MARKS = dict(remnant=mark_remnant, unsewn=mark_unsewn, interlock=mark_interlock, aftercut=mark_aftercut, quint=mark_quint)

def mark_khad(o):
    """Three strips woven over and under: สานขัด."""
    b = o["bg"]
    return (f'<rect x="-31" y="-46" width="24" height="92" rx="12" fill="{o["fg"]}"/>'
            f'<rect x="-46" y="-12" width="92" height="24" rx="12" fill="{o["acc"]}" stroke="{b}" stroke-width="5"/>'
            f'<rect x="7" y="-46" width="24" height="92" rx="12" fill="{o["fg"]}" stroke="{b}" stroke-width="5"/>')

def mark_sansfil(o):
    return (f'<path d="M-40,40 L28,-28 Q36,-38 42,-42 Q38,-36 28,-28" fill="none" stroke="{o["fg"]}" stroke-width="5" stroke-linecap="round"/>'
            f'<ellipse cx="30" cy="-30" rx="7" ry="2.4" transform="rotate(-45 30 -30)" fill="{o["bg"]}"/>'
            f'<circle cx="-40" cy="40" r="3" fill="{o["acc"]}"/>')

def mark_pointfive(o):
    t = text(".5", 84, 0, 22, o["fg"], o["font"][0])
    return (t + f'<line x1="-30" y1="40" x2="30" y2="40" stroke="{o["acc"]}" stroke-width="2.5"/>'
            f'<line x1="-30" y1="32" x2="-30" y2="48" stroke="{o["acc"]}" stroke-width="2.5"/>'
            f'<line x1="30" y1="32" x2="30" y2="48" stroke="{o["acc"]}" stroke-width="2.5"/>')

def mark_praneet(o):
    g = []
    for k in range(5):
        a = -90 + 72 * k
        g.append(f'<ellipse cx="0" cy="-24" rx="11" ry="22" transform="rotate({a + 90})" fill="{o["acc"]}"/>')
    g.append(f'<circle r="8" fill="{o["bg"]}"/><circle r="4" fill="{o["fg"]}"/>')
    return "".join(g)

def mark_monohide(o):
    return (f'<circle r="44" fill="none" stroke="{o["fg"]}" stroke-width="3.2"/>'
            f'<line x1="-15" y1="0" x2="15" y2="0" stroke="{o["acc"]}" stroke-width="4.5" stroke-linecap="round"/>')

MARKS.update(khad=mark_khad, sansfil=mark_sansfil, pointfive=mark_pointfive, praneet=mark_praneet, monohide=mark_monohide)

def mark_lamiad(o):
    return mark_praneet(o)

def mark_benja(o):
    g = []
    for k, c in enumerate(o["petals"]):
        g.append(f'<ellipse cx="0" cy="-24" rx="11" ry="22" transform="rotate({72 * k})" fill="{c}"/>')
    g.append(f'<circle r="8" fill="{o["bg"]}"/><circle r="4" fill="{o["acc"]}"/>')
    return "".join(g)

def mark_banjong(o):
    return (f'<rect x="-44" y="-44" width="88" height="88" rx="14" fill="none" stroke="{o["fg"]}" stroke-width="2"/>'
            f'<path d="M-16,26 L-16,-4 Q-16,-22 0,-22 Q16,-22 16,-4 L16,26" fill="none" stroke="{o["fg"]}" stroke-width="3"/>'
            f'<line x1="-28" y1="4" x2="28" y2="4" stroke="{o["acc"]}" stroke-width="4" stroke-linecap="round"/>')

def mark_kanok(o):
    return (f'<path d="M-4,46 C-34,30 -36,-6 -12,-28 C-6,-34 -2,-42 -6,-50 C18,-38 32,-14 22,10 '
            f'C16,24 4,24 2,14 C0,4 10,-2 8,-14 C-4,-4 -14,12 -8,30 C-6,38 -6,42 -4,46 Z" fill="{o["acc"]}"/>')

def mark_hattha(o):
    """Four fingers and a thumb on a gold palm line: five pairs of hands."""
    g = [f'<rect x="-36" y="10" width="12" height="36" rx="6" transform="rotate(-38 -30 40)" fill="{o["fg"]}"/>']
    for x, h in ((-13, 64), (2, 74), (17, 66), (32, 50)):
        g.append(f'<rect x="{x-6}" y="{38-h}" width="12" height="{h}" rx="6" fill="{o["fg"]}"/>')
    g.append(f'<rect x="-30" y="34" width="68" height="12" rx="6" fill="{o["acc"]}"/>')
    return "".join(g)

MARKS.update(lamiad=mark_lamiad, benja=mark_benja, banjong=mark_banjong, kanok=mark_kanok, hattha=mark_hattha)

def svg(w, h, body, bg):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>')

def board(o):
    W, H = 1200, 720
    m = f'<g transform="translate(600,190) scale(1.7)">{MARKS[o["key"]](o)}</g>'
    size = 116 if len(o["name"]) <= 7 else 96
    if o.get("thai_first"):
        t1 = text(o["th"], 150, 600, 450, o["fg"], o["thfont"][0])
        t2 = text(o["name"], 38, 600, 525, o["acc"], o["font"][0], o["tracking"])
        t3 = text(o["tag_th"], 34, 600, 615, o["fg"], o.get("thbody", o["thfont"])[0])
        return svg(W, H, m + t1 + t2 + t3, o["bg"])
    t1 = text(o["name"], size, 600, 440, o["fg"], o["font"][0], o["tracking"])
    t2 = text(o["th"], 34, 600, 515, o["acc"], o["thfont"][0])
    t3 = text(o["tag_en"], 32, 600, 612, o["fg"], o["font"][0], .04)
    return svg(W, H, m + t1 + t2 + t3, o["bg"])

def tag(o):
    """Hang tag 500 x 800 with a punched hole, the way it would hang on a product."""
    W, H = 560, 860
    h = o["heroes"][0]
    shape = (f'<path d="M80,40 H480 Q520,40 520,80 V780 Q520,820 480,820 H80 Q40,820 40,780 V80 Q40,40 80,40 Z" fill="{o["bg"]}"/>'
             f'<circle cx="280" cy="100" r="16" fill="#E7E3DC"/><circle cx="280" cy="100" r="16" fill="none" stroke="{o["acc"]}" stroke-width="2"/>')
    m = f'<g transform="translate(280,250) scale(1.05)">{MARKS[o["key"]](o)}</g>'
    size = 58 if len(o["name"]) <= 7 else 48
    body = [shape, m,
            (text(o["th"], 76, 280, 405, o["fg"], o["thfont"][0]) if o.get("thai_first")
             else text(o["name"], size, 280, 400, o["fg"], o["font"][0], o["tracking"] * .8)),
            f'<line x1="120" y1="450" x2="440" y2="450" stroke="{o["acc"]}" stroke-width="1.5"/>',
            text(h["name"], 34, 280, 520, o["fg"], o.get("thbody", o["thfont"])[0]),
            text(f"{h['price']:,} THB", 44, 280, 600, o["acc"], o["font"][0], .06),
            text("ทำจากเศษหนังแท้ · ไม่มีด้าย · ไม่มีกาว", 22, 280, 690, o["fg"], o.get("thbody", o["thfont"])[0]),
            text("No. 001 / 100", 22, 280, 740, o["fg"], o["font"][0], .1)]
    return svg(W, H, "".join(body), "#E7E3DC")

if __name__ == "__main__":
    for o in OPTIONS:
        open(os.path.join(OUT, f"{o['key']}-board.svg"), "w").write(board(o))
        open(os.path.join(OUT, f"{o['key']}-tag.svg"), "w").write(tag(o))
    print("built", len(OPTIONS) * 2)
