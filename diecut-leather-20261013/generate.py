"""Generate 1:1 die-cut drawings (DXF / SVG / PDF) for the 6 leather patterns.

Units: mm. Origin: bottom-left of each pattern's bounding box, Y up (CAD convention).
CUT  (black) = outline, full-cut steel rule
SLIT (red)   = through-cut slit / slot for interlocking
Dimensions were read off the artboard screenshot (approx. +/-0.5 mm).
"""
import math, os
import ezdxf
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- geometry
# segment: ("line", (x1,y1), (x2,y2))  |  ("arc", (cx,cy), r, a0, a1, ccw)  angles in deg
def pt(c, r, a):
    return (c[0] + r * math.cos(math.radians(a)), c[1] + r * math.sin(math.radians(a)))

def ang(c, p):
    return math.degrees(math.atan2(p[1] - c[1], p[0] - c[0])) % 360

def seg_start(s):
    return s[1] if s[0] == "line" else pt(s[1], s[2], s[3])

def seg_end(s):
    return s[2] if s[0] == "line" else pt(s[1], s[2], s[4])

def sweep(s):
    a0, a1, ccw = s[3], s[4], s[5]
    return ((a1 - a0) % 360 or 360) if ccw else -((a0 - a1) % 360 or 360)

def circle_union(circles):
    """Outer outline (CCW arcs) of a union of circles."""
    arcs = []
    for i, (ci, ri) in enumerate(circles):
        cuts = []
        for j, (cj, rj) in enumerate(circles):
            if i == j:
                continue
            d = math.dist(ci, cj)
            if d >= ri + rj or d <= abs(ri - rj):
                continue
            a = (ri**2 - rj**2 + d**2) / (2 * d)
            h = math.sqrt(ri**2 - a**2)
            mx = ci[0] + a * (cj[0] - ci[0]) / d
            my = ci[1] + a * (cj[1] - ci[1]) / d
            for sgn in (1, -1):
                p = (mx + sgn * h * (cj[1] - ci[1]) / d, my - sgn * h * (cj[0] - ci[0]) / d)
                cuts.append(ang(ci, p))
        cuts = sorted(set(round(c, 9) for c in cuts))
        if not cuts:
            arcs.append(("arc", ci, ri, 0, 360, True))
            continue
        for k, a0 in enumerate(cuts):
            a1 = cuts[(k + 1) % len(cuts)]
            mid = a0 + ((a1 - a0) % 360) / 2
            m = pt(ci, ri, mid)
            if all(math.dist(m, cj) > rj - 1e-6 for j, (cj, rj) in enumerate(circles) if j != i):
                arcs.append(("arc", ci, ri, a0, a1, True))
    return chain(arcs)

def chain(segs):
    out, rest = [segs[0]], segs[1:]
    while rest:
        e = seg_end(out[-1])
        k = min(range(len(rest)), key=lambda k: math.dist(e, seg_start(rest[k])))
        out.append(rest.pop(k))
    return out

def L(a, b):
    return ("line", a, b)

# ---------------------------------------------------------------- patterns
P = []

# 01 Bear head 95 x 90
face_c, face_r = (47.5, 41.5), 41.5
ear_r = 12.5
earL, earR = (12.5, 77.5), (82.5, 77.5)
cut = circle_union([(face_c, face_r), (earL, ear_r), (earR, ear_r)])
slits = []
for a in (225, 315):
    m = pt(face_c, 30.5, a)
    t = math.radians(a + 90)
    dx, dy = 8.5 * math.cos(t), 8.5 * math.sin(t)
    slits.append(L((m[0] - dx, m[1] - dy), (m[0] + dx, m[1] + dy)))
P.append(dict(code="01", name="Bear head", W=95, H=90, cut=cut, slits=slits,
              geom=[f"Face circle  R{face_r}  center ({face_c[0]}, {face_c[1]})",
                    f"Ear circles  R{ear_r}  centers ({earL[0]}, {earL[1]}) / ({earR[0]}, {earR[1]})",
                    "Outline = union of the 3 circles",
                    "Slits 17.0 long, tangent to R30.5 from face center, at 225 / 315 deg"]))

