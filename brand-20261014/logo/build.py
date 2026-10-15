"""Build the logo set as outlined SVG (no fonts needed by the printer). Four logos, used one at a time, never side by side:

  OCT. 26          the name, drawn from circles and lines. "OCT. " : "26" = phi^2 : 1, so the word is 5 x its cap height.
                   stroke = cap / phi^4, dot = stroke * phi, clear space = dot * phi
  tag 26           the symbol for small and square places (profile picture, icon, sticker). A 1 : phi hang tag,
                   the 26 sits on its golden line. Never placed next to the name: it already says 26.
  FIVE BEARS       sub-brand lockup: bear, ห้าหมี, FIVE BEARS, by OCT. 26
  bear             the sub-brand symbol. The bear is the real die outline of pattern 01, turned 45 degrees;
                   its two slits are the cheeks, the heart in the middle is Mama Bear.
Each comes in three colour versions: on light, on dark, one colour (for stamping and single-colour print).
Collection plates (SOI. 02, Love) are collection names, not logos.
"""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, "logolab"))
from brand import C, BRAND, SUB
from textpath import text_path
import geometry as G
PHI = G.PHI
JOST, JOSTR, TH = "alt/Jost-Medium.ttf", "alt/Jost-Regular.ttf", "alt/Anuphan-Medium.ttf"
MITR, MITRB = "Mitr-Medium.ttf", "Mitr-SemiBold.ttf"
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
        mono = body == "#000000"                 # one-colour version: details knocked out in full white, no tints
        inner, op_e, op_s = ("#FFFFFF", 1, 1) if mono else (C["cream"], .55, .8)
        for e in EARS:
            ex, ey = rot(e); g.append(f'<circle cx="{ex:.2f}" cy="{ey:.2f}" r="6.2" fill="{inner}" opacity="{op_e}"/>')
        for a, b in SLITS:
            (ax, ay), (bx, by) = rot(a), rot(b)
            g.append(f'<line x1="{ax:.2f}" y1="{ay:.2f}" x2="{bx:.2f}" y2="{by:.2f}" stroke="{inner}" '
                     f'stroke-width="2.6" stroke-linecap="round" opacity="{op_s}"/>')
        g.append(f'<circle cx="-13.5" cy="-7" r="3.8" fill="{face}"/><circle cx="13.5" cy="-7" r="3.8" fill="{face}"/>')
    g.append(f'<path d="{heart(0, 10.5, 25 if detail else 34)}" fill="{heart_c}"/>')
    g.append("</g>")
    return "".join(g)

def text(t, size, x, y, fill, font="Mitr-SemiBold.ttf", tracking=0.0, anchor="start"):
    d, w, (x0, y0, x1, y1) = text_path(t, size, font, tracking)
    x -= (x0 + x1) / 2 if anchor == "middle" else x0     # align the ink, not the pen origin (no side bearing)
    return f'<path transform="translate({x:.2f},{y:.2f})" d="{d}" fill="{fill}"/>', (x1 - x0), (y1 - y0)

def ink(t, size, font, tracking=0.0):
    """Outline and ink box (x0, y0, x1, y1) of a line of text; y is relative to the baseline."""
    d, _, box = text_path(t, size, font, tracking)
    return d, box

def put(d, box, x, y, fill):
    """Place a line so its ink box's top-left corner is at (x, y)."""
    return f'<path transform="translate({x - box[0]:.2f},{y - box[1]:.2f})" d="{d}" fill="{fill}"/>'

def justify(t, size, font, target):
    """Letter-space a line so its ink is exactly `target` wide (tracking is linear in width)."""
    _, b0 = ink(t, size, font, 0); _, b1 = ink(t, size, font, 1)
    w0, w1 = b0[2] - b0[0], b1[2] - b1[0]
    return ink(t, size, font, (target - w0) / (w1 - w0))

def size_for(t, font, target, dim=0):
    """Font size at which the ink is `target` wide (dim=0) or tall (dim=1)."""
    _, b = ink(t, 100, font)
    return 100 * target / ((b[2] - b[0]) if dim == 0 else (b[3] - b[1]))

def tagline(name_w):
    """our crafted things. sits under the name, its ink exactly name width / phi^(1/2), cap / phi below the baseline."""
    t = "our crafted things."
    return ink(t, size_for(t, JOST, name_w / PHI ** 0.5), JOST)

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

INK, PAPER, COB, TOM = C["ink"], C["paper"], C["cobalt"], C["tomato"]
CAP = 100.0                                   # cap height in file units
CLEAR = G.DOT * PHI                           # clear space

def oct_wordmark(fg=INK, dot=TOM, bg=None):
    g, w = word("OCT. 26", CAP, fg, dot, _u("ow"))
    W, H = w + 2 * CLEAR, CAP + 2 * CLEAR
    return svg(round(W), round(H), f'<g transform="translate({CLEAR:.2f},{CLEAR + CAP:.2f})">{g}</g>', bg)

