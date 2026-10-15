"""Golden-ratio letterforms for the OCT. 26 logo proposals.

Every measure comes from one unit: cap height H = 100 and phi = 1.618.
  stroke w      = H / phi^4  = 14.59
  dot           = w * phi    = 23.61   (the dot is the one element bigger than the stroke)
  digit width D = H / phi    = 61.80
  T width       = H * phi/2  = 80.90
  C opening     = 360 / phi^3 = 84.98 degrees
  letter gap    = w,  word gap = H / phi^2 = 38.20
  OCT. 26       "OCT. " : "26" = phi^2 : 1 (its word gap becomes 32.2)
Glyphs are drawn as strokes on centre lines (butt caps), so they stay clean at any size.
"""
import math

PHI = (1 + 5 ** .5) / 2
H = 100.0
W = H / PHI ** 4
DOT = W * PHI
D = H / PHI
TW = H * PHI / 2
C_OPEN = 360 / PHI ** 3
GAP = W
WORD = H / PHI ** 2

def _pt(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)

def glyph_O(x, col, uid=""):
    r = H / 2 - W / 2
    return f'<circle cx="{x + H/2:.2f}" cy="{-H/2:.2f}" r="{r:.2f}" fill="none" stroke="{col}" stroke-width="{W:.2f}"/>', H

def glyph_C(x, col, uid=""):
    r = H / 2 - W / 2; cx, cy = x + H / 2, -H / 2; half = C_OPEN / 2
    x1, y1 = _pt(cx, cy, r, half); x2, y2 = _pt(cx, cy, r, 360 - half)
    adv = cx + (H / 2) * math.cos(math.radians(half)) - x
    return (f'<path d="M{x1:.2f},{y1:.2f} A{r:.2f},{r:.2f} 0 1 1 {x2:.2f},{y2:.2f}" fill="none" stroke="{col}" stroke-width="{W:.2f}"/>', adv)

def glyph_T(x, col, uid=""):
    return (f'<rect x="{x:.2f}" y="{-H:.2f}" width="{TW:.2f}" height="{W:.2f}" fill="{col}"/>'
            f'<rect x="{x + TW/2 - W/2:.2f}" y="{-H:.2f}" width="{W:.2f}" height="{H:.2f}" fill="{col}"/>', TW)

def glyph_dot(x, col):
    return f'<circle cx="{x + DOT/2:.2f}" cy="{-DOT/2:.2f}" r="{DOT/2:.2f}" fill="{col}"/>', DOT

def glyph_2(x, col, uid="g2"):
    rr = D / 2 - W / 2; cx, cy = x + D / 2, -H + D / 2
    sx, sy = _pt(cx, cy, rr, 155)
    ex, ey = _pt(cx, cy, rr, 38)
    return (f'<clipPath id="{uid}"><rect x="{x:.2f}" y="{-H:.2f}" width="{D:.2f}" height="{H:.2f}"/></clipPath>'
            f'<g clip-path="url(#{uid})"><path d="M{sx:.2f},{sy:.2f} A{rr:.2f},{rr:.2f} 0 1 1 {ex:.2f},{ey:.2f} L{x + W*.3:.2f},{-W*.7:.2f}" fill="none" '
            f'stroke="{col}" stroke-width="{W:.2f}"/>'
            f'<rect x="{x:.2f}" y="{-W:.2f}" width="{D:.2f}" height="{W:.2f}" fill="{col}"/></g>', D)

