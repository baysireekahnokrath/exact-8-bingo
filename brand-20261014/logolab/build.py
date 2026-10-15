"""Logo Lab: three golden-ratio logo directions for OCT. 26, presented before any final artwork.

python3 logolab/build.py -> site/logolab.html (all drawings inline)
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, ROOT)
import importlib.util
import geometry as G
_spec = importlib.util.spec_from_file_location("site_build", os.path.join(ROOT, "site", "build.py"))
_site = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_site)
head, E, link = _site.head, _site.E, _site.link

INK, CREAM, DOTC, PAPER, GUIDE, LEATHER = "#3A2318", "#F3E3CF", "#D9772B", "#FFFBF5", "#2F7FBF", "#9A5B2C"
PHI = G.PHI

def svg(vb, body, label, cls=""):
    return f'<svg class="{cls}" viewBox="{vb}" role="img" aria-label="{E(label)}" xmlns="http://www.w3.org/2000/svg">{body}</svg>'

def lbl(x, y, t, size=7, anchor="start", col=GUIDE):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{col}" text-anchor="{anchor}" font-family="IBM Plex Mono, monospace">{E(t)}</text>'

# ---------------------------------------------------------------- A: the wordmark
def wordmark_svg(ink=INK, dot=DOTC, bg=None, uid="a", pad=24):
    s, w, _ = G.wordmark(ink, dot, uid)
    rect = f'<rect x="{-pad}" y="{-G.H - pad}" width="{w + 2*pad}" height="{G.H + 2*pad}" fill="{bg}"/>' if bg else ""
    return svg(f"{-pad} {-G.H - pad} {w + 2*pad:.1f} {G.H + 2*pad}", rect + s, "โลโก้ OCT. 26 แบบเส้นเรขาคณิต")

def wordmark_construction():
    s, w, st = G.wordmark("#C9B7A3", DOTC, "ac")
    g = [s]
    ln = lambda x1, y1, x2, y2, dash="2 2": f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GUIDE}" stroke-width=".6" stroke-dasharray="{dash}"/>'
    for y, t in ((0, "baseline"), (-G.H, "cap  H = 100"), (-G.H / PHI, "H/φ = 61.8"), (-G.H / PHI ** 2, "H/φ² = 38.2")):
        g.append(ln(-10, y, w + 10, y)); g.append(lbl(w + 12, y + 2.5, t))
    o = st["O"]; g.append(f'<circle cx="{o + 50}" cy="-50" r="50" fill="none" stroke="{GUIDE}" stroke-width=".6"/>')
    g.append(lbl(o + 50, -50 + 2.5, "O = วงกลม H", anchor="middle"))
    c = st["C"]; cx = c + 50
    for a in (G.C_OPEN / 2, -G.C_OPEN / 2):
        x2 = cx + 60 * math.cos(math.radians(a)); y2 = -50 + 60 * math.sin(math.radians(a))
        g.append(ln(cx, -50, x2, y2, "1 1.5"))
    g.append(lbl(cx + 34, -47, f"ช่องเปิด 360/φ³ = {G.C_OPEN:.0f}°", 5.5))
    t = st["T"]; g.append(ln(t, -G.H - 8, t + G.TW, -G.H - 8, "0")); g.append(lbl(t + G.TW / 2, -G.H - 11, "T = H·φ/2 = 80.9", anchor="middle"))
    g.append(lbl(t + G.TW / 2 + 9, -G.H + G.W + 9, f"เส้น w = H/φ⁴ = {G.W:.1f}", 5.5))
    d = st["."]; g.append(f'<circle cx="{d + G.DOT/2:.1f}" cy="{-G.DOT/2:.1f}" r="{G.DOT/2 + 3:.1f}" fill="none" stroke="{GUIDE}" stroke-width=".6"/>')
    g.append(lbl(d + G.DOT / 2, 14, f"จุด = w·φ = {G.DOT:.1f}", anchor="middle"))
    two = st["2"]; six = st["6"]
    g.append(ln(two, 10, six + G.D, 10, "0")); g.append(lbl((two + six + G.D) / 2, 20, "เลข กว้าง D = H/φ = 61.8", anchor="middle"))
    g.append(ln(d + G.DOT, -G.DOT - 6, two, -G.DOT - 6, "0")); g.append(lbl((d + G.DOT + two) / 2, -G.DOT - 9, "H/φ² = 38.2", 5.5, "middle"))
    return svg(f"-14 {-G.H - 22} {w + 75:.0f} {G.H + 50}", "".join(g), "เส้นโครงของโลโก้ แสดงสัดส่วนทองคำ", "wide")

def favicon_A(ink=INK, dot=DOTC, bg=PAPER):
    # ring O and the dot, sitting on one baseline, centred in a square
    r = G.H / 2 - G.W / 2; total = G.H + G.GAP / PHI + G.DOT; side = total + 24
    ox = (side - total) / 2; base = side / 2 + G.H / 2
    return (f'<rect width="{side:.1f}" height="{side:.1f}" rx="{side/PHI**3:.1f}" fill="{bg}"/>'
            f'<circle cx="{ox + 50:.1f}" cy="{base - 50:.1f}" r="{r:.1f}" fill="none" stroke="{ink}" stroke-width="{G.W:.1f}"/>'
            f'<circle cx="{ox + G.H + G.GAP/PHI + G.DOT/2:.1f}" cy="{base - G.DOT/2:.1f}" r="{G.DOT/2:.1f}" fill="{dot}"/>'), side

# ---------------------------------------------------------------- B: the golden tag
TWID = 100.0; THGT = TWID * PHI; CH = TWID / PHI ** 3; HOLE = TWID / PHI ** 4; MARG = TWID / PHI ** 4

def tag_shape(fill):
    return (f'<path d="M{CH:.2f},0 H{TWID - CH:.2f} L{TWID},{CH:.2f} V{THGT:.2f} H0 V{CH:.2f} Z" fill="{fill}"/>')

def tag_body(fill=INK, ink=CREAM, dot=DOTC, uid="b", holebg=PAPER):
    g = [tag_shape(fill), f'<circle cx="{TWID/2}" cy="{CH:.2f}" r="{HOLE/2:.2f}" fill="{holebg}"/>']
    d, dw = G.digits_26(0, ink, uid + "d")
    s = (TWID - 2 * MARG) / dw
    base = THGT / PHI
    g.append(f'<g transform="translate({MARG:.2f},{base:.2f}) scale({s:.4f})">{d}</g>')
    w, ww, _ = G.wordmark(ink, dot, uid + "w")
    # only OCT. : wordmark up to the dot
    oct_part, oct_w = _oct(ink, dot, uid + "o")
    s2 = (TWID - 2 * MARG) / oct_w * .62
    g.append(f'<g transform="translate({(TWID - oct_w * s2)/2:.2f},{THGT - CH:.2f}) scale({s2:.4f})">{oct_part}</g>')
    return "".join(g)

def _oct(ink, dot, uid):
    parts, x = [], 0.0
    for fn, gap in ((G.glyph_O, G.GAP * .8), (G.glyph_C, G.GAP), (G.glyph_T, G.GAP / PHI)):
        s, adv = fn(x, ink); parts.append(s); x += adv + gap
    s, adv = G.glyph_dot(x, dot); parts.append(s)
    return "".join(parts), x + adv

def tag_construction():
    g = [tag_body("#E9DCCB", "#C9B7A3", DOTC, "bc", PAPER)]
    ln = lambda x1, y1, x2, y2, dash="2 2": f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GUIDE}" stroke-width=".5" stroke-dasharray="{dash}"/>'
    g.append(f'<rect x="0" y="0" width="{TWID}" height="{THGT:.1f}" fill="none" stroke="{GUIDE}" stroke-width=".5"/>')
    g.append(ln(0, TWID, TWID, TWID)); g.append(ln(TWID / PHI, TWID, TWID / PHI, THGT))
    # golden spiral arcs through the squares
    g.append(f'<path d="M0,{TWID} A{TWID},{TWID} 0 0 1 {TWID},0" fill="none" stroke="{GUIDE}" stroke-width=".5" opacity=".7"/>')
    g.append(f'<path d="M{TWID},0 M{TWID},{TWID} A{TWID/PHI:.1f},{TWID/PHI:.1f} 0 0 1 {TWID - TWID/PHI:.1f},{THGT:.1f}" fill="none" stroke="{GUIDE}" stroke-width=".5" opacity=".7"/>')
    g.append(lbl(TWID + 4, TWID / 2, "1 : φ", 6)); g.append(lbl(TWID + 4, TWID + 3, "ฐานเลข 26 = H/φ", 5))
    g.append(lbl(TWID + 4, CH + 2, f"มุมตัด = W/φ³ ({CH:.1f})", 5)); g.append(lbl(TWID + 4, CH + 9, f"รู = W/φ⁴ ({HOLE:.1f})", 5))
    g.append(lbl(TWID + 4, THGT - CH + 2, "OCT. ห่างขอบล่าง W/φ³", 5))
    return svg(f"-6 -6 {TWID + 74:.0f} {THGT + 12:.0f}", "".join(g), "เส้นโครงของป้ายห้อยสัดส่วนทองคำ")

# ---------------------------------------------------------------- C: the seal
R0 = 50.0; RIN = R0 / PHI; BAND = R0 / PHI ** 6

def seal_body(ink=INK, dot=DOTC, fillc=None, text=True, uid="c"):
    g = []
    if fillc: g.append(f'<circle cx="0" cy="0" r="{R0}" fill="{fillc}"/>')
    g.append(f'<circle cx="0" cy="0" r="{R0 - BAND/2:.2f}" fill="none" stroke="{ink}" stroke-width="{BAND:.2f}"/>')
    g.append(f'<circle cx="0" cy="0" r="{RIN:.2f}" fill="none" stroke="{ink}" stroke-width="{BAND/PHI:.2f}"/>')
    d, dw = G.digits_26(0, ink, uid + "d")
    s = (RIN * 2 / PHI) / dw
    g.append(f'<g transform="translate({-dw*s/2:.2f},{G.H*s/2:.2f}) scale({s:.4f})">{d}</g>')
    rt = (R0 - BAND + RIN) / 2
    if text:
        g.append(f'<defs><path id="{uid}t" d="M{-rt:.2f},0 A{rt:.2f},{rt:.2f} 0 1 1 {rt:.2f},0"/><path id="{uid}b" d="M{-rt:.2f},0 A{rt:.2f},{rt:.2f} 0 0 0 {rt:.2f},0"/></defs>'
                 f'<text font-family="Jost, sans-serif" font-weight="500" font-size="6.6" letter-spacing="1.5" fill="{ink}" dominant-baseline="middle">'
                 f'<textPath href="#{uid}t" startOffset="50%" text-anchor="middle">OUR CRAFTED THINGS</textPath></text>'
                 f'<text font-family="Jost, sans-serif" font-weight="500" font-size="6.6" letter-spacing="1.5" fill="{ink}" dominant-baseline="middle">'
                 f'<textPath href="#{uid}b" startOffset="50%" text-anchor="middle">EST. 26 · 10 · 2026</textPath></text>')
    for sx in (-1, 1):
        g.append(f'<circle cx="{sx * rt:.2f}" cy="0" r="{BAND * .9:.2f}" fill="{dot}"/>')
    return "".join(g)

def seal_construction():
    g = [seal_body("#C9B7A3", DOTC, None, True, "cc")]
    for i, (r, t) in enumerate(((R0, "D = 100"), (RIN, "D/φ = 61.8"), (RIN / PHI, "D/φ² = 38.2"))):
        g.append(f'<circle r="{r:.2f}" fill="none" stroke="{GUIDE}" stroke-width=".5" stroke-dasharray="2 2"/>')
        y = -R0 + 8 + i * 9
        g.append(f'<line x1="{r * .7:.1f}" y1="{-r * .7:.1f}" x2="{R0 + 3}" y2="{y - 1.5:.1f}" stroke="{GUIDE}" stroke-width=".3"/>')
        g.append(lbl(R0 + 4, y, t, 5))
    g.append(lbl(0, R0 + 9, f"ขอบ = D/φ⁶ ({BAND*2:.1f}) · เลข 26 กว้าง = วงใน/φ", 5, "middle"))
    return svg(f"{-R0 - 8} {-R0 - 8} {2*R0 + 48} {2*R0 + 22}", "".join(g), "เส้นโครงของตราประทับสัดส่วนทองคำ")

# ---------------------------------------------------------------- tests
def at_sizes(make_svg, sizes=(16, 24, 32, 48, 64)):
    return "".join(f'<figure class="sz"><div style="width:{s}px;height:{s}px">{make_svg()}</div><figcaption>{s}px</figcaption></figure>' for s in sizes)

def deboss(body_fn, vb):
    """Pressed into leather: the mark in a darker brown with a light edge below it."""
    return svg(vb, f'<rect x="-999" y="-999" width="3000" height="3000" fill="{LEATHER}"/>'
                   f'<g transform="translate(0,1.2)" opacity=".55">{body_fn("#C98B55")}</g><g>{body_fn("#6A3A18")}</g>', "ตัวอย่างปั๊มลงหนัง")

def build():
    fa, side = favicon_A()
    favA = lambda: svg(f"0 0 {side:.0f} {side:.0f}", fa, "ไอคอน O.")
    favB = lambda: svg(f"-12 -2 {TWID + 24} {THGT + 4:.0f}", tag_body(uid="fb"), "ไอคอนป้ายห้อย")
    favC = lambda: svg(f"{-R0-2} {-R0-2} {2*R0+4} {2*R0+4}",
                       f'<circle r="{R0}" fill="{INK}"/>' + seal_body(CREAM, DOTC, None, False, "fc"), "ไอคอนตรา")
    wm_dark = wordmark_svg(CREAM, DOTC, INK, "ad")
    wm_black = wordmark_svg("#000", "#000", "#FFF", "ak")
    wm_white = wordmark_svg("#FFF", "#FFF", "#000", "aw")
    s_wm, w_wm, _ = G.wordmark("#000", "#000", "deb")
    deb_A = deboss(lambda c: G.wordmark(c, c, "x" + c[1:])[0], f"-20 -124 {w_wm + 40:.0f} 148")
    deb_B = deboss(lambda c: tag_body(c, LEATHER, c, "y" + c[1:], LEATHER), f"-20 -10 {TWID + 40} {THGT + 20:.0f}")
    deb_C = deboss(lambda c: seal_body(c, c, None, True, "z" + c[1:]), f"{-R0-12} {-R0-12} {2*R0+24} {2*R0+24}")
    tag_lockup = svg(f"-10 -10 {TWID + 20 + 40 + w_wm * .5:.0f} {THGT + 20:.0f}",
                     tag_body(uid="tl") + f'<g transform="translate({TWID + 40},{THGT/PHI:.1f}) scale(.5)">{G.wordmark(INK, DOTC, "tlw")[0]}</g>',
                     "ป้ายห้อยคู่กับโลโก้ตัวอักษร")
    seal_big = svg(f"{-R0-4} {-R0-4} {2*R0+8} {2*R0+8}", seal_body(INK, DOTC, PAPER, True, "sb"), "ตราประทับ OCT. 26")
    billboard = svg(f"0 0 1600 500", f'<rect width="1600" height="500" fill="{INK}"/>'
                    f'<g transform="translate(120,330) scale(2.2)">{G.wordmark(CREAM, DOTC, "bb")[0]}</g>'
                    f'<text x="124" y="420" font-family="Jost, sans-serif" font-size="34" letter-spacing="10" fill="{CREAM}" opacity=".8">OUR CRAFTED THINGS</text>',
                    "ตัวอย่างป้ายบิลบอร์ด", "wide")

    phi_rows = "".join(f'<tr><td>{E(a)}</td><td class="mono">{E(b)}</td><td class="n mono">{c}</td></tr>' for a, b, c in [
        ("ความสูงตัวอักษร", "H", "100"), ("ความหนาเส้น", "H ÷ φ⁴", f"{G.W:.1f}"), ("จุด (ส่วนที่โดดเด่น)", "เส้น × φ", f"{G.DOT:.1f}"),
        ("ความกว้างตัวเลข", "H ÷ φ", f"{G.D:.1f}"), ("ความกว้าง T", "H × φ ÷ 2", f"{G.TW:.1f}"),
        ("ช่องเปิดของ C", "360° ÷ φ³", f"{G.C_OPEN:.0f}°"), ("ระยะระหว่างคำ", "H ÷ φ²", f"{G.WORD:.1f}"),
        ("ป้ายห้อย", "กว้าง : สูง = 1 : φ", "100 : 161.8"), ("ตราประทับ", "วงนอก : วงใน = φ : 1", "100 : 61.8")])

    # our own read, 1..3 for: clean, memorable, timeless, versatile, relevant
    SC = {"A": (3, 2, 3, 3, 2), "B": (3, 3, 3, 3, 3), "C": (2, 2, 3, 1, 3)}
    CRIT = ["เรียบ สะอาด", "จำง่าย", "ไม่ตกยุค", "ใช้ได้ทุกขนาด", "ตรงกับแบรนด์"]
    dots = lambda n: "".join(f'<i class="d{" on" if i < n else ""}"></i>' for i in range(3))
    score = "".join(f'<tr><td><b>{k}</b></td>' + "".join(f"<td>{dots(v)}</td>" for v in vals) + "</tr>" for k, vals in SC.items())

    def direction(key, title, idea, hero, cons, favicon, extra, why, weak):
        return f"""<section id="{key.lower()}" class="dir"><span class="eyebrow">ทางที่ {key}</span><h2>{E(title)}</h2><p class="lead">{E(idea)}</p>
