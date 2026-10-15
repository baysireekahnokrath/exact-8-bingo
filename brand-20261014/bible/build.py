"""Brand bible drawings as outlined SVG: positioning map, brand pattern, hang tags, story card, bag,
birthday-edition card and booth plan. Reuses the logo helpers so every mark is the real one.

Golden sizes, drawn at 8 px per mm: tag 55 x 89, card 89 x 55, edition card 89 x 89, bag 130 x 210 x 80.
Inside each piece: margin = width / phi^4, chamfer = width / phi^3, the main line sits on the golden line (height / phi).
Palette #2: paper, ink, cobalt, tomato; sun, mint and pink for FIVE BEARS and the birthday brands.

python3 bible/build.py -> bible/svg/*.svg
"""
import importlib.util, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "logo"))
from brand import C, PRODUCTS, FAMILY
import bible as BB

spec = importlib.util.spec_from_file_location("logo_build", os.path.join(ROOT, "logo", "build.py"))
L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
text, wordmark, bear, svg, BW, BH = L.text, L.wordmark, L.bear, L.svg, L.BW, L.BH
word, tag, fit, by_line, PHI = L.word, L.tag, L._fit, L.by_line, L.PHI
JOST, TH, PLEX = "alt/Jost-Medium.ttf", "alt/Anuphan-Medium.ttf", "IBMPlexSansThai-Regular.ttf"
OUT = os.path.join(HERE, "svg"); os.makedirs(OUT, exist_ok=True)

PAT = os.path.join(os.path.dirname(ROOT), "diecut-leather-20261014", "svg")
SRC = {"02": "02-pinwheel-4-lobe.svg", "03": "03-capsule-cross.svg", "04": "04-rounded-square-diagonal.svg",
       "05": "05-circle.svg", "06": "06-soft-cross.svg"}

def piece(code):
    """(viewBox, cut path markup, slit markup) of a real die outline."""
    s = open(os.path.join(PAT, SRC[code])).read()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    cut = re.search(r'<g id="CUT"[^>]*>(.*?)</g>', s, re.S).group(1)
    sl = re.search(r'<g id="SLIT"[^>]*>(.*?)</g>', s, re.S).group(1)
    return [float(v) for v in vb.split()], cut, sl

def place(code, x, y, size, fill, slit, rot=0):
    (vx, vy, vw, vh), cut, sl = piece(code)
    s = size / max(vw, vh)
    cx, cy = vx + vw / 2, vy + vh / 2
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({rot}) scale({s:.4f}) translate({-cx:.2f},{-cy:.2f})">'
            f'<g fill="{fill}" fill-rule="evenodd" stroke="none">{cut}</g>'
            f'<g fill="none" stroke="{slit}" stroke-width="{max(vw, vh) * .025:.2f}" stroke-linecap="round">{sl}</g></g>')

INK, PAPER, COB, TOM, PINK, SUN = C["ink"], C["paper"], C["cobalt"], C["tomato"], C["pink"], C["sun"]
MUTE, LINE, SOFT = "#4A4A55", "#F1DCCB", "#A9A5B4"
MITR, MITRB = "Mitr-Medium.ttf", "Mitr-SemiBold.ttf"
K = 8                                            # px per mm
_n = [0]
def _u(p):
    _n[0] += 1; return f"bb{p}{_n[0]}"

def at(x, y, g):
    return f'<g transform="translate({x:.2f},{y:.2f})">{g}</g>'

def word_w(t, width, fg, dot):
    """Geometric brand name scaled to a given width. Returns (group at 0,0 baseline, cap)."""
    _, w100 = word(t, 100, fg, dot, _u("m"))
    cap = 100 * width / w100
    return word(t, cap, fg, dot, _u("w"))[0], cap

def line_fit(t, size, x, y, max_w, fill, font, anchor="middle", tracking=0.0):
    while L.text_path(t, size, font, tracking)[1] > max_w: size -= 1
    return text(t, size, x, y, fill, font, tracking=tracking, anchor=anchor)[0]