def glyph_6(x, col, uid="g6"):
    rr = D / 2 - W / 2; cx, cy = x + D / 2, -D / 2
    ex, ey = x + D * .64, -H - W                     # start above the cap line, clipped flat
    dx, dy = ex - cx, ey - cy; dist = math.hypot(dx, dy)
    base = math.degrees(math.atan2(dy, dx)); off = math.degrees(math.acos(rr / dist))
    tx, ty = _pt(cx, cy, rr, base - off)          # tangent point on the left of the bowl
    if tx > cx: tx, ty = _pt(cx, cy, rr, base + off)
    return (f'<clipPath id="{uid}"><rect x="{x - W:.2f}" y="{-H:.2f}" width="{D + 2*W:.2f}" height="{H + W:.2f}"/></clipPath>'
            f'<g clip-path="url(#{uid})"><circle cx="{cx:.2f}" cy="{cy:.2f}" r="{rr:.2f}" fill="none" stroke="{col}" stroke-width="{W:.2f}"/>'
            f'<line x1="{ex:.2f}" y1="{ey:.2f}" x2="{tx:.2f}" y2="{ty:.2f}" stroke="{col}" stroke-width="{W:.2f}"/></g>', D)

# ---------------------------------------------------------------- the rest of the alphabet
# Bowls of S, 3 and the bars of E sit a little above centre: top : bottom = 1 : phi^(1/4).
Q = PHI ** .25
SA = (H + W) / (1 + Q)            # top bowl of S and 3
SB = (H + W) - SA                 # bottom bowl
def _clip(uid, x, w):
    return f'<clipPath id="{uid}"><rect x="{x - W:.2f}" y="{-H:.2f}" width="{w + 2*W:.2f}" height="{H:.2f}"/></clipPath>'

def _stroke(d, col, uid=None, join="miter"):
    g = f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{W:.2f}" stroke-linejoin="{join}"/>'
    return f'<g clip-path="url(#{uid})">{g}</g>' if uid else g

def glyph_I(x, col, uid=""):
    return f'<rect x="{x:.2f}" y="{-H:.2f}" width="{W:.2f}" height="{H:.2f}" fill="{col}"/>', W

def glyph_E(x, col, uid=""):
    wid = D; mid_w = D * PHI / 2
    inner = H - 3 * W; upper = inner / (1 + Q)
    ym = -H + W + upper
    return (f'<rect x="{x:.2f}" y="{-H:.2f}" width="{W:.2f}" height="{H:.2f}" fill="{col}"/>'
            f'<rect x="{x:.2f}" y="{-H:.2f}" width="{wid:.2f}" height="{W:.2f}" fill="{col}"/>'
            f'<rect x="{x:.2f}" y="{ym:.2f}" width="{mid_w:.2f}" height="{W:.2f}" fill="{col}"/>'
            f'<rect x="{x:.2f}" y="{-W:.2f}" width="{wid:.2f}" height="{W:.2f}" fill="{col}"/>', wid)

def _bowl(x, col, top, height, wid):
    """Stem-side bowl used by P, R and D: straight top and bottom, half circle on the right."""
    r = height / 2 - W / 2; cx = x + wid - height / 2; cy = top + height / 2
    sx = x + W / 2
    return (f"M{sx:.2f},{top + W/2:.2f} L{cx:.2f},{top + W/2:.2f} A{r:.2f},{r:.2f} 0 0 1 {cx:.2f},{top + height - W/2:.2f} L{sx:.2f},{top + height - W/2:.2f}", cx)

def glyph_P(x, col, uid="gP"):
    d, _ = _bowl(x, col, -H, H / PHI, D)
    return (f'<rect x="{x:.2f}" y="{-H:.2f}" width="{W:.2f}" height="{H:.2f}" fill="{col}"/>' + _stroke(d, col), D)

def glyph_R(x, col, uid="gR"):
    d, cx = _bowl(x, col, -H, H / PHI, D)
    leg = f"M{cx - W*.2:.2f},{-H + H/PHI - W/2:.2f} L{x + D + W*.3:.2f},{W:.2f}"
    return (_clip(uid, x, D) + f'<rect x="{x:.2f}" y="{-H:.2f}" width="{W:.2f}" height="{H:.2f}" fill="{col}"/>'
            + _stroke(d, col) + _stroke(leg, col, uid), D)

