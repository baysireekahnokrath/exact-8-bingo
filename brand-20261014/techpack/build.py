"""Tech pack for the 30 booth products: what to cut, how to put it together, how to check it.

Every drawing uses the real die outlines (diecut-leather-20261014/svg, heart straps from 20261013/assembly-01).
Joint rule (pieces 03 04 05 06): each piece has two A sides (wing with a slot at both ends of its fold line, opposite
each other) and two B sides (a slit in the middle of the fold line). A joint is always the A wing of one piece pushed
through the B slit of the other; the A wing's corners spread and lock, the B wing lies over the outside.
Nets are worked out in 3D, so each joint number shows up exactly twice: once on an A wing, once on a B slit.

python3 techpack/build.py -> site/techpack.html, techpack/print.html (A4, one product per page)
"""
import html, importlib.util, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); REPO = os.path.dirname(ROOT)
sys.path.insert(0, ROOT)
import brand as B
import bible as BB

spec = importlib.util.spec_from_file_location("site_build", os.path.join(ROOT, "site", "build.py"))
S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
E = lambda t: html.escape(str(t))

DIE_DIR = os.path.join(REPO, "diecut-leather-20261014", "svg")
STRAP_DIR = os.path.join(REPO, "diecut-leather-20261013", "assembly-01")
FILES = {"01": "01-bear-head", "02": "02-pinwheel-4-lobe", "03": "03-capsule-cross", "04": "04-rounded-square-diagonal",
         "05": "05-circle", "06": "06-soft-cross"}
INK, TOM, COB, PAPER = B.C["ink"], B.C["tomato"], B.C["cobalt"], B.C["paper"]
TONES = ["#B8743A", "#8F5527", "#D49A5E", "#6E4222", "#C48448", "#A6693A"]   # leather scraps, material colour only

# ---------------------------------------------------------------- die data
DIE = {   # code: name, fold square side, B slit, A neck, base rotation that puts B on top/bottom, half reach after it
    "01": ("หัวหมี", None, 17.91, 17.41, 0, None),
    "02": ("กังหัน", 54.0, None, None, 0, 45.0),
    "03": ("กากบาทแคปซูล", 45.0, 22.5, 22.0, 90, 45.0),
    "04": ("สี่เหลี่ยมมน", 63.64, 30.0, 29.5, 45, 63.64),
    "05": ("วงกลม", 63.64, 30.0, 29.5, 0, 45.0),
    "06": ("กากบาทนุ่ม", 60.0, 17.5, 17.0, 0, 45.0),
}
SIZE = {"01": "104.4 × 104.4", "02": "90 × 90", "03": "90 × 90", "04": "90 × 90", "05": "Ø 90", "06": "90 × 90",
        "01-S200": "200 × 24", "01-S250": "250 × 24"}

def load(code):
    """(width, height, cut path d, slit lines) of a die, in mm."""
    if code.startswith("01-S"):
        f = os.path.join(STRAP_DIR, f"01S-heart-strap-{code[-3:]}.svg")
    else:
        f = os.path.join(DIE_DIR, FILES[code] + ".svg")
    s = open(f).read()
    w, h = (float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s).groups())
    d = " ".join(re.findall(r'<path d="([^"]+)"', s))
    lines = [tuple(float(v) for v in m) for m in re.findall(r'<line x1="([-\d.]+)" y1="([-\d.]+)" x2="([-\d.]+)" y2="([-\d.]+)"', s)]
    return w, h, d, lines

GEO = {c: load(c) for c in list(FILES) + ["01-S200", "01-S250"]}

def piece(code, cx, cy, rot=0, fill=TONES[0], k=1.0, slits=True):
    """A die outline centred on (cx, cy), rotated, filled with a leather tone; slits in tomato."""
    w, h, d, lines = GEO[code]
    sl = "".join(f'<line x1="{a:.2f}" y1="{b:.2f}" x2="{c:.2f}" y2="{e:.2f}"/>' for a, b, c, e in lines) if slits else ""
    return (f'<g transform="translate({cx:.2f},{cy:.2f}) rotate({rot}) scale({k}) translate({-w/2:.2f},{-h/2:.2f})">'
            f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width=".35" stroke-linejoin="round"/>'
            f'<g stroke="{TOM}" stroke-width="1.1" stroke-linecap="round">{sl}</g></g>')

def tag_a(x, y, n, r=6.2):
    """Joint number on an A wing (the wing that goes in): filled."""
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{INK}"/>'
            f'<text x="{x:.2f}" y="{y + r*.42:.2f}" text-anchor="middle" font-size="{r*1.2:.1f}" font-weight="700" fill="#fff">{n}</text>')

def tag_b(x, y, n, r=6.2):
    """Joint number on a B slit (the side that receives): ring."""
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="#fff" stroke="{TOM}" stroke-width="1.6"/>'
            f'<text x="{x:.2f}" y="{y + r*.42:.2f}" text-anchor="middle" font-size="{r*1.2:.1f}" font-weight="700" fill="{TOM}">{n}</text>')

def note(x, y, t, size=6.5, anchor="middle", fill=INK):
    return f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}" font-size="{size}" fill="{fill}">{E(t)}</text>'

def svg(x0, y0, w, h, body, label):
    return (f'<svg viewBox="{x0:.1f} {y0:.1f} {w:.1f} {h:.1f}" role="img" aria-label="{E(label)}" '
            f'xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans Thai, Anuphan, sans-serif">{body}</svg>')

# ---------------------------------------------------------------- 3D bookkeeping for nets
def neg(v): return tuple(-a for a in v)
def axis_of(n):                       # the face's A axis: x faces -> y, y faces -> z, z faces -> x (works for a full cube)
    i = [abs(a) for a in n].index(1)
    a = [0, 0, 0]; a[(i + 1) % 3] = 1
    return tuple(a)
def par(u, v): return abs(sum(a * b for a, b in zip(u, v))) == 1

