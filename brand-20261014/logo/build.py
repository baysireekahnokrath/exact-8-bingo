"""Build the OCT. 26 logo set and the FIVE BEARS sub-brand set as outlined SVG (no fonts needed by the printer).

OCT. 26: Syne Bold wordmark, the full stop is a brick-orange dot. Thai lines use Anuphan.
FIVE BEARS (sub-brand, "by OCT. 26"):
The bear is the real die outline of pattern 01, turned 45 degrees so the ears sit on top.
Its two slits become the cheeks. The heart in the middle is Mama Bear.
"""
import math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT); sys.path.insert(0, HERE)
from brand import C, BRAND, SUB
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

def svg(w, h, body, bg=None, title="OCT. 26"):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<title>{title}</title>{rect}{body}</svg>')

def stacked(fg, bear_c, heart_c, face, bg=None):
    W, H = 600, 640
    b = bear(W / 2 - 190 * BW / BH / 2 * 1, 40, 190, bear_c, heart_c, face)
    t1, _, _ = text(SUB["th"], 150, W / 2, 420, fg, anchor="middle")
    t2, _, _ = text(SUB["en"], 44, W / 2, 500, fg, "Mitr-Medium.ttf", tracking=.22, anchor="middle")
    t3, _, _ = text(SUB["by"], 30, W / 2, 568, bear_c if bg is None else fg, "alt/Syne-Bold.ttf", tracking=.04, anchor="middle")
    return svg(W, H, b + t1 + t2 + t3, bg, "ห้าหมี FIVE BEARS by OCT. 26")

def horizontal(fg, bear_c, heart_c, face, bg=None):
    W, H = 1000, 300
    b = bear(30, 45, 210, bear_c, heart_c, face)
    t1, _, _ = text(SUB["th"], 150, 290, 185, fg)
    t2, w2, _ = text(SUB["en"], 42, 296, 255, fg, "Mitr-Medium.ttf", tracking=.22)
    t3, _, _ = text(SUB["by"], 30, 296 + w2 + 26, 255, bear_c if fg != "#000000" else fg, "alt/Syne-Bold.ttf", tracking=.04)
    return svg(W, H, b + t1 + t2 + t3, bg, "ห้าหมี FIVE BEARS by OCT. 26")

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
    t, _, _ = text(SUB["tag_th"], 46, W / 2, 330, C["cocoa"], "Mitr-Medium.ttf", anchor="middle")
    return svg(round(W), 370, "".join(parts) + t, bg)

def sticker():
    W = 400; h = 190; w = h * BW / BH
    b = bear((W - w) / 2, 70, h, C["cream"], C["heart"], C["cocoa"])
    t, _, _ = text(SUB["th"], 64, W / 2, 335, C["cream"], anchor="middle")
    return svg(W, W, f'<circle cx="200" cy="200" r="200" fill="{C["caramel"]}"/>' + b + t)


# ---------------------------------------------------------------- OCT. 26
SYNE, TH = "alt/Syne-Bold.ttf", "alt/Anuphan-Medium.ttf"

def wordmark(x, base, size, fg, dot, two_lines=False, anchor="start"):
    """OCT + dot + 26 on one line, or OCT. over a larger 26. Returns (svg, width, height)."""
    d1, w1, b1 = text_path("OCT", size, SYNE)
    r = size * .085
    if not two_lines:
        d2, w2, b2 = text_path("26", size, SYNE)
        dx = b1[2] + size * .06 + 2 * r + size * .3 - b2[0]
        total = dx + b2[2] - b1[0]
        x0 = x - (total / 2 if anchor == "middle" else 0) - b1[0]
        parts = (f'<path transform="translate({x0:.2f},{base:.2f})" d="{d1}" fill="{fg}"/>'
                 f'<circle cx="{x0 + b1[2] + size * .06 + r:.2f}" cy="{base - r:.2f}" r="{r:.2f}" fill="{dot}"/>'
                 f'<path transform="translate({x0 + dx:.2f},{base:.2f})" d="{d2}" fill="{fg}"/>')
        return parts, total, size * .66
    big = size * 1.62
    d2, w2, b2 = text_path("26", big, SYNE)
    w_top = b1[2] - b1[0] + size * .06 + 2 * r
    cx = x if anchor == "middle" else x + max(w_top, b2[2] - b2[0]) / 2
    x1 = cx - w_top / 2 - b1[0]
    x2 = cx - (b2[0] + b2[2]) / 2
    base2 = base + size * .2 + big * .66
    parts = (f'<path transform="translate({x1:.2f},{base:.2f})" d="{d1}" fill="{fg}"/>'
             f'<circle cx="{x1 + b1[2] + size * .06 + r:.2f}" cy="{base - r:.2f}" r="{r:.2f}" fill="{dot}"/>'
             f'<path transform="translate({x2:.2f},{base2:.2f})" d="{d2}" fill="{fg}"/>')
    return parts, max(w_top, b2[2] - b2[0]), base2 - base + size * .66

