"""Build the OCT. 26 logo set and the FIVE BEARS sub-brand set as outlined SVG (no fonts needed by the printer).

Every measure comes from phi (see logolab/geometry.py and the Logo Lab page):
  OCT. 26 wordmark   letters drawn from circles and lines, stroke = cap / phi^4, dot = stroke * phi
  symbol             a 1 : phi hang tag; the 26 sits on its golden line, OCT. near the foot
  seal               rings phi : 1, for hot-stamping leather
  clear space        one dot * phi around every mark
FIVE BEARS (sub-brand, "by OCT. 26"):
The bear is the real die outline of pattern 01, turned 45 degrees so the ears sit on top.
Its two slits become the cheeks. The heart in the middle is Mama Bear.
"""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, "logolab"))
from brand import C, BRAND, SUB
from textpath import text_path
import geometry as G
PHI = G.PHI
JOST, JOSTR, TH = "alt/Jost-Medium.ttf", "alt/Jost-Regular.ttf", "alt/Anuphan-Medium.ttf"
SYNE = JOST            # old name kept for drawings in other folders

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


# ---------------------------------------------------------------- the wordmark
def word(t, cap, fg, dot, uid):
    """Any brand name (OCT. 26, SOI. 02, MAR. 23 ...) at cap height `cap`. Returns (svg group at 0,0 baseline, width)."""
    s, w = G.word(t, fg, dot, uid)
    k = cap / G.H
    return f'<g transform="scale({k:.5f})">{s}</g>', w * k

_uid = [0]
def _u(p):
    _uid[0] += 1; return f"{p}{_uid[0]}"

def wordmark(x, base, size, fg, dot, two_lines=False, anchor="start", left="OCT", right="26"):
    """Kept for other drawings. `size` is the old font size: cap height = size * 0.66.
    Two lines: LEFT. over a bigger RIGHT, the second line phi times the first."""
    cap = size * .66
    if not two_lines:
        g, w = word(f"{left}. {right}", cap, fg, dot, _u("wm"))
        x0 = x - (w / 2 if anchor == "middle" else 0)
        return f'<g transform="translate({x0:.2f},{base:.2f})">{g}</g>', w, cap
    g1, w1 = word(f"{left}.", cap, fg, dot, _u("wa"))
    g2, w2 = word(right, cap * PHI, fg, dot, _u("wb"))
    cx = x if anchor == "middle" else x + max(w1, w2) / 2
    base2 = base + cap / PHI + cap * PHI
    return (f'<g transform="translate({cx - w1/2:.2f},{base:.2f})">{g1}</g>'
            f'<g transform="translate({cx - w2/2:.2f},{base2:.2f})">{g2}</g>'), max(w1, w2), base2 - base + cap

# ---------------------------------------------------------------- the tag symbol (1 : phi)
TW_, TH_ = 100.0, 100.0 * PHI
CH = TW_ / PHI ** 3; HOLE = TW_ / PHI ** 4; MARG = TW_ / PHI ** 4

def tag(x, y, h, fill, ink, dot, hole, num="26", mon="OCT"):
    """Hang tag of height h, top-left at (x, y). The number's baseline sits on the golden line."""
    k = h / TH_
    d, dw = G.word(num, ink, dot, _u("tn"))
    sd = (TW_ - 2 * MARG) / dw
    o, ow = G.word(f"{mon}.", ink, dot, _u("to"))
    so = (TW_ - 2 * MARG) / ow / PHI
    return (f'<g transform="translate({x:.2f},{y:.2f}) scale({k:.5f})">'
            f'<path d="M{CH:.2f},0 H{TW_ - CH:.2f} L{TW_},{CH:.2f} V{TH_:.2f} H0 V{CH:.2f} Z" fill="{fill}"/>'
            f'<circle cx="{TW_/2}" cy="{CH:.2f}" r="{HOLE/2:.2f}" fill="{hole}"/>'
            f'<g transform="translate({MARG:.2f},{TH_/PHI:.2f}) scale({sd:.5f})">{d}</g>'
            f'<g transform="translate({(TW_ - ow*so)/2:.2f},{TH_ - CH:.2f}) scale({so:.5f})">{o}</g></g>')

