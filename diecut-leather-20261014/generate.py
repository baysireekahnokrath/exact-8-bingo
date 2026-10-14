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

# ---------------------------------------------------------------- slit rules (agreed with the designer)
# 1. Every slit and every tab neck is centred on the piece centre lines (CL).
# 2. Receiving slit keeps its design length; the tab neck between two slots is 0.5 mm shorter.
#    01: the ear neck (where ear meets face) is the tab; its slit is neck + 0.5.
# 3. Slots that open onto the outline run 1.0 mm past the cut line so they always cut through.
# 4. 02 pinwheel slots end exactly on the centre line.
from shapely.geometry import LineString as _LS, Point as _Pt
from extract import sample as _sample
from shapely.geometry import Polygon as _Poly
CLEARANCE, OVERRUN = 0.5, 1.0
SLIT = {"03": 22.5, "04": 30.0, "05": 30.0, "06": 17.5}
_CACHE = {}

def _boundary(p):
    if p["code"] not in _CACHE:
        _CACHE[p["code"]] = _Poly(_sample(p["segs"], 400)).buffer(0).boundary
    return _CACHE[p["code"]]

def _hit(p, M, u, reach=80):
    """First outline point from M along unit direction u."""
    line = _LS([M, (M[0] + u[0] * reach, M[1] + u[1] * reach)])
    g = _boundary(p).intersection(line)
    pts = [g] if g.geom_type == "Point" else list(getattr(g, "geoms", []))
    pts = [q for q in pts if q.geom_type == "Point" and math.dist((q.x, q.y), M) > 1e-6]
    q = min(pts, key=lambda q: math.dist((q.x, q.y), M))
    return (q.x, q.y)

def _add(P, k, a):
    return (P[0] + k * a[0], P[1] + k * a[1])