def frames(cells, start):
    """Roll a net: cells {name: (col, row)} -> {name: (normal, right, down)}; every fold goes the same way."""
    out = {start: ((0, 0, 1), (1, 0, 0), (0, 1, 0))}
    todo = [start]
    while todo:
        f = todo.pop(); n, r, d = out[f]; c0, r0 = cells[f]
        for g, (c1, r1) in cells.items():
            if g in out: continue
            dc, dr = c1 - c0, r1 - r0
            if (dc, dr) == (1, 0): out[g] = (r, neg(n), d)
            elif (dc, dr) == (-1, 0): out[g] = (neg(r), n, d)
            elif (dc, dr) == (0, 1): out[g] = (d, r, neg(n))
            elif (dc, dr) == (0, -1): out[g] = (neg(d), r, n)
            else: continue
            todo.append(g)
    return out

SIDES = {"right": (1, 0), "left": (-1, 0), "down": (0, 1), "up": (0, -1)}

def side_dir(fr, s):
    n, r, d = fr
    return {"right": r, "left": neg(r), "down": d, "up": neg(d)}[s]

def net(cells, start, order, dies, tones=None, reach=None, extra=None, free_label="ขอบบน"):
    """Exploded net. order: list of (face, face) pairs in joint order. dies: {face: die code}."""
    fr = frames(cells, start)
    normal = {f: fr[f][0] for f in cells}
    face_of = {v: k for k, v in normal.items()}
    joint = {frozenset(p): i + 1 for i, p in enumerate(order)}
    reach = reach or max(DIE[dies[f]][5] for f in cells)
    cell = 2 * reach + 14
    body = []
    for i, (f, (c, r)) in enumerate(cells.items()):
        n, rt, dn = fr[f]
        code = dies[f]
        horiz_a = par(axis_of(n), rt)                     # A wings left/right in this cell?
        rot = DIE[code][4] + (0 if horiz_a else 90)
        cx, cy = c * cell, r * cell
        body.append(piece(code, cx, cy, rot, (tones or TONES)[i % len(tones or TONES)]))
        lab = DIE[code][1] / 2 + (DIE[code][5] - DIE[code][1] / 2) / 2
        for s, (ux, uy) in SIDES.items():
            sd = side_dir(fr[f], s)
            g = face_of.get(sd)
            x, y = cx + ux * lab, cy + uy * lab
            if g is None:
                body.append(note(x, y + 2.3, free_label, 5.6, fill="#5B5B66"))
                continue
            j = joint[frozenset((f, g))]
            body.append(tag_a(x, y, j) if par(sd, axis_of(n)) else tag_b(x, y, j))
        body.append(note(cx, cy + 2.6, FACE_TH.get(f, f), 7.5, fill="#fff"))
        if extra: body.append(extra(f, cx, cy))
    cols = max(c for c, _ in cells.values()) + 1; rows = max(r for _, r in cells.values()) + 1
    return body, cell, cols, rows

FACE_TH = {"D": "ก้น", "U": "ฝา", "F": "หน้า", "B": "หลัง", "L": "ซ้าย", "R": "ขวา"}
CUBE = {"U": (1, 0), "B": (1, 1), "L": (0, 2), "D": (1, 2), "R": (2, 2), "F": (1, 3)}
CUBE_ORDER = [("D", "F"), ("D", "R"), ("D", "B"), ("D", "L"), ("F", "R"), ("R", "B"), ("B", "L"), ("L", "F"),
              ("U", "B"), ("U", "R"), ("U", "F"), ("U", "L")]

def draw_net(cells, start, order, dies, label, **kw):
    body, cell, cols, rows = net(cells, start, order, dies, **kw)
    h = cell / 2
    return svg(-h, -h, cols * cell, rows * cell, "".join(body), label)

def cube(dies, label="แผนภาพประกอบกล่องลูกบาศก์ 6 ชิ้น", **kw):
    return draw_net(CUBE, "D", CUBE_ORDER, dies, label, **kw)

def open_box(dies, label="แผนภาพประกอบกล่องเปิดด้านบน 5 ชิ้น"):
    cells = {k: v for k, v in CUBE.items() if k != "U"}
    return draw_net(cells, "D", CUBE_ORDER[:8], dies, label)

def ring(code, label="แผนภาพปลอก 4 ชิ้นต่อเป็นวง"):
    cells = {"F": (0, 0), "R": (1, 0), "B": (2, 0), "L": (3, 0)}
    return draw_net(cells, "F", [("F", "R"), ("R", "B"), ("B", "L"), ("L", "F")], {k: code for k in cells}, label,
                    free_label="ขอบแก้ว")

def sandwich(code, joints=4, label="แผนภาพประกบ 2 ชิ้น"):
    """Two pieces face to face, the top one turned 90 degrees, so every edge pairs an A wing with a B slit."""
    reach = DIE[code][5]; cell = 2 * reach + 14; lab = DIE[code][1] / 2 + (reach - DIE[code][1] / 2) / 2
    base = DIE[code][4]
    body = [piece(code, 0, 0, base, TONES[0]), piece(code, cell, 0, base + 90, TONES[2]),
            note(0, 2.6, "ชิ้นล่าง", 7.5, fill="#fff"), note(cell, 2.6, "ชิ้นบน", 7.5, fill="#fff")]
    names = ["up", "right", "down", "left"]
    for k, s in enumerate(names):
        ux, uy = SIDES[s]; n = k + 1
        a_low = s in ("left", "right")                    # native piece: A wings left/right
        if n > joints:
            body += [note(ux * lab, uy * lab + 2.3, "ฝา", 6, fill="#5B5B66"), note(cell + ux * lab, uy * lab + 2.3, "ฝา", 6, fill="#5B5B66")]
            continue
        body.append(tag_a(ux * lab, uy * lab, n) if a_low else tag_b(ux * lab, uy * lab, n))
        body.append(tag_b(cell + ux * lab, uy * lab, n) if a_low else tag_a(cell + ux * lab, uy * lab, n))
    body.append(f'<path d="M{reach + 2:.1f},0 L{cell - reach - 2:.1f},0" stroke="{INK}" stroke-width=".8" marker-end="url(#ar)"/>')
    body.insert(0, ARROW)
    h = cell / 2
    return svg(-h, -h, 2 * cell, cell, "".join(body), label)