# ---------------------------------------------------------------- seal (phi : 1), text outlined along the ring
def ring_text(t, r, size, fill, top=True, font=JOST, tracking=.18, max_deg=360 / PHI ** 2):
    """Letters around a circle. top=True reads clockwise over the top; False reads left to right along the bottom.
    The text may span at most 360/phi^2 = 137.5 degrees (the golden angle), so it never reaches the side dots."""
    while True:
        widths = [text_path(ch, size, font)[1] for ch in t]
        adv = [w + size * tracking for w in widths]
        total = sum(adv) - size * tracking
        if math.degrees(total / r) <= max_deg: break
        size /= PHI ** .125
    span = total / r                                     # radians
    capH = size * .7
    out = []
    pos = -span / 2 if top else span / 2
    for ch, w, a in zip(t, widths, adv):
        dpath = text_path(ch, size, font)[0]
        mid = pos + (w / 2 / r if top else -w / 2 / r)
        if top:
            ang = mid; rr = r - capH / 2
            px, py = rr * math.sin(ang), -rr * math.cos(ang); rot_ = math.degrees(ang)
        else:
            ang = math.pi + mid; rr = r + capH / 2
            px, py = rr * math.sin(ang), -rr * math.cos(ang); rot_ = math.degrees(ang) + 180
        if dpath.strip():
            out.append(f'<g transform="translate({px:.2f},{py:.2f}) rotate({rot_:.2f}) translate({-w/2:.2f},0)"><path d="{dpath}" fill="{fill}"/></g>')
        pos += a / r if top else -a / r
    return "".join(out)

def seal(cx, cy, R, ink, dot, fill=None):
    rin = R / PHI; band = R / PHI ** 6
    g = [f'<g transform="translate({cx:.2f},{cy:.2f})">']
    if fill: g.append(f'<circle r="{R:.2f}" fill="{fill}"/>')
    g.append(f'<circle r="{R - band/2:.2f}" fill="none" stroke="{ink}" stroke-width="{band:.2f}"/>')
    g.append(f'<circle r="{rin:.2f}" fill="none" stroke="{ink}" stroke-width="{band/PHI:.2f}"/>')
    n, nw = word("26", rin * 2 / PHI * G.H / (2 * G.D + G.GAP), ink, dot, _u("sn"))
    g.append(f'<g transform="translate({-nw/2:.2f},{rin * 2 / PHI * G.H / (2 * G.D + G.GAP) / 2:.2f})">{n}</g>')
    rt = (R - band + rin) / 2; size = (R - band - rin) / PHI
    g.append(ring_text("OUR CRAFTED THINGS", rt, size, ink, True))
    g.append(ring_text("EST. 26 · 10 · 2026", rt, size, ink, False))
    for sx in (-1, 1):
        g.append(f'<circle cx="{sx * rt:.2f}" cy="0" r="{band * .9:.2f}" fill="{dot}"/>')
    g.append("</g>")
    return "".join(g)

# ---------------------------------------------------------------- OCT. 26 files
INK, PAPER, COB, TOM = C["ink"], C["paper"], C["cobalt"], C["tomato"]
CAP = 100.0                                   # cap height in file units
CLEAR = G.DOT * PHI                           # clear space

def oct_wordmark(fg=INK, dot=TOM, bg=None):
    g, w = word("OCT. 26", CAP, fg, dot, _u("ow"))
    W, H = w + 2 * CLEAR, CAP + 2 * CLEAR
    return svg(round(W), round(H), f'<g transform="translate({CLEAR:.2f},{CLEAR + CAP:.2f})">{g}</g>', bg)

def oct_horizontal(fg=INK, dot=TOM, sub=COB, bg=None, tagfill=COB, tagink=PAPER, mono=False):
    """Tag + wordmark: the tag is phi times the cap height; the wordmark fills the tag's top square."""
    th = CAP * PHI; gap = CAP / PHI ** 2
    g, w = word("OCT. 26", CAP, fg, dot, _u("oh"))
    tl, _, _ = text("our crafted things.", CAP / PHI ** 3 / .5, 0, 0, sub, JOST, tracking=.04)
    holebg = bg or PAPER
    x0 = CLEAR; y0 = CLEAR
    parts = tag(x0, y0, th, tagfill, tagink, dot if not mono else tagink, holebg)
    parts += f'<g transform="translate({x0 + th/PHI + gap:.2f},{y0 + CAP:.2f})">{g}</g>'
    parts += f'<g transform="translate({x0 + th/PHI + gap:.2f},{y0 + th:.2f})">{tl}</g>'
    W = x0 + th / PHI + gap + w + CLEAR; H = th + 2 * CLEAR
    return svg(round(W), round(H), parts, bg)

