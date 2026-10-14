"""1:1 die-cut drawing set for the 20261014 revision, built from the designer's vector PDF.

Outputs: diecut-drawings-1to1.pdf, dxf/*.dxf (CUT / SLIT layers, true arcs and ellipses), svg/*.svg
"""
import math, os, sys
import ezdxf
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from extract import load, bez_pt

SRC = os.path.join(HERE, "source-20261014.pdf")
DATE = "2026-10-14"

# ---------------------------------------------------------------- classify bezier -> arc / ellipse / spline
def classify(s, tol=0.03):
    if s[0] == "line":
        return ("line", s[1], s[2])
    p0, c1, c2, p3 = s[1:]
    if max(math.dist(p0, q) for q in (c1, c2, p3)) < 0.05:      # micro joint in the artwork
        return ("line", p0, p3)
    t0 = (c1[0] - p0[0], c1[1] - p0[1]) if math.dist(c1, p0) > 1e-6 else (c2[0] - p0[0], c2[1] - p0[1])
    t1 = (p3[0] - c2[0], p3[1] - c2[1]) if math.dist(c2, p3) > 1e-6 else (p3[0] - c1[0], p3[1] - c1[1])
    samples = [bez_pt(s, i / 8) for i in range(9)]
    # circle: centre where the two end normals meet
    n0, n1 = (-t0[1], t0[0]), (-t1[1], t1[0])
    det = n0[0] * (-n1[1]) - n0[1] * (-n1[0])
    if abs(det) > 1e-9:
        dx, dy = p3[0] - p0[0], p3[1] - p0[1]
        a = (dx * (-n1[1]) - dy * (-n1[0])) / det
        C = (p0[0] + a * n0[0], p0[1] + a * n0[1])
        r = math.dist(C, p0)
        if r < 1e4 and all(abs(math.dist(C, q) - r) < tol for q in samples):
            a0 = math.degrees(math.atan2(p0[1] - C[1], p0[0] - C[0])) % 360
            a1 = math.degrees(math.atan2(p3[1] - C[1], p3[0] - C[0])) % 360
            ccw = (p0[0] - C[0]) * t0[1] - (p0[1] - C[1]) * t0[0] > 0
            return ("arc", C, r, a0, a1, ccw)
    # axis-aligned quarter ellipse
    hz = lambda t: abs(t[1]) < 2e-3 * abs(t[0]) and abs(t[0]) > 1e-9
    vt = lambda t: abs(t[0]) < 2e-3 * abs(t[1]) and abs(t[1]) > 1e-9
    C = None
    if hz(t0) and vt(t1): C = (p0[0], p3[1])
    elif vt(t0) and hz(t1): C = (p3[0], p0[1])
    if C:
        rx = max(abs(p0[0] - C[0]), abs(p3[0] - C[0])); ry = max(abs(p0[1] - C[1]), abs(p3[1] - C[1]))
        if rx > 1e-6 and ry > 1e-6 and all(abs(((q[0] - C[0]) / rx) ** 2 + ((q[1] - C[1]) / ry) ** 2 - 1) < 0.002 for q in samples):
            return ("ellipse", C, rx, ry, p0, p3, t0)
    return ("spline", p0, c1, c2, p3)

# ---------------------------------------------------------------- slit rules (agreed with the designer, 2026-10-14)
# Slot overrun past the outline is intentional: it guarantees the slot is cut right through. Keep as drawn.
# Receiving slits (B) are 0.5 mm longer than the tab neck: +0.25 mm at each end, centre unchanged.
CLEARANCE = 0.5
RECEIVERS = {"03": [0, 1], "04": [4, 5], "05": [4, 5], "06": [0, 1]}   # slit indexes in extraction order

def final_slits(p):
    out = []
    for i, sl in enumerate(p["slits"]):
        a, b = sl["raw"]
        note = f"runs {sl['trimmed']:.2f} past outline (as drawn)" if sl["trimmed"] > 0.05 else ""
        if i in RECEIVERS.get(p["code"], []):
            L = math.dist(a, b); ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L; e = CLEARANCE / 2
            a, b = (a[0] - ux * e, a[1] - uy * e), (b[0] + ux * e, b[1] + uy * e)
            note = f"lengthened {L:.2f} -> {L + CLEARANCE:.2f} (+0.25 each end)"
        out.append({"a": (round(a[0], 3), round(a[1], 3)), "b": (round(b[0], 3), round(b[1], 3)), "note": note})
    return out