def pattern(W=987, H=610, step=144, size=89):
    """Tissue-paper pattern, 987 x 610 (phi : 1): the five SOI. 02 pieces on a Fibonacci grid, one colour per family member."""
    codes = list(SRC); cols = [C[k] for _, k, _ in FAMILY]; out = []
    for j, y in enumerate(range(-step // 2, H + step, step)):
        for i, x in enumerate(range(-step // 2 + (step // 2 if j % 2 else 0), W + step, step)):
            k = codes[(i + j * 2) % len(codes)]
            out.append(place(k, x, y, size, cols[(i + j * 3) % len(cols)], PAPER, rot=(i * 17 + j * 29) % 90))
    return svg(W, H, "".join(out), PAPER, "ลายกระดาษห่อ OCT. 26")

def posmap(W=720, H=560):
    """Qualitative positioning map; axes are labelled as opinion, not survey data."""
    x0, y0, x1, y1 = 120, 40, W - 40, H - 100
    g = [f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="#FFFFFF" stroke="{LINE}" stroke-width="2"/>',
         f'<line x1="{(x0+x1)/2}" y1="{y0}" x2="{(x0+x1)/2}" y2="{y1}" stroke="{LINE}" stroke-width="2" stroke-dasharray="6 6"/>',
         f'<line x1="{x0}" y1="{(y0+y1)/2}" x2="{x1}" y2="{(y0+y1)/2}" stroke="{LINE}" stroke-width="2" stroke-dasharray="6 6"/>']
    for t, x, y, a in (("ซื้อสำเร็จ", x0, y1 + 40, "start"), ("ต่อเองได้", x1, y1 + 40, "end")):
        d, w, b = L.text_path(t, 24, TH)
        xx = x - (b[2] if a == "end" else 0)
        g.append(f'<path transform="translate({xx:.1f},{y})" d="{d}" fill="{MUTE}"/>')
    for t, y in (("มีเรื่องเล่า", y0 + 26), ("หนังแท้", y0 + 56), ("ของทั่วไป", y1 - 8)):
        d, w, b = L.text_path(t, 22, TH)
        g.append(f'<path transform="translate({x0 - 12 - b[2]:.1f},{y})" d="{d}" fill="{MUTE}"/>')
    for name, px, py in BB.MAP:
        cx, cy = x0 + px * (x1 - x0), y1 - py * (y1 - y0)
        me = name == "OCT. 26"
        g.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{16 if me else 10}" fill="{TOM if me else SOFT}"/>')
        if me:
            wm, tw = word("OCT. 26", 18, INK, TOM, _u("map"))
            tx = cx - tw - 24 if px > .6 else cx + 24
            g.append(at(tx, cy + 9, wm))
        else:
            d, w, b = L.text_path(name, 22, TH)
            tx = cx - b[2] - 24 if px > .6 else cx + 20
            g.append(f'<path transform="translate({tx:.1f},{cy + 8:.1f})" d="{d}" fill="{MUTE}"/>')
    d, w, b = L.text_path("แผนที่จากความเห็นของเรา ยังไม่ใช่ผลสำรวจลูกค้า", 18, PLEX)
    g.append(f'<path transform="translate({x0},{H - 18})" d="{d}" fill="{MUTE}"/>')
    return svg(W, H, "".join(g), None, "แผนที่ตำแหน่งแบรนด์ OCT. 26")

# ---------------------------------------------------------------- hang tag, 55 x 89 mm (1 : phi)
TW, TH_ = 55 * K, 89 * K
CH, M = TW / PHI ** 3, TW / PHI ** 4             # chamfer 13 mm, margin 8 mm
GL = TH_ / PHI                                   # golden line, 55 mm from the top
HOLE_R = 2.5 * K                                 # 5 mm hole

def tag_shape(x, y, fill, stroke=None):
    st = f' stroke="{stroke}" stroke-width="2"' if stroke else ""
    return (f'<path d="M{x+CH:.1f},{y} H{x+TW-CH:.1f} L{x+TW},{y+CH:.1f} V{y+TH_} H{x} V{y+CH:.1f} Z" fill="{fill}"{st}/>'
            f'<circle cx="{x+TW/2}" cy="{y+CH:.1f}" r="{HOLE_R}" fill="#FFFFFF"/>')

def tag_back(x, y, name, name_font, price, code, lines):
    """Paper side: name on the phi^2 line, price, code; story lines from the golden line down; handle at the foot."""
    cx, mw = x + TW / 2, TW - 2 * M
    g = [tag_shape(x, y, PAPER, LINE)]
    g.append(line_fit(name, 34, cx, y + TH_ / PHI ** 2, mw, INK, name_font))
    g.append(text(f"{price} บาท", 42, cx, y + TH_ / PHI ** 2 + 55, TOM, TH, anchor="middle")[0])
    g.append(text(code, 20, cx, y + TH_ / PHI ** 2 + 89, MUTE, JOST, tracking=.1, anchor="middle")[0])
    g.append(f'<line x1="{x+M:.1f}" y1="{y+GL-34:.1f}" x2="{x+TW-M:.1f}" y2="{y+GL-34:.1f}" stroke="{LINE}" stroke-width="2"/>')
    for i, t in enumerate(lines):
        g.append(line_fit(t, 21, cx, y + GL + i * 34, mw, INK, PLEX))
    g.append(text("@oct26.crafted", 21, cx, y + TH_ - M, COB, JOST, anchor="middle")[0])
    return "".join(g)

def tag_soi2(p):
    """Front: ink tag, SOI. 02 on the golden line. Back: product and care."""
    W, H = 3 * 34 + 2 * TW, 2 * 34 + TH_
    x, y = 34, 34
    wm, cap = word_w("SOI. 02", TW - 2 * M, PAPER, TOM)
    d1, b1 = L.justify("FROM OUR ROOT", L.size_for("FROM OUR ROOT", JOST, cap / PHI ** 2, 1), JOST, TW - 2 * M)
    bl, blw = by_line(0, 0, TW / PHI ** 7, PAPER, TOM)
    g = [tag_shape(x, y, INK), at(x + M, y + GL, wm), L.put(d1, b1, x + M, y + GL + cap / PHI ** 3, PAPER),
         at(x + (TW - blw) / 2, y + TH_ - M, bl)]
    g.append(tag_back(x + TW + 34, y, p["name"], TH, p["price"], BB.product_code(p),
                      ["เศษหนังวัวแท้ ทุกชิ้นสีไม่ซ้ำ", "ชิ้นนี้ต่อด้วยปีกและร่อง", "ไม่ใช้กาว", "เช็ดด้วยผ้าแห้ง เลี่ยงน้ำ"]))
    return svg(W, H, "".join(g), None, "ป้ายห้อย SOI. 02 55 × 89 มม. หน้าและหลัง")

def tag_love(p):
    """Front: pink tag, sun bear above the golden line, Love on it. Back: product and story."""
    W, H = 3 * 34 + 2 * TW, 2 * 34 + TH_
    x, y = 34, 34
    size = 150
    while L.text_path("Love", size, MITRB)[1] > TW - 2 * M: size -= 2
    cap = size * .72
    bh = TW / PHI ** 2; bw = bh * BW / BH
    g = [tag_shape(x, y, PINK), bear(x + (TW - bw) / 2, y + GL - cap - 21 - bh, bh, SUN, TOM, INK),
         text("Love", size, x + TW / 2, y + GL, INK, MITRB, anchor="middle")[0],
         line_fit("ห้าหมี FIVE BEARS", 26, x + TW / 2, y + GL + 55, TW - 2 * M, INK, MITR)]
    bl, blw = by_line(0, 0, TW / PHI ** 7, INK, TOM)
    g.append(at(x + (TW - blw) / 2, y + TH_ - M, bl))
    g.append(tag_back(x + TW + 34, y, p["name"], MITR, p["price"], BB.product_code(p),
                      ["หัวใจอยู่ตรงกลางเสมอ", "หมีตัวนี้ตัดจากเศษหนังแท้", "ต่อกันด้วยรัก", "ประกอบโดยลูก ๆ บ้านห้าหมี"]))
    return svg(W, H, "".join(g), None, "ป้ายห้อย Love 55 × 89 มม. หน้าและหลัง")

# ---------------------------------------------------------------- story card, 89 x 55 mm (phi : 1)
def card():
    """Front: the name alone, phi of the card's width, baseline on the golden line. Back tells why 26."""
    w, h = 89 * K, 55 * K; m = h / PHI ** 4
    W, H = w + 68, 2 * h + 3 * 34
    x, y1, y2 = 34, 34, 34 + h + 34
    wm, cap = word_w("OCT. 26", w / PHI, INK, TOM)
    td, tb = L.tagline(w / PHI)
    g = [f'<rect x="{x}" y="{y1}" width="{w}" height="{h}" fill="{PAPER}" stroke="{LINE}" stroke-width="2"/>',
         at(x + (w - w / PHI) / 2, y1 + h / PHI, wm), L.put(td, tb, x + (w - (tb[2] - tb[0])) / 2, y1 + h / PHI + cap / PHI, COB)]
    # back
    g.append(f'<rect x="{x}" y="{y2}" width="{w}" height="{h}" fill="{PAPER}" stroke="{LINE}" stroke-width="2"/>')
    g.append(text("ทำไมชื่อ OCT. 26", 34, x + m, y2 + m + 26, INK, TH)[0])
    lines = ["OCT. ย่อจาก our crafted things และคือเดือนตุลาคม",
             "26 คือวันเกิดของแม่ แบรนด์เกิดวันเดียวกัน",
             "เศษหนังแท้ที่เกือบถูกขายไปเป็นกระสอบ",
             "ทั้งห้าคนในบ้านช่วยกันทำ แพ็ค และขาย"]
    q = 144
    for i, t in enumerate(lines):
        g.append(line_fit(t, 21, x + m, y2 + m + 26 + 55 + i * 34, w - 2 * m, INK, PLEX, anchor="start"))
    g.append(f'<rect x="{x + w - m - q:.1f}" y="{y2 + h - m - q:.1f}" width="{q}" height="{q}" rx="8" fill="#FFFFFF" stroke="{COB}" stroke-width="2" stroke-dasharray="6 5"/>')
    g.append(text("QR IG", 21, x + w - m - q / 2, y2 + h - m - q / 2 + 8, COB, JOST, anchor="middle")[0])
    g.append(text("@oct26.crafted", 21, x + m, y2 + h - m, TOM, JOST)[0])
    return svg(W, H, "".join(g), None, "การ์ดเล่าเรื่อง 89 × 55 มม. หน้าและหลัง")

# ---------------------------------------------------------------- bag, 130 x 210 x 80 mm
def bag():
    """Matte cobalt paper bag, cotton rope. Front 130 x 210 is 1 : phi, gusset 80 = 130 / phi. No kraft."""
    k = 3; pw, ph, gw = 130 * k, 210 * k, 80 * k
    x0, y0 = 60, 160
    W, H = x0 + pw + gw // 2 + 40, y0 + ph + 40
    side = "#1A35A3"
    hx = [x0 + pw / PHI ** 3, x0 + pw - pw / PHI ** 3]
    g = [f'<path d="M{hx[0]:.1f},{y0+24} C{hx[0]:.1f},{y0-150} {hx[1]:.1f},{y0-150} {hx[1]:.1f},{y0+24}" fill="none" stroke="#D9C9B6" stroke-width="10" stroke-linecap="round"/>',
         f'<rect x="{x0}" y="{y0}" width="{pw}" height="{ph}" fill="{COB}"/>',
         f'<path d="M{x0+pw},{y0} L{x0+pw+gw/2},{y0+21} L{x0+pw+gw/2},{y0+ph-13} L{x0+pw},{y0+ph} Z" fill="{side}"/>',
         f'<rect x="{x0}" y="{y0}" width="{pw}" height="34" fill="#00000026"/>',
         "".join(f'<circle cx="{x:.1f}" cy="{y0+24}" r="6" fill="{PAPER}"/>' for x in hx)]
    wm, cap = word_w("OCT. 26", pw / PHI, PAPER, TOM)
    td, tb = L.tagline(pw / PHI)
    base = y0 + ph / PHI ** 2
    g += [at(x0 + (pw - pw / PHI) / 2, base, wm), L.put(td, tb, x0 + (pw - (tb[2] - tb[0])) / 2, base + cap / PHI, PAPER)]
    return svg(W, H, "".join(g), None, "ถุงกระดาษด้านสีน้ำเงินโคบอลต์ 130 × 210 × 80 มม.")

# ---------------------------------------------------------------- birthday-edition card, 89 x 89 mm
def edition():
    s = 89 * K; m = s / PHI ** 5
    W = s + 68; x = y = 34
    wm, cap = word_w("OCT. 26", s / PHI ** 2, INK, TOM)
    no, ncap = word_w("NO. 42", s / PHI, INK, TOM)
    g = [f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{PAPER}" stroke="{LINE}" stroke-width="2"/>',
         f'<rect x="{x+m:.1f}" y="{y+m:.1f}" width="{s-2*m:.1f}" height="{s-2*m:.1f}" fill="none" stroke="{INK}" stroke-width="3"/>',
         at(x + (s - s / PHI ** 2) / 2, y + s / PHI ** 3, wm),
         at(x + (s - s / PHI) / 2, y + s / PHI, no),
         text("รุ่นวันเกิด · 26 ต.ค. 2569", 26, x + s / 2, y + s / PHI + 55, MUTE, TH, anchor="middle")[0],
         text("07 / 42", 55, x + s / 2, y + s / PHI + 55 + 76, TOM, JOST, anchor="middle")[0],
         text("เลขรุ่นคืออายุของแม่ เลขชิ้นเขียนด้วยมือ ไม่ทำซ้ำ", 20, x + s / 2, y + s - m - 34, MUTE, PLEX, anchor="middle")[0]]
    return svg(W, W, "".join(g), None, "การ์ดรุ่นวันเกิด OCT. 26 – No. 42 ขนาด 89 × 89 มม.")

def booth():
    """Top-down plan of a 2 m x 2 m booth: two tables, demo spot, workshop box, cash point."""
    W, H = 760, 700
    g = [f'<rect x="60" y="40" width="640" height="560" fill="#FFFFFF" stroke="{LINE}" stroke-width="3"/>',
         f'<rect x="60" y="40" width="640" height="40" fill="{INK}"/>']
    g.append(text("แบ็คดรอป OCT. 26 + ป้าย SOI. 02", 22, 380, 68, PAPER, TH, anchor="middle")[0])
    g.append(f'<rect x="90" y="380" width="285" height="120" rx="8" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>'
             f'<rect x="385" y="380" width="285" height="120" rx="8" fill="#FFE3F1" stroke="{PINK}" stroke-width="3"/>')
    wm, ww = word("SOI. 02", 20, INK, TOM, _u("bt"))
    t, tw, _ = text("โต๊ะ ", 26, 0, 0, INK, TH)
    x0 = 232 - (tw + 8 + ww) / 2
    g.append(at(x0, 435, t) + at(x0 + tw + 8, 435, wm))
    g.append(text("ของใช้ทุกวัน 23 แบบ", 20, 232, 470, MUTE, PLEX, anchor="middle")[0])
    g.append(text("โต๊ะห้าหมี Love", 28, 527, 435, INK, MITR, anchor="middle")[0])
    g.append(text("ราวหมีห้าตัวแขวนหน้าโต๊ะ", 20, 527, 470, MUTE, PLEX, anchor="middle")[0])
    spots = [(380, 545, "จุดสาธิต ลองดึง", TOM), (185, 250, "กล่องลองต่อ เด็ก ๆ", C["mint"]),
             (600, 250, "รับเงิน QR", SUN), (380, 200, "ที่ยืนพ่อหรือแม่", COB)]
    for x, y, t, c in spots:
        g.append(f'<circle cx="{x}" cy="{y}" r="21" fill="{c}"/>')
        g.append(text(t, 22, x, y + 52, INK, TH, anchor="middle")[0])
    g.append(f'<path d="M380,660 L380,612" stroke="{MUTE}" stroke-width="3" marker-end="url(#a)"/>')
    g.append(text("ทางเดิน ลูกค้าเดินเข้าจากด้านนี้", 22, 380, 692, MUTE, TH, anchor="middle")[0])
    g.insert(0, f'<defs><marker id="a" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
                f'<path d="M0,0 L10,5 L0,10 z" fill="{MUTE}"/></marker></defs>')
    return svg(W, H, "".join(g), None, "ผังบูธ OCT. 26")

SAMPLE_SOI = next(p for p in PRODUCTS if p["n"] == 18)
SAMPLE_LOVE = next(p for p in PRODUCTS if p["n"] == 23)
FILES = {
    "map.svg": posmap(),
    "pattern.svg": pattern(),
    "tag-soi2.svg": tag_soi2(SAMPLE_SOI),
    "tag-love.svg": tag_love(SAMPLE_LOVE),
    "card.svg": card(),
    "bag.svg": bag(),
    "edition.svg": edition(),
    "booth.svg": booth(),
}

if __name__ == "__main__":
    for name, s in FILES.items():
        open(os.path.join(OUT, name), "w").write(s)
    print(len(FILES), "files in", OUT)
