"""Build the pattern-05 cube assembly page + Rev B (slot 18) cut files."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import generate as g

R = 45.0
H = R / math.sqrt(2)          # 31.82, half of the fold square
SLIT = 30.0                   # receiver slit (B), centred
SLOT = 18.0                   # tab slot (A) from each corner. Rev A drawing = 15
# screen coords (y down). edge k: 0 right, 1 top, 2 left, 3 bottom
DIR = [(1, 0), (0, -1), (-1, 0), (0, 1)]
TAN = [(0, 1), (1, 0), (0, -1), (-1, 0)]
FILL = {"base": "var(--l-base)", "light": "var(--l-light)", "dark": "var(--l-dark)"}

def depth(s):
    return max(math.sqrt(R * R - s * s) - H, 0.0)

def cap(cx, cy, k, n=36):
    d, t = DIR[k], TAN[k]
    mx, my = cx + H * d[0], cy + H * d[1]
    pts = [(mx - H * t[0], my - H * t[1])]
    for i in range(n + 1):
        s = -H + 2 * H * i / n
        pts.append((mx + s * t[0] + depth(s) * d[0], my + s * t[1] + depth(s) * d[1]))
    pts.append((mx + H * t[0], my + H * t[1]))
    return "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " Z"

def edge_pt(cx, cy, k, s):
    d, t = DIR[k], TAN[k]
    return (cx + H * d[0] + s * t[0], cy + H * d[1] + s * t[1])

def seg(p, q, cls):
    return f'<line x1="{p[0]:.2f}" y1="{p[1]:.2f}" x2="{q[0]:.2f}" y2="{q[1]:.2f}" class="{cls}"/>'

def cuts(cx, cy, k, tab):
    """Red cut marks on edge k: tab -> two end slots, receiver -> centred slit."""
    if tab:
        return (seg(edge_pt(cx, cy, k, -H), edge_pt(cx, cy, k, -H + SLOT), "sl")
                + seg(edge_pt(cx, cy, k, H - SLOT), edge_pt(cx, cy, k, H), "sl"))
    return seg(edge_pt(cx, cy, k, -SLIT / 2), edge_pt(cx, cy, k, SLIT / 2), "sl")

def square(cx, cy, tone):
    return f'<rect x="{cx-H:.2f}" y="{cy-H:.2f}" width="{2*H:.2f}" height="{2*H:.2f}" fill="{FILL[tone]}" class="pc"/>'

def assembly(pieces, seams):
    """pieces: {name: (cx, cy, tone, tab_edges)}; seams: set of (name, k) joined to a neighbour."""
    free, sq, under, over, marks = [], [], [], [], []
    for name, (cx, cy, tone, tabs) in pieces.items():
        sq.append(square(cx, cy, tone))
        for k in range(4):
            tab = k in tabs
            if (name, k) in seams:
                (under if tab else over).append(
                    f'<path d="{cap(cx, cy, k)}" class="hid"/>' if tab else
                    f'<path d="{cap(cx, cy, k)}" fill="{FILL[tone]}" class="pc"/>')
            else:
                free.append(f'<path d="{cap(cx, cy, k)}" fill="{FILL[tone]}" class="pc"/>')
                marks.append(cuts(cx, cy, k, tab))
    return "".join(free + sq + under + over + marks)

def label(x, y, text, cls="lb", anchor="start"):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{text}</text>'

def callout(x1, y1, x2, y2, text, anchor="start"):
    dx = 1.2 if anchor == "start" else -1.2
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="co"/>'
            f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="0.9" class="cod"/>' + label(x2 + dx, y2 + 1.4, text, "lb", anchor))

# ---- step 1: one Rev B piece, annotated
def step1():
    cx, cy = 100, 62
    body = (f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="var(--l-light)" class="pc"/>'
            f'<rect x="{cx-H:.2f}" y="{cy-H:.2f}" width="{2*H:.2f}" height="{2*H:.2f}" class="fd"/>'
            + cuts(cx, cy, 1, False) + cuts(cx, cy, 3, False) + cuts(cx, cy, 0, True) + cuts(cx, cy, 2, True))
    ann = (callout(cx, cy - H - 6, cx + 42, 8, "ปีก B ตัวรับ · slit กลาง 30")
           + callout(cx - H, cy - H + 9, 10, 18, "slot 18 (แบบเดิม 15)")
           + callout(cx - H - 6, cy + 4, 10, 76, "ปีก A ตัวเสียบ")
           + callout(cx + H, cy, cx + 50, cy + 36, "คอปีก A 27.6")
           + callout(cx + 10, cy + 12, cx + 50, cy + 48, "ตัวชิ้น 63.6 × 63.6"))
    badge = (f'<g transform="translate(34,104)"><rect x="-17" y="-8" width="34" height="13" class="bd"/>'
             + label(0, 1, "× 6 ชิ้น", "lbb", "middle") + "</g>")
    return f'<svg viewBox="0 0 200 118" role="img" aria-label="ชิ้น 05 Rev B พร้อมชื่อส่วนต่าง ๆ">{body}{ann}{badge}</svg>'

# ---- step 2: one joint, detail (flat)
def step2():
    F, G = (62, 64), (62 + 2 * H, 64)
    pieces = {"F": (*F, "light", {0, 2}), "G": (*G, "dark", {1, 3})}
    art = assembly(pieces, {("F", 0), ("G", 2)})
    ex = F[0] + H
    joint = (seg((ex, F[1] - H), (ex, F[1] - H + SLOT), "sl") + seg((ex, F[1] + H - SLOT), (ex, F[1] + H), "sl")
             + seg((ex + 0.9, F[1] - SLIT / 2), (ex + 0.9, F[1] + SLIT / 2), "sl"))
    ann = (label(F[0], F[1] + 3, "A", "big", "middle") + label(G[0], G[1] + 3, "B", "big inv", "middle")
           + callout(ex - 6, F[1] + 4, 6, 124, "ปีก B ของชิ้นขวา ทับด้านนอกชิ้นซ้าย")
           + callout(ex + 8, F[1] - 6, 118, 8, "ปีก A สอดผ่าน slit ไปอยู่ใต้ชิ้นขวา")
           + callout(ex + 3, F[1] + H - 4, 128, 124, "ปีกนก 2 ข้างกางล็อก"))
    return f'<svg viewBox="0 0 200 132" role="img" aria-label="รอยต่อแบบเสียบปีกผ่าน slit">{art}{joint}{ann}</svg>'

# ---- step 3: flat net, base + 4 walls
def step3():
    c = 115
    s = 2 * H
    pieces = {"base": (c, c, "base", {1, 3}),
              "xr": (c + s, c, "light", {0, 2}), "xl": (c - s, c, "light", {0, 2}),
              "zt": (c, c - s, "dark", {0, 2}), "zb": (c, c + s, "dark", {0, 2})}
    seams = {("base", 0), ("base", 1), ("base", 2), ("base", 3), ("xr", 2), ("xl", 0), ("zt", 3), ("zb", 1)}
    art = assembly(pieces, seams)
    ann = (label(c, c + 3, "ฐาน", "big inv", "middle") + label(c + s, c + 3, "1", "big", "middle")
           + label(c, c - s + 3, "2", "big inv", "middle") + label(c - s, c + 3, "3", "big", "middle")
           + label(c, c + s + 3, "4", "big inv", "middle"))
    return f'<svg viewBox="0 0 230 230" role="img" aria-label="ต่อผนัง 4 ชิ้นเข้ากับฐาน">{art}{ann}</svg>'

# ---- Rev B cut files
def rev_b():
    s, S = 45 - H, 45 + H
    p = dict(code="05B", name="Circle Rev B", W=90, H=90, cut=[("arc", (45, 45), 45, 0, 360, True)],
             slits=[g.L((30, S), (60, S)), g.L((30, s), (60, s)),
                    g.L((s, S), (s, S - SLOT)), g.L((s, s), (s, s + SLOT)),
                    g.L((S, S), (S, S - SLOT)), g.L((S, s), (S, s + SLOT))])
    doc = g.new_doc(); g.dxf_add(doc.modelspace(), p)
    doc.saveas(os.path.join(HERE, "05-circle-revB-slot18.dxf"))
    g.write_svg(p, os.path.join(HERE, "05-circle-revB-slot18.svg"))

def main():
    tpl = open(os.path.join(HERE, "template.html")).read()
    js = open(os.path.join(HERE, "model05.js")).read()
    html = (tpl.replace("__STEP1__", step1()).replace("__STEP2__", step2()).replace("__STEP3__", step3())
               .replace("__MODEL_JS__", js))
    open(os.path.join(HERE, "index.html"), "w").write(html)
    rev_b()
    print("ok", len(html))

if __name__ == "__main__":
    main()