def oct_stacked(fg=INK, dot=TOM, sub=COB, bg=None, tagfill=COB, tagink=PAPER):
    g, w = word("OCT. 26", CAP, fg, dot, _u("os"))
    th = CAP * PHI ** 2
    tl, tlw, _ = text("our crafted things.", CAP / PHI ** 3 / .5, 0, 0, sub, JOST, tracking=.04)
    W = w + 2 * CLEAR
    y = CLEAR
    parts = tag((W - th / PHI) / 2, y, th, tagfill, tagink, dot, bg or PAPER)
    y += th + CAP / PHI
    parts += f'<g transform="translate({CLEAR:.2f},{y + CAP:.2f})">{g}</g>'
    y += CAP + CAP / PHI ** 2
    parts += f'<g transform="translate({(W - tlw)/2:.2f},{y + CAP/PHI**2:.2f})">{tl}</g>'
    H = y + CAP / PHI ** 2 + CLEAR
    return svg(round(W), round(H), parts, bg)

def oct_mark(fill=COB, ink=PAPER, dot=TOM, bg=None, side=400):
    h = side / PHI * 1.1
    return svg(side, side, tag((side - h / PHI) / 2, (side - h) / 2, h, fill, ink, dot, bg or "#FFFFFF"), bg)

def oct_seal(ink=INK, dot=TOM, fill=None, side=400):
    return svg(side, side, seal(side / 2, side / 2, side / 2 - 2, ink, dot, fill), None, "OCT. 26 seal")

def avatar():
    W = 1080
    h = W / PHI
    body = f'<circle cx="540" cy="540" r="540" fill="{COB}"/>' + tag((W - h / PHI) / 2, (W - h) / 2, h, PAPER, INK, TOM, COB)
    return svg(W, W, body)

def oct_sticker():
    W = 340                                     # 34 mm at 10 px/mm
    h = W / PHI
    return svg(W, W, f'<circle cx="{W/2}" cy="{W/2}" r="{W/2}" fill="{TOM}"/>' + tag((W - h / PHI) / 2, (W - h) / 2, h, PAPER, INK, INK, TOM))

def _fit(t, cap, font, tracking, max_w, fill):
    """Jost line at the given cap height, shrunk by phi steps until it fits max_w."""
    while True:
        p, w, _ = text(t, cap / .7, 0, 0, fill, font, tracking=tracking)
        if w <= max_w: return p, w
        cap /= PHI ** .25

def soi_sign():
    """Collection plate, phi : 1. SOI. 02 cap = plate height / phi^3, its baseline on the golden line."""
    H_ = 360.0; W_ = H_ * PHI; m = H_ / PHI ** 4
    cap = H_ / PHI ** 3
    g, w = word("SOI. 02", cap, PAPER, TOM, _u("ss"))
    t1, t1w = _fit("FROM OUR ROOT", cap / PHI ** 2, JOST, .3, W_ - 2 * m, PAPER)
    t2, t2w = _fit("A COLLECTION BY OCT. 26", cap / PHI ** 3, JOST, .22, W_ - 2 * m, TOM)
    base = H_ / PHI
    body = (f'<rect width="{W_:.1f}" height="{H_:.0f}" rx="{H_/PHI**5:.1f}" fill="{INK}"/>'
            f'<g transform="translate({(W_ - w)/2:.2f},{base:.2f})">{g}</g>'
            f'<g transform="translate({(W_ - t1w)/2:.2f},{base + cap/PHI:.2f})">{t1}</g>'
            f'<g transform="translate({(W_ - t2w)/2:.2f},{H_ - m:.2f})">{t2}</g>')
    return svg(round(W_), round(H_), body, None, "SOI. 02 by OCT. 26")

def love_badge():
    """phi^2 : 1 plate. Bear = height / phi, Love cap = height / phi^2 on the golden line."""
    H_ = 360.0; W_ = H_ * PHI ** 2; m = H_ / PHI ** 4
    bh = H_ / PHI; bw = bh * BW / BH
    b = bear(m, (H_ - bh) / 2, bh, C["sun"], TOM, INK)
    x = m + bw + m
    base = H_ / PHI
    t1, _, _ = text("Love", H_ / PHI ** 2 / .72, x, base, INK, "Mitr-SemiBold.ttf")
    t2, t2w, _ = text("ห้าหมี FIVE BEARS", H_ / PHI ** 5 / .72, x + 6, base + H_ / PHI ** 4, INK, "Mitr-Medium.ttf")
    bl, blw = by_line(0, 0, H_ / PHI ** 6, INK, TOM)
    body = (f'<rect width="{W_:.1f}" height="{H_:.0f}" rx="{H_/PHI**5:.1f}" fill="{C["pink"]}"/>' + b + t1 + t2
            + f'<g transform="translate({x + 6:.2f},{base + H_/PHI**4 + H_/PHI**5:.2f})">{bl}</g>')
    return svg(round(W_), round(H_), body, None, "Love · ห้าหมี FIVE BEARS")

