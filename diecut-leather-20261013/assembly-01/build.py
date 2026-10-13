"""Build the pattern-01 bear charm assembly page + heart-strap (01-S) cut files."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import generate as g

BEAR = g.P[0]
W_STRAP = 13.0                 # fits the 17 mm slits at the ~31 deg approach angle (needs 15.2)
LOBE_R, LOBE_X = 5.5, 12.0     # heart: lobes R5.5 at (12, +/-5.5) from the tip -> width 22, length 17.5
HEART_LEN = LOBE_X + LOBE_R
LENGTHS = {"keyring": 200, "handle": 250}

# ---------------------------------------------------------------- heart strap geometry (CAD, y up)
# Each strap end is a heart whose point faces into the strap. The point hides in the slit;
# the lobes (22 wide) sit on the front of the bear and stop the strap pulling back through.
def heart_geom():
    d = math.hypot(LOBE_X, LOBE_R)
    phi = math.atan2(-LOBE_R, LOBE_X) - math.asin(LOBE_R / d)
    tl = math.sqrt(d * d - LOBE_R ** 2)
    T = (tl * math.cos(phi), tl * math.sin(phi))           # lower tangent point (tip at 0,0)
    xn = (W_STRAP / 2) / math.tan(-phi)                      # where the heart is as wide as the strap
    return T, xn

def ang(c, p):
    return math.degrees(math.atan2(p[1] - c[1], p[0] - c[0])) % 360

def heart_local_pts(n=24):
    """Visible heart (from the neck to the lobes), local coords: tip at 0, lobes toward +x."""
    T, xn = heart_geom()
    cl, cu = (LOBE_X, -LOBE_R), (LOBE_X, LOBE_R)
    pts = [(xn, -W_STRAP / 2), T]
    a0, a1 = math.radians(ang(cl, T)), math.radians(90)
    a1 += 2 * math.pi if a1 < a0 else 0
    pts += [(cl[0] + LOBE_R * math.cos(a0 + (a1 - a0) * i / n), cl[1] + LOBE_R * math.sin(a0 + (a1 - a0) * i / n)) for i in range(1, n + 1)]
    b0, b1 = math.radians(270), math.radians(ang(cu, (T[0], -T[1])))
    b1 += 2 * math.pi if b1 < b0 else 0
    pts += [(cu[0] + LOBE_R * math.cos(b0 + (b1 - b0) * i / n), cu[1] + LOBE_R * math.sin(b0 + (b1 - b0) * i / n)) for i in range(1, n + 1)]
    pts += [(xn, W_STRAP / 2)]
    return pts

def strap_segments(L):
    T, xn = heart_geom()
    h = W_STRAP / 2
    o = L - HEART_LEN                                     # right heart tip x
    R = lambda p: (o + p[0], p[1])                        # right heart: local -> strap
    M = lambda p: (HEART_LEN - p[0], p[1])                # left heart: mirrored
    clR, cuR = R((LOBE_X, -LOBE_R)), R((LOBE_X, LOBE_R))
    clL, cuL = M((LOBE_X, -LOBE_R)), M((LOBE_X, LOBE_R))
    Tl, Tu = T, (T[0], -T[1])
    return [
        g.L(M((xn, -h)), R((xn, -h))),
        g.L(R((xn, -h)), R(Tl)),
        ("arc", clR, LOBE_R, ang(clR, R(Tl)), 90.0, True),
        ("arc", cuR, LOBE_R, 270.0, ang(cuR, R(Tu)), True),
        g.L(R(Tu), R((xn, h))),
        g.L(R((xn, h)), M((xn, h))),
        g.L(M((xn, h)), M(Tu)),
        ("arc", cuL, LOBE_R, ang(cuL, M(Tu)), 270.0, True),
        ("arc", clL, LOBE_R, 90.0, ang(clL, M(Tl)), True),
        g.L(M(Tl), M((xn, -h))),
    ]

def strap_files():
    for name, L in LENGTHS.items():
        segs = strap_segments(L)
        p = dict(code="01S", name=f"Heart strap {L}", W=L, H=24, cut=[(s[0],) + tuple(
            ((v[0], v[1] + 12) if isinstance(v, tuple) else v) for v in s[1:]) for s in segs], slits=[])
        # shift arcs' centers too (handled above: tuples are points/centers)
        doc = g.new_doc(); g.dxf_add(doc.modelspace(), p)
        doc.saveas(os.path.join(HERE, f"01S-heart-strap-{L}.dxf"))
        g.write_svg(p, os.path.join(HERE, f"01S-heart-strap-{L}.svg"))

# ---------------------------------------------------------------- SVG helpers (screen, y down)
def path_from(segs, ox, oy, flip_h):
    """CAD segments -> svg path in screen coords; flip_h = height used to flip y."""
    return g.svg_path([(s[0],) + tuple(((v[0] + ox, v[1] + oy) if isinstance(v, tuple) else v) for v in s[1:]) for s in segs], flip_h)

def bear(ox, oy, fill="var(--l-light)", mirror=False, slits=True):
    """Bear outline at screen offset (ox, oy). mirror=True draws the back view."""
    tr = f'translate({ox},{oy})' + (' translate(95,0) scale(-1,1)' if mirror else '')
    out = f'<g transform="{tr}"><path d="{g.svg_path(BEAR["cut"], 90)}" fill="{fill}" class="pc"/>'
    if slits:
        out += "".join(f'<line x1="{s[1][0]:.2f}" y1="{90-s[1][1]:.2f}" x2="{s[2][0]:.2f}" y2="{90-s[2][1]:.2f}" class="sl"/>' for s in BEAR["slits"])
    return out + "</g>"

def label(x, y, text, cls="lb", anchor="start"):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{text}</text>'

def callout(x1, y1, x2, y2, text, anchor="start"):
    dx = 1.2 if anchor == "start" else -1.2
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="co"/>'
            f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="0.9" class="cod"/>' + label(x2 + dx, y2 + 1.4, text, "lb", anchor))

SL = [((s[1][0] + s[2][0]) / 2, 90 - (s[1][1] + s[2][1]) / 2) for s in BEAR["slits"]]   # slit centres, screen
CENTER = (47.5, 90 - 41.5)

def unit(a, b):
    d = math.hypot(b[0] - a[0], b[1] - a[1]); return ((b[0] - a[0]) / d, (b[1] - a[1]) / d)

# ---- step 1: parts
def step1():
    L = LENGTHS["keyring"]
    sc = 0.95
    strap = f'<g transform="translate(8,118) scale({sc})"><path d="{path_from(strap_segments(L), 0, 12, 24)}" fill="var(--l-red)" class="pc"/></g>'
    dims = (f'<line x1="8" y1="{118+26*sc:.1f}" x2="{8+L*sc:.1f}" y2="{118+26*sc:.1f}" class="dm"/>'
            + label(8 + L * sc / 2, 118 + 31 * sc, f"{L} mm (ห่วงพวงกุญแจ) · {LENGTHS['handle']} mm (คล้องหูกระเป๋า)", "lbd", "middle"))
    ann = (bear(56, 6) + label(150, 30, "01 Bear head", "lbb") + label(150, 37, "95 × 90 mm · × 1 ชิ้น", "lb")
           + label(150, 46, "slit 17 mm × 2", "lb")
           + callout(8 + 8 * sc, 118 + 4 * sc, 8, 108, "หัวใจ กว้าง 22 ยาว 17.5", "start")
           + callout(8 + 100 * sc, 118 + 12 * sc - 6.5 * sc, 120, 108, "สาย 01-S กว้าง 13 mm · × 1 เส้น"))
    return f'<svg viewBox="0 0 210 152" role="img" aria-label="ชิ้นส่วน: หมี 01 และสายหัวใจ 01-S">{ann}{strap}{dims}</svg>'

# ---- step 2: how a heart goes through a slit (3 panels)
def end_pts(fold=False):
    """Strap end with heart, local (x along strap, tip of heart at 0); strap runs to x = -16."""
    hp = heart_local_pts()
    pts = [(-16, -W_STRAP / 2)] + hp + [(-16, W_STRAP / 2)]
    if fold:
        pts = [(x, y) for x, y in pts if y <= 0.001] + [(-16, 0)]   # folded on the axis: one lobe shows
    return pts

def draw_end(ox, oy, fold=False, rot=90):
    """Draw strap end; heart lobes point down the page (rot=90)."""
    c, s_ = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    w = [(ox + x * c - y * s_, oy + x * s_ + y * c) for x, y in end_pts(fold)]
    return '<path d="M' + " L".join(f"{a:.2f},{b:.2f}" for a, b in w) + ' Z" fill="var(--l-red)" class="pc"/>'

def step2():
    pa = draw_end(30, 22, fold=True) + label(30, 64, "1 พับหัวใจครึ่งตามยาว", "lb", "middle")
    T, xn = heart_geom()
    pb = (f'<rect x="72" y="{22 + xn - 2:.1f}" width="56" height="4" fill="var(--l-light)" class="pc"/>'
          + f'<line x1="91.5" y1="{22 + xn:.1f}" x2="108.5" y2="{22 + xn:.1f}" class="sl"/>'
          + draw_end(100, 22, fold=True)
          + label(131, 22 + xn - 3, "ด้านหลัง", "lbs") + label(131, 22 + xn + 6, "ด้านหน้า", "lbs")
          + label(100, 64, "2 ดันหัวใจผ่าน slit จากด้านหลัง", "lb", "middle"))
    pc = (draw_end(170, 22) + f'<line x1="161.5" y1="{22 + xn:.1f}" x2="178.5" y2="{22 + xn:.1f}" class="sl"/>'
          + f'<line x1="159" y1="{22 + HEART_LEN + 4:.1f}" x2="181" y2="{22 + HEART_LEN + 4:.1f}" class="dm"/>'
          + label(170, 22 + HEART_LEN + 9, "กว้าง 22 &gt; slit 17", "lbd", "middle")
          + label(170, 64, "3 กางหัวใจ ล็อกกับขอบ slit", "lb", "middle"))
    return f'<svg viewBox="0 0 210 70" role="img" aria-label="วิธีสอดหัวใจผ่าน slit">{pa}{pb}{pc}</svg>'

# ---- step 3: thread the key ring onto the strap middle
def step3():
    L = LENGTHS["keyring"]; sc = 0.95
    strap = f'<g transform="translate(8,30) scale({sc})"><path d="{path_from(strap_segments(L), 0, 12, 24)}" fill="var(--l-red)" class="pc"/></g>'
    mid = 8 + L * sc / 2
    ring = (f'<ellipse cx="{mid:.1f}" cy="41.4" rx="4" ry="13" class="ring"/>'
            + f'<line x1="{mid:.1f}" y1="24" x2="{mid:.1f}" y2="59" class="dm"/>')
    ann = (label(mid, 70, "ร้อยห่วงพวงกุญแจเข้ากลางสาย", "lb", "middle")
           + label(8, 18, "ด้านผิวของสายหันลง (จะแนบกับหลังหมี)", "lbs"))
    return f'<svg viewBox="0 0 210 76" role="img" aria-label="ร้อยห่วงเข้ากลางสาย">{strap}{ring}{ann}</svg>'

# ---- step 4: back view, first heart in
def legline(sx, sy, ex, ey, cls="leg"):
    return f'<line x1="{sx:.2f}" y1="{sy:.2f}" x2="{ex:.2f}" y2="{ey:.2f}" class="{cls}"/>'

def step4():
    ox, oy = 40, 26
    # back view = mirror: left slit appears on the right
    sR = (ox + 95 - SL[0][0], oy + SL[0][1])          # bear's left slit, seen from behind
    apex = (ox + 47.5, oy - 8)
    art = bear(ox, oy, mirror=True)
    art += legline(*sR, apex[0] + 1.9, apex[1]) + f'<circle cx="{sR[0]:.2f}" cy="{sR[1]:.2f}" r="1.2" class="cod"/>'
    art += legline(apex[0] - 1.9, apex[1], apex[0] - 30, apex[1] + 6, "legf")
    art += f'<ellipse cx="{apex[0]:.1f}" cy="{apex[1]-11:.1f}" rx="3.5" ry="11" class="ring"/>'
    ann = (label(ox + 47.5, oy + 105, "มองจากด้านหลัง", "lbs", "middle")
           + callout(sR[0] + 2, sR[1] + 2, 172, 112, "สอดหัวใจข้างแรกผ่าน slit")
           + callout(apex[0] - 20, apex[1] + 4.5, 4, 14, "ปลายอีกข้างยังว่างอยู่"))
    return f'<svg viewBox="0 0 210 122" role="img" aria-label="สอดหัวใจข้างแรก มองจากด้านหลัง">{art}{ann}</svg>'

def model_data():
    pts = []
    for s in BEAR["cut"]:
        sw = g.sweep(s); n = max(8, int(abs(sw) / 4))
        for i in range(n):
            a = math.radians(s[3] + sw * i / n)
            pts.append([round(s[1][0] + s[2] * math.cos(a), 3), round(s[1][1] + s[2] * math.sin(a), 3)])
    T, xn = heart_geom()
    return json.dumps({"outline": pts, "slits": [[list(s[1]), list(s[2])] for s in BEAR["slits"]],
                       "center": [47.5, 41.5], "heart": {"pts": [[round(x, 3), round(y, 3)] for x, y in heart_local_pts()],
                       "neck": xn, "w": W_STRAP}})

def main():
    tpl = open(os.path.join(HERE, "template.html")).read()
    js = open(os.path.join(HERE, "model01.js")).read().replace("__DATA__", model_data())
    html = (tpl.replace("__STEP1__", step1()).replace("__STEP2__", step2()).replace("__STEP3__", step3())
               .replace("__STEP4__", step4()).replace("__MODEL_JS__", js))
    open(os.path.join(HERE, "index.html"), "w").write(html)
    strap_files()
    print("ok", len(html))

if __name__ == "__main__":
    main()
