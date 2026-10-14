"""Build the FIVE BEARS logo set as outlined SVG (no fonts needed by the printer).

The bear is the real die outline of pattern 01, turned 45 degrees so the ears sit on top.
Its two slits become the cheeks. The heart in the middle is Mama Bear.
"""
import math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT); sys.path.insert(0, HERE)
from brand import C, BRAND
from textpath import text_path

OUT = os.path.join(HERE, "svg"); os.makedirs(OUT, exist_ok=True)
SRC = os.path.join(ROOT, "..", "diecut-leather-20261014", "svg", "01-bear-head.svg")

M = (41.685, 62.675)                      # centre of the head circle in the die file (mm)
EARS = [(41.685, 12.675), (91.685, 62.675)]
SLITS = [((11.200, 71.615), (11.200, 53.705)), ((32.745, 93.160), (50.655, 93.160))]
A = math.radians(-45)

def rot(p):
    x, y = p[0] - M[0], p[1] - M[1]
    return (x * math.cos(A) - y * math.sin(A), x * math.sin(A) + y * math.cos(A))

def die_path():
    d = re.search(r'<path d="([^"]+)"', open(SRC).read()).group(1)
    nums = iter(float(v) for v in re.findall(r"-?\d+\.\d+|-?\d+", d))
    out = []
    for tok in re.findall(r"[MCLZ]|-?\d+\.\d+,-?\d+\.\d+|-?\d+\.\d+ -?\d+\.\d+", d):
        if tok in "MCLZ":
            out.append(tok)
        else:
            x, y = (float(v) for v in re.split(r"[ ,]", tok))
            rx, ry = rot((x, y)); out.append(f"{rx:.3f},{ry:.3f}")
    return " ".join(out)

BODY = die_path()

def heart(cx, cy, w):
    s = w / 2
    pts = [(0, .95), (-1.25, .05), (-1.0, -.95), (-.5, -.95), (-.2, -.95), (0, -.72), (0, -.45),
           (0, -.72), (.2, -.95), (.5, -.95), (1.0, -.95), (1.25, .05), (0, .95)]
    q = [f"{cx + x * s:.2f},{cy + y * s:.2f}" for x, y in pts]
    return f"M{q[0]} C{q[1]} {q[2]} {q[3]} C{q[4]} {q[5]} {q[6]} C{q[7]} {q[8]} {q[9]} C{q[10]} {q[11]} {q[12]} Z"

# bounding box of the turned bear: x ±48.04, y -48.04 .. +41.68 (mm in die units)
BX0, BY0, BW, BH = -48.04, -48.04, 96.08, 89.72

def bear(x, y, h, body, heart_c, face=None, detail=True):
    """Bear mark scaled to height h with its top-left at (x, y)."""
    s = h / BH
    face = face or C["cocoa"]
    g = [f'<g transform="translate({x - BX0 * s:.2f},{y - BY0 * s:.2f}) scale({s:.4f})">',
         f'<path d="{BODY}" fill="{body}"/>']
    if detail:
        for e in EARS:
            ex, ey = rot(e); g.append(f'<circle cx="{ex:.2f}" cy="{ey:.2f}" r="6.2" fill="{C["cream"]}" opacity=".55"/>')
        for a, b in SLITS:
            (ax, ay), (bx, by) = rot(a), rot(b)
            g.append(f'<line x1="{ax:.2f}" y1="{ay:.2f}" x2="{bx:.2f}" y2="{by:.2f}" stroke="{C["cream"]}" '
                     f'stroke-width="2.6" stroke-linecap="round" opacity=".8"/>')
        g.append(f'<circle cx="-13.5" cy="-7" r="3.8" fill="{face}"/><circle cx="13.5" cy="-7" r="3.8" fill="{face}"/>')
    g.append(f'<path d="{heart(0, 10.5, 25 if detail else 34)}" fill="{heart_c}"/>')
    g.append("</g>")
    return "".join(g)

def text(t, size, x, y, fill, font="Mitr-SemiBold.ttf", tracking=0.0, anchor="start"):
    d, w, (x0, y0, x1, y1) = text_path(t, size, font, tracking)
    if anchor == "middle":
        x -= (x0 + x1) / 2
    return f'<path transform="translate({x:.2f},{y:.2f})" d="{d}" fill="{fill}"/>', (x1 - x0), (y1 - y0)

def svg(w, h, body, bg=None):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<title>{BRAND["th"]} {BRAND["en"]}</title>{rect}{body}</svg>')

def stacked(fg, bear_c, heart_c, face, bg=None):
    W, H = 600, 640
    b = bear(W / 2 - 190 * BW / BH / 2 * 1, 40, 190, bear_c, heart_c, face)
    t1, _, _ = text(BRAND["th"], 150, W / 2, 420, fg, anchor="middle")
    t2, _, _ = text(BRAND["en"], 44, W / 2, 500, fg, "Mitr-Medium.ttf", tracking=.22, anchor="middle")
    t3, _, _ = text(BRAND["tag_th"], 34, W / 2, 575, bear_c if bg is None else fg, "Mitr-Regular.ttf", anchor="middle")
    return svg(W, H, b + t1 + t2 + t3, bg)