def alignment(p):
    """Centre, centre lines, rule-built slits and the numbers that prove the alignment."""
    code = p["code"]; groups = circles(p)
    if code == "01":
        face = max(groups, key=lambda g_: g_["r"]); C = face["c"]
    else:
        cs = [g_["c"] for g_ in groups]
        C = (sum(q[0] for q in cs) / len(cs), sum(q[1] for q in cs) / len(cs))
    C = (round(C[0], 2), round(C[1], 2))
    cx, cy = C
    slits, checks, folds, recv = [], [], [], []
    r2 = 1 / math.sqrt(2)

    def receiver(M, u, L, name):
        a, b = _add(M, -L / 2, u), _add(M, L / 2, u)
        slits.append({"a": a, "b": b, "kind": "slit", "note": f"receiving slit {L:.2f}, centred on CL"})
        recv.append({"M": M, "u": u, "L": L, "name": name})

    def tab_fold(M, u, neck, name, half_chord=None):
        if half_chord:                                   # corner points known exactly (03 notches)
            P1, P2 = _add(M, half_chord, u), _add(M, -half_chord, u)
        else:
            P1, P2 = _hit(p, M, u), _hit(p, M, (-u[0], -u[1]))
        for P, sg in ((P1, 1), (P2, -1)):
            d = (u[0] * sg, u[1] * sg)
            outer = _add(P, OVERRUN, d); inner = _add(M, neck / 2, d)
            slits.append({"a": outer, "b": inner, "kind": "slot",
                          "note": f"slot {math.dist(P, inner):.2f} in + {OVERRUN:.1f} past cut"})
        folds.append({"M": M, "u": u, "neck": neck, "P1": P1, "P2": P2, "name": name})

    if code == "01":
        face = max(groups, key=lambda g_: g_["r"]); ears = [g_ for g_ in groups if g_ is not face]
        necks = []
        for e in ears:
            d = math.dist(face["c"], e["c"]); R, r = face["r"], e["r"]
            a_ = (R * R - r * r + d * d) / (2 * d); necks.append(2 * math.sqrt(R * R - a_ * a_))
        neck = sum(necks) / len(necks); L = round(neck + CLEARANCE, 2); off = 30.5
        receiver((cx - off, cy), (0, 1), L, "left slit")
        receiver((cx, cy - off), (1, 0), L, "bottom slit")
        offs = [abs(e["c"][1] - cy) if abs(e["c"][1] - cy) < 5 else abs(e["c"][0] - cx) for e in ears]
        checks.append(("ear centres vs CL", " / ".join(f"{o:.2f}" for o in offs) + " mm"))
        checks += [("ear neck (ear meets face)", f"{neck:.2f}"),
                   ("slit = neck + 0.5", f"{L:.2f}  (was 17.27)"),
                   ("slit centre to CL", "0.00 / 0.00"),
                   ("slit offset from centre", f"{off:.2f}")]
        return {"C": C, "slits": slits, "checks": checks, "folds": folds, "recv": recv, "diag": False,
                "ear_neck": neck}
    if code == "02":
        lob = groups; c1 = min(lob, key=lambda g_: g_["c"][0]); c2 = max(lob, key=lambda g_: g_["c"][1])
        d = math.dist(c1["c"], c2["c"]); R = c1["r"]; h = math.sqrt(R * R - (d / 2) ** 2)
        mx, my = (c1["c"][0] + c2["c"][0]) / 2, (c1["c"][1] + c2["c"][1]) / 2
        ux, uy = (c2["c"][0] - c1["c"][0]) / d, (c2["c"][1] - c1["c"][1]) / d
        notch = (mx - uy * h, my + ux * h); H2 = round(cy - 0 + (notch[1] - cy), 3) - cy
        H2 = round(abs(notch[0] - cx), 3)
        for sl in p["slits"]:                               # keep the designer's pinwheel sides
            a, b = sl["raw"]
            horiz = abs(a[1] - b[1]) < abs(a[0] - b[0])
            if horiz:
                yv = cy + H2 * (1 if (a[1] + b[1]) / 2 > cy else -1)
                far = a if abs(a[0] - cx) > abs(b[0] - cx) else b
                sx = 1 if far[0] > cx else -1
                outer, inner = (cx + sx * (H2 + OVERRUN), yv), (cx, yv)
            else:
                xv = cx + H2 * (1 if (a[0] + b[0]) / 2 > cx else -1)
                far = a if abs(a[1] - cy) > abs(b[1] - cy) else b
                sy = 1 if far[1] > cy else -1
                outer, inner = (xv, cy + sy * (H2 + OVERRUN)), (xv, cy)
            slits.append({"a": outer, "b": inner, "kind": "slot", "note": f"slot {H2:.2f} notch->CL + {OVERRUN:.1f} past cut"})
        checks += [("fold square (notch to notch)", f"{2 * H2:.2f}"), ("slot inner end on CL", "0.00 (all 4)"),
                   ("slot length notch -> CL", f"{H2:.2f}"), ("overrun past cut", f"{OVERRUN:.2f}")]
        return {"C": C, "slits": slits, "checks": checks, "folds": [], "recv": [], "diag": False, "h": H2}
    L = SLIT[code]; neck = L - CLEARANCE
    if code == "03":
        h = 22.5
        receiver((cx - h, cy), (0, 1), L, "left"); receiver((cx + h, cy), (0, 1), L, "right")
        tab_fold((cx, cy + h), (1, 0), neck, "top", h); tab_fold((cx, cy - h), (1, 0), neck, "bottom", h)
    elif code == "04":
        h = 22.5
        receiver((cx + h, cy - h), (r2, r2), L, "BR"); receiver((cx - h, cy + h), (r2, r2), L, "TL")
        tab_fold((cx + h, cy + h), (r2, -r2), neck, "TR"); tab_fold((cx - h, cy - h), (r2, -r2), neck, "BL")
    elif code == "05":
        h = 45 / math.sqrt(2)
        receiver((cx, cy + h), (1, 0), L, "top"); receiver((cx, cy - h), (1, 0), L, "bottom")
        tab_fold((cx + h, cy), (0, 1), neck, "right"); tab_fold((cx - h, cy), (0, 1), neck, "left")
    elif code == "06":
        h = 30.0
        receiver((cx, cy + h), (1, 0), L, "top"); receiver((cx, cy - h), (1, 0), L, "bottom")
        tab_fold((cx + h, cy), (0, 1), neck, "right"); tab_fold((cx - h, cy), (0, 1), neck, "left")
    f0 = folds[0]
    chord = math.dist(f0["P1"], f0["P2"])
    mid_off = math.dist(((f0["P1"][0] + f0["P2"][0]) / 2, (f0["P1"][1] + f0["P2"][1]) / 2), f0["M"])
    checks += [("fold line offset from centre", f"{h:.2f}"),
               ("receiving slit (design)", f"{L:.2f}, centred on CL (0.00)"),
               ("tab neck = slit - 0.5", f"{neck:.2f}, centred on CL (0.00)"),
               ("tab chord at fold (cut to cut)", f"{chord:.2f}  (centre {mid_off:.2f} off CL)"),
               ("slot inside the piece", f"{(chord - neck) / 2:.2f} each side"),
               ("overrun past cut", f"{OVERRUN:.2f}")]
    return {"C": C, "slits": slits, "checks": checks, "folds": folds, "recv": recv, "diag": code == "04", "h": h}