def grid(code, cols, rows, label):
    reach = DIE[code][5]; cell = 2 * reach + 14; lab = DIE[code][1] / 2 + (reach - DIE[code][1] / 2) / 2
    base = DIE[code][4]; body = []; n = 0; num = {}
    for r in range(rows):                                  # build each row, then hook it to the row above
        for c in range(cols - 1):
            n += 1; num[(r, c, "right")] = num[(r, c + 1, "left")] = n
        if r:
            for c in range(cols):
                n += 1; num[(r - 1, c, "down")] = num[(r, c, "up")] = n
    for r in range(rows):
        for c in range(cols):
            flip = (r + c) % 2
            cx, cy = c * cell, r * cell
            body.append(piece(code, cx, cy, base + 90 * flip, TONES[(r * cols + c) % len(TONES)]))
            for s, (ux, uy) in SIDES.items():
                j = num.get((r, c, s))
                if not j: continue
                a = (s in ("left", "right")) != bool(flip)
                body.append((tag_a if a else tag_b)(cx + ux * lab, cy + uy * lab, j, 5.6))
    h = cell / 2
    return svg(-h, -h, cols * cell, rows * cell, "".join(body), label)

ARROW = (f'<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto">'
         f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>')

# ---------------------------------------------------------------- bear drawings
BEAR_LEFT_SLIT = (11.2, 62.66); BEAR_BOTTOM_SLIT = (41.7, 93.16)
BEAR_EAR_TOP = (41.685, 12.675); BEAR_EAR_RIGHT = (91.685, 62.675)

def bear_at(x, y, fill=TONES[0]):
    """Bear die with its top-left at (x, y), native orientation: ears top and right, slits left and bottom."""
    w = GEO["01"][0]
    return piece("01", x + w / 2, y + w / 2, 0, fill)

def bear_chain(n=5):
    w = GEO["01"][0]; step = w + 18; body = [ARROW]
    for i in range(n):
        x = i * step
        body.append(bear_at(x, 0, TONES[i % len(TONES)]))
        if i < n - 1:
            body.append(tag_a(x + BEAR_EAR_RIGHT[0], BEAR_EAR_RIGHT[1], i + 1))
        if i > 0:
            body.append(tag_b(x + BEAR_LEFT_SLIT[0] + 9, BEAR_LEFT_SLIT[1], i))
        body.append(note(x + 41.7, 66, ["พ่อ", "แม่", "ลูก 1", "ลูก 2", "ลูก 3"][i % 5], 9, fill="#fff"))
    body.append(note(BEAR_EAR_TOP[0], -6, "ผูกเชือก", 7))
    body.append(note((n - 1) * step + BEAR_EAR_TOP[0], -6, "ผูกเชือก", 7))
    return svg(-6, -16, n * step, w + 26, "".join(body), "แผนภาพราวหมีห้าตัว หูขวาของตัวหนึ่งเสียบร่องแก้มของตัวถัดไป")

def bear_strap(length, ring=False):
    w = GEO["01"][0]; sw, sh, _, _ = GEO[f"01-S{length}"]
    k = 1.0
    body = [ARROW, bear_at(0, 0)]
    body += [tag_b(BEAR_LEFT_SLIT[0] + 9, BEAR_LEFT_SLIT[1], 1), tag_b(BEAR_BOTTOM_SLIT[0], BEAR_BOTTOM_SLIT[1] - 9, 2)]
    sx, sy = w + 20, 30
    body.append(piece(f"01-S{length}", sx + sw / 2, sy + sh / 2, 0, TONES[1]))
    body.append(tag_a(sx + 6, sy + sh / 2, "ก"))
    body.append(note(sx + sw / 2, sy + sh + 10, f"สายหัวใจ {length} มม.", 7))
    body.append(f'<path d="M{sx - 2},{sy + sh/2} C{sx - 30},{sy + sh/2} {BEAR_LEFT_SLIT[0] - 14},{BEAR_LEFT_SLIT[1] - 30} {BEAR_LEFT_SLIT[0] - 2},{BEAR_LEFT_SLIT[1] - 8}" '
                f'fill="none" stroke="{COB}" stroke-width="1" stroke-dasharray="3 2" marker-end="url(#ar)"/>')
    if ring:
        body.append(f'<circle cx="{sx + sw + 9}" cy="{sy + sh/2}" r="7" fill="none" stroke="#8A8A94" stroke-width="2.4"/>')
        body.append(note(sx + sw + 9, sy + sh + 10, "ห่วงโลหะ", 6.5))
    return svg(-10, -8, sx + sw + (24 if ring else 8) + 10, w + 18, "".join(body), "แผนภาพร้อยสายหัวใจผ่านร่องของหัวหมี")

def single(code, label, extra="", tone=TONES[0]):
    w, h, _, _ = GEO[code]
    body = [piece(code, w / 2, h / 2, 0, tone),
            f'<path d="M0,{h + 6} L{w},{h + 6} M0,{h + 3} L0,{h + 9} M{w},{h + 3} L{w},{h + 9}" stroke="{INK}" stroke-width=".4"/>',
            note(w / 2, h + 14, f"{SIZE[code]} มม.", 7), extra]
    return svg(-6, -6, w + 12, h + 26, "".join(body), label)

def pinwheel(extra=""):
    w = GEO["02"][0]; c = w / 2; body = [piece("02", c, c, 0, TONES[0])]
    body.append(f'<rect x="{c - 27}" y="{c - 27}" width="54" height="54" fill="none" stroke="{PAPER}" stroke-width=".8" stroke-dasharray="2 1.6"/>')
    for i, (ux, uy) in enumerate(((0, -1), (1, 0), (0, 1), (-1, 0))):
        body.append(tag_a(c + ux * 36, c + uy * 36, i + 1))
    body.append(note(c, c + 2.5, "ช่องใส่ของ 5.4 ซม.", 5.4, fill="#fff"))
    body.append(extra)
    return svg(-4, -4, w + 8, w + 8, "".join(body), "แผนภาพพับกลีบกังหันตามลำดับ 1 ถึง 4")

def row_of(codes, label, k=1.0):
    gap = 10; x = 0; body = []
    for i, code in enumerate(codes):
        w, h, _, _ = GEO[code]
        body.append(piece(code, x + w / 2, h / 2, 0, TONES[i % len(TONES)]))
        body.append(note(x + w / 2, h + 10, f"{code} · {SIZE[code]}", 6.5))
        x += w + gap
    return svg(-4, -4, x - gap + 8, max(GEO[c][1] for c in codes) + 20, "".join(body), label)

def kit(code, n, cols, label):
    w, h, _, _ = GEO[code]; k = .5; step = w * k + 6; body = []
    for i in range(n):
        body.append(piece(code, (i % cols) * step + w * k / 2, (i // cols) * step + h * k / 2, 90 * (i % 2), TONES[i % len(TONES)], k))
    rows = (n + cols - 1) // cols
    return svg(-3, -3, cols * step, rows * step, "".join(body), label)

def pips(n, cx, cy, s=7):
    pos = {1: [(0, 0)], 2: [(-1, -1), (1, 1)], 3: [(-1, -1), (0, 0), (1, 1)], 4: [(-1, -1), (1, -1), (-1, 1), (1, 1)],
           5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)], 6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)]}[n]
    return "".join(f'<circle cx="{cx + x*s:.1f}" cy="{cy + y*s:.1f}" r="2.6" fill="{PAPER}" stroke="{INK}" stroke-width=".4"/>' for x, y in pos)