# ---------------------------------------------------------------- DXF / SVG
def dxf_add(msp, p, ox=0, oy=0):
    o = lambda q: (q[0] + ox, q[1] + oy)
    for s in p["segs"]:
        k = classify(s)
        A = {"layer": "CUT"}
        if k[0] == "line":
            msp.add_line(o(k[1]), o(k[2]), dxfattribs=A)
        elif k[0] == "arc":
            _, C, r, a0, a1, ccw = k
            msp.add_arc(o(C), r, a0 if ccw else a1, a1 if ccw else a0, dxfattribs=A)
        elif k[0] == "ellipse":
            _, C, rx, ry, p0, p3, t0 = k
            if rx >= ry:
                major, ratio = (rx, 0), ry / rx
                par = lambda q: math.atan2((q[1] - C[1]) / ry, (q[0] - C[0]) / rx)
            else:
                major, ratio = (0, ry), rx / ry
                par = lambda q: math.atan2(-(q[0] - C[0]) / rx, (q[1] - C[1]) / ry)
            s0, s1 = par(p0), par(p3)
            mid = bez_pt(s, 0.5); sm = par(mid)
            # pick the CCW order whose span contains the mid point
            def inside(a, b, m):
                span = (b - a) % (2 * math.pi); return (m - a) % (2 * math.pi) <= span
            if not inside(s0, s1, sm):
                s0, s1 = s1, s0
            msp.add_ellipse(o(C), major_axis=major, ratio=ratio, start_param=s0, end_param=s1, dxfattribs=A)
        else:
            msp.add_open_spline([o(q) for q in k[1:]], degree=3, knots=[0, 0, 0, 0, 1, 1, 1, 1], dxfattribs=A)
    for sl in final_slits(p):
        msp.add_line(o(sl["a"]), o(sl["b"]), dxfattribs={"layer": "SLIT"})

def new_doc():
    doc = ezdxf.new("R2010", setup=False)
    doc.units = ezdxf.units.MM; doc.header["$INSUNITS"] = 4
    doc.layers.add("CUT", color=7); doc.layers.add("SLIT", color=1); doc.layers.add("NOTE_NOT_CUT", color=8)
    return doc

def svg_d(segs, H):
    f = lambda q: f"{q[0]:.3f},{H - q[1]:.3f}"
    d = [f"M{f(segs[0][1])}"]
    for s in segs:
        d.append(f"L{f(s[2])}" if s[0] == "line" else f"C{f(s[2])} {f(s[3])} {f(s[4])}")
    return " ".join(d) + " Z"