def glyph_D(x, col, uid=""):
    d, _ = _bowl(x, col, -H, H, TW)
    return f'<rect x="{x:.2f}" y="{-H:.2f}" width="{W:.2f}" height="{H:.2f}" fill="{col}"/>' + _stroke(d, col), TW

def glyph_M(x, col, uid="gM"):
    wid = H
    d = f"M{x + W/2:.2f},{W:.2f} L{x + W/2:.2f},{-H:.2f} L{x + wid/2:.2f},{-W*.2:.2f} L{x + wid - W/2:.2f},{-H:.2f} L{x + wid - W/2:.2f},{W:.2f}"
    return _clip(uid, x, wid) + _stroke(d, col, uid), wid

def glyph_N(x, col, uid="gN"):
    wid = TW
    d = f"M{x + W/2:.2f},{W:.2f} L{x + W/2:.2f},{-H:.2f} L{x + wid - W/2:.2f},0 L{x + wid - W/2:.2f},{-H - W:.2f}"
    return _clip(uid, x, wid) + _stroke(d, col, uid), wid

def glyph_A(x, col, uid="gA"):
    wid = TW
    d = f"M{x - W*.1:.2f},{W:.2f} L{x + wid/2:.2f},{-H - W*1.2:.2f} L{x + wid + W*.1:.2f},{W:.2f}"
    ybar = -H / PHI ** 2
    half = (ybar + H) / H * wid / 2           # half-width of the triangle at the bar
    return (_clip(uid, x, wid) + _stroke(d, col, uid)
            + f'<rect x="{x + wid/2 - half:.2f}" y="{ybar - W/2:.2f}" width="{2*half:.2f}" height="{W:.2f}" fill="{col}"/>', wid)

def glyph_S(x, col, uid=""):
    ra = SA / 2 - W / 2; rb = SB / 2 - W / 2; wid = SB
    cx = x + wid / 2; ca = -H + SA / 2; cb = -SB / 2
    p1 = _pt(cx, ca, ra, -25); p2 = (cx, ca + ra); p3 = _pt(cx, cb, rb, 155)
    d = (f"M{p1[0]:.2f},{p1[1]:.2f} A{ra:.2f},{ra:.2f} 0 1 0 {p2[0]:.2f},{p2[1]:.2f} "
         f"A{rb:.2f},{rb:.2f} 0 1 1 {p3[0]:.2f},{p3[1]:.2f}")
    return _stroke(d, col, join="round"), wid

def glyph_3(x, col, uid=""):
    ra = SA / 2 - W / 2; rb = SB / 2 - W / 2; wid = SB
    cx = x + wid / 2; ca = -H + SA / 2; cb = -SB / 2
    p1 = _pt(cx, ca, ra, 205); p2 = (cx - W * .3, ca + ra); p3 = _pt(cx, cb, rb, 155)
    d = (f"M{p1[0]:.2f},{p1[1]:.2f} A{ra:.2f},{ra:.2f} 0 1 1 {cx:.2f},{ca + ra:.2f} L{p2[0]:.2f},{p2[1]:.2f} M{cx:.2f},{cb - rb:.2f} "
         f"A{rb:.2f},{rb:.2f} 0 1 1 {p3[0]:.2f},{p3[1]:.2f}")
    return _stroke(d, col), wid

def glyph_0(x, col, uid=""):
    r = D / 2 - W / 2; cx = x + D / 2; top = -H + D / 2; bot = -D / 2
    d = (f"M{cx - r:.2f},{bot:.2f} L{cx - r:.2f},{top:.2f} A{r:.2f},{r:.2f} 0 0 1 {cx + r:.2f},{top:.2f} "
         f"L{cx + r:.2f},{bot:.2f} A{r:.2f},{r:.2f} 0 0 1 {cx - r:.2f},{bot:.2f} Z")
    return _stroke(d, col), D