def horizontal(fg, bear_c, heart_c, face, bg=None):
    W, H = 1000, 300
    b = bear(30, 45, 210, bear_c, heart_c, face)
    t1, _, _ = text(BRAND["th"], 150, 290, 185, fg)
    t2, _, _ = text(BRAND["en"], 42, 296, 255, fg, "Mitr-Medium.ttf", tracking=.22)
    return svg(W, H, b + t1 + t2, bg)

def mark(bear_c, heart_c, face, bg=None, pad=40):
    h = 400 - 2 * pad; w = h * BW / BH
    return svg(400, 400, bear((400 - w) / 2, pad + (400 - 2 * pad - h) / 2, h, bear_c, heart_c, face), bg)

def family(bg=None):
    sizes = [("cocoa", 1.0), ("heart", .9), ("honey", .7), ("peach", .64), ("sage", .58)]
    H0 = 220; gap = 18; x = 30; parts = []
    for k, f in sizes:
        h = H0 * f; w = h * BW / BH
        hc = C["cream"] if k == "heart" else C["heart"]
        face = C["cream"] if k == "cocoa" else C["cocoa"]
        parts.append(bear(x, 30 + H0 - h, h, C[k], hc, face)); x += w + gap
    W = x + 12
    t, _, _ = text(BRAND["tag_th"], 46, W / 2, 330, C["cocoa"], "Mitr-Medium.ttf", anchor="middle")
    return svg(round(W), 370, "".join(parts) + t, bg)

def avatar():
    W = 1080; h = 560; w = h * BW / BH
    b = bear((W - w) / 2, 170, h, C["caramel"], C["heart"], C["cocoa"])
    t, _, _ = text(BRAND["en"], 70, W / 2, 900, C["cocoa"], "Mitr-SemiBold.ttf", tracking=.2, anchor="middle")
    return svg(W, W, f'<circle cx="540" cy="540" r="540" fill="{C["cream"]}"/>' + b + t)

def sticker():
    W = 400; h = 190; w = h * BW / BH
    b = bear((W - w) / 2, 70, h, C["cream"], C["heart"], C["cocoa"])
    t, _, _ = text(BRAND["th"], 64, W / 2, 335, C["cream"], anchor="middle")
    return svg(W, W, f'<circle cx="200" cy="200" r="200" fill="{C["caramel"]}"/>' + b + t)

def banner(W, H, safe_w, safe_h):
    """Cover image: family of bears on the left half of the safe area, name and line on the right."""
    sizes = [("cocoa", 1.0), ("heart", .9), ("honey", .7), ("peach", .64), ("sage", .58)]
    unit = sum(f * BW / BH for _, f in sizes) + .06 * 4          # width per 1 px of H0
    H0 = min(safe_h * .62, safe_w * .44 / unit)
    gap = H0 * .06
    cx, cy = (W - safe_w) / 2, (H - safe_h) / 2
    tsize = min(safe_h * .3, safe_w * .2)
    block = H0 * unit + tsize * .25 + tsize * 2.6          # bears + gap + text block width (approx)
    x = cx + max(0, (safe_w - block) / 2)
    base = cy + safe_h / 2 + H0 / 2
    parts = []
    for k, f in sizes:
        h = H0 * f; w = h * BW / BH
        hc = C["cream"] if k == "heart" else C["heart"]
        face = C["cream"] if k == "cocoa" else C["cocoa"]
        parts.append(bear(x, base - h, h, C[k], hc, face)); x += w + gap
    tx = x + tsize * .25
    ty = cy + safe_h / 2
    t1, _, _ = text(BRAND["th"], tsize, tx, ty + tsize * .1, C["cocoa"])
    t2, _, _ = text(BRAND["en"], tsize * .3, tx + tsize * .03, ty + tsize * .55, C["caramel"], "Mitr-Medium.ttf", tracking=.22)
    t3, _, _ = text(BRAND["tag_th"], tsize * .26, tx + tsize * .03, ty + tsize * .98, C["cocoa"], "Mitr-Regular.ttf")
    return svg(W, H, "".join(parts) + t1 + t2 + t3, C["cream"])

FILES = {
    "logo-stacked.svg": stacked(C["cocoa"], C["caramel"], C["heart"], C["cocoa"]),
    "logo-stacked-reverse.svg": stacked(C["cream"], C["caramel"], C["heart"], C["cocoa"], C["cocoa"]),
    "logo-horizontal.svg": horizontal(C["cocoa"], C["caramel"], C["heart"], C["cocoa"]),
    "logo-horizontal-mono.svg": horizontal("#000000", "#000000", "#FFFFFF", "#FFFFFF"),
    "mark.svg": mark(C["caramel"], C["heart"], C["cocoa"]),
    "mark-mono.svg": mark(C["cocoa"], C["cream"], C["cream"]),
    "mark-for-stamp.svg": mark("#000000", "#FFFFFF", "#FFFFFF"),
    "family.svg": family(),
    "avatar-1080.svg": avatar(),
    "sticker-3cm.svg": sticker(),
    "cover-facebook-1640x624.svg": banner(1640, 624, 1400, 520),
    "cover-youtube-2560x1440.svg": banner(2560, 1440, 1546, 423),
    "cover-shopee-1200x600.svg": banner(1200, 600, 1080, 480),
}

if __name__ == "__main__":
    for name, s in FILES.items():
        open(os.path.join(OUT, name), "w").write(s)
    print(len(FILES), "files in", OUT)
