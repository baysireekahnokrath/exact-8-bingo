"""Read the designer's vector PDF and return exact pattern geometry (mm, CAD axes: origin bottom-left, y up).

Black 0.75 pt strokes = CUT outline, red 0.5 pt strokes = SLIT. Dimension lines (1 pt) and text are ignored.
Segments: ("line", p0, p1) or ("bez", p0, c1, c2, p3).
"""
import math
import pymupdf
from shapely.geometry import LineString, Polygon

PT = 25.4 / 72
BLACK, RED = (0.01, 0.02, 0.02), (0.93, 0.12, 0.14)

# drawing index in the PDF -> pattern code (matches the 20261013 numbering)
ORDER = [("01", 37, "Bear head"), ("02", 0, "Pinwheel 4-lobe"), ("03", 143, "Capsule cross"),
         ("04", 40, "Rounded square diagonal"), ("05", 5, "Circle"), ("06", 171, "Soft cross")]

def _col(x, key):
    return tuple(round(v, 2) for v in (x.get(key) or ()))

def bez_pt(s, t):
    p0, c1, c2, p3 = s[1:]
    u = 1 - t
    return (u**3 * p0[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t**3 * p3[1])

def sample(segs, n=48):
    pts = []
    for s in segs:
        if s[0] == "line":
            pts.append(s[1])
        else:
            pts += [bez_pt(s, i / n) for i in range(n)]
    return pts

def subpaths(items):
    """Split drawing items into continuous runs."""
    runs, cur = [], []
    for it in items:
        if cur and math.dist(cur[-1][-1], it[0]) > 1e-3:
            runs.append(cur); cur = []
        cur.append(it)
    if cur:
        runs.append(cur)
    return runs

def load(path):
    doc = pymupdf.open(path); page = doc[0]
    dr = page.get_drawings()
    slits_all = [x for x in dr if _col(x, "color") == RED and abs((x.get("width") or 0) - 0.5) < 0.05]
    out = []
    for code, idx, name in ORDER:
        x = dr[idx]
        assert _col(x, "color") == BLACK and abs(x["width"] - 0.75) < 0.05, code
        items = []
        for it in x["items"]:
            pts = [(q.x * PT, q.y * PT) for q in it[1:] if hasattr(q, "x")]
            items.append(pts)
        runs = subpaths(items)
        # drop stray specks (e.g. a 0.01 mm dot left in the artwork)
        def span(run):
            xs = [p[0] for seg in run for p in seg]; ys = [p[1] for seg in run for p in seg]
            return max(max(xs) - min(xs), max(ys) - min(ys))
        dropped = [r for r in runs if span(r) < 0.5]
        main = max(runs, key=span)
        xs = [p[0] for seg in main for p in seg]; ys = [p[1] for seg in main for p in seg]
        # true bbox from the sampled curve (control points can overshoot)
        tmp = [("line", s[0], s[1]) if len(s) == 2 else ("bez", *s) for s in main]
        sp = sample(tmp)
        x0, x1 = min(p[0] for p in sp), max(p[0] for p in sp)
        y0, y1 = min(p[1] for p in sp), max(p[1] for p in sp)
        f = lambda p: (round(p[0] - x0, 4), round(y1 - p[1], 4))
        segs = []
        for s in main:
            if len(s) == 2:
                if math.dist(*s) > 1e-6:
                    segs.append(("line", f(s[0]), f(s[1])))
            else:
                if max(math.dist(s[0], q) for q in s[1:]) > 1e-6:
                    segs.append(("bez", *[f(q) for q in s]))
        poly = Polygon(sample(segs)).buffer(0)
        slits = []
        for sx in slits_all:
            r = sx["rect"]
            if r.x0 * PT > x0 - 8 and r.x1 * PT < x1 + 8 and r.y0 * PT > y0 - 8 and r.y1 * PT < y1 + 8:
                a, b = [(q.x * PT, q.y * PT) for q in sx["items"][0][1:3]]
                raw = (f(a), f(b))
                clip = LineString(raw).intersection(poly.buffer(1e-4))
                if clip.is_empty:
                    continue
                cs = list(clip.coords) if clip.geom_type == "LineString" else list(max(clip.geoms, key=lambda g: g.length).coords)
                c0, c1 = (round(cs[0][0], 3), round(cs[0][1], 3)), (round(cs[-1][0], 3), round(cs[-1][1], 3))
                # keep the drawn direction
                if math.dist(c0, raw[0]) > math.dist(c1, raw[0]):
                    c0, c1 = c1, c0
                slits.append(dict(raw=raw, cut=(c0, c1), trimmed=round(math.dist(*raw) - math.dist(c0, c1), 2)))
        out.append(dict(code=code, name=name, W=round(x1 - x0, 2), H=round(y1 - y0, 2), segs=segs, slits=slits,
                        dropped=len(dropped), poly=poly))
    return out

if __name__ == "__main__":
    import sys
    for p in load(sys.argv[1]):
        print(p["code"], p["name"], p["W"], "x", p["H"], "segs", len(p["segs"]), "dropped", p["dropped"])
        for s in p["slits"]:
            (a, b) = s["cut"]
            print("   slit", a, "->", b, "L=%.2f" % math.dist(a, b), "trimmed %.2f" % s["trimmed"])