def glyph_1(x, col, uid="g1"):
    wid = H / PHI ** 2 + W
    sx = x + wid - W / 2
    d = f"M{x + W*.2:.2f},{-H + H/PHI**3:.2f} L{sx:.2f},{-H - W*.4:.2f} L{sx:.2f},{W:.2f}"
    return _clip(uid, x, wid) + _stroke(d, col, uid), wid

def glyph_4(x, col, uid="g4"):
    wid = D; sx = x + D * .72; yb = -H / PHI ** 2
    d = f"M{sx:.2f},{W:.2f} L{sx:.2f},{-H - W:.2f} L{x + W*.4:.2f},{yb:.2f}"
    return (_clip(uid, x, wid) + _stroke(d, col, uid)
            + f'<rect x="{x:.2f}" y="{yb - W/2:.2f}" width="{wid:.2f}" height="{W:.2f}" fill="{col}"/>', wid)

def glyph_7(x, col, uid="g7"):
    wid = D
    d = f"M{x:.2f},{-H + W/2:.2f} L{x + wid - W/2:.2f},{-H + W/2:.2f} L{x + D/PHI**2:.2f},{W:.2f}"
    return _clip(uid, x, wid) + _stroke(d, col, uid), wid

def glyph_9(x, col, uid="g9"):
    s, adv = glyph_6(x, col, uid)
    return f'<g transform="rotate(180 {x + D/2:.2f} {-H/2:.2f})">{s}</g>', adv

GLYPHS = {"O": glyph_O, "C": glyph_C, "T": glyph_T, "S": glyph_S, "I": glyph_I, "E": glyph_E, "P": glyph_P,
          "R": glyph_R, "D": glyph_D, "M": glyph_M, "N": glyph_N, "A": glyph_A, "0": glyph_0, "1": glyph_1,
          "2": glyph_2, "3": glyph_3, "4": glyph_4, "6": glyph_6, "7": glyph_7, "9": glyph_9}

# The master logo is split on the golden ratio: "OCT. " : "26" = phi^2 : 1, so the whole word is (phi^2 + 1) : 1
# of the number. Its word gap comes from that split (32.2); every other name uses the plain word gap H / phi^2.
SPLIT = {"OCT. 26"}

def _space(text):
    if text in SPLIT:
        left, right = text.split(" ")
        return PHI ** 2 * word(right, "#000", "#000")[1] - word(left, "#000", "#000")[1]
    return WORD

def word(text, ink, dot, uid="w", stops=None):
    """Lay out any brand name built from GLYPHS, '.' and ' '. Returns (svg, width).
    Pass a dict as `stops` to get the x position where each character starts."""
    parts, x, sp = [], 0.0, None
    for i, ch in enumerate(text):
        if stops is not None:
            stops.setdefault(ch, x)
        if ch == " ":
            sp = _space(text) if sp is None else sp
            x += sp; continue
        if ch == ".":
            s, adv = glyph_dot(x, dot)
        else:
            fn = GLYPHS[ch]
            try:
                s, adv = fn(x, ink, f"{uid}{i}")
            except TypeError:
                s, adv = fn(x, ink)
        parts.append(s); x += adv
        nxt = text[i + 1] if i + 1 < len(text) else ""
        if nxt and nxt not in " ":
            x += GAP / PHI if nxt == "." else GAP
    return "".join(parts), x

def wordmark(ink, dot, uid="wm"):
    """OCT. 26 on the baseline y=0, cap line y=-H. Returns (svg, width, stops) where stops are x positions."""
    st = {}
    s, w = word("OCT. 26", ink, dot, uid, st)
    return s, w, st

def digits_26(x, ink, uid):
    a, adv = glyph_2(x, ink, uid + "a")
    b, _ = glyph_6(x + adv + GAP, ink, uid)
    return a + b, adv + GAP + D

if __name__ == "__main__":
    _, width, stops = wordmark("#000", "#f00")
    print(f"w={W:.2f} dot={DOT:.2f} D={D:.2f} T={TW:.2f} C open={C_OPEN:.1f} width={width:.1f} ratio={width/H:.3f}")