DICE = {"F": 1, "B": 6, "R": 2, "L": 5, "U": 3, "D": 4}

# ---------------------------------------------------------------- product sheets
def T(code): return DIE[code][0] if code in DIE else B.PIECE_NAME[code]

CUBE_STEPS = [
    "วางชิ้นก้นตรงกลาง ผนัง 4 ชิ้นรอบ ๆ ตามแผนภาพ ด้านสวยของหนังคว่ำลงโต๊ะ",
    "รอยต่อ 1–4 ทำตอนวางราบ: บีบปีกนกของปีกที่มีวงทึบให้แคบ สอดผ่านร่องกลางที่มีเลขเดียวกัน ปล่อยให้ปีกกางล็อก",
    "ยกผนังทั้ง 4 ขึ้นตั้งฉาก แล้วทำรอยต่อ 5–8 ที่มุมทีละมุม",
    "ใส่ของ (ถ้ามี) แล้วปิดฝาด้วยรอยต่อ 9–12",
    "บีบมุมทั้ง 8 ให้เข้ารูป ปีกด้านรับทุกปีกต้องพับทับอยู่ด้านนอก",
]
OPEN_STEPS = CUBE_STEPS[:3] + ["ขอบบนทั้ง 4 ด้านไม่ต้องต่อ ปล่อยปีกตั้งขึ้นหรือพับออกตามแบบสินค้า"]
RING_STEPS = ["เรียง 4 ชิ้นเป็นแถว สลับทิศตามแผนภาพ ด้านสวยคว่ำลง",
              "ทำรอยต่อ 1–3 ตอนวางราบ", "ม้วนเป็นวงรอบแก้วจริง แล้วปิดวงด้วยรอยต่อ 4",
              "ปีกขอบบนและขอบล่างพับออกด้านนอก ไม่ต้องต่อ"]
SAND_STEPS = ["วางชิ้นล่างด้านสวยคว่ำลง วางของ (ถ้ามี) ตรงกลาง",
              "หมุนชิ้นบน 90 องศา ด้านสวยหงายขึ้น วางทับให้สี่เหลี่ยมกลางตรงกัน",
              "พับปีกทุกด้านเข้าหากัน แล้วทำรอยต่อตามเลขทีละขอบ"]

QC_ALL = ["ด้านสวยของหนังไม่มีรอยถลอก รู หรือรอยพับลึก",
          "ขอบตัดเรียบ ไม่มีเส้นใยหนังลุ่ย",
          "ร่องทุกเส้นขาดตลอดความยาว ไม่มีเยื่อหนังค้าง และปลายร่องไม่ฉีก"]
QC_JOINT = ["ทุกรอยต่อดึงเบา ๆ แล้วไม่หลุด ปีกนกกางเต็มทั้งสองข้าง",
            "สอดปีกได้ด้วยแรงนิ้ว ถ้าต้องดันจนหนังยับ ให้แยกชิ้นนั้นไปทำสินค้าชิ้นเดียว"]
QC_BOX = ["ตั้งบนโต๊ะแล้วไม่โยก มุมทั้ง 8 ได้ฉาก", "ผนังที่อยู่ตรงข้ามกันใช้หนังโทนเดียวกัน"]

PROTO_TEST = {
    2: ["เหน็บมุมกระดาษแล้วไม่หลุดตอนปิดหนังสือ", "ไม่ทิ้งรอยยับบนหน้ากระดาษ"],
    3: ["สายหัวใจร้อยผ่านร่องได้ไม่ฝืด และไม่เลื่อนหลุดเวลาแกว่ง", "เขียนชื่อด้านหลังด้วยปากกาอะไรแล้วไม่ลอก"],
    4: ["ห่วงรัดผ้าเช็ดปากพับได้แน่นพอ", "เช็ดคราบอาหารออกได้"],
    5: ["ธนบัตรพับให้เหลือไม่เกิน 5 ซม. แล้วใส่ได้", "กลีบสุดท้ายล็อกไม่เด้งออก"],
    6: ["แหวนและต่างหูไม่หลุดเมื่อเขย่า"], 7: ["การ์ด 5 × 5 ซม. ใส่ได้พอดี", "ผูกเชือกติดกล่องตรงไหนแล้วไม่ฉีกร่อง"],
    8: ["ประกอบหนังจริงแล้วกล่องได้ฉาก", "เปิดปิดฝาซ้ำ 20 ครั้ง ร่องไม่ขาด"],
    9: ["ตอกจุดชัดทุกด้าน และด้านตรงข้ามรวมกันได้ 7", "ทอยแล้วกล่องไม่ยุบ"],
    10: ["AirTag (กว้าง 3.2 ซม.) ใส่ได้และไม่หลุด", "ต้องมีห่วงหรือสายคล้องกระเป๋าไหม (ยังไม่มีในรายการชิ้นส่วน)"],
    11: ["ต่อและแกะซ้ำ 50 ครั้ง ร่องไม่ขาด", "เด็กต่อเองได้โดยไม่มีคนช่วย"],
    12: ["ผนังไม่ล้มเมื่อใส่ปากกา 10 ด้าม", "ปีกบนตั้งเป็นยอดมงกุฎได้เองโดยไม่ต้องดัด"],
    13: ["แผ่นวางราบไม่โก่ง", "จานร้อนวางแล้วหนังไม่ด่าง"],
    14: ["วัดรอบแก้วร้อนของร้านจริงก่อน แล้วลองว่าปลอกไม่หลุดตอนยก"],
    15: ["ไม้ก๊อก 6 × 6 ซม. ไม่เลื่อน", "แก้วเย็นวางแล้วน้ำไม่ซึมถึงโต๊ะ"],
    16: ["เหรียญสิบ 5 เหรียญใส่ได้", "ฝาไม่เปิดเองในกระเป๋า"],
    17: ["ปีกของ 04 กับร่องของ 05 แน่นเท่ากับต่อชนิดเดียวกัน"],
    18: ["ใส่สบู่หรือขนม 100 กรัม ก้นไม่หลุด", "จับเวลาทำ 10 กล่อง เพื่อรับงานแต่งจำนวนมาก"],
    19: ["ตั้งแปรง 6 ด้ามแล้วไม่ล้ม"], 20: ["แขวนแล้วรอยต่อไม่คลายเอง", "ริบบิ้นผูกตรงมุมไหนแล้วกล่องห้อยตรง"],
    21: ["หูเสียบร่องแก้มแน่น ราวไม่หลุดตอนแขวน", "หมีห้อยแล้วตั้งตรงไม่เอียง"],
    23: ["ห่วงโลหะไม่ขูดหนังจนขาด", "ดึงสายแรง ๆ แล้วไม่หลุดจากร่อง"],
    25: ["เป่าแล้วหมุนได้จริง หนังหนักกว่ากระดาษ ถ้าไม่หมุนให้ขายเป็นของตกแต่ง", "หมุดยึดไม่ฉีกจุดกลาง"],
}