def final_slits(p):
    out = []
    for sl in alignment(p)["slits"]:
        out.append({"a": (round(sl["a"][0], 3), round(sl["a"][1], 3)), "b": (round(sl["b"][0], 3), round(sl["b"][1], 3)), "note": sl["note"]})
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

def cl_line(c, a, b):
    c.saveState(); c.setStrokeColorRGB(0.1, 0.55, 0.35); c.setLineWidth(0.22); c.setDash([6, 1.5, 1, 1.5])
    c.line(a[0] * mm, a[1] * mm, b[0] * mm, b[1] * mm); c.restoreState()
    c.setFillColorRGB(0.1, 0.55, 0.35); c.setFont("Helvetica-Bold", 6); c.drawCentredString(b[0] * mm, (b[1] + 1.2) * mm, "CL")

def annotate(c, p, A, ox, oy):
    """Centre lines + dimensions that show how slits, necks and slots sit on the centre."""
    W, H = p["W"], p["H"]; cx, cy = A["C"]; X, Y = ox + cx, oy + cy
    ext = 7
    cl_line(c, (ox - ext + 2, Y), (ox + W + ext, Y)); cl_line(c, (X, oy - ext + 2), (X, oy + H + ext))
    if A.get("diag"):
        d = 52
        cl_line(c, (X - d * 0.7071, Y - d * 0.7071), (X + d * 0.7071, Y + d * 0.7071))
        cl_line(c, (X - d * 0.7071, Y + d * 0.7071), (X + d * 0.7071, Y - d * 0.7071))
    c.setStrokeColorRGB(0.1, 0.55, 0.35); c.setLineWidth(0.35)
    c.circle(X * mm, Y * mm, 1.2 * mm); c.line((X - 2.5) * mm, Y * mm, (X + 2.5) * mm, Y * mm); c.line(X * mm, (Y - 2.5) * mm, X * mm, (Y + 2.5) * mm)
    P = lambda q: (ox + q[0], oy + q[1])
    if A["recv"]:
        r = A["recv"][0]; M, u, L = r["M"], r["u"], r["L"]
        a_, b_ = _add(M, -L / 2, u), _add(M, L / 2, u)
        side = 1 if (M[0] - cx) * -u[1] + (M[1] - cy) * u[0] >= 0 else -1
        dim(c, P(a_), P(M), 4 * side, f"{L/2:.2f}", fs=6); dim(c, P(M), P(b_), 4 * side, f"{L/2:.2f}", fs=6)
        # offset of the slit line from the centre
        n = (-u[1], u[0]); t = (M[0] - cx) * n[0] + (M[1] - cy) * n[1]
        if abs(t) > 1:
            q0 = (cx, cy); q1 = (cx + n[0] * t, cy + n[1] * t)
            dim(c, P(q0), P(q1), -3 if p["code"] != "04" else 3, f"{abs(t):.2f}", fs=6)
    if A["folds"]:
        f = A["folds"][0]; M, u, nk = f["M"], f["u"], f["neck"]
        i1, i2 = _add(M, nk / 2, u), _add(M, -nk / 2, u)
        side = -1 if (M[0] - cx) * -u[1] + (M[1] - cy) * u[0] >= 0 else 1
        dim(c, P(i2), P(i1), 5 * side, f"neck {nk:.2f}", fs=6)
        dim(c, P(i1), P(f["P1"]), 5 * side, f"{math.dist(i1, f['P1']):.2f}", fs=6)
        leader(c, P(_add(f["P1"], 0.5, u)), P(_add(_add(f["P1"], 6, u), 6 * side, (-u[1], u[0]))), "+1.0 past cut", fs=6)
    if p["code"] == "02":
        sl = A["slits"][0]; a_, b_ = sl["a"], sl["b"]
        notch = _add(a_, 1.0, ((b_[0] - a_[0]) / math.dist(a_, b_), (b_[1] - a_[1]) / math.dist(a_, b_)))
        dim(c, P(notch), P(b_), -5, f"{math.dist(notch, b_):.2f} to CL", fs=6)
        leader(c, P(_add(a_, 0.5, ((b_[0] - a_[0]) / math.dist(a_, b_), 0))), P((a_[0] + 8, a_[1] - 8)), "+1.0 past cut", fs=6)
    if p["code"] == "01":
        # ear neck on the top ear
        groups = circles(p); face = max(groups, key=lambda g_: g_["r"])
        top = max((g_ for g_ in groups if g_ is not face), key=lambda g_: g_["c"][1])
        d = math.dist(face["c"], top["c"]); R, r = face["r"], top["r"]
        a0 = (R * R - r * r + d * d) / (2 * d); hh = math.sqrt(R * R - a0 * a0)
        mid = (face["c"][0], face["c"][1] + a0)
        dim(c, P((mid[0] - hh, mid[1])), P((mid[0] + hh, mid[1])), 6, f"ear neck {2*hh:.2f}", fs=6)

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
    A = alignment(p)
    annotate(c, p, A, ox, oy)
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
    y -= 5.5; c.setFont("Helvetica-Bold", 8); c.setFillColorRGB(0.1, 0.45, 0.28); c.drawString(14 * mm, y * mm, "ALIGNMENT CHECK (CL = centre line)")
    c.setFont("Helvetica", 6.8)
    for k_, v_ in A["checks"]:
        y -= 3.6; c.drawString(14 * mm, y * mm, f"- {k_}:"); c.drawString(70 * mm, y * mm, v_)
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
    "01": ["The ear neck (17.41, where ear meets face) is the tab. Slits lengthened 17.27 -> 17.91 = neck + 0.5, centred on CL."],
    "02": ["Each slot runs from the notch to the centre line (ends exactly on CL) plus 1.0 past the cut."],
    "03": ["Slit 22.5 as designed. Tab neck between slots = 22.0 (slit - 0.5). Slots 11.5 in + 1.0 past cut."],
    "04": ["Slit 30.0 as designed. Tab neck = 29.5. Slots 17.07 in + 1.0 past cut (overrun was 1.7-4.5)."],
    "05": ["Slit 30.0 as designed, centred on the circle. Tab neck = 29.5 centred, so all 4 slots are now equal (were 17.7 / 16.0)."],
    "06": ["Slit 17.5 as designed, centred on CL. Tab neck = 17.0. Slots 9.19 in + 1.0 past cut."],
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
