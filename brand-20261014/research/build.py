"""Front views of the three crossbody bag concepts, drawn from the real die outlines.

Each piece gets a different leather shade, because every bag is made of different scraps.
python3 research/build.py -> research/svg/bag-<key>.svg
"""
import importlib.util, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, "logo"))

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

L = load("logo_build", os.path.join(ROOT, "logo", "build.py"))
BBD = load("bible_build", os.path.join(ROOT, "bible", "build.py"))
import research as R
OUT = os.path.join(HERE, "svg"); os.makedirs(OUT, exist_ok=True)
SHADES = ["#B8743A", "#8A5A33", "#C98B4E", "#6E4A2F", "#A3683A", "#D29A5F", "#7B4B2A"]
INK, MUTE, PAPER = "#1C1B22", "#4A4A55", "#FFF6EC"   # palette #2; leather shades stay, they are the material

def grid(x0, y0, cols, rows, code, m, seed):
    g = []
    for r in range(rows):
        for c in range(cols):
            fill = SHADES[(seed + r * 3 + c * 5) % len(SHADES)]
            g.append(BBD.place(code, x0 + m * c + m / 2, y0 + m * r + m / 2, m * 1.08, fill, PAPER))
    return "".join(g)

def strap(x1, y1, x2, top):
    """Five heart straps hanging in an arc: drawn as a curve with five hearts on it."""
    cx = (x1 + x2) / 2
    g = [f'<path d="M{x1},{y1} C{x1},{top} {x2},{top} {x2},{y1}" fill="none" stroke="#8A5A33" stroke-width="10" stroke-linecap="round"/>']
    for i in range(5):
        t = (i + 1) / 6
        # cubic bezier point
        px = (1 - t) ** 3 * x1 + 3 * (1 - t) ** 2 * t * x1 + 3 * (1 - t) * t ** 2 * x2 + t ** 3 * x2
        py = (1 - t) ** 3 * y1 + 3 * (1 - t) ** 2 * t * top + 3 * (1 - t) * t ** 2 * top + t ** 3 * y1
        g.append(f'<path d="{L.heart(px, py, 22)}" fill="#FF5A36"/>')
    for x in (x1, x2):
        g.append(f'<rect x="{x-7}" y="{y1-16}" width="14" height="22" rx="4" fill="#9A9A9A"/>')
    return "".join(g)

def label(t, x, y, size=22, fill=MUTE, anchor="middle"):
    return L.text(t, size, x, y, fill, "alt/Anuphan-Medium.ttf", anchor=anchor)[0]

def draw(b):
    W, H = 560, 600
    code, m = b["code"], 62
    g = [f'<rect width="{W}" height="{H}" rx="20" fill="#FFFFFF"/>']
    key = b["key"]
    if key == "box":
        cols, rows = 3, 2
        x0 = (W - cols * m) / 2; y0 = 300
        g.append(strap(x0 + 8, y0 - m * .55, x0 + cols * m - 8, 30))
        g.append(f'<rect x="{x0 + cols * m}" y="{y0 - 8}" width="{m * .45}" height="{rows * m + 8}" fill="#5A3A24"/>')
        g.append(grid(x0, y0, cols, rows, code, m, 1))
        g.append(grid(x0, y0 - m * .62, cols, 1, code, m, 4))       # lid folded over the top
        g.append(f'<circle cx="{W/2}" cy="{y0 + m*.3}" r="9" fill="#C9A45C"/>')
    elif key == "phone":
        cols, rows = 2, 3
        x0 = (W - cols * m) / 2; y0 = 240
        g.append(strap(x0 + 8, y0 + 4, x0 + cols * m - 8, 20))
        g.append(grid(x0, y0, cols, rows, code, m, 2))
        g.append(f'<rect x="{x0+18}" y="{y0-34}" width="{cols*m-36}" height="40" rx="8" fill="#2B2B33"/>')   # phone peeking out
    else:
        cols, rows = 2, 2
        x0 = (W - cols * m) / 2 - 20; y0 = 300
        g.append(strap(x0 + 8, y0 - m * .3, x0 + cols * m + 40, 40))
        g.append(f'<path d="M{x0+cols*m},{y0} l40,-30 v{rows*m} l-40,30 z" fill="#5A3A24"/>')
        g.append(f'<path d="M{x0},{y0} l40,-30 h{cols*m} l-40,30 z" fill="#6E4A2F"/>')
        g.append(grid(x0, y0, cols, rows, code, m, 3))
        bh = 70; bw = bh * L.BW / L.BH
        g.append(L.bear(x0 + cols * m + 30, y0 + rows * m - 10, bh, "#B8743A", "#FF5A36", INK))
    g.append(label(f"{b['name']} · {b['size']}", W / 2, H - 70, 26, INK))
    g.append(label(f"แบบ {code} × {b['pieces']} ชิ้น · รอยต่อ {b['joints']} จุด · สายหัวใจ 5 เส้น", W / 2, H - 32, 20))
    return L.svg(W, H, "".join(g), None, f"กระเป๋า {b['name']}")

if __name__ == "__main__":
    rows = R.bag_rows()
    for b in rows:
        open(os.path.join(OUT, f"bag-{b['key']}.svg"), "w").write(draw(b))
    print(len(rows), "bags in", OUT)