def assembly(p):
    """(diagram svg, steps list, extra QC list) for one product."""
    n, parts = p["n"], dict(p["parts"])
    if n in (1, 2, 22):
        return single("01", "หัวหมี 01"), p["steps"], []
    if n in (24, 27, 28):
        code = {24: "02", 27: "04", 28: "05"}[n]
        return single(code, T(code)), ["ตรวจตามรายการ QC", "ใส่ซองหรือมัดชุด"], []
    if n == 26:
        return single("03", "ป้ายห้อย 03"), p["steps"], ["เชือกร้อยผ่านร่องแล้วไม่ฉีกปลายร่อง"]
    if n == 29:
        return row_of(["01", "02", "04", "05"], "ที่รองแก้ว 4 ลาย"), p["steps"], ["สี่ชิ้นในชุดเป็นหนังคนละโทน"]
    if n in (3, 4, 23):
        L = 250 if n == 3 else 200
        st = (["ใส่ห่วงโลหะที่ปลายสายด้านหัวใจ"] if n == 23 else []) + [
            "สอดปลายสาย (ก) เข้าร่องแก้ม 1 จากด้านหน้า ออกด้านหลัง",
            "อ้อมด้านหลัง แล้วสอดออกทางร่องล่าง 2 ให้หมีอยู่กลางสาย",
            p["steps"][-1]]
        return bear_strap(L, ring=n == 23), st, ["สายไม่บิดเมื่อมองจากด้านหน้า", "หมีเลื่อนอยู่กลางสายได้ แต่ไม่หลุดเอง"]
    if n == 21:
        return bear_chain(5), ["เรียงหมี 5 ตัวตามแผนภาพ เลือกหนัง 5 โทน", "รอยต่อ 1–4: สอดหูขวาของหมีตัวหนึ่ง (วงทึบ) เข้าร่องแก้มของตัวถัดไป (วงโปร่ง)",
                               "ผูกเชือกแขวนที่หูบนของหมีตัวแรกและตัวสุดท้าย"], ["หมีทั้ง 5 ตัวหันหน้าด้านเดียวกัน"]
    if n in (5, 6, 7):
        return pinwheel(), ["วางของตรงกลาง (ช่องสี่เหลี่ยมประ 5.4 ซม.)", "พับกลีบ 1 ถึง 4 เข้ากลางตามลำดับ",
                            "สอดกลีบ 4 ใต้กลีบ 1 ให้ร่องของกลีบขัดกันแบบกังหัน"] + p["steps"][2:], ["กลีบทั้ง 4 ซ้อนกันเท่ากัน ไม่เบี้ยว"]
    if n == 25:
        ex = f'<circle cx="45" cy="45" r="2.4" fill="#8A8A94"/>'
        return pinwheel(ex), ["พับปลายกลีบเข้าหาจุดกลางทีละกลีบตามเลข อย่าพับทับร่อง", "ตอกหมุดผ่านจุดกลางยึดกับไม้ (ผู้ใหญ่ทำ)",
                              "เป่าดูว่าหมุน"], ["หมุดแน่น ไม่โยก"]
    if n in (8, 9, 18, 20, 30):
        code = list(parts)[0]
        if n == 9:
            extra = lambda f, cx, cy: pips(DICE[f], cx, cy - 4)
            return cube({k: code for k in CUBE}, extra=extra), ["ตอกจุดบนแต่ละชิ้นก่อนประกอบ ตามจำนวนในแผนภาพ"] + CUBE_STEPS, QC_BOX
        st = list(CUBE_STEPS)
        if n == 30:
            st = ["แพ็ค 6 ชิ้นพร้อมการ์ดวิธีต่อ (ใช้แผนภาพนี้) ไม่ต้องประกอบที่บ้าน",
                  "ประกอบตัวอย่าง 1 กล่องไว้โชว์ที่บูธ ตามขั้นตอนด้านล่าง"] + CUBE_STEPS
        if n == 20: st.append("ผูกริบบิ้นที่มุมบน")
        if n == 8: st[3] = "วางแหวนบนก้น แล้วปิดฝาด้วยรอยต่อ 9–12 ฝาเปิดได้โดยถอดรอยต่อ 11 จุดเดียว"
        return cube({k: code for k in CUBE}), st, QC_BOX
    if n == 17:
        dies = {"D": "04", "U": "05", "F": "04", "B": "04", "L": "05", "R": "05"}
        return cube(dies), ["ชิ้นเหลี่ยม 04 เป็นก้น หน้า และหลัง ชิ้นกลม 05 เป็นฝา ซ้าย และขวา"] + CUBE_STEPS, QC_BOX
    if n in (12, 19):
        code = list(parts)[0]
        st = list(OPEN_STEPS)
        if n == 12: st[-1] = "ปีกขอบบนพับตั้งขึ้นเป็นยอดมงกุฎ"
        return open_box({k: code for k in CUBE if k != "U"}), st, QC_BOX
    if n == 14:
        return ring("05"), RING_STEPS, ["ปลอกพอดีแก้ว ไม่หลวมจนเลื่อนลง"]
    if n in (10, 15, 16):
        code = list(parts)[0]
        j = p["joints"]
        st = list(SAND_STEPS)
        if n == 15: st[0] = "วางชิ้นล่างด้านสวยคว่ำลง วางแผ่นไม้ก๊อกตรงกลาง"
        if n == 10: st[0] = "วางชิ้นล่างด้านสวยคว่ำลง วาง AirTag ตรงกลาง"
        if n == 16: st.append("ขอบบน (ฝา) ไม่ต้องต่อ ใช้เปิดปิดใส่เหรียญ")
        return sandwich(code, j), st, ["ของข้างในไม่ขยับเมื่อเขย่า"]
    if n == 13:
        return grid("04", 3, 4, "แผนภาพแผ่นรองจาน 3 × 4 ชิ้น"), ["วางชิ้นเป็นตาราง 3 แถวตามขวาง 4 แถวตามยาว สลับทิศชิ้นแบบตารางหมากรุก",
                 "ทำรอยต่อในแถวเดียวกันก่อน แล้วค่อยต่อแถวเข้าหากัน ตามเลข 1–17", "พลิกด้านหน้าขึ้น ปีกที่ซ้อนกันจะเป็นลายข้าวหลามตัด"], ["แผ่นวางราบ ไม่มีมุมยก"]
    if n == 11:
        return kit("03", 24, 8, "ชุดตัวต่อ 24 ชิ้น"), ["คัดชิ้น 24 ชิ้น อย่างน้อย 4 โทน", "ใส่ถุงผ้าพร้อมการ์ดวิธีเล่น",
                                                   "ประกอบตัวอย่างลูกบาศก์ 1 อันไว้โชว์ที่บูธ"], ["นับครบ 24 ชิ้น"]
    raise ValueError(n)