def oct_horizontal(fg, dot, sub, bg=None):
    W, H = 1000, 330
    wm, w, _ = wordmark(W / 2, 185, 190, fg, dot, anchor="middle")
    t, _, _ = text(BRAND["tag_en"], 40, W / 2, 268, sub, SYNE, tracking=.02, anchor="middle")
    return svg(W, H, wm + t, bg)

def oct_stacked(fg, dot, sub, bg=None):
    W, H = 600, 680
    wm, _, _ = wordmark(W / 2, 210, 150, fg, dot, two_lines=True, anchor="middle")
    t1, _, _ = text(BRAND["tag_en"], 38, W / 2, 575, sub, SYNE, tracking=.02, anchor="middle")
    t2, _, _ = text(BRAND["tag_th"], 34, W / 2, 630, sub, TH, anchor="middle")
    return svg(W, H, wm + t1 + t2, bg)

def oct_mark(fill, fg, dot, W=400):
    wm, _, _ = wordmark(W / 2, W * .39, W * .2, fg, dot, two_lines=True, anchor="middle")
    return svg(W, W, f'<circle cx="{W/2}" cy="{W/2}" r="{W/2}" fill="{fill}"/>' + wm)

def oct_avatar():
    W = 1080
    wm, _, _ = wordmark(W / 2, 395, 200, C["chestnut"], C["brick"], two_lines=True, anchor="middle")
    t, _, _ = text(BRAND["tag_en"], 50, W / 2, 870, C["leaf"], SYNE, tracking=.02, anchor="middle")
    return svg(W, W, f'<circle cx="540" cy="540" r="540" fill="{C["oct_cream"]}"/>' + wm + t)

def soi_sign(W=600, H=360):
    """Collection badge for Soi 2, drawn like a Bangkok street sign in the OCT. 26 colours."""
    th, _, _ = text("ซอย ๒", 104, W / 2, 158, C["oct_cream"], TH, anchor="middle")
    en, _, _ = text("SOI 2", 96, W / 2, 268, C["oct_cream"], SYNE, tracking=.04, anchor="middle")
    by, _, _ = text("OCT. 26", 26, W / 2, 322, C["brick"], SYNE, tracking=.08, anchor="middle")
    body = (f'<rect width="{W}" height="{H}" rx="34" fill="{C["chestnut"]}"/>'
            f'<rect x="14" y="14" width="{W-28}" height="{H-28}" rx="24" fill="none" stroke="{C["oct_cream"]}" stroke-width="5"/>'
            f'<line x1="60" y1="188" x2="{W-60}" y2="188" stroke="{C["brick"]}" stroke-width="5" stroke-linecap="round"/>')
    return svg(W, H, body + th + en + by, title="Soi 2 · OCT. 26")

def love_badge(W=600, H=360):
    """Collection badge for Love, the first FIVE BEARS collection."""
    h = 150; w = h * BW / BH
    b = bear(70, (H - h) / 2 - 10, h, C["caramel"], C["heart"], C["cocoa"])
    t1, _, _ = text("Love", 120, 300, 190, C["heart"], "Mitr-SemiBold.ttf")
    t2, _, _ = text("ห้าหมี FIVE BEARS", 34, 304, 250, C["cocoa"], "Mitr-Medium.ttf")
    t3, _, _ = text(SUB["by"], 22, 306, 292, C["caramel"], SYNE, tracking=.06)
    body = f'<rect width="{W}" height="{H}" rx="34" fill="{C["cream"]}"/>'
    return svg(W, H, body + b + t1 + t2 + t3, title="Love · ห้าหมี FIVE BEARS")