def oct_mark(fill=COB, ink=PAPER, dot=TOM, bg=None, side=400, hole=None):
    """The tag in a square: tag height = side / phi, the same as on the profile picture."""
    h = side / PHI
    return svg(side, side, tag((side - h / PHI) / 2, (side - h) / 2, h, fill, ink, dot, hole or bg or "#FFFFFF"), bg)

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
    """Collection plate, phi : 1. One justified block: SOI. 02 (cap = height / phi^3), then two lines letter-spaced
    to exactly its width, caps stepping down by phi. Gaps = cap / phi^3. The block sits in the plate's centre."""
    H_ = 360.0; W_ = H_ * PHI
    cap = H_ / PHI ** 3; gap = cap / PHI ** 3
    g, w = word("SOI. 02", cap, PAPER, TOM, _u("ss"))
    d1, b1 = justify("FROM OUR ROOT", size_for("FROM OUR ROOT", JOST, cap / PHI ** 2, 1), JOST, w)
    d2, b2 = justify("A COLLECTION BY OCT. 26", size_for("A COLLECTION BY OCT", JOST, cap / PHI ** 3, 1), JOST, w)
    h1, h2 = b1[3] - b1[1], b2[3] - b2[1]
    top = (H_ - (cap + gap + h1 + gap + h2)) / 2; x = (W_ - w) / 2
    body = (f'<rect width="{W_:.1f}" height="{H_:.0f}" rx="{H_/PHI**5:.1f}" fill="{INK}"/>'
            f'<g transform="translate({x:.2f},{top + cap:.2f})">{g}</g>'
            + put(d1, b1, x, top + cap + gap, PAPER) + put(d2, b2, x, top + cap + gap + h1 + gap, TOM))
    return svg(round(W_), round(H_), body, None, "SOI. 02 by OCT. 26")

def love_badge():
    """phi^2 : 1 plate. Bear = height / phi. The text block is exactly as tall as the bear: Love's top on the bear's
    top, by OCT. 26 on the bear's bottom. ห้าหมี FIVE BEARS is as wide as Love. The whole group is centred."""
    H_ = 360.0; W_ = H_ * PHI ** 2
    bh = H_ / PHI; bw = bh * BW / BH; top = (H_ - bh) / 2; bot = top + bh
    d1, b1 = ink("Love", size_for("Love", MITRB, bh / PHI, 1), MITRB)
    lw = b1[2] - b1[0]
    d2, b2 = ink("ห้าหมี FIVE BEARS", size_for("ห้าหมี FIVE BEARS", MITR, lw), MITR)
    h2 = b2[3] - b2[1]
    bcap = h2 / PHI ** 2
    bl, blw = by_line(0, 0, bcap, INK, TOM)
    _, bb = ink("by", bcap / .7, JOSTR)
    by_top = bot + bb[1]                                   # ascender of "b" above the baseline
    free = by_top - (top + bh / PHI) - h2                  # room left between Love and the by line
    gap = bh / PHI ** 3
    group = bw + gap + lw; x0 = (W_ - group) / 2; xt = x0 + bw + gap
    body = (f'<rect width="{W_:.1f}" height="{H_:.0f}" rx="{H_/PHI**5:.1f}" fill="{C["pink"]}"/>'
            + bear(x0, top, bh, C["sun"], TOM, INK) + put(d1, b1, xt, top, INK)
            + put(d2, b2, xt, top + bh / PHI + free / 2, INK)
            + f'<g transform="translate({xt:.2f},{bot:.2f})">{bl}</g>')
    return svg(round(W_), round(H_), body, None, "Love · ห้าหมี FIVE BEARS")