def who(p, steps):
    if p["n"] == 25: return "ผู้ใหญ่ (ตอกหมุด)"
    if p["joints"] == 0: return "ลูก ๆ ทำได้ทั้งหมด"
    if p["joints"] <= 4: return "ลูก ๆ ทำได้หลังซ้อม 3 ชิ้น"
    return "ผู้ใหญ่หรือพี่คนโต"

def money(v): return f"{v:,.2f}".rstrip("0").rstrip(".")

def sheet(p):
    code = BB.product_code(p)
    diagram, steps, qc_extra = assembly(p)
    tag = "Love" if p["coll"] == "love" else "SOI. 02"
    bom = "".join(f"<tr><td>{E(T(c))} <span class='mono'>{c}</span></td><td class='n'>{q}</td><td class='mono'>{SIZE[c]}</td>"
                  f"<td>{'เศษใหญ่' if c.startswith('01') else 'เศษเล็ก'}</td></tr>" for c, q in p["parts"])
    if p["extra"]:
        bom += f"<tr><td>{E(p['extra'][0])}</td><td class='n'>1</td><td>-</td><td>{money(p['extra'][1])} บาท</td></tr>"
    bom += f"<tr><td>ป้ายห้อย {tag} 55 × 89 มม. และซองหรือถุง</td><td class='n'>1</td><td>-</td><td>{money(B.PACKAGING)} บาท</td></tr>"
    asm_s = p["joints"] * 20
    total_min = p["stock"] * (asm_s + 60) / 60
    specs = [("ขนาดเสร็จ", p["size"]), ("ชิ้นหนัง", f"{p['npieces']} ชิ้น"), ("รอยต่อที่บ้าน", f"{p['joints']} จุด"),
             ("เวลาประกอบ", f"{asm_s} วินาที + แพ็ค 60 วินาที"), ("ใครทำ", who(p, steps)),
             ("ต้นทุน", f"{money(p['cost'])} บาท"), ("ราคาขาย", f"{p['price']} บาท"), ("กำไรต่อชิ้น", f"{money(p['profit'])} บาท ({p['margin']:.0%})"),
             ("ผลิตไปบูธ", f"{p['stock']} ชิ้น · ประมาณ {total_min:.0f} นาที")]
    spec_rows = "".join(f"<tr><th>{E(a)}</th><td>{E(b)}</td></tr>" for a, b in specs)
    qc = QC_ALL + (QC_JOINT if p["joints"] else []) + qc_extra
    tests = PROTO_TEST.get(p["n"], [])
    test_html = (f'<div class="card warn"><h4>ต้องลองต้นแบบก่อนผลิต</h4><ul>{"".join(f"<li>{E(t)}</li>" for t in tests)}</ul></div>'
                 if tests and p["status"] != B.READY else "")
    chip = S.status_chip(p["status"])
    return f"""<section class="tp" id="p{p['n']:02d}">
<header class="tph"><span class="code">{code}</span><div><h2>{E(p['name'])}</h2>
<p class="cap">{E(p['line'])} · <span class="chip {chip}">{E(p['status'])}</span> · {E(p['hook'])}</p></div></header>
<div class="tpgrid"><figure class="dia">{diagram}<figcaption class="cap">● ปีกเสียบ (มีร่องที่ปลายสองข้าง) &nbsp; ○ ร่องรับ (ร่องกลาง) · เลขเดียวกันคือรอยต่อเดียวกัน · เส้นแดงคือร่องที่บล็อกตัด</figcaption></figure>
<div class="side"><table class="spec">{spec_rows}</table></div></div>
<div class="tpgrid2"><div><h4>ชิ้นส่วน</h4><div class="tbl"><table><thead><tr><th>ชิ้น</th><th>จำนวน</th><th>ขนาด มม.</th><th>วัสดุ</th></tr></thead><tbody>{bom}</tbody></table></div>
<h4>ขั้นตอน</h4><ol>{"".join(f"<li>{E(s)}</li>" for s in steps)}</ol></div>
<div><h4>ตรวจก่อนแพ็ค</h4><ul class="qc">{"".join(f"<li>{E(q)}</li>" for q in qc)}</ul>{test_html}</div></div>
</section>"""