def oct_sticker():
    W = 400
    wm, _, _ = wordmark(W / 2, 168, 82, C["oct_cream"], C["brick"], two_lines=True, anchor="middle")
    return svg(W, W, f'<circle cx="200" cy="200" r="200" fill="{C["chestnut"]}"/>' + wm)

def oct_banner(W, H, safe_w, safe_h):
    """Cover: OCT. 26 and its line on the left of the safe area; the bear family and Soi 2 sign on the right."""
    cx, cy = (W - safe_w) / 2, (H - safe_h) / 2
    size = min(safe_h * .46, safe_w * .145)
    wm, ww, _ = wordmark(cx + safe_w * .04, cy + safe_h * .5, size, C["chestnut"], C["brick"])
    t1, _, _ = text(BRAND["tag_en"], size * .27, cx + safe_w * .04 + size * .05, cy + safe_h * .5 + size * .5, C["leaf"], SYNE, tracking=.02)
    t2, _, _ = text("Soi 2  ·  ห้าหมี FIVE BEARS", size * .23, cx + safe_w * .04 + size * .05, cy + safe_h * .5 + size * .86, C["chestnut"], TH)
    sizes = [("cocoa", 1.0), ("heart", .9), ("honey", .7), ("peach", .64), ("sage", .58)]
    unit = sum(f * BW / BH for _, f in sizes) + .06 * 4
    room = safe_w - (ww + safe_w * .12)
    H0 = min(safe_h * .5, room / unit)
    x = cx + safe_w - H0 * unit - safe_w * .02
    base = cy + safe_h / 2 + H0 / 2
    parts = []
    for k, f in sizes:
        h = H0 * f; w = h * BW / BH
        hc = C["cream"] if k == "heart" else C["heart"]
        face = C["cream"] if k == "cocoa" else C["cocoa"]
        parts.append(bear(x, base - h, h, C[k], hc, face)); x += w + H0 * .06
    return svg(W, H, wm + t1 + t2 + "".join(parts), C["oct_cream"])

FILES = {
    # OCT. 26 (master brand)
    "oct-horizontal.svg": oct_horizontal(C["chestnut"], C["brick"], C["leaf"]),
    "oct-stacked.svg": oct_stacked(C["chestnut"], C["brick"], C["leaf"]),
    "oct-stacked-reverse.svg": oct_stacked(C["oct_cream"], C["brick"], C["oct_cream"], C["chestnut"]),
    "oct-horizontal-mono.svg": oct_horizontal("#000000", "#000000", "#000000"),
    "oct-mark.svg": oct_mark(C["chestnut"], C["oct_cream"], C["brick"]),
    "oct-mark-stamp.svg": oct_mark("#000000", "#FFFFFF", "#FFFFFF"),
    "oct-sticker-3cm.svg": oct_sticker(),
    "avatar-1080.svg": oct_avatar(),
    "soi2-sign.svg": soi_sign(),
    "love-badge.svg": love_badge(),
    "cover-facebook-1640x624.svg": oct_banner(1640, 624, 1400, 520),
    "cover-youtube-2560x1440.svg": oct_banner(2560, 1440, 1546, 423),
    "cover-shopee-1200x600.svg": oct_banner(1200, 600, 1080, 480),
    # ห้าหมี FIVE BEARS by OCT. 26 (sub-brand)
    "fivebears-stacked.svg": stacked(C["cocoa"], C["caramel"], C["heart"], C["cocoa"]),
    "fivebears-stacked-reverse.svg": stacked(C["cream"], C["caramel"], C["heart"], C["cocoa"], C["cocoa"]),
    "fivebears-horizontal.svg": horizontal(C["cocoa"], C["caramel"], C["heart"], C["cocoa"]),
    "fivebears-horizontal-mono.svg": horizontal("#000000", "#000000", "#FFFFFF", "#FFFFFF"),
    "mark.svg": mark(C["caramel"], C["heart"], C["cocoa"]),
    "mark-mono.svg": mark(C["cocoa"], C["cream"], C["cream"]),
    "mark-for-stamp.svg": mark("#000000", "#FFFFFF", "#FFFFFF"),
    "family.svg": family(),
    "fivebears-sticker-3cm.svg": sticker(),
}

if __name__ == "__main__":
    for f in os.listdir(OUT):
        if f not in FILES: os.remove(os.path.join(OUT, f))
    for name, s in FILES.items():
        open(os.path.join(OUT, name), "w").write(s)
    print(len(FILES), "files in", OUT)