def banner(W, H, safe_w, safe_h):
    """Cover: the lockup takes the left 1/phi of the safe area, the family of bears the rest."""
    cx, cy = (W - safe_w) / 2, (H - safe_h) / 2
    left_w = safe_w / PHI
    cap = min(safe_h / PHI / PHI, left_w / (5.2 + PHI ** -1 + PHI ** -2) )
    th = cap * PHI
    g, w = word("OCT. 26", cap, INK, TOM, _u("bn"))
    tl, _, _ = text("our crafted things.", cap / PHI ** 3 / .5, 0, 0, COB, JOST, tracking=.04)
    y0 = cy + (safe_h - th) / 2
    parts = tag(cx, y0, th, COB, PAPER, TOM, PAPER)
    xw = cx + th / PHI + cap / PHI ** 2
    parts += f'<g transform="translate({xw:.2f},{y0 + cap:.2f})">{g}</g><g transform="translate({xw:.2f},{y0 + th:.2f})">{tl}</g>'
    parts += family_row(cx + left_w + safe_w / PHI ** 4, cy + safe_h / 2, safe_w / PHI ** 2 - safe_w / PHI ** 4, safe_h / PHI)
    return svg(W, H, parts, PAPER)

# ---------------------------------------------------------------- FIVE BEARS (sub-brand)
FAM = [("cobalt", 1.0), ("tomato", PHI ** -.25), ("sun", PHI ** -.5), ("mint", PHI ** -.75), ("pink", PHI ** -1)]

def family_row(x, mid_y, max_w, max_h):
    unit = sum(f * BW / BH for _, f in FAM) + (len(FAM) - 1) / PHI ** 4
    h0 = min(max_h, max_w / unit)
    parts = []
    for k, f in FAM:
        h = h0 * f; w = h * BW / BH
        hc = PAPER if k == "tomato" else TOM
        face = PAPER if k in ("cobalt",) else INK
        parts.append(bear(x, mid_y + h0 / 2 - h, h, C[k], hc, face)); x += w + h0 / PHI ** 4
    return "".join(parts)

def by_line(x, y, cap, fg, dot):
    t, tw, _ = text("by", cap / .7, x, y, fg, JOSTR)
    g, w = word("OCT. 26", cap, fg, dot, _u("by"))
    return t + f'<g transform="translate({x + tw + cap/PHI:.2f},{y:.2f})">{g}</g>', tw + cap / PHI + w

def stacked(fg, bear_c, heart_c, face, bg=None):
    W = 600.0
    bh = W / PHI ** 2; bw = bh * BW / BH
    y = W / PHI ** 4
    b = bear((W - bw) / 2, y, bh, bear_c, heart_c, face); y += bh + W / PHI ** 5
    t1, _, h1 = text(SUB["th"], W / PHI ** 3 / .62, W / 2, y + W / PHI ** 3, fg, anchor="middle"); y += W / PHI ** 3 + W / PHI ** 5
    t2, _, _ = text(SUB["en"], W / PHI ** 6 / .7, W / 2, y + W / PHI ** 6, fg, JOST, tracking=.3, anchor="middle"); y += W / PHI ** 6 + W / PHI ** 5
    byc = TOM if fg != "#000000" else fg
    bl, blw = by_line(0, 0, W / PHI ** 7, fg, byc)
    t3 = f'<g transform="translate({(W - blw)/2:.2f},{y + W/PHI**7:.2f})">{bl}</g>'; y += W / PHI ** 7 + W / PHI ** 4
    return svg(round(W), round(y), b + t1 + t2 + t3, bg, "ห้าหมี FIVE BEARS by OCT. 26")

def horizontal(fg, bear_c, heart_c, face, bg=None):
    H_ = 300.0
    bh = H_ / PHI; bw = bh * BW / BH
    x = H_ / PHI ** 4
    b = bear(x, (H_ - bh) / 2, bh, bear_c, heart_c, face); x += bw + H_ / PHI ** 4
    t1, w1, _ = text(SUB["th"], H_ / PHI ** 2 / .62, x, H_ / 2 + H_ / PHI ** 5, fg)
    t2, w2, _ = text(SUB["en"], H_ / PHI ** 5 / .7, x + 4, H_ / 2 + H_ / PHI ** 3, fg, JOST, tracking=.3)
    byc = TOM if fg != "#000000" else fg
    bl, blw = by_line(0, 0, H_ / PHI ** 6, fg, byc)
    t3 = f'<g transform="translate({x + 4 + w2 + H_/PHI**5:.2f},{H_/2 + H_/PHI**3:.2f})">{bl}</g>'
    W = x + max(w1, w2 + blw + H_ / PHI ** 5) + H_ / PHI ** 4
    return svg(round(W), round(H_), b + t1 + t2 + t3, bg, "ห้าหมี FIVE BEARS by OCT. 26")

