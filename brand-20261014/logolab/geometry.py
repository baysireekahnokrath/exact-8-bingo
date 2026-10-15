"""Golden-ratio letterforms for the OCT. 26 logo proposals.

Every measure comes from one unit: cap height H = 100 and phi = 1.618.
  stroke w      = H / phi^4  = 14.59
  dot           = w * phi    = 23.61   (the dot is the one element bigger than the stroke)
  digit width D = H / phi    = 61.80
  T width       = H * phi/2  = 80.90
  C opening     = 360 / phi^3 = 84.98 degrees
  letter gap    = w,  word gap = H / phi^2 = 38.20
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

def glyph_O(x, col):
    r = H / 2 - W / 2
    return f'<circle cx="{x + H/2:.2f}" cy="{-H/2:.2f}" r="{r:.2f}" fill="none" stroke="{col}" stroke-width="{W:.2f}"/>', H

def glyph_C(x, col):
    r = H / 2 - W / 2; cx, cy = x + H / 2, -H / 2; half = C_OPEN / 2
    x1, y1 = _pt(cx, cy, r, half); x2, y2 = _pt(cx, cy, r, 360 - half)
    adv = cx + (H / 2) * math.cos(math.radians(half)) - x
    return (f'<path d="M{x1:.2f},{y1:.2f} A{r:.2f},{r:.2f} 0 1 1 {x2:.2f},{y2:.2f}" fill="none" stroke="{col}" stroke-width="{W:.2f}"/>', adv)

def glyph_T(x, col):
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

def wordmark(ink, dot, uid="wm"):
    """OCT. 26 on the baseline y=0, cap line y=-H. Returns (svg, width, stops) where stops are x positions."""
    parts, x, stops = [], 0.0, {}
    for key, fn, gap in (("O", glyph_O, GAP * .8), ("C", glyph_C, GAP), ("T", glyph_T, GAP / PHI),
                         (".", None, WORD), ("2", glyph_2, GAP), ("6", None, 0)):
        stops[key] = x
        if key == ".":
            s, adv = glyph_dot(x, dot)
        elif key == "6":
            s, adv = glyph_6(x, ink, uid + "6")
        elif key == "2":
            s, adv = glyph_2(x, ink, uid + "2")
        else:
            s, adv = fn(x, ink)
        parts.append(s); x += adv + gap
    return "".join(parts), x, stops

def digits_26(x, ink, uid):
    a, adv = glyph_2(x, ink, uid + "a")
    b, _ = glyph_6(x + adv + GAP, ink, uid)
    return a + b, adv + GAP + D

if __name__ == "__main__":
    _, width, stops = wordmark("#000", "#f00")
    print(f"w={W:.2f} dot={DOT:.2f} D={D:.2f} T={TW:.2f} C open={C_OPEN:.1f} width={width:.1f} ratio={width/H:.3f}")