# 02 Four-lobe pinwheel 90 x 90
r2, off2 = 29.25, 15.75
c2 = [((45 + off2, 45), r2), ((45, 45 + off2), r2), ((45 - off2, 45), r2), ((45, 45 - off2), r2)]
cut = circle_union(c2)
# outer intersection of top & left lobes -> fold-square corner
d = off2 * math.sqrt(2); a = d / 2; h = math.sqrt(r2**2 - a**2)
q = 45 - off2 / 2 - h / math.sqrt(2)            # fold square: q .. 90-q
Q = 90 - q
s2 = 29.25
slits = [L((q, Q), (q + s2, Q)), L((Q, Q), (Q, Q - s2)), L((Q, q), (Q - s2, q)), L((q, q), (q, q + s2))]
P.append(dict(code="02", name="Pinwheel 4-lobe", W=90, H=90, cut=cut, slits=slits,
              geom=[f"4 lobe circles  R{r2}  centers 45 +/- {off2} on X and Y axes",
                    f"Fold square (lobe chords) {q:.2f} .. {Q:.2f}  ({Q-q:.2f} sq.)",
                    f"4 slots {s2} long on the fold lines, starting at the notches, pinwheel (CW)"]))

# 03 Plus / capsule cross 90 x 90
cut = [("arc", (45, 67.5), 22.5, 0, 180, True), ("arc", (22.5, 45), 22.5, 90, 270, True),
       ("arc", (45, 22.5), 22.5, 180, 360, True), ("arc", (67.5, 45), 22.5, 270, 90, True)]
slits = [L((30, 67.5), (60, 67.5)), L((30, 22.5), (60, 22.5)),
         L((22.5, 67.5), (22.5, 53.5)), L((22.5, 22.5), (22.5, 36.5)),
         L((67.5, 67.5), (67.5, 53.5)), L((67.5, 22.5), (67.5, 36.5))]
P.append(dict(code="03", name="Capsule cross", W=90, H=90, cut=cut, slits=slits,
              geom=["Center square 45 x 45 (22.5 .. 67.5) = fold lines",
                    "4 semicircle flaps R22.5 on each side of the square",
                    "Top/bottom fold: center slit 30.0 (X 30 .. 60)",
                    "Left/right fold: end slots 14.0 from each corner"]))

# 04 Rounded square 90 x 90, diagonal slits
rc = 5.0
cut = [L((rc, 0), (90 - rc, 0)), ("arc", (90 - rc, rc), rc, 270, 360, True),
       L((90, rc), (90, 90 - rc)), ("arc", (90 - rc, 90 - rc), rc, 0, 90, True),
       L((90 - rc, 90), (rc, 90)), ("arc", (rc, 90 - rc), rc, 90, 180, True),
       L((0, 90 - rc), (0, rc)), ("arc", (rc, rc), rc, 180, 270, True)]
k = 15 / math.sqrt(2); hl = 15 / math.sqrt(2)
slits = [L((45, 90), (45 + k, 90 - k)), L((90, 45), (90 - k, 45 + k)),
         L((0, 45), (k, 45 - k)), L((45, 0), (45 - k, k)),
         L((22.5 - hl, 67.5 - hl), (22.5 + hl, 67.5 + hl)),
         L((67.5 - hl, 22.5 - hl), (67.5 + hl, 22.5 + hl))]
P.append(dict(code="04", name="Rounded square diagonal", W=90, H=90, cut=cut, slits=slits,
              geom=[f"Square 90 x 90, corner R{rc}",
                    "Fold lines = diamond through edge midpoints (side 63.64)",
                    "TR / BL fold: end slots 15.0 at 45 deg from edge midpoints",
                    "TL / BR fold: center slit 30.0 centered at (22.5, 67.5) / (67.5, 22.5)"]))

# 05 Circle 90
s = 45 - 45 / math.sqrt(2); S = 90 - s
cut = [("arc", (45, 45), 45, 0, 360, True)]
slits = [L((30, S), (60, S)), L((30, s), (60, s)),
         L((s, S), (s, S - 15)), L((s, s), (s, s + 15)),
         L((S, S), (S, S - 15)), L((S, s), (S, s + 15))]
P.append(dict(code="05", name="Circle", W=90, H=90, cut=cut, slits=slits,
              geom=["Circle D90 (R45), center (45, 45)",
                    f"Fold lines = inscribed square {s:.2f} .. {S:.2f} (63.64 sq.)",
                    "Top/bottom fold: center slit 30.0 (X 30 .. 60)",
                    "Left/right fold: end slots 15.0 from each corner"]))

