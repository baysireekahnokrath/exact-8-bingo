"""Brand bible drawings as outlined SVG: positioning map, brand pattern, hang tags, story card, bag,
birthday-edition card and booth plan. Reuses the logo helpers so every mark is the real one.

python3 bible/build.py -> bible/svg/*.svg
"""
import importlib.util, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "logo"))
from brand import C, PRODUCTS
import bible as BB

spec = importlib.util.spec_from_file_location("logo_build", os.path.join(ROOT, "logo", "build.py"))
L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
text, wordmark, bear, svg, BW, BH = L.text, L.wordmark, L.bear, L.svg, L.BW, L.BH
SYNE, TH, PLEX = "alt/Syne-Bold.ttf", "alt/Anuphan-Medium.ttf", "IBMPlexSansThai-Regular.ttf"
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

def pattern(W=900, H=600, bg=None, fill=None, slit=None, step=150, size=104):
    """Tissue-paper pattern: the five SOI. 02 pieces on a tilted grid."""
    bg, fill, slit = bg or C["oct_cream"], fill or "#E6CDAE", slit or C["oct_cream"]
    codes = list(SRC); out = []
    for j, y in enumerate(range(-step // 2, H + step, step)):
        for i, x in enumerate(range(-step // 2 + (step // 2 if j % 2 else 0), W + step, step)):
            k = codes[(i + j * 2) % len(codes)]
            out.append(place(k, x, y, size, fill, slit, rot=(i * 17 + j * 29) % 90))
    return svg(W, H, "".join(out), bg, "ลายกระดาษห่อ OCT. 26")

def posmap(W=720, H=560):
    """Qualitative positioning map; axes are labelled as opinion, not survey data."""
    x0, y0, x1, y1 = 120, 40, W - 40, H - 100
    ink, mute, line = C["chestnut"], "#8C735E", "#D8C2A6"
    g = [f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="#FFFBF5" stroke="{line}" stroke-width="2"/>',
         f'<line x1="{(x0+x1)/2}" y1="{y0}" x2="{(x0+x1)/2}" y2="{y1}" stroke="{line}" stroke-width="2" stroke-dasharray="6 6"/>',
         f'<line x1="{x0}" y1="{(y0+y1)/2}" x2="{x1}" y2="{(y0+y1)/2}" stroke="{line}" stroke-width="2" stroke-dasharray="6 6"/>']
    for t, x, y, a in (("ซื้อสำเร็จ", x0, y1 + 40, "start"), ("ต่อเองได้", x1, y1 + 40, "end")):
        d, w, b = L.text_path(t, 24, TH)
        xx = x - (b[2] if a == "end" else 0)
        g.append(f'<path transform="translate({xx:.1f},{y})" d="{d}" fill="{mute}"/>')
    for t, y in (("มีเรื่องเล่า", y0 + 26), ("หนังแท้", y0 + 56), ("ของทั่วไป", y1 - 8)):
        d, w, b = L.text_path(t, 22, TH)
        g.append(f'<path transform="translate({x0 - 12 - b[2]:.1f},{y})" d="{d}" fill="{mute}"/>')
    for name, px, py in BB.MAP:
        cx, cy = x0 + px * (x1 - x0), y1 - py * (y1 - y0)
        me = name == "OCT. 26"
        r = 16 if me else 10
        g.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{C["brick"] if me else "#BFA588"}"/>')
        d, w, b = L.text_path(name, 26 if me else 22, SYNE if me else TH)
        tx = cx - b[2] - 24 if px > .6 else cx + 20
        g.append(f'<path transform="translate({tx:.1f},{cy + 8:.1f})" d="{d}" fill="{ink if me else mute}"/>')
    d, w, b = L.text_path("แผนที่จากความเห็นของเรา ยังไม่ใช่ผลสำรวจลูกค้า", 18, PLEX)
    g.append(f'<path transform="translate({x0},{H - 18})" d="{d}" fill="{mute}"/>')
    return svg(W, H, "".join(g), None, "แผนที่ตำแหน่งแบรนด์ OCT. 26")

def hole(cx, cy, bg):
    return f'<circle cx="{cx}" cy="{cy}" r="14" fill="{bg}"/><circle cx="{cx}" cy="{cy}" r="14" fill="none" stroke="#00000022" stroke-width="2"/>'

def tag_shape(x, y, w, h, fill):
    c = 36
    return (f'<path d="M{x+c},{y} H{x+w-c} L{x+w},{y+c} V{y+h} H{x} V{y+c} Z" fill="{fill}" stroke="#00000018" stroke-width="2"/>')

def tag_soi2(p):
    """5 x 9 cm hang tag, front and back, at 60 px per cm."""
    W, H, w, h = 760, 600, 300, 540
    paper, ink = "#F6EEE3", C["chestnut"]          # cream cotton paper, no kraft
    g = [tag_shape(40, 30, w, h, paper), hole(190, 80, "#FFFFFF"), tag_shape(420, 30, w, h, ink), hole(570, 80, "#FFFFFF")]
    # front: mini soi sign, product name, code
    g.append(f'<rect x="75" y="140" width="230" height="138" rx="12" fill="{ink}"/>')
    wm, _, _ = wordmark(190, 214, 50, C["oct_cream"], C["brick"], anchor="middle", left="SOI", right="02"); g.append(wm)
    g.append(text("FROM OUR ROOT", 13, 190, 250, C["oct_cream"], SYNE, tracking=.3, anchor="middle")[0])
    size = 30
    while L.text_path(p["name"], size, TH)[1] > 250: size -= 1
    g.append(text(p["name"], size, 190, 352, ink, TH, anchor="middle")[0])
    g.append(text(f"{p['price']} บาท", 34, 190, 400, ink, TH, anchor="middle")[0])
    g.append(text(BB.product_code(p), 22, 190, 445, "#6E5440", SYNE, tracking=.1, anchor="middle")[0])
    wm, _, _ = wordmark(190, 520, 34, ink, C["brick"], anchor="middle"); g.append(wm)
    # back
    lt = C["oct_cream"]
    g.append(text("From our root", 28, 570, 170, lt, SYNE, anchor="middle")[0])
    for i, t in enumerate(["เศษหนังวัวแท้ ทุกชิ้นสีไม่ซ้ำ", "ชิ้นนี้ต่อด้วยปีกและร่อง", "ไม่ใช้กาว", "เช็ดด้วยผ้าแห้ง เลี่ยงน้ำ"]):
        g.append(text(t, 22, 570, 240 + i * 40, lt, PLEX, anchor="middle")[0])
    g.append(text("ทำกันเองทั้งบ้าน ในซอย 2", 22, 570, 430, C["brick"], TH, anchor="middle")[0])
    g.append(text("@oct26.crafted", 22, 570, 510, lt, SYNE, anchor="middle")[0])
    return svg(W, H, "".join(g), None, "ป้ายห้อย SOI. 02 หน้าและหลัง")

def tag_love(p):
    W, H, w, h = 760, 600, 300, 540
    paper, ink = C["cream"], C["cocoa"]
    g = [tag_shape(40, 30, w, h, paper), hole(190, 80, "#FFFBF5"), tag_shape(420, 30, w, h, C["heart"]), hole(570, 80, "#FFFBF5")]
    bh = 150; bw = bh * BW / BH
    g.append(bear(190 - bw / 2, 125, bh, C["caramel"], C["heart"], ink))
    g.append(text("Love", 58, 190, 345, C["heart"], "Mitr-SemiBold.ttf", anchor="middle")[0])
    size = 26
    while L.text_path(p["name"], size, "Mitr-Medium.ttf")[1] > 250: size -= 1
    g.append(text(p["name"], size, 190, 395, ink, "Mitr-Medium.ttf", anchor="middle")[0])
    g.append(text(f"{p['price']} บาท", 32, 190, 440, ink, "Mitr-SemiBold.ttf", anchor="middle")[0])
    g.append(text("ห้าหมี FIVE BEARS", 22, 190, 495, ink, "Mitr-Medium.ttf", anchor="middle")[0])
    g.append(text("by OCT. 26", 18, 190, 525, C["caramel"], SYNE, tracking=.06, anchor="middle")[0])
    g.append(text("หัวใจอยู่ตรงกลางเสมอ", 26, 570, 190, "#FFFFFF", "Mitr-Medium.ttf", anchor="middle")[0])
    for i, t in enumerate(["หมีตัวนี้ตัดจากเศษหนังแท้", "ต่อกันด้วยรัก", "ประกอบโดยลูก ๆ บ้านห้าหมี"]):
        g.append(text(t, 21, 570, 260 + i * 40, "#FFFFFF", PLEX, anchor="middle")[0])
    g.append(text(BB.product_code(p), 22, 570, 440, "#FFFFFF", SYNE, tracking=.1, anchor="middle")[0])
    g.append(text("@oct26.crafted", 22, 570, 510, "#FFFFFF", SYNE, anchor="middle")[0])
    return svg(W, H, "".join(g), None, "ป้ายห้อย Love หน้าและหลัง")

def card():
    """9 x 5.5 cm story card, front over back, 80 px per cm."""
    W, H, w, h = 760, 960, 720, 440
    g = [f'<rect x="20" y="20" width="{w}" height="{h}" rx="16" fill="{C["chestnut"]}"/>',
         f'<rect x="20" y="500" width="{w}" height="{h}" rx="16" fill="{C["oct_cream"]}" stroke="#00000018" stroke-width="2"/>']
    wm, _, _ = wordmark(380, 200, 110, C["oct_cream"], C["brick"], anchor="middle"); g.append(wm)
    g.append(text("our crafted things.", 34, 380, 300, C["oct_cream"], SYNE, anchor="middle")[0])
    g.append(text("ของที่เราทำกันเอง", 28, 380, 350, "#E9D5BF", TH, anchor="middle")[0])
    g.append(text("ทำไมชื่อ OCT. 26", 34, 70, 580, C["chestnut"], TH)[0])
    lines = ["OCT. ย่อจาก our crafted things และคือเดือนตุลาคม",
             "26 คือวันเกิดของแม่ แบรนด์เกิดวันเดียวกัน",
             "เศษหนังแท้ที่เกือบถูกขายไปเป็นกระสอบ",
             "ทั้งห้าคนในบ้านช่วยกันทำ แพ็ค และขาย"]
    for i, t in enumerate(lines):
        g.append(text(t, 22, 70, 640 + i * 42, C["chestnut"], PLEX)[0])
    g.append(f'<rect x="560" y="790" width="130" height="130" rx="10" fill="#FFFFFF" stroke="{C["leaf"]}" stroke-width="2" stroke-dasharray="6 5"/>')
    g.append(text("QR IG", 24, 625, 862, C["leaf"], SYNE, anchor="middle")[0])
    g.append(text("@oct26.crafted", 24, 70, 900, C["brick"], SYNE)[0])
    return svg(W, H, "".join(g), None, "การ์ดเล่าเรื่อง หน้าและหลัง")

def bag():
    """Matte dark paper bag with cotton rope handles and a printed label: no kraft."""
    W, H = 600, 680
    body, side, rope, ink = C["chestnut"], "#2A1910", "#EFE3D3", C["oct_cream"]
    g = [f'<path d="M190,190 C190,60 410,60 410,190" fill="none" stroke="{rope}" stroke-width="12" stroke-linecap="round"/>',
         f'<path d="M100,180 L500,180 L520,640 L80,640 Z" fill="{body}"/>',
         f'<path d="M500,180 L540,200 L556,628 L520,640 Z" fill="{side}"/>',
         f'<path d="M100,180 L500,180 L498,214 L102,214 Z" fill="#00000030"/>',
         f'<circle cx="190" cy="200" r="7" fill="{rope}"/><circle cx="410" cy="200" r="7" fill="{rope}"/>']
    wm, _, _ = wordmark(300, 395, 76, ink, C["brick"], anchor="middle"); g.append(wm)
    g.append(text("our crafted things.", 26, 300, 450, "#CDB49E", SYNE, anchor="middle")[0])
    g.append(text("อาร์ตการ์ดเคลือบด้าน · หูเชือกผ้าคอตตอน", 20, 300, 600, "#CDB49E", TH, anchor="middle")[0])
    return svg(W, H, "".join(g), None, "ถุงกระดาษด้านสีเข้ม")

def edition():
    W = 720
    g = [f'<rect x="20" y="20" width="680" height="680" rx="18" fill="{C["oct_cream"]}" stroke="#00000018" stroke-width="2"/>',
         f'<rect x="50" y="50" width="620" height="620" rx="10" fill="none" stroke="{C["chestnut"]}" stroke-width="3"/>']
    wm, _, _ = wordmark(360, 190, 70, C["chestnut"], C["brick"], anchor="middle"); g.append(wm)
    g.append(text("No. 42", 150, 360, 380, C["chestnut"], SYNE, anchor="middle")[0])
    g.append(text("รุ่นวันเกิด · 26 ต.ค. 2569", 30, 360, 450, "#6E5440", TH, anchor="middle")[0])
    g.append(text("07 / 42", 64, 360, 560, C["brick"], SYNE, anchor="middle")[0])
    g.append(text("เลขรุ่นคืออายุของแม่ เลขชิ้นเขียนด้วยมือ ไม่ทำซ้ำ", 22, 360, 625, "#6E5440", PLEX, anchor="middle")[0])
    return svg(W, W, "".join(g), None, "การ์ดรุ่นวันเกิด OCT. 26 – No. 42")

def booth():
    """Top-down plan of a 2 m x 2 m booth: two tables, demo spot, workshop box, cash point."""
    W, H = 760, 700
    ink, mute = C["chestnut"], "#8C735E"
    g = [f'<rect x="60" y="40" width="640" height="560" fill="#FFFBF5" stroke="#D8C2A6" stroke-width="3"/>',
         f'<rect x="60" y="40" width="640" height="40" fill="{C["chestnut"]}"/>']
    g.append(text("แบ็คดรอป OCT. 26 + ป้าย SOI. 02", 22, 380, 68, C["oct_cream"], TH, anchor="middle")[0])
    g.append(f'<rect x="90" y="380" width="285" height="120" rx="8" fill="{C["oct_cream"]}" stroke="{ink}" stroke-width="3"/>'
             f'<rect x="385" y="380" width="285" height="120" rx="8" fill="{C["cream"]}" stroke="{C["heart"]}" stroke-width="3"/>')
    g.append(text("โต๊ะ SOI. 02", 28, 232, 435, ink, SYNE, anchor="middle")[0])
    g.append(text("ของใช้ทุกวัน 23 แบบ", 20, 232, 470, mute, PLEX, anchor="middle")[0])
    g.append(text("โต๊ะห้าหมี Love", 28, 527, 435, C["heart"], "Mitr-Medium.ttf", anchor="middle")[0])
    g.append(text("ราวหมีห้าตัวแขวนหน้าโต๊ะ", 20, 527, 470, mute, PLEX, anchor="middle")[0])
    spots = [(380, 545, "จุดสาธิต ลองดึง", C["brick"]), (185, 250, "กล่องลองต่อ เด็ก ๆ", C["leaf"]),
             (600, 250, "รับเงิน QR", C["honey"]), (380, 200, "ที่ยืนพ่อหรือแม่", "#BFA588")]
    for x, y, t, c in spots:
        g.append(f'<circle cx="{x}" cy="{y}" r="22" fill="{c}"/>')
        g.append(text(t, 22, x, y + 52, ink, TH, anchor="middle")[0])
    g.append(f'<path d="M380,660 L380,612" stroke="{mute}" stroke-width="3" marker-end="url(#a)"/>')
    g.append(text("ทางเดิน ลูกค้าเดินเข้าจากด้านนี้", 22, 380, 692, mute, TH, anchor="middle")[0])
    g.insert(0, f'<defs><marker id="a" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
                f'<path d="M0,0 L10,5 L0,10 z" fill="{mute}"/></marker></defs>')
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