<div class="hero">{hero}</div>
<h3>เส้นโครง</h3><div class="cons">{cons}</div>
<h3>เล็กสุดถึงใหญ่สุด</h3><div class="sizes">{at_sizes(favicon)}</div>
<div class="grid">{extra}</div>
<div class="duo"><div class="card"><h3>จุดแข็ง</h3><p>{E(why)}</p></div><div class="card"><h3>ข้อควรระวัง</h3><p>{E(weak)}</p></div></div></section>"""

    tile = lambda inner, cap, dark=False: f'<figure class="tile{" dk" if dark else ""}"><div>{inner}</div><figcaption>{E(cap)}</figcaption></figure>'
    A = direction("A", "ตัวอักษรเรขาคณิต · O. เป็นสัญลักษณ์",
                  "วาดตัวอักษรเองทุกตัวจากวงกลม เส้นตรง และสัดส่วนทองคำ ไม่ใช้ฟอนต์สำเร็จ จุดสีคือส่วนเดียวที่ใหญ่กว่าเส้น จึงเป็นสิ่งที่คนจำ ไอคอนเล็กใช้ O กับจุด",
                  wordmark_svg(), wordmark_construction(), favA,
                  tile(wm_dark, "บนพื้นเข้ม", True) + tile(wm_black, "ขาวดำ") + tile(wm_white, "กลับสี", True) + tile(deb_A, "ปั๊มลงหนัง") + tile(billboard, "บิลบอร์ด 1600 × 500", True),
                  "เรียบที่สุด ไม่ขึ้นกับเทรนด์ฟอนต์ ใช้กับ SOI. 02 และ MAR. 23 ได้ด้วยกติกาเดียวกัน",
                  "ไม่มีรูปสัญลักษณ์ที่แข็งแรง ไอคอน O. อาจดูคล้ายแบรนด์อื่นที่ใช้วงกลม ต้องพึ่งจุดสีให้คนจำ")
    B = direction("B", "ป้ายห้อยทองคำ · ตัวอักษรชุดเดียวกับทาง A",
                  "สัญลักษณ์คือป้ายห้อยสัดส่วน 1 : φ ซึ่งเป็นทั้งป้ายของงานทำมือ และหน้าปฏิทินที่บอกวันที่ 26 ฐานของเลข 26 อยู่ตรงเส้นแบ่งทองคำของป้ายพอดี",
                  tag_lockup, tag_construction(), favB,
                  tile(svg(f"-10 -10 {TWID + 20} {THGT + 20:.0f}", tag_body(INK, CREAM, DOTC, "bd", INK) , "ป้ายบนพื้นเข้ม"), "บนพื้นเข้ม (รูป่วนเป็นสีพื้น)", True)
                  + tile(svg(f"-10 -10 {TWID + 20} {THGT + 20:.0f}", tag_body("#000", "#FFF", "#FFF", "bk", "#FFF"), "ขาวดำ"), "ขาวดำ")
                  + tile(deb_B, "ปั๊มลงหนัง") + tile(svg(f"-10 -10 {TWID + 20} {THGT + 20:.0f}", tag_body(INK, CREAM, DOTC, "bs", PAPER), "ใช้เป็นป้ายห้อยจริง"), "ใช้เป็นป้ายห้อยจริงได้เลย"),
                  "รูปทรงที่คนจำได้แม้ไม่เห็นตัวหนังสือ เล่าทั้งงานทำมือ (ป้ายห้อย) และวันที่ (ปฏิทิน) ใช้ซ้ำได้ทุกแบรนด์วันเกิด แค่เปลี่ยนเลข",
                  "ป้ายห้อยเป็นรูปที่แบรนด์อื่นก็ใช้ จุดที่ทำให้เป็นของเราคือสัดส่วนทองคำ มุมตัด และเลขวันที่ ต้องคงไว้ทุกครั้ง")
    C = direction("C", "ตราประทับ · สำหรับปั๊มหนัง",
                  "วงกลมสองวงสัดส่วน φ : 1 ตัวหนังสือวิ่งรอบวง เลข 26 อยู่กลาง เหมาะกับการปั๊มร้อนลงบนหนังแท้ แบบที่ร้านงานหนังดี ๆ ใช้",
                  seal_big, seal_construction(), favC,
                  tile(svg(f"{-R0-4} {-R0-4} {2*R0+8} {2*R0+8}", seal_body(CREAM, DOTC, INK, True, "cd"), "ตราบนพื้นเข้ม"), "บนพื้นเข้ม", True)
                  + tile(svg(f"{-R0-4} {-R0-4} {2*R0+8} {2*R0+8}", seal_body("#000", "#000", "#FFF", True, "ck"), "ตราขาวดำ"), "ขาวดำ")
                  + tile(deb_C, "ปั๊มลงหนัง"),
                  "ดูเป็นงานหนังแท้ทันที เหมาะกับการปั๊มลงสินค้า และใช้เป็นตราของรุ่นวันเกิด No. 42",
                  "ตัวหนังสือรอบวงอ่านไม่ออกเมื่อเล็กกว่า 2 ซม. ไอคอนจึงต้องตัดเหลือแค่เลข 26 และตราวงกลมเป็นรูปที่แบรนด์งานหนังใช้กันมาก")

    nav = '<a href="#why">ทำไมต้องเปลี่ยน</a><a href="#phi">สัดส่วน</a><a href="#a">ทาง A</a><a href="#b">ทาง B</a><a href="#c">ทาง C</a><a href="#pick">เทียบและเลือก</a>'
    css = """