# 06 Soft cross (4 lobes + concave fillets) 90 x 90
R6, Lc, RF = 16.0, 29.0, 16.0
# fillet center at (45+aa, 45+aa): solve aa^2 + (Lc-aa)^2 = (R6+RF)^2
aa = (2 * Lc + math.sqrt(4 * Lc**2 - 8 * (Lc**2 - (R6 + RF)**2))) / 4
lobes = [(45 + Lc * math.cos(math.radians(t)), 45 + Lc * math.sin(math.radians(t))) for t in (0, 90, 180, 270)]
fil = [(45 + sx * aa, 45 + sy * aa) for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1))]
def tan_pt(lc, fc):
    dd = math.dist(lc, fc)
    return (lc[0] + R6 * (fc[0] - lc[0]) / dd, lc[1] + R6 * (fc[1] - lc[1]) / dd)
cut = []
for i in range(4):
    lc = lobes[i]
    fprev, fnext = fil[i - 1], fil[i]          # fil[i] lies CCW after lobe i
    t0, t1 = tan_pt(lc, fprev), tan_pt(lc, fnext)
    cut.append(("arc", lc, R6, ang(lc, t0), ang(lc, t1), True))
    nl = lobes[(i + 1) % 4]
    u0, u1 = t1, tan_pt(nl, fnext)
    cut.append(("arc", fnext, RF, ang(fnext, u0), ang(fnext, u1), False))
f6 = 13.2; F6 = 90 - f6
ye = math.sqrt(R6**2 - (f6 - (45 - Lc))**2)
slits = [L((37.5, F6), (52.5, F6)), L((37.5, f6), (52.5, f6)),
         L((f6, 45 + ye), (f6, 45 + ye - 5)), L((f6, 45 - ye), (f6, 45 - ye + 5)),
         L((F6, 45 + ye), (F6, 45 + ye - 5)), L((F6, 45 - ye), (F6, 45 - ye + 5))]
P.append(dict(code="06", name="Soft cross", W=90, H=90, cut=cut, slits=slits,
              geom=[f"4 lobes R{R6}, centers {Lc} from (45,45) on X/Y axes",
                    f"4 concave fillets R{RF}, centers ({45+aa:.2f}, {45+aa:.2f}) etc.",
                    f"Fold lines = square {f6} .. {F6}",
                    "Top/bottom fold: center slit 15.0 (X 37.5 .. 52.5)",
                    "Left/right fold: end slots 5.0 from the outline"]))

# ---------------------------------------------------------------- writers
def dxf_add(msp, p, ox=0, oy=0):
    for sgm in p["cut"]:
        add_seg(msp, sgm, "CUT", ox, oy)
    for sgm in p["slits"]:
        add_seg(msp, sgm, "SLIT", ox, oy)

def add_seg(msp, s, layer, ox, oy):
    if s[0] == "line":
        msp.add_line((s[1][0] + ox, s[1][1] + oy), (s[2][0] + ox, s[2][1] + oy), dxfattribs={"layer": layer})
        return
    c = (s[1][0] + ox, s[1][1] + oy)
    if abs(sweep(s)) >= 359.999:
        msp.add_circle(c, s[2], dxfattribs={"layer": layer})
    elif s[5]:
        msp.add_arc(c, s[2], s[3], s[4], dxfattribs={"layer": layer})
    else:
        msp.add_arc(c, s[2], s[4], s[3], dxfattribs={"layer": layer})

def new_doc():
    doc = ezdxf.new("R2000", setup=False)
    doc.units = ezdxf.units.MM
    doc.header["$INSUNITS"] = 4
    doc.layers.add("CUT", color=7)
    doc.layers.add("SLIT", color=1)
    doc.layers.add("NOTE_NOT_CUT", color=8)
    return doc

def svg_path(segs, H):
    f = lambda p: f"{p[0]:.3f},{H - p[1]:.3f}"
    out = []
    for i, s in enumerate(segs):
        if s[0] == "line":
            out.append(f"M{f(s[1])} L{f(s[2])}" if i == 0 else f"L{f(s[2])}")
            continue
        sw = sweep(s)
        if i == 0:
            out.append(f"M{f(seg_start(s))}")
        if abs(sw) >= 359.999:   # full circle -> two halves
            mid = pt(s[1], s[2], s[3] + 180)
            out.append(f"A{s[2]},{s[2]} 0 0 0 {f(mid)} A{s[2]},{s[2]} 0 0 0 {f(seg_start(s))}")
            continue
        large = 1 if abs(sw) > 180 else 0
        flag = 0 if sw > 0 else 1        # SVG y is flipped
        out.append(f"A{s[2]},{s[2]} 0 {large} {flag} {f(seg_end(s))}")
    return " ".join(out) + " Z"