# ---------------------------------------------------------------- front matter
def die_table():
    use, big, small = B.piece_usage()
    rows = ""
    for c in FILES:
        name, fold, slit, neck = DIE[c][:4]
        prods = [p for p in B.PRODUCTS if any(k == c for k, _ in p["parts"])]
        rows += (f"<tr><td><b class='mono'>{c}</b> {E(name)}</td><td class='mono'>{SIZE[c]}</td>"
                 f"<td class='mono'>{fold or '-'}</td><td class='mono'>{slit or '-'} / {neck or '-'}</td>"
                 f"<td class='n'>{B.DIE_PRICE[c]:,}</td><td class='n'>{money(B.PIECE_COST[c])}</td><td class='n'>{use.get(c, 0)}</td>"
                 f"<td>{len(prods)} แบบ</td></tr>")
    strap = sum(use.get(k, 0) for k in ("01-S200", "01-S250"))
    rows += (f"<tr><td><b class='mono'>01-S</b> สายหัวใจ 200 และ 250</td><td class='mono'>200/250 × 24</td><td>-</td><td>-</td>"
             f"<td class='n'>ยังไม่มีราคา</td><td class='n'>{money(B.PIECE_COST['01-S200'])}</td><td class='n'>{strap}</td><td>4 แบบ</td></tr>")
    return rows, big, small

def gallery():
    """The six dies side by side at the same scale, A and B sides marked."""
    body = []; x = 0
    for c in FILES:
        w, h, _, _ = GEO[c]
        body.append(piece(c, x + w / 2, 52, 0, TONES[0]))
        body.append(note(x + w / 2, 118, f"{c} {DIE[c][0]}", 8))
        x += w + 12
    return svg(-4, -4, x - 4, 128, "".join(body), "บล็อกทั้ง 6 แบบ ขนาดเท่าจริงเทียบกัน")

CSS = """
.tp{border-top:2px solid var(--ink);padding-top:var(--s4);margin-top:var(--s6);display:flex;flex-direction:column;gap:var(--s4)}
.tph{display:flex;gap:var(--s4);align-items:flex-start}.tph h2{margin:0}
.code{font-family:var(--logo);font-weight:500;background:var(--ink);color:var(--bg);padding:4px 10px;border-radius:6px;white-space:nowrap}
.tpgrid{display:grid;gap:var(--s4);grid-template-columns:1.618fr 1fr;align-items:start}
.tpgrid2{display:grid;gap:var(--s4);grid-template-columns:1fr 1fr;align-items:start}
@media (max-width:760px){.tpgrid,.tpgrid2{grid-template-columns:1fr}}
.dia{margin:0;background:#fff;border:1px solid var(--line);border-radius:var(--s3);padding:var(--s3)}
.dia svg{width:100%;height:auto;max-height:520px;display:block}
.spec{width:100%;border-collapse:collapse;font-size:15px}.spec th{text-align:left;color:var(--muted);font-weight:400;padding:6px 8px 6px 0;white-space:nowrap;vertical-align:top}
.spec td{padding:6px 0;border-bottom:1px solid var(--line)}
h4{margin:var(--s3) 0 var(--s2);font-family:var(--display);font-size:17px}
ol,ul{padding-left:1.3em;margin:0}li{margin:4px 0}
.qc li::marker{content:"☐  "}
.card.warn{border:2px solid #E9B44C;background:#FFF8E5;margin-top:var(--s3)}
.toc{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:6px}
.toc a{display:flex;gap:8px;text-decoration:none;color:var(--ink);padding:6px 8px;border:1px solid var(--line);border-radius:8px;background:var(--paper)}
.toc .mono{color:var(--muted)}
.legend{display:flex;gap:var(--s4);flex-wrap:wrap;align-items:center}.legend svg{width:233px;height:auto;flex:none}
@media print{
  @page{size:A4;margin:12mm}
  body{background:#fff}.wrap{max-width:none;padding:0}
  nav.top,.noprint{display:none}
  .tp{break-before:page;margin-top:0;border-top:none}
  .tpgrid{grid-template-columns:1.4fr 1fr}.tpgrid2{grid-template-columns:1fr 1fr}
  .dia svg{max-height:100mm}
  body{font-size:11px}.spec{font-size:10.5px}h2{font-size:19px}h4{font-size:12.5px;margin:5px 0 3px}li{margin:0}
  .tbl{overflow:visible}.tbl table{width:100%;font-size:9.5px}.tbl th,.tbl td{padding:3px 5px}
  .front section{break-inside:avoid}
  .front{break-after:page}
}
"""