.wide{width:100%;height:auto}.hero{background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:22px;display:flex;justify-content:center}
.hero svg{max-height:240px;width:100%;height:auto}.cons{background:#FFFFFF;border:1px solid var(--line);border-radius:18px;padding:14px;overflow-x:auto}
.cons svg{width:100%;height:auto;min-width:520px;max-height:420px}
.sizes{display:flex;gap:18px;align-items:flex-end;flex-wrap:wrap;background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:16px}
.sz{margin:0;display:flex;flex-direction:column;align-items:center;gap:6px}.sz div svg{width:100%;height:100%;display:block}
.sz figcaption{font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums}
.tile{margin:0;display:flex;flex-direction:column;gap:6px}.tile>div{background:#FFFFFF;border:1px solid var(--line);border-radius:14px;padding:14px;display:flex;justify-content:center;align-items:center;min-height:150px}
.tile.dk>div{background:#1F140E}.tile svg{width:100%;height:auto;max-height:200px}.tile figcaption{font-size:13px;color:var(--muted)}
.duo{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr))}
i.d{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:3px;background:var(--line)}i.d.on{background:var(--brick)}
td i{vertical-align:middle}
"""
    return f"""{head("OCT. 26 Logo Lab")}<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@500&family=IBM+Plex+Mono:wght@400&display=swap"><style>{css}</style>
<div class="wrap">
<nav class="top" aria-label="หัวข้อ">{nav}</nav>
<header style="padding-top:28px;display:flex;flex-direction:column;gap:12px"><span class="eyebrow">LOGO LAB · 16 ต.ค. 2569 · นำเสนอก่อนทำจริง</span>
<h1>โลโก้ OCT. 26 จากสัดส่วนทองคำ</h1>
<p class="lead">สามทาง ใช้ตัวอักษรชุดใหม่ชุดเดียวกัน ที่วาดเองจากวงกลม เส้นตรง และ φ = 1.618 ไม่ใช้ฟอนต์สำเร็จ ทุกทางทดสอบตั้งแต่ไอคอน 16 พิกเซล จนถึงบิลบอร์ด ขาวดำ และปั๊มลงหนัง เลือกทางแล้วค่อยทำไฟล์จริงทั้งชุด</p>
<div class="hero">{wordmark_svg()}</div></header>

<section id="why"><span class="eyebrow">ทำไมต้องเปลี่ยน</span><h2>โลโก้เดิมไม่ cool เพราะอะไร</h2><div class="grid">
<div class="card"><h3>ฟอนต์เป็นของเทรนด์</h3><p>Syne เป็นฟอนต์ที่ฮิตช่วงปี 2020 ตัวกว้างและแปลกตา อีกไม่กี่ปีจะดูเชย และใครก็โหลดมาใช้ได้</p></div>
<div class="card"><h3>ไม่มีระบบสัดส่วน</h3><p>ขนาดจุด ระยะห่าง และความหนาเส้นมาจากฟอนต์ ไม่ได้ออกแบบให้สัมพันธ์กัน จึงดูเหมือนพิมพ์ชื่อ ไม่ใช่โลโก้</p></div>
<div class="card"><h3>ไม่มีสัญลักษณ์ตอนเล็ก</h3><p>พอย่อเป็นไอคอน 16 พิกเซล ตัวหนังสืออ่านไม่ออก และไม่มีรูปทรงอะไรให้คนจำ</p></div></div></section>

<section id="phi"><span class="eyebrow">สัดส่วน</span><h2>ทุกขนาดมาจากตัวเลขเดียว</h2>
<p class="lead">เริ่มจากความสูงตัวอักษร H = 100 แล้วหารหรือคูณด้วย φ ทุกค่า ทำให้ทุกส่วนสัมพันธ์กันเอง ตาคนจึงรู้สึกว่าลงตัว แม้ไม่รู้ว่าทำไม</p>
<div class="tbl"><table><thead><tr><th>ส่วน</th><th>สูตร</th><th>ค่า</th></tr></thead><tbody>{phi_rows}</tbody></table></div></section>
{A}{B}{C}
<section id="pick"><span class="eyebrow">เทียบและเลือก</span><h2>เทียบกับห้าข้อที่ต้องการ</h2>
<div class="tbl"><table><thead><tr><th>ทาง</th>{"".join(f"<th>{c}</th>" for c in CRIT)}</tr></thead><tbody>{score}</tbody></table></div>
<p class="cap">คะแนนเป็นความเห็นของเรา สามจุดคือดีที่สุด</p>
<div class="card" style="border:2px solid var(--brick)"><h3>ข้อเสนอ: ทาง B ใช้คู่กับตัวอักษรของทาง A</h3>
<p style="margin-top:6px">ตัวอักษรเรขาคณิตใช้เป็นชื่อแบรนด์ทุกที่ ป้ายห้อยทองคำเป็นสัญลักษณ์และไอคอน ส่วนตราประทับของทาง C เก็บไว้ใช้ปั๊มลงหนังและรุ่นวันเกิด สามอย่างนี้ใช้ตัวอักษรชุดเดียวกัน จึงไปด้วยกันได้</p>
<p class="cap" style="margin-top:6px">สีในหน้านี้ยังเป็นสีตั้งต้น เลือกสีจาก {link("colorlab", "Color Lab")} หรือ {link("palettes", "หน้าสุ่มสี")} ได้แยกกัน หลังเลือกทางแล้วจะวาดตัวอักษรที่เหลือ (S I M A R E P D N V และเลข 0 1 3 7 9) ด้วยกติกาเดียวกัน สำหรับ SOI. 02 และแบรนด์วันเกิด</p></div></section>
</div>"""

if __name__ == "__main__":
    out = os.path.join(ROOT, "site", "logolab.html")
    open(out, "w").write(build())
    print("wrote", out)