def banner(W, H, safe_w, safe_h):
    """Cover. Name on the left edge of the safe area, the five bears on the right edge. The tallest bear is exactly
    as tall as the letters (cap line to baseline) and every bear stands on the name's baseline: one line of type."""
    cx, cy = (W - safe_w) / 2, (H - safe_h) / 2
    cap = min(safe_h / PHI ** 3, safe_w / PHI / 5)
    g, w = word("OCT. 26", cap, INK, TOM, _u("bn"))
    td, tb = tagline(w)
    gap = cap / PHI
    block = cap + gap + (tb[3] - tb[1])
    base = cy + (safe_h - block) / 2 + cap
    parts = f'<g transform="translate({cx:.2f},{base:.2f})">{g}</g>' + put(td, tb, cx, base + gap, COB)
    unit = sum(f * BW / BH for _, f in FAM) + (len(FAM) - 1) / PHI ** 4
    h0 = min(cap, (safe_w - w - safe_w / PHI ** 4) / unit)
    parts += family_row(cx + safe_w - h0 * unit, base - h0 / 2, safe_w, h0)
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
    """Bear, ห้าหมี, FIVE BEARS, by OCT. 26. Centred on one axis; FIVE BEARS is letter-spaced to the width of ห้าหมี;
    every gap between rows (ink to ink) is the same, W / phi^5."""
    W = 600.0; m = W / PHI ** 4; gap = W / PHI ** 5
    bh = W / PHI ** 2; bw = bh * BW / BH
    d1, b1 = ink(SUB["th"], W / PHI ** 3 / .62, MITRB)
    tw = b1[2] - b1[0]
    d2, b2 = justify(SUB["en"], size_for("FIVE BEARS", JOST, tw / PHI ** 5, 1), JOST, tw)
    byc = TOM if fg != "#000000" else fg
    bcap = (b2[3] - b2[1]) / PHI
    bl, blw = by_line(0, 0, bcap, fg, byc)
    _, bb = ink("by", bcap / .7, JOSTR)
    y = m
    parts = bear((W - bw) / 2, y, bh, bear_c, heart_c, face); y += bh + gap
    parts += put(d1, b1, (W - tw) / 2, y, fg); y += b1[3] - b1[1] + gap
    parts += put(d2, b2, (W - tw) / 2, y, fg); y += b2[3] - b2[1] + gap
    parts += f'<g transform="translate({(W - blw)/2:.2f},{y - bb[1]:.2f})">{bl}</g>'; y += -bb[1] + m
    return svg(round(W), round(y), parts, bg, "ห้าหมี FIVE BEARS by OCT. 26")

def mark(bear_c, heart_c, face, bg=None, pad=None):
    side = 400.0; h = side / PHI; w = h * BW / BH
    return svg(400, 400, bear((side - w) / 2, (side - h) / 2, h, bear_c, heart_c, face), bg, "ห้าหมี")

def family(bg=None):
    W = 1000.0
    row = family_row(W / PHI ** 6, 160, W - 2 * W / PHI ** 6, 220)
    t, _, _ = text(SUB["tag_th"], W / PHI ** 6 / .62, W / 2, 330, INK, "Mitr-Medium.ttf", anchor="middle")
    return svg(round(W), 370, row + t, bg, "ห้าหมี ครอบครัวหมีห้าตัว")

def sticker():
    W = 340.0; h = W / PHI; w = h * BW / BH
    return svg(340, 340, f'<circle cx="170" cy="170" r="170" fill="{C["sun"]}"/>' + bear((W - w) / 2, (W - h) / 2 - W / PHI ** 6, h, PAPER, TOM, INK), None, "ห้าหมี")

MONO = "#000000"
FILES = {
    # 1. OCT. 26, the name: main logo
    "oct-wordmark.svg": oct_wordmark(),
    "oct-wordmark-reverse.svg": oct_wordmark(PAPER, TOM),
    "oct-wordmark-mono.svg": oct_wordmark(MONO, MONO),
    # 2. tag 26: symbol
    "oct-mark.svg": oct_mark(),
    "oct-mark-reverse.svg": oct_mark(PAPER, INK, TOM, None, hole=INK),
    "oct-mark-mono.svg": oct_mark(MONO, "#FFFFFF", "#FFFFFF"),
    # 3. ห้าหมี FIVE BEARS by OCT. 26
    "fivebears.svg": stacked(INK, C["sun"], TOM, INK),
    "fivebears-reverse.svg": stacked(PAPER, C["sun"], TOM, INK),
    "fivebears-mono.svg": stacked(MONO, MONO, "#FFFFFF", "#FFFFFF"),
    # 4. bear: sub-brand symbol
    "bear.svg": mark(C["sun"], TOM, INK),
    "bear-mono.svg": mark(MONO, "#FFFFFF", "#FFFFFF"),
    # where they are used
    "avatar-1080.svg": avatar(),
    "oct-sticker-34mm.svg": oct_sticker(),
    "fivebears-sticker-34mm.svg": sticker(),
    "cover-facebook-1640x624.svg": banner(1640, 624, 1400, 520),
    "cover-youtube-2560x1440.svg": banner(2560, 1440, 1546, 423),
    "cover-shopee-1200x600.svg": banner(1200, 600, 1080, 480),
    "family.svg": family(),
    # collection names (not logos)
    "soi2-sign.svg": soi_sign(),
    "love-badge.svg": love_badge(),
}

if __name__ == "__main__":
    for f in os.listdir(OUT):
        if f not in FILES: os.remove(os.path.join(OUT, f))
    for f in os.listdir(os.path.join(HERE, "png")):
        if f[:-4] + ".svg" not in FILES: os.remove(os.path.join(HERE, "png", f))
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