def write_svg(p, path):
    W, H = p["W"], p["H"]
    lines = "\n".join(
        f'  <line x1="{s[1][0]:.3f}" y1="{H - s[1][1]:.3f}" x2="{s[2][0]:.3f}" y2="{H - s[2][1]:.3f}"/>'
        for s in p["slits"])
    open(path, "w").write(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">
 <title>{p["code"]} {p["name"]} - {W}x{H} mm - 1:1</title>
 <g id="CUT" fill="none" stroke="#000000" stroke-width="0.2">
  <path d="{svg_path(p["cut"], H)}"/>
 </g>
 <g id="SLIT" fill="none" stroke="#FF0000" stroke-width="0.2">
{lines}
 </g>
</svg>
''')

# ---- PDF drawing
RED = (0.9, 0.0, 0.0)
BLUE = (0.05, 0.3, 0.75)

def draw_segs(c, segs, ox, oy, close=True):
    p = c.beginPath()
    for i, s in enumerate(segs):
        st = seg_start(s)
        if i == 0:
            p.moveTo((ox + st[0]) * mm, (oy + st[1]) * mm)
        if s[0] == "line":
            p.lineTo((ox + s[2][0]) * mm, (oy + s[2][1]) * mm)
        else:
            cx, cy, r = s[1][0] + ox, s[1][1] + oy, s[2]
            p.arcTo((cx - r) * mm, (cy - r) * mm, (cx + r) * mm, (cy + r) * mm, s[3], sweep(s))
    if close:
        p.close()
    c.drawPath(p, stroke=1, fill=0)

def arrow(c, x, y, ux, uy, size=1.8):
    px, py = -uy, ux
    p = c.beginPath()
    p.moveTo(x * mm, y * mm)
    p.lineTo((x - ux * size + px * size * 0.3) * mm, (y - uy * size + py * size * 0.3) * mm)
    p.lineTo((x - ux * size - px * size * 0.3) * mm, (y - uy * size - py * size * 0.3) * mm)
    p.close()
    c.drawPath(p, stroke=0, fill=1)

def dim(c, a, b, offset, text=None, fs=7):
    """Aligned dimension between a and b (page mm), offset to the left of a->b."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    Ld = math.hypot(dx, dy); ux, uy = dx / Ld, dy / Ld
    nx, ny = -uy, ux
    a2 = (a[0] + nx * offset, a[1] + ny * offset); b2 = (b[0] + nx * offset, b[1] + ny * offset)
    c.setStrokeColorRGB(*BLUE); c.setFillColorRGB(*BLUE); c.setLineWidth(0.25)
    sgn = 1 if offset >= 0 else -1
    for p0, p1 in ((a, a2), (b, b2)):
        c.line((p0[0] + nx * sgn * 0.8) * mm, (p0[1] + ny * sgn * 0.8) * mm,
               (p1[0] + nx * sgn * 1.5) * mm, (p1[1] + ny * sgn * 1.5) * mm)
    c.line(a2[0] * mm, a2[1] * mm, b2[0] * mm, b2[1] * mm)
    arrow(c, a2[0], a2[1], -ux, -uy); arrow(c, b2[0], b2[1], ux, uy)
    t = text or f"{Ld:.1f}".rstrip("0").rstrip(".")
    c.saveState()
    mx, my = (a2[0] + b2[0]) / 2 + nx * 1.0 * (1 if sgn > 0 else -2.6), (a2[1] + b2[1]) / 2 + ny * 1.0 * (1 if sgn > 0 else -2.6)
    c.translate(mx * mm, my * mm)
    rot = math.degrees(math.atan2(uy, ux))
    if rot > 90.1 or rot < -89.9:
        rot += 180
    c.rotate(rot)
    c.setFont("Helvetica", fs)
    c.drawCentredString(0, 0, t)
    c.restoreState()

def leader(c, p_on, p_txt, text, color=BLUE, fs=7):
    c.setStrokeColorRGB(*color); c.setFillColorRGB(*color); c.setLineWidth(0.25)
    c.line(p_on[0] * mm, p_on[1] * mm, p_txt[0] * mm, p_txt[1] * mm)
    ux, uy = p_on[0] - p_txt[0], p_on[1] - p_txt[1]; l = math.hypot(ux, uy)
    arrow(c, p_on[0], p_on[1], ux / l, uy / l)
    c.setFont("Helvetica", fs)
    if p_txt[0] < p_on[0]:
        c.drawRightString((p_txt[0] - 0.8) * mm, (p_txt[1] - 1) * mm, text)
    else:
        c.drawString((p_txt[0] + 0.8) * mm, (p_txt[1] - 1) * mm, text)

def centermark(c, x, y, s=1.5):
    c.setStrokeColorRGB(*BLUE); c.setLineWidth(0.2)
    c.line((x - s) * mm, y * mm, (x + s) * mm, y * mm); c.line(x * mm, (y - s) * mm, x * mm, (y + s) * mm)

def title_block(c, p, sheet, total, title, subtitle):
    x0, y0, w, h = 10, 10, 190, 34
    c.setStrokeColorRGB(0, 0, 0); c.setFillColorRGB(0, 0, 0); c.setLineWidth(0.5)
    c.rect(8 * mm, 8 * mm, 194 * mm, 281 * mm)
    c.rect(x0 * mm, y0 * mm, w * mm, h * mm)
    c.setLineWidth(0.3)
    for xx in (110, 150):
        c.line(xx * mm, y0 * mm, xx * mm, (y0 + h) * mm)
    c.line(x0 * mm, (y0 + 17) * mm, (x0 + w) * mm, (y0 + 17) * mm)
    c.setFont("Helvetica-Bold", 12); c.drawString(13 * mm, 35 * mm, title)
    c.setFont("Helvetica", 8); c.drawString(13 * mm, 30 * mm, subtitle)
    c.setFont("Helvetica", 7)
    c.drawString(13 * mm, 22 * mm, "Project: Leather no-sew interlocking patterns (20261013)")
    c.drawString(13 * mm, 17.5 * mm, "Material: genuine leather 1.2-2.0 mm  |  Process: steel-rule / clicker die")
    c.drawString(13 * mm, 13 * mm, "Dims read from artboard screenshot: verify vs. original .ai before die order")
    c.drawString(113 * mm, 37 * mm, "SCALE"); c.setFont("Helvetica-Bold", 11); c.drawString(113 * mm, 31 * mm, "1 : 1")
    c.setFont("Helvetica", 7); c.drawString(113 * mm, 22 * mm, "UNITS: mm"); c.drawString(113 * mm, 17.5 * mm, "TOL: +/-0.2 mm")
    c.drawString(113 * mm, 13 * mm, "PAPER: A4  (print 100%)")
    c.drawString(153 * mm, 37 * mm, "DATE: 2026-10-13")
    c.drawString(153 * mm, 31 * mm, f"SHEET: {sheet} / {total}")
    c.drawString(153 * mm, 22 * mm, "DRAWN: Claude Code")
    c.drawString(153 * mm, 17.5 * mm, "CHECKED: ________")
    c.drawString(153 * mm, 13 * mm, "APPROVED: ________")

def legend(c, x, y):
    c.setLineWidth(0.6)
    c.setStrokeColorRGB(0, 0, 0); c.line(x * mm, y * mm, (x + 10) * mm, y * mm)
    c.setStrokeColorRGB(*RED); c.line(x * mm, (y - 5) * mm, (x + 10) * mm, (y - 5) * mm)
    c.setFillColorRGB(0, 0, 0); c.setFont("Helvetica", 7)
    c.drawString((x + 12) * mm, (y - 1) * mm, "CUT  - outline, full-cut rule")
    c.drawString((x + 12) * mm, (y - 6) * mm, "SLIT - through-cut slit / slot (red)")
    c.setStrokeColorRGB(*BLUE); c.setLineWidth(0.25)
    c.line(x * mm, (y - 10) * mm, (x + 10) * mm, (y - 10) * mm)
    c.drawString((x + 12) * mm, (y - 11) * mm, "Dimension - not cut")

def scale_bar(c, x, y):
    c.setStrokeColorRGB(0, 0, 0); c.setLineWidth(0.4)
    c.line(x * mm, y * mm, (x + 50) * mm, y * mm)
    for i in range(0, 51, 10):
        c.line((x + i) * mm, y * mm, (x + i) * mm, (y + (2 if i % 50 else 3)) * mm)
    c.setFont("Helvetica", 6.5); c.setFillColorRGB(0, 0, 0)
    c.drawString(x * mm, (y - 3.5) * mm, "Check print: this bar must measure exactly 50 mm")

def fmt(p):
    return f"({p[0]:.2f}, {p[1]:.2f})"

def pattern_page(c, p, sheet, total):
    W, H = p["W"], p["H"]
    ox, oy = (210 - W) / 2, 150
    title_block(c, p, sheet, total, f"PATTERN {p['code']} - {p['name'].upper()}",
                f"Overall {W} x {H} mm  |  1 cut outline + {len(p['slits'])} slits")
    # geometry
    c.setStrokeColorRGB(0, 0, 0); c.setLineWidth(0.35)
    draw_segs(c, p["cut"], ox, oy)
    c.setStrokeColorRGB(*RED); c.setLineWidth(0.35)
    for s in p["slits"]:
        c.line((ox + s[1][0]) * mm, (oy + s[1][1]) * mm, (ox + s[2][0]) * mm, (oy + s[2][1]) * mm)
    # bounding / overall dims
    c.setStrokeColorRGB(0.6, 0.6, 0.6); c.setLineWidth(0.15); c.setDash(1, 1)
    c.rect(ox * mm, oy * mm, W * mm, H * mm); c.setDash()
    dim(c, (ox, oy), (ox + W, oy), -10)
    dim(c, (ox, oy), (ox, oy + H), 10)
    c.setFont("Helvetica", 6.5); c.setFillColorRGB(*BLUE)
    c.drawString((ox - 4) * mm, (oy - 4) * mm, "0,0")
    centermark(c, ox, oy, 2)
    PAGE_DIMS[p["code"]](c, p, ox, oy)
    # tables
    y = oy - 25
    c.setFillColorRGB(0, 0, 0); c.setFont("Helvetica-Bold", 8); c.drawString(14 * mm, y * mm, "GEOMETRY")
    c.setFont("Helvetica", 7)
    for g in p["geom"]:
        y -= 4; c.drawString(14 * mm, y * mm, "- " + g)
    y -= 7
    c.setFont("Helvetica-Bold", 8); c.drawString(14 * mm, y * mm, "SLIT COORDINATES (origin = bottom-left 0,0)")
    c.setFont("Helvetica", 7)
    for i, s in enumerate(p["slits"], 1):
        y -= 4
        c.drawString(14 * mm, y * mm, f"S{i}:  {fmt(s[1])}  ->  {fmt(s[2])}    L = {math.dist(s[1], s[2]):.2f}")
    legend(c, 140, oy - 25)
    scale_bar(c, 140, oy - 45)

# per-pattern dimension annotations (page coords = ox+x, oy+y)
def d01(c, p, ox, oy):
    fc = (ox + 47.5, oy + 41.5); centermark(c, *fc)
    leader(c, (fc[0] + 41.5 * math.cos(math.radians(-20)), fc[1] + 41.5 * math.sin(math.radians(-20))), (ox + 108, oy + 18), "R41.5")
    for e, side in ((earL, -1), (earR, 1)):
        ec = (ox + e[0], oy + e[1]); centermark(c, *ec)
        a = 135 if side < 0 else 45
        leader(c, (ec[0] + 12.5 * math.cos(math.radians(a)), ec[1] + 12.5 * math.sin(math.radians(a))),
               (ec[0] + side * 14, ec[1] + 18), "R12.5")
    dim(c, (ox + 12.5, oy + 90), (ox + 82.5, oy + 90), 8, "70 (ear c-c)")
    dim(c, (ox + 95, oy), (ox + 95, oy + 41.5), -8, "41.5")
    dim(c, (ox + 95, oy + 41.5), (ox + 95, oy + 77.5), -8, "36")
    s = p["slits"][1]; dim(c, (ox + s[1][0], oy + s[1][1]), (ox + s[2][0], oy + s[2][1]), 3, "17")
    c.setFillColorRGB(*BLUE); c.setFont("Helvetica", 6.5)
    c.drawString((ox + 30) * mm, (oy + 33) * mm, "slits 45 deg, tangent to R30.5")

def d02(c, p, ox, oy):
    q = p["slits"][0][1][0]; Q = 90 - q
    for cc in ((45 + off2, 45), (45, 45 + off2), (45 - off2, 45), (45, 45 - off2)):
        centermark(c, ox + cc[0], oy + cc[1], 1)
    leader(c, (ox + 45 + off2 + r2 * math.cos(math.radians(-30)), oy + 45 + r2 * math.sin(math.radians(-30))),
           (ox + 103, oy + 15), "4x R29.25")
    dim(c, (ox + q, oy + Q), (ox + Q, oy + Q), 24, f"{Q - q:.2f} (fold sq.)")
    dim(c, (ox + q, oy + Q), (ox + q + s2, oy + Q), 4, "29.25")
    dim(c, (ox + 90, oy), (ox + 90, oy + q), -6, f"{q:.2f}")
    dim(c, (ox + 45 - off2, oy + 45), (ox + 45 + off2, oy + 45), 3, "31.5", fs=6)
    c.setFillColorRGB(*BLUE); c.setFont("Helvetica", 6.5)
    c.drawString((ox + 26) * mm, (oy + 40) * mm, "lobe centers 45 +/- 15.75")

def d03(c, p, ox, oy):
    leader(c, (ox + 45 + 22.5 * math.cos(math.radians(45)), oy + 67.5 + 22.5 * math.sin(math.radians(45))),
           (ox + 85, oy + 98), "4x R22.5")
    dim(c, (ox + 22.5, oy + 22.5), (ox + 67.5, oy + 22.5), -4, "45")
    dim(c, (ox + 30, oy + 67.5), (ox + 60, oy + 67.5), 4, "30")
    dim(c, (ox + 22.5, oy + 67.5), (ox + 30, oy + 67.5), 4, "7.5", fs=6)
    dim(c, (ox + 22.5, oy + 67.5), (ox + 22.5, oy + 53.5), -4, "14")
    dim(c, (ox + 90, oy + 22.5), (ox + 90, oy + 67.5), -6, "45")

def d04(c, p, ox, oy):
    leader(c, (ox + 90 - rc + rc * math.cos(math.radians(45)), oy + 90 - rc + rc * math.sin(math.radians(45))),
           (ox + 100, oy + 98), "4x R5")
    s = p["slits"]
    dim(c, (ox + s[0][1][0], oy + s[0][1][1]), (ox + s[0][2][0], oy + s[0][2][1]), -3, "15")
    dim(c, (ox + s[4][1][0], oy + s[4][1][1]), (ox + s[4][2][0], oy + s[4][2][1]), 3, "30")
    dim(c, (ox, oy + 90), (ox + 45, oy + 90), 4, "45")
    dim(c, (ox + 90, oy), (ox + 90, oy + 45), -6, "45")
    c.setStrokeColorRGB(*BLUE); c.setLineWidth(0.15); c.setDash([2, 1, 0.5, 1])
    for a, b in (((0, 45), (45, 90)), ((45, 90), (90, 45)), ((90, 45), (45, 0)), ((45, 0), (0, 45))):
        c.line((ox + a[0]) * mm, (oy + a[1]) * mm, (ox + b[0]) * mm, (oy + b[1]) * mm)
    c.setDash()
    c.setFillColorRGB(*BLUE); c.setFont("Helvetica", 6.5)
    c.drawString((ox + 33) * mm, (oy + 44) * mm, "fold diamond (ref. only)")

def d05(c, p, ox, oy):
    centermark(c, ox + 45, oy + 45)
    leader(c, (ox + 45 + 45 * math.cos(math.radians(-30)), oy + 45 + 45 * math.sin(math.radians(-30))),
           (ox + 104, oy + 12), "R45 (D90)")
    dim(c, (ox + 30, oy + S), (ox + 60, oy + S), 4, "30")
    dim(c, (ox + s, oy + S), (ox + 30, oy + S), 4, f"{30 - s:.2f}", fs=6)
    dim(c, (ox + s, oy + S), (ox + s, oy + S - 15), -4, "15")
    dim(c, (ox + s, oy + s), (ox + S, oy + s), -4, f"{S - s:.2f}")
    dim(c, (ox + 90, oy), (ox + 90, oy + s), -6, f"{s:.2f}")

def d06(c, p, ox, oy):
    for lc in lobes:
        centermark(c, ox + lc[0], oy + lc[1], 1)
    leader(c, (ox + lobes[1][0] + R6 * math.cos(math.radians(60)), oy + lobes[1][1] + R6 * math.sin(math.radians(60))),
           (ox + 80, oy + 100), "4x R16 (lobe)")
    fc = fil[3]
    v = pt(fc, RF, 135)
    leader(c, (ox + v[0], oy + v[1]), (ox + 102, oy + 8), "4x R16 (concave)")
    dim(c, (ox + 45, oy + 45), (ox + 45 + Lc, oy + 45), 3, "29", fs=6)
    dim(c, (ox + 37.5, oy + F6), (ox + 52.5, oy + F6), 4, "15")
    dim(c, (ox + f6, oy + 45 + ye), (ox + f6, oy + 45 + ye - 5), -4, "5")
    dim(c, (ox + 90, oy), (ox + 90, oy + f6), -6, f"{f6}")
    centermark(c, ox + 45, oy + 45)

PAGE_DIMS = {"01": d01, "02": d02, "03": d03, "04": d04, "05": d05, "06": d06}

def overview_page(c, total):
    title_block(c, None, 1, total, "OVERVIEW - 6 LEATHER DIE-CUT PATTERNS", "Reduced scale on this sheet only (approx. 1:1.6). Sheets 2-7 are 1:1.")
    sc = 0.62
    pos = [(18, 205), (80, 205), (142, 205), (18, 120), (80, 120), (142, 120)]
    for p, (x, y) in zip(P, pos):
        c.saveState(); c.translate(x * mm, y * mm); c.scale(sc, sc)
        c.setStrokeColorRGB(0, 0, 0); c.setLineWidth(0.5); draw_segs(c, p["cut"], 0, 0)
        c.setStrokeColorRGB(*RED)
        for s in p["slits"]:
            c.line(s[1][0] * mm, s[1][1] * mm, s[2][0] * mm, s[2][1] * mm)
        c.restoreState()
        c.setFillColorRGB(0, 0, 0); c.setFont("Helvetica-Bold", 8)
        c.drawString(x * mm, (y + p["H"] * sc + 4) * mm, f"{p['code']}  {p['name']}")
        c.setFont("Helvetica", 7)
        c.drawString(x * mm, (y + p["H"] * sc + 0.5) * mm, f"{p['W']} x {p['H']} mm  |  {len(p['slits'])} slits")
    y = 108
    c.setFont("Helvetica-Bold", 8); c.drawString(14 * mm, y * mm, "DIE MAKER NOTES")
    c.setFont("Helvetica", 7)
    notes = [
        "1. All drawings 1:1, mm. Use DXF files (layers CUT / SLIT) for production; this PDF is the dimensioned reference.",
        "2. CUT (black) = outline, full cut. SLIT (red) = through cut, same rule height as CUT so slits cut fully through leather.",
        "3. Slits that start on the outline (open slots) must join the outline rule cleanly (T-joint), no gap, no overcut past outline.",
        "4. Suggested rule: 2pt (0.71 mm) centre-bevel, height 23.8 mm (or per die maker std.) for leather 1.2-2.0 mm.",
        "5. Recommended: dia. 1.5 mm round punch at the closed end of each slit to stop leather tearing (confirm with designer).",
        "6. Concave sharp corners (01, 02, 03) - die maker may use smallest practical inner radius (<= R0.5).",
        "7. Add ejection rubber/foam inside the outline and both sides of each slit.",
        "8. Dimensions are derived from the artboard screenshot (+/-0.5 mm). Confirm against the original .ai file before cutting steel.",
    ]
    for n in notes:
        y -= 4.5; c.drawString(14 * mm, y * mm, n)
    legend(c, 140, 62)
    scale_bar(c, 14, 54)

def main():
    total = len(P) + 1
    c = canvas.Canvas(os.path.join(OUT, "diecut-drawings-1to1.pdf"), pagesize=A4)
    c.setTitle("Leather die-cut drawings 1:1 - 20261013")
    overview_page(c, total); c.showPage()
    for i, p in enumerate(P, 2):
        pattern_page(c, p, i, total); c.showPage()
    c.save()

    os.makedirs(os.path.join(OUT, "dxf"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "svg"), exist_ok=True)
    allp = new_doc(); amsp = allp.modelspace()
    for i, p in enumerate(P):
        slug = f"{p['code']}-{p['name'].lower().replace(' ', '-').replace('/', '')}"
        doc = new_doc(); dxf_add(doc.modelspace(), p); doc.saveas(os.path.join(OUT, "dxf", slug + ".dxf"))
        write_svg(p, os.path.join(OUT, "svg", slug + ".svg"))
        ox, oy = (i % 3) * 120, -(i // 3) * 120
        dxf_add(amsp, p, ox, oy)
        amsp.add_text(f"{p['code']} {p['name']} {p['W']}x{p['H']}", height=3.5,
                      dxfattribs={"layer": "NOTE_NOT_CUT"}).set_placement((ox, oy + p["H"] + 5))
    allp.saveas(os.path.join(OUT, "dxf", "all-patterns.dxf"))

if __name__ == "__main__":
    main()
