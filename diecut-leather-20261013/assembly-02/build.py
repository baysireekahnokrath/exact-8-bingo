"""Build the pattern-02 assembly page: flat step drawings (SVG) + inline 3D model."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import generate as g

H, R, C = 27.0, 29.25, 11.25
# screen coords (y down). edge k: 0 right, 1 top, 2 left, 3 bottom
DIR = [(1, 0), (0, -1), (-1, 0), (0, 1)]
TAN = [(0, 1), (1, 0), (0, -1), (-1, 0)]          # clockwise traversal on screen
FILL = {"base": "var(--l-base)", "light": "var(--l-light)", "dark": "var(--l-dark)"}

def depth(s):
    return max(math.sqrt(R * R - s * s) - C, 0.0)

def cap(cx, cy, k, s0, s1, n=24):
    d, t = DIR[k], TAN[k]
    mx, my = cx + H * d[0], cy + H * d[1]
    pts = [(mx + s0 * t[0], my + s0 * t[1])]
    for i in range(n + 1):
        s = s0 + (s1 - s0) * i / n
        pts.append((mx + s * t[0] + depth(s) * d[0], my + s * t[1] + depth(s) * d[1]))
    pts.append((mx + s1 * t[0], my + s1 * t[1]))
    return "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " Z"

def square(cx, cy, tone, extra=""):
    return f'<rect x="{cx-H}" y="{cy-H}" width="{2*H}" height="{2*H}" fill="{FILL[tone]}" class="pc" {extra}/>'

def woven(pieces, seams):
    """pieces: {name:(cx,cy,tone)}; seams: set of (name,k) whose lobe lies on a neighbour."""
    under, over, free = [], [], []
    for name, (cx, cy, tone) in pieces.items():
        for k in range(4):
            if (name, k) in seams:
                under.append(f'<path d="{cap(cx, cy, k, -H, 0)}" class="hid"/>')
                over.append(f'<path d="{cap(cx, cy, k, 0, H)}" fill="{FILL[tone]}" class="pc"/>')
            else:
                free.append(f'<path d="{cap(cx, cy, k, -H, H)}" fill="{FILL[tone]}" class="pc"/>')
    sq = [square(cx, cy, tone) for cx, cy, tone in pieces.values()]
    return "".join(free + sq + under + over)

def label(x, y, text, cls="lb", anchor="middle"):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{text}</text>'

def callout(x1, y1, x2, y2, text, anchor="start"):
    dx = 1.2 if anchor == "start" else -1.2
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="co"/><circle cx="{x1}" cy="{y1}" r="0.9" class="cod"/>'
            + label(x2 + dx, y2 + 1.3, text, "lb", anchor))

# ---- step 1: one piece, annotated
def step1():
    p = g.P[1]
    W = p["W"]
    path = g.svg_path(p["cut"], W)
    slits = "".join(f'<line x1="{s[1][0]:.2f}" y1="{W-s[1][1]:.2f}" x2="{s[2][0]:.2f}" y2="{W-s[2][1]:.2f}" class="sl"/>' for s in p["slits"])
    fold = '<rect x="18" y="18" width="54" height="54" class="fd"/>'
    body = (f'<g transform="translate(40,12)"><path d="{path}" fill="var(--l-light)" class="pc"/>{fold}{slits}'
            + callout(30, 6, -6, -2, "กลีบ (lobe)", "end")
            + callout(30, 18, -6, 12, "slot 29.25", "end")
            + callout(72, 50, 104, 46, "แนวพับ / แนวต่อ")
            + callout(45, 45, 104, 62, "ตัวชิ้น 54 × 54")
            + "</g>")
    badge = '<g transform="translate(165,92)"><rect x="-17" y="-9" width="34" height="14" class="bd"/>' + label(0, 1.2, "× 5 ชิ้น", "lbb") + "</g>"
    return f'<svg viewBox="0 0 190 112" role="img" aria-label="ชิ้น 02 พร้อมชื่อส่วนต่าง ๆ">{body}{badge}</svg>'

# ---- step 2: one seam, detail
def step2():
    A, B = (60, 62), (114, 62)
    pieces = {"A": (*A, "light"), "B": (*B, "dark")}
    seams = {("A", 0), ("B", 2)}
    art = woven(pieces, seams)
    ann = (label(A[0], A[1] + 2, "A", "big") + label(B[0], B[1] + 2, "B", "big inv")
           + callout(90, 76, 8, 124, "ครึ่งล่าง: กลีบ A ทับบน B")
           + callout(84, 48, 8, 8, "ครึ่งบน: กลีบ B ทับบน A")
           + callout(87, 62, 140, 8, "จุดไขว้ตรงกลาง"))
    return f'<svg viewBox="0 0 190 130" role="img" aria-label="รอยต่อระหว่างชิ้น A กับ B">{art}{ann}</svg>'

# ---- step 3: flat net, 4 walls woven to the base
def step3():
    cx, cy = 95, 95
    pieces = {"base": (cx, cy, "base"), "w1": (cx + 54, cy, "light"), "w2": (cx, cy - 54, "dark"),
              "w3": (cx - 54, cy, "light"), "w4": (cx, cy + 54, "dark")}
    seams = {("base", 0), ("base", 1), ("base", 2), ("base", 3),
             ("w1", 2), ("w2", 3), ("w3", 0), ("w4", 1)}
    art = woven(pieces, seams)
    ann = (label(cx, cy + 2, "ฐาน", "big inv") + label(cx + 54, cy + 2, "1", "big") + label(cx, cy - 52, "2", "big inv")
           + label(cx - 54, cy + 2, "3", "big") + label(cx, cy + 56, "4", "big inv"))
    return f'<svg viewBox="-6 -6 202 202" role="img" aria-label="วางผนัง 4 ชิ้นรอบฐานแล้วต่อเข้ากับฐาน">{art}{ann}</svg>'

def main():
    tpl = open(os.path.join(HERE, "template.html")).read()
    js = open(os.path.join(HERE, "model.js")).read()
    html = (tpl.replace("__STEP1__", step1()).replace("__STEP2__", step2()).replace("__STEP3__", step3())
               .replace("__MODEL_JS__", js))
    open(os.path.join(HERE, "index.html"), "w").write(html)
    print("ok", len(html))

if __name__ == "__main__":
    main()