def mark(bear_c, heart_c, face, bg=None, pad=None):
    side = 400.0; h = side / PHI * 1.1; w = h * BW / BH
    return svg(400, 400, bear((side - w) / 2, (side - h) / 2, h, bear_c, heart_c, face), bg, "ห้าหมี")

def family(bg=None):
    W = 1000.0
    row = family_row(W / PHI ** 6, 160, W - 2 * W / PHI ** 6, 220)
    t, _, _ = text(SUB["tag_th"], W / PHI ** 6 / .62, W / 2, 330, INK, "Mitr-Medium.ttf", anchor="middle")
    return svg(round(W), 370, row + t, bg, "ห้าหมี ครอบครัวหมีห้าตัว")

def sticker():
    W = 340.0; h = W / PHI; w = h * BW / BH
    return svg(340, 340, f'<circle cx="170" cy="170" r="170" fill="{C["sun"]}"/>' + bear((W - w) / 2, (W - h) / 2 - W / PHI ** 6, h, PAPER, TOM, INK), None, "ห้าหมี")

FILES = {
    # OCT. 26 (master brand)
    "oct-wordmark.svg": oct_wordmark(),
    "oct-horizontal.svg": oct_horizontal(),
    "oct-stacked.svg": oct_stacked(),
    "oct-stacked-reverse.svg": oct_stacked(PAPER, TOM, PAPER, COB, PAPER, COB),
    "oct-horizontal-mono.svg": oct_horizontal("#000000", "#000000", "#000000", None, "#000000", "#FFFFFF", True),
    "oct-mark.svg": oct_mark(),
    "oct-mark-stamp.svg": oct_mark("#000000", "#FFFFFF", "#FFFFFF"),
    "oct-seal.svg": oct_seal(),
    "oct-sticker-34mm.svg": oct_sticker(),
    "avatar-1080.svg": avatar(),
    "soi2-sign.svg": soi_sign(),
    "love-badge.svg": love_badge(),
    "cover-facebook-1640x624.svg": banner(1640, 624, 1400, 520),
    "cover-youtube-2560x1440.svg": banner(2560, 1440, 1546, 423),
    "cover-shopee-1200x600.svg": banner(1200, 600, 1080, 480),
    # ห้าหมี FIVE BEARS by OCT. 26 (sub-brand)
    "fivebears-stacked.svg": stacked(INK, C["sun"], TOM, INK),
    "fivebears-stacked-reverse.svg": stacked(PAPER, C["sun"], TOM, INK, COB),
    "fivebears-horizontal.svg": horizontal(INK, C["sun"], TOM, INK),
    "fivebears-horizontal-mono.svg": horizontal("#000000", "#000000", "#FFFFFF", "#FFFFFF"),
    "mark.svg": mark(C["sun"], TOM, INK),
    "mark-mono.svg": mark(INK, PAPER, PAPER),
    "mark-for-stamp.svg": mark("#000000", "#FFFFFF", "#FFFFFF"),
    "family.svg": family(),
    "fivebears-sticker-34mm.svg": sticker(),
}

if __name__ == "__main__":
    for f in os.listdir(OUT):
        if f not in FILES: os.remove(os.path.join(OUT, f))
    for name, s in FILES.items():
        open(os.path.join(OUT, name), "w").write(s)
    # PNG render jobs come from each file's own viewBox: big pieces (covers, avatar, family) at 1x, marks at 2x
    jobs = []
    for name, s in FILES.items():
        w, h = (round(float(v)) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s).groups())
        jobs.append({"src": os.path.join(OUT, name), "out": os.path.join(HERE, "png", name[:-4] + ".png"),
                     "w": w, "h": h, "scale": 1 if max(w, h) >= 1000 else 2, "transparent": True})
    json.dump(jobs, open(os.path.join(HERE, "jobs.json"), "w"), indent=1)
    print(len(FILES), "files in", OUT, "· node tools/render.mjs logo/jobs.json for PNG")