def write_svg(p, path):
    W, H = p["W"], p["H"]
    lines = "\n".join(f'  <line x1="{a[0]:.3f}" y1="{H-a[1]:.3f}" x2="{b[0]:.3f}" y2="{H-b[1]:.3f}"/>' for a, b in ((s["a"], s["b"]) for s in final_slits(p)))
    open(path, "w").write(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">
 <title>{p["code"]} {p["name"]} - {W}x{H} mm - 1:1 - rev {DATE}</title>
 <g id="CUT" fill="none" stroke="#000000" stroke-width="0.2"><path d="{svg_d(p["segs"], H)}"/></g>
 <g id="SLIT" fill="none" stroke="#FF0000" stroke-width="0.2">
{lines}
 </g>
</svg>
''')

# ---------------------------------------------------------------- PDF drawing helpers
RED, BLUE = (0.9, 0, 0), (0.05, 0.3, 0.75)

def draw_outline(c, segs, ox, oy):
    p = c.beginPath(); s0 = segs[0][1]
    p.moveTo((ox + s0[0]) * mm, (oy + s0[1]) * mm)
    for s in segs:
        if s[0] == "line":
            p.lineTo((ox + s[2][0]) * mm, (oy + s[2][1]) * mm)
        else:
            p.curveTo(*[(v + (ox if i % 2 == 0 else oy)) * mm for q in s[2:] for i, v in enumerate(q)])
    p.close(); c.drawPath(p, stroke=1, fill=0)

def arrow(c, x, y, ux, uy, size=1.8):
    px, py = -uy, ux; p = c.beginPath()
    p.moveTo(x * mm, y * mm)
    p.lineTo((x - ux * size + px * size * 0.3) * mm, (y - uy * size + py * size * 0.3) * mm)
    p.lineTo((x - ux * size - px * size * 0.3) * mm, (y - uy * size - py * size * 0.3) * mm)
    p.close(); c.drawPath(p, stroke=0, fill=1)

def dim(c, a, b, offset, text=None, fs=7):
    dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; nx, ny = -uy, ux
    a2 = (a[0] + nx * offset, a[1] + ny * offset); b2 = (b[0] + nx * offset, b[1] + ny * offset)
    c.setStrokeColorRGB(*BLUE); c.setFillColorRGB(*BLUE); c.setLineWidth(0.25)
    sg = 1 if offset >= 0 else -1
    for p0, p1 in ((a, a2), (b, b2)):
        c.line((p0[0] + nx * sg * 0.8) * mm, (p0[1] + ny * sg * 0.8) * mm, (p1[0] + nx * sg * 1.5) * mm, (p1[1] + ny * sg * 1.5) * mm)
    c.line(a2[0] * mm, a2[1] * mm, b2[0] * mm, b2[1] * mm)
    arrow(c, a2[0], a2[1], -ux, -uy); arrow(c, b2[0], b2[1], ux, uy)
    c.saveState()
    k = 1 if sg > 0 else -2.6
    c.translate(((a2[0] + b2[0]) / 2 + nx * k) * mm, ((a2[1] + b2[1]) / 2 + ny * k) * mm)
    rot = math.degrees(math.atan2(uy, ux))
    if rot > 90.1 or rot < -89.9: rot += 180
    c.rotate(rot); c.setFont("Helvetica", fs); c.drawCentredString(0, 0, text or f"{L:.2f}"); c.restoreState()

def leader(c, p_on, p_txt, text, fs=7):
    c.setStrokeColorRGB(*BLUE); c.setFillColorRGB(*BLUE); c.setLineWidth(0.25)
    c.line(p_on[0] * mm, p_on[1] * mm, p_txt[0] * mm, p_txt[1] * mm)
    ux, uy = p_on[0] - p_txt[0], p_on[1] - p_txt[1]; l = math.hypot(ux, uy); arrow(c, p_on[0], p_on[1], ux / l, uy / l)
    c.setFont("Helvetica", fs)
    (c.drawRightString if p_txt[0] < p_on[0] else c.drawString)((p_txt[0] + (-0.8 if p_txt[0] < p_on[0] else 0.8)) * mm, (p_txt[1] - 1) * mm, text)

def centermark(c, x, y, s=1.2):
    c.setStrokeColorRGB(*BLUE); c.setLineWidth(0.2)
    c.line((x - s) * mm, y * mm, (x + s) * mm, y * mm); c.line(x * mm, (y - s) * mm, x * mm, (y + s) * mm)

def frame(c, sheet, total, title, sub):
    c.setStrokeColorRGB(0, 0, 0); c.setFillColorRGB(0, 0, 0); c.setLineWidth(0.5)
    c.rect(8 * mm, 8 * mm, 194 * mm, 281 * mm); c.rect(10 * mm, 10 * mm, 190 * mm, 34 * mm)
    c.setLineWidth(0.3)
    for xx in (110, 150): c.line(xx * mm, 10 * mm, xx * mm, 44 * mm)
    c.line(10 * mm, 27 * mm, 200 * mm, 27 * mm)
    c.setFont("Helvetica-Bold", 12); c.drawString(13 * mm, 35 * mm, title)
    c.setFont("Helvetica", 8); c.drawString(13 * mm, 30 * mm, sub)
    c.setFont("Helvetica", 7)
    c.drawString(13 * mm, 22 * mm, "Project: Leather no-sew interlocking patterns  |  REV 20261014")
    c.drawString(13 * mm, 17.5 * mm, "Source: 20261014_pattern-leather-cre.pdf (vector, exact geometry)")
    c.drawString(13 * mm, 13 * mm, "Material: leather 1.2-2.0 mm  |  Process: steel-rule / clicker die")
    c.drawString(113 * mm, 37 * mm, "SCALE"); c.setFont("Helvetica-Bold", 11); c.drawString(113 * mm, 31 * mm, "1 : 1")
    c.setFont("Helvetica", 7); c.drawString(113 * mm, 22 * mm, "UNITS: mm")
    c.drawString(113 * mm, 17.5 * mm, "TOL: +/-0.2 mm"); c.drawString(113 * mm, 13 * mm, "PAPER: A4 (print 100%)")
    c.drawString(153 * mm, 37 * mm, f"DATE: {DATE}"); c.drawString(153 * mm, 31 * mm, f"SHEET: {sheet} / {total}")
    c.drawString(153 * mm, 22 * mm, "DRAWN: Claude Code"); c.drawString(153 * mm, 17.5 * mm, "CHECKED: ________")
    c.drawString(153 * mm, 13 * mm, "APPROVED: ________")

def legend(c, x, y):
    c.setLineWidth(0.6); c.setStrokeColorRGB(0, 0, 0); c.line(x * mm, y * mm, (x + 10) * mm, y * mm)
    c.setStrokeColorRGB(*RED); c.line(x * mm, (y - 5) * mm, (x + 10) * mm, (y - 5) * mm)
    c.setStrokeColorRGB(*BLUE); c.setLineWidth(0.25); c.line(x * mm, (y - 10) * mm, (x + 10) * mm, (y - 10) * mm)
    c.setFillColorRGB(0, 0, 0); c.setFont("Helvetica", 7)
    c.drawString((x + 12) * mm, (y - 1) * mm, "CUT  - outline, full-cut rule")
    c.drawString((x + 12) * mm, (y - 6) * mm, "SLIT - through-cut slit / slot")
    c.drawString((x + 12) * mm, (y - 11) * mm, "Dimension - not cut")

def calibration(c, x, y):
    """100 mm ruler + 50 mm square. If these do not measure true, the print was scaled."""
    c.setStrokeColorRGB(0, 0, 0); c.setFillColorRGB(0, 0, 0); c.setLineWidth(0.4)
    c.line(x * mm, y * mm, (x + 100) * mm, y * mm)
    for i in range(0, 101):  # mm ticks
        h = 3 if i % 10 == 0 else (2 if i % 5 == 0 else 1)
        c.setLineWidth(0.3 if i % 10 == 0 else 0.15); c.line((x + i) * mm, y * mm, (x + i) * mm, (y + h) * mm)
    c.setFont("Helvetica", 5.5)
    for i in range(0, 101, 10): c.drawCentredString((x + i) * mm, (y + 4) * mm, str(i))
    c.setLineWidth(0.4); c.rect(140 * mm, 48 * mm, 50 * mm, 50 * mm)
    c.setFont("Helvetica", 6.5); c.drawCentredString(165 * mm, 72 * mm, "50 x 50 mm square")
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(x * mm, (y - 5) * mm, "PRINT AT 100% / ACTUAL SIZE - turn OFF 'Fit to page' / 'Shrink'.")
    c.setFont("Helvetica", 7)
    c.drawString(x * mm, (y - 9) * mm, "Ruler must read 100 mm and the square 50 x 50 mm. If not, the drawing is NOT 1:1.")

def scale_bar(c, x, y):
    c.setStrokeColorRGB(0, 0, 0); c.setLineWidth(0.4); c.line(x * mm, y * mm, (x + 50) * mm, y * mm)
    for i in range(0, 51, 10): c.line((x + i) * mm, y * mm, (x + i) * mm, (y + (3 if i in (0, 50) else 2)) * mm)
    c.setFont("Helvetica", 6.5); c.setFillColorRGB(0, 0, 0)
    c.drawString(x * mm, (y - 3.5) * mm, "Check print: this bar must measure exactly 50 mm")

def circles(p):
    """Group Bezier arcs into true circles. Radius from segment end points (they lie on the drawn circle)."""
    groups = []
    for seg in p["segs"]:
        k = classify(seg)
        if k[0] != "arc":
            continue
        sweep = ((k[4] - k[3]) % 360) if k[5] else ((k[3] - k[4]) % 360)
        if sweep < 3:                       # micro joints - part of a neighbouring circle
            continue
        for g_ in groups:
            if math.dist(g_["c"], k[1]) < 0.6 and abs(g_["r"] - k[2]) < 0.4:
                g_["arcs"].append((seg, k)); break
        else:
            groups.append({"c": k[1], "r": k[2], "arcs": [(seg, k)]})
    for g_ in groups:
        cs = [k[1] for _, k in g_["arcs"]]
        g_["c"] = (sum(q[0] for q in cs) / len(cs), sum(q[1] for q in cs) / len(cs))
        ends = [q for seg, _ in g_["arcs"] for q in (seg[1], seg[-1])]
        g_["r"] = sum(math.dist(g_["c"], q) for q in ends) / len(ends)
        g_["pts"] = [bez_pt(seg, t / 10) for seg, _ in g_["arcs"] for t in range(1, 10)]
    return groups

def ellipses(p):
    out = {}
    for s in p["segs"]:
        k = classify(s)
        if k[0] == "ellipse":
            out.setdefault((round(2 * k[2], 2), round(2 * k[3], 2)), set()).add((round(k[1][0], 2), round(k[1][1], 2)))
    return out

def pattern_page(c, p, sheet, total, notes):
    W, H = p["W"], p["H"]; ox, oy = (210 - W) / 2, 162
    frame(c, sheet, total, f"PATTERN {p['code']} - {p['name'].upper()}", f"Overall {W:.2f} x {H:.2f} mm  |  1 cut outline + {len(p['slits'])} slits  |  REV 20261014")
    c.setStrokeColorRGB(0, 0, 0); c.setLineWidth(0.35); draw_outline(c, p["segs"], ox, oy)
    c.setStrokeColorRGB(*RED); c.setLineWidth(0.35)
    FS = final_slits(p)
    for sl in FS:
        a, b = sl["a"], sl["b"]; c.line((ox + a[0]) * mm, (oy + a[1]) * mm, (ox + b[0]) * mm, (oy + b[1]) * mm)
    # slit tags
    c.setFillColorRGB(*RED); c.setFont("Helvetica-Bold", 6)
    cx, cy = W / 2, H / 2
    for i, sl in enumerate(FS, 1):
        a, b = sl["a"], sl["b"]; m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        v = (m[0] - cx, m[1] - cy); l = math.hypot(*v) or 1
        tx, ty = m[0] - v[0] / l * 4.5, m[1] - v[1] / l * 4.5
        c.drawCentredString((ox + tx) * mm, (oy + ty - 1) * mm, f"S{i}")
    c.setStrokeColorRGB(0.6, 0.6, 0.6); c.setLineWidth(0.15); c.setDash(1, 1)
    c.rect(ox * mm, oy * mm, W * mm, H * mm); c.setDash()
    dim(c, (ox, oy), (ox + W, oy), -10, f"{W:.2f}"); dim(c, (ox, oy), (ox, oy + H), 10, f"{H:.2f}")
    c.setFont("Helvetica", 6.5); c.setFillColorRGB(*BLUE); c.drawString((ox - 4) * mm, (oy - 4) * mm, "0,0"); centermark(c, ox, oy, 2)
    groups = circles(p)
    # one label per radius value; centre marks on every circle
    byr = []
    for g_ in sorted(groups, key=lambda g_: -g_["r"]):
        for e in byr:
            if abs(e["r"] - g_["r"]) < 0.06:
                e["members"].append(g_); break
        else:
            byr.append({"r": g_["r"], "members": [g_]})
    slots = [(ox - 18, oy + H + 3), (ox + W + 7, oy + H + 3), (ox - 18, oy + 6), (ox + W + 7, oy + 3),
             (ox - 18, oy + H * 0.7), (ox + W + 7, oy + H / 2)]
    free = list(slots); geo = []
    for e in byr:
        for g_ in e["members"]:
            centermark(c, ox + g_["c"][0], oy + g_["c"][1])
        if free:
            best = min(((math.dist((ox + q[0], oy + q[1]), sl), q, sl) for g_ in e["members"] for q in g_["pts"] for sl in free))
            _, q, sl = best; free.remove(sl)
            n = len(e["members"])
            leader(c, (ox + q[0], oy + q[1]), sl, f"{n}x R{e['r']:.2f}" if n > 1 else f"R{e['r']:.2f}")
        geo.append(f"R{e['r']:.2f}  centre" + ("s" if len(e["members"]) > 1 else "") + ": " +
                   ", ".join(f"({g_['c'][0]:.2f}, {g_['c'][1]:.2f})" for g_ in e["members"]))
    for (a_, b_), cs in ellipses(p).items():
        geo.append(f"Ellipse {a_:.2f} x {b_:.2f}  centres: " + ", ".join(f"({x:.2f}, {y:.2f})" for x, y in sorted(cs)))
        for x, y in cs: centermark(c, ox + x, oy + y)
    y = oy - 20
    c.setFillColorRGB(0, 0, 0); c.setFont("Helvetica-Bold", 8); c.drawString(14 * mm, y * mm, "GEOMETRY (from designer vector file)")
    c.setFont("Helvetica", 6.8)
    for g_ in geo[:6]:
        y -= 3.6; c.drawString(14 * mm, y * mm, "- " + g_)
    y -= 5.5; c.setFont("Helvetica-Bold", 8); c.drawString(14 * mm, y * mm, "SLIT COORDINATES (origin = bottom-left 0,0)")
    c.setFont("Helvetica", 6.8)
    for i, sl in enumerate(FS, 1):
        a, b = sl["a"], sl["b"]; y -= 3.6
        t = f"   ({sl['note']})" if sl["note"] else ""
        c.drawString(14 * mm, y * mm, f"S{i}:  ({a[0]:.2f}, {a[1]:.2f})  ->  ({b[0]:.2f}, {b[1]:.2f})    L = {math.dist(a, b):.2f}{t}")
    if notes:
        y -= 5.5; c.setFont("Helvetica-Bold", 8); c.setFillColorRGB(0.7, 0.3, 0.05); c.drawString(14 * mm, y * mm, "NOTES")
        c.setFont("Helvetica", 6.8)
        for n_ in notes:
            y -= 3.6; c.drawString(14 * mm, y * mm, "- " + n_)
    legend(c, 140, oy - 20)
    calibration(c, 14, 60)

def overview(c, P, total):
    frame(c, 1, 1, "OVERVIEW - NOT TO SCALE", "Reduced view of all 6 patterns. Use diecut-drawings-1to1-rev20261014.pdf for 1:1.")
    sc = 0.58
    pos = [(16, 200), (80, 205), (142, 205), (18, 118), (80, 118), (142, 118)]
    for p, (x, y) in zip(P, pos):
        c.saveState(); c.translate(x * mm, y * mm); c.scale(sc, sc)
        c.setStrokeColorRGB(0, 0, 0); c.setLineWidth(0.5); draw_outline(c, p["segs"], 0, 0)
        c.setStrokeColorRGB(*RED)
        for sl in final_slits(p):
            a, b = sl["a"], sl["b"]; c.line(a[0] * mm, a[1] * mm, b[0] * mm, b[1] * mm)
        c.restoreState()
        c.setFillColorRGB(0, 0, 0); c.setFont("Helvetica-Bold", 8); c.drawString(x * mm, (y + p["H"] * sc + 4) * mm, f"{p['code']}  {p['name']}")
        c.setFont("Helvetica", 7); c.drawString(x * mm, (y + p["H"] * sc + 0.5) * mm, f"{p['W']:.2f} x {p['H']:.2f} mm  |  {len(p['slits'])} slits")
    y = 106
    c.setFont("Helvetica-Bold", 8); c.drawString(14 * mm, y * mm, "DIE MAKER NOTES")
    c.setFont("Helvetica", 7)
    for n in [
        "1. 1:1 sheets are in the separate 1:1 PDF. Produce from the DXF files (layers CUT / SLIT; true arcs and ellipses).",
        "2. Geometry is taken directly from the designer's vector PDF of 2026-10-14 - no re-tracing.",
        "3. CUT (black) = outline, full cut. SLIT (red) = through cut, same rule height as CUT.",
        "4. Slot lines run past the outline on purpose (as drawn) so the slot is cut right through. Keep the overrun.",
        "5. A 0.01 mm stray point inside pattern 03 was removed - it is not a cut.",
        "6. Receiving slits are 0.5 mm longer than the tab neck they take (+0.25 mm each end) - see each sheet.",
        "7. Suggested rule: 2pt centre-bevel, 23.8 mm height (or die maker standard) for leather 1.2-2.0 mm.",
        "8. Optional: dia. 1.5 mm round punch at the closed end of each slit to stop tearing (confirm with designer).",
    ]:
        y -= 4.5; c.drawString(14 * mm, y * mm, n)
    legend(c, 140, 62)

NOTES = {
    "01": ["Bear rotated 45 deg vs 20261013: ears at top and right; slits vertical (left) and horizontal (bottom)."],
    "02": ["Pinwheel slots 27.0 = half of the 54.1 fold edge. Unchanged from the artwork."],
    "03": ["Receiving slits S1, S2 lengthened 22.50 -> 23.00 so the 22.5 tab neck has 0.5 mm clearance."],
    "04": ["Receiving slits S5, S6 lengthened 30.00 -> 30.50 (tab neck ~29.9)."],
    "05": ["Receiving slits S5, S6 lengthened 30.00 -> 30.50 (tab neck 30.0).",
           "Slot pairs differ as drawn: top 17.7, bottom 16.0 - kept as in the artwork."],
    "06": ["Receiving slits S1, S2 lengthened 17.50 -> 18.00 (tab neck 17.5). Lobes are true ellipses in the DXF."],
}

def main():
    P = load(SRC)
    c = canvas.Canvas(os.path.join(HERE, "diecut-drawings-1to1-rev20261014.pdf"), pagesize=A4)
    c.setTitle("Leather die-cut drawings 1:1 - REV 20261014 - print at 100%")
    for i, p in enumerate(P, 1):
        pattern_page(c, p, i, len(P), NOTES.get(p["code"], [])); c.showPage()
    c.save()
    c = canvas.Canvas(os.path.join(HERE, "overview-not-to-scale-rev20261014.pdf"), pagesize=A4)
    c.setTitle("Overview - not to scale - REV 20261014")
    overview(c, P, 1); c.showPage(); c.save()
    os.makedirs(os.path.join(HERE, "dxf"), exist_ok=True); os.makedirs(os.path.join(HERE, "svg"), exist_ok=True)
    allp = new_doc(); amsp = allp.modelspace()
    for i, p in enumerate(P):
        slug = f"{p['code']}-{p['name'].lower().replace(' ', '-')}"
        doc = new_doc(); dxf_add(doc.modelspace(), p); doc.saveas(os.path.join(HERE, "dxf", slug + ".dxf"))
        write_svg(p, os.path.join(HERE, "svg", slug + ".svg"))
        ox, oy = (i % 3) * 125, -(i // 3) * 125
        dxf_add(amsp, p, ox, oy)
        amsp.add_text(f"{p['code']} {p['name']} {p['W']:.2f}x{p['H']:.2f} REV20261014", height=3.5,
                      dxfattribs={"layer": "NOTE_NOT_CUT"}).set_placement((ox, oy + p["H"] + 5))
    allp.saveas(os.path.join(HERE, "dxf", "all-patterns-rev20261014.dxf"))
    # report
    for p in P:
        kinds = {}
        for s in p["segs"]:
            k = classify(s)[0]; kinds[k] = kinds.get(k, 0) + 1
        print(p["code"], kinds)

if __name__ == "__main__":
    main()