def build():
    rows, big, small = die_table()
    t = B.event_totals()
    toc = "".join(f'<a href="#p{p["n"]:02d}"><span class="mono">{BB.product_code(p)}</span> {E(p["name"])}</a>' for p in B.PRODUCTS)
    legend = svg(-8, -8, 120, 16, tag_a(0, 0, 1) + note(10, 2.4, "ปีกเสียบ", 7, "start") + tag_b(52, 0, 1) + note(62, 2.4, "ร่องรับ", 7, "start"), "สัญลักษณ์")
    sheets = "".join(sheet(p) for p in B.PRODUCTS)
    old = 950 * 6
    return f"""{S.head("OCT. 26 Tech Pack")}<style>{CSS}</style>
<div class="wrap">
<nav class="top noprint" aria-label="หัวข้อ"><a href="#dies">บล็อก</a><a href="#rule">วิธีอ่านแบบ</a><a href="#plan">แผนผลิต</a><a href="#list">สินค้า 30 แบบ</a></nav>
<div class="front">
<header style="padding-top:28px;display:flex;flex-direction:column;gap:12px"><span class="eyebrow">TECH PACK · 15 ต.ค. 2569 · บูธ 23–25 ต.ค.</span>
<h1>สินค้า 30 แบบ จากบล็อก 6 แบบ</h1>
<p class="lead">หนึ่งหน้าต่อหนึ่งสินค้า บอกว่าต้องตัดชิ้นไหนกี่ชิ้น ต่อตรงไหนก่อนหลัง ใช้เวลาเท่าไร ใครทำได้ และต้องตรวจอะไรก่อนแพ็ค ส่งให้ช่างหรือให้ลูก ๆ ทำตามได้เลย</p>
<p class="cap">ภาพทุกภาพใช้เส้นตัดจริงจากไฟล์บล็อก rev 20261014 เลขรอยต่อคำนวณจากรูปทรงสามมิติของกล่อง เลขหนึ่งเลขจึงมีสองที่เสมอ ที่ปีกเสียบหนึ่งที่ และที่ร่องรับหนึ่งที่ · ฉบับพิมพ์ A4 กดพิมพ์จากเบราว์เซอร์ได้ หนึ่งสินค้าหนึ่งหน้า</p></header>

<section id="dies"><span class="eyebrow">บล็อก</span><h2>บล็อกไม้ 6 แบบ ราคาจริง {sum(B.DIE_PRICE.values()):,} บาท</h2>
<div class="dia">{gallery()}</div>
<div class="tbl"><table><thead><tr><th>บล็อก</th><th>ขนาด มม.</th><th>สี่เหลี่ยมพับ มม.</th><th>ร่อง / คอปีก มม.</th><th>ราคาบล็อก บาท</th><th>ต้นทุนต่อชิ้น บาท</th><th>ต้องตัดไปบูธ ชิ้น</th><th>ใช้ใน</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="cap">ราคาบล็อกได้มา 15 ต.ค. 2569 ถูกกว่าที่ประมาณไว้ ({old:,} บาท) อยู่ {old - sum(B.DIE_PRICE.values()):,} บาท ต้นทุนต่อชิ้น = ค่าหนัง + ค่าตัด 1.5 บาท + ราคาบล็อกเฉลี่ย {B.DIE_QTY:,} ชิ้น บล็อกสายหัวใจยังไม่มีราคา ตอนนี้ยังใช้ตัวเลขประมาณเดิม 950 บาท ต้องตัดไปบูธ: เศษใหญ่ {big} ชิ้น จากที่ตัดได้ {B.LOT_CAPACITY['ใหญ่']} · เศษเล็ก {small} ชิ้น จากที่ตัดได้ {B.LOT_CAPACITY['เล็ก']}</p></section>

<section id="rule"><span class="eyebrow">วิธีอ่านแบบ</span><h2>รอยต่อแบบเดียว ใช้กับทุกกล่อง</h2>
<div class="grid">
<div class="card"><h3>ปีกเสียบ ●</h3><p>ด้านที่มีร่องสั้นตรงปลายเส้นพับทั้งสองข้าง ปีกจึงเหลือแค่คอตรงกลางกับปีกนกสองข้าง บีบปีกนกให้แคบแล้วสอดเข้าร่อง ปล่อยแล้วปีกจะกางล็อกเอง</p></div>
<div class="card"><h3>ร่องรับ ○</h3><p>ด้านที่มีร่องยาวตรงกลางเส้นพับ ร่องยาวกว่าคอปีก 0.5 มม. ปีกรับจะพับทับอยู่ด้านนอกชิ้นที่เสียบเข้ามา</p></div>
<div class="card"><h3>กติกา</h3><p>ทุกชิ้นของ 03 04 05 06 มีปีกเสียบ 2 ด้านตรงข้ามกัน และร่องรับอีก 2 ด้าน รอยต่อหนึ่งจุดคือปีกเสียบคู่กับร่องรับเสมอ เลขเดียวกันในภาพคือคู่เดียวกัน</p></div></div>
<div class="legend">{legend}<span class="cap">ด้านสวยของหนัง (ด้านเกรน) อยู่ด้านนอกของสินค้าเสมอ · 04 กับ 05 ใช้สี่เหลี่ยมพับ ร่อง และคอปีกขนาดเดียวกัน จึงต่อข้ามแบบกันได้</span></div></section>

<section id="plan"><span class="eyebrow">แผนผลิต</span><h2>ของไปบูธ {t['units']} ชิ้น</h2>
<div class="grid s">
<div class="card"><p class="cap">ประกอบ</p><p style="font-size:28px;font-weight:600">{t['assembly_h']:.1f} ชม.</p><p class="cap">รอยต่อละ 20 วินาที</p></div>
<div class="card"><p class="cap">ตรวจและแพ็ค</p><p style="font-size:28px;font-weight:600">{t['pack_h']:.1f} ชม.</p><p class="cap">ชิ้นละ 60 วินาที</p></div>
<div class="card"><p class="cap">ต้นทุนรวม</p><p style="font-size:28px;font-weight:600">{t['cost']:,.0f} บาท</p><p class="cap">ขายหมดได้ {t['sales']:,.0f} บาท</p></div></div>
<div class="card"><h3>ลำดับงาน</h3><ol>
<li>วัดความหนาเศษหนังแต่ละล็อตก่อนตัด ลองสอดปีกกับร่องของชิ้นแรก ถ้าฝืดจนหนังยับ ให้แยกเศษหนาไปทำที่รองแก้ว</li>
<li>ตัดชิ้นตามตารางบล็อก แยกกองตามแบบ และตามโทนสี</li>
<li>ทำต้นแบบ 1 ชิ้นของทุกสินค้าที่ยังเป็น "ลองต้นแบบก่อน" ทดสอบตามกล่องสีเหลืองในหน้านั้น ตัวไหนไม่ผ่าน ตัดออกจากบูธ</li>
<li>ผลิตตามจำนวน แล้วตรวจทุกชิ้นตามรายการ "ตรวจก่อนแพ็ค" ก่อนติดป้ายห้อย</li></ol>
<p class="cap">ตัวเลขเวลาและค่าแรงเป็นค่าตั้งต้นจาก Google Sheet ต้นทุน ให้จับเวลาจริงตอนทำต้นแบบ แล้วแก้ใน brand.py</p></div></section>

<section id="list"><span class="eyebrow">สินค้า</span><h2>สินค้า 30 แบบ</h2><div class="toc">{toc}</div></section>
</div>
{sheets}
</div>"""

if __name__ == "__main__":
    out = os.path.join(ROOT, "site", "techpack.html")
    open(out, "w").write(build())
    print("wrote", out)
