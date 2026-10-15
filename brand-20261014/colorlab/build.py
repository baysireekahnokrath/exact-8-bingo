"""Color Lab: OCT. 26 palette directions, each drawn on the same board so they compare fairly.

The brand colour is not decided yet (owner, 15 Oct 2026). Every board uses the same logo, the same
hang tag, the five birthday brands and the FIVE BEARS mark; only the colours change.

python3 colorlab/build.py -> colorlab/svg/<key>.svg
"""
import importlib.util, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "logo"))
spec = importlib.util.spec_from_file_location("logo_build", os.path.join(ROOT, "logo", "build.py"))
L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
SYNE, TH, PLEX = "alt/Syne-Bold.ttf", "alt/Anuphan-Medium.ttf", "IBMPlexSansThai-Regular.ttf"
OUT = os.path.join(HERE, "svg"); os.makedirs(OUT, exist_ok=True)

# key, family, name, idea, colours {paper, ink, dot, deep, a1..a5 for the five birthday brands}, notes
OPTIONS = [
    ("oct", "ตั้งต้น", "October Warm", "สีที่ใช้อยู่ตอนนี้ ครีม เกาลัด ส้มอิฐ อุ่นและปลอดภัย",
     dict(paper="#F3E3CF", ink="#3A2318", dot="#D9772B", deep="#3A2318",
          fam=["#D9772B", "#8A6A3A", "#B8743A", "#6F9A8D", "#C9A27A"]),
     "อบอุ่น เป็นธรรมชาติ แต่ไม่สะดุดตาในบูธที่มีของเยอะ"),
    ("candy", "สีสด สะดุดตา", "Soi Candy", "สีป้ายรถเมล์และขนมไทย แดงมะเขือเทศ น้ำเงินโคบอลต์ เหลืองทานตะวัน",
     dict(paper="#FFF6EC", ink="#1C1B22", dot="#FF5A36", deep="#2449D8",
          fam=["#FF5A36", "#2449D8", "#FFC23C", "#2EC4A0", "#FF8AC4"]),
     "เห็นจากปลายทางเดิน ลูก ๆ ชอบ ห้าแบรนด์วันเกิดได้คนละสีชัดเจน แต่ต้องคุมไม่ให้ดูเป็นของเล่น"),
    ("tropic", "สีสด สะดุดตา", "Mango Market", "ตลาดผลไม้ไทย มะม่วง ใบตอง ม่วงอัญชัน ฟ้าใส",
     dict(paper="#FFFBEF", ink="#16302A", dot="#FFA21F", deep="#0F6B52",
          fam=["#FFA21F", "#0F6B52", "#8E6CF0", "#36B7F0", "#FF6B6B"]),
     "สดแต่ยังดูโต เหมาะกับของใช้ในบ้านและของฝาก เขียวเข้มทำให้ดูเป็นธรรมชาติ"),
    ("saddle", "หรูแบบเงียบ", "Saddle & Bone", "สีกระดูกกับหนังอานม้า แบบแบรนด์หนังยุโรป",
     dict(paper="#EFE9DF", ink="#2B1D16", dot="#8B5A2B", deep="#2B1D16",
          fam=["#8B5A2B", "#B08D57", "#6B6155", "#A0522D", "#4E5B4A"]),
     "ดูแพงทันที ราคาขยับขึ้นได้ แต่ใกล้กับแบรนด์หนังทั่วไป ต้องใช้ป้าย SOI. และเรื่องเล่าช่วยให้จำได้"),
    ("oxblood", "หรูแบบเงียบ", "Ink & Oxblood", "น้ำเงินหมึก แดงเลือดนก ทองเหลือง แบบร้านเครื่องเขียนเก่า",
     dict(paper="#F5F2EC", ink="#1E2430", dot="#7A1F24", deep="#1E2430",
          fam=["#7A1F24", "#A88B55", "#3D5A80", "#5E6B4E", "#8C6F8C"]),
     "ภูมิฐาน เหมาะกับของขวัญองค์กรและงานแต่ง อาจดูขรึมเกินไปสำหรับห้าหมี"),
    ("grandjoke", "หรูแบบตลก", "Grand Joke", "ดำ ครีม ทอง แบบแบรนด์หรู แล้วแกล้งใส่จุดชมพูฟลามิงโก",
     dict(paper="#F3EBDD", ink="#121212", dot="#FF6FAE", deep="#121212",
          fam=["#FF6FAE", "#C9A45C", "#7FD1C1", "#FFD23F", "#9B8CFF"]),
     "หรูก่อน ยิ้มทีหลัง ทำให้คนหยุดดู แต่ต้องมีอารมณ์ขันในคำและรูปตลอด ไม่งั้นจุดชมพูดูหลงที่"),
    ("pistachio", "หรูแบบตลก", "Pistachio Butler", "เขียวพิสตาชิโอ ดำพ่อบ้าน แดงกุ้งมังกร ทอง",
     dict(paper="#FAF3E3", ink="#161616", dot="#E8553A", deep="#9DBE6E",
          fam=["#E8553A", "#9DBE6E", "#C6A15B", "#6FA8DC", "#F2A7A0"]),
     "แปลกและจำง่าย ดูเหมือนร้านขนมหรูที่ไม่ถือตัว ห้าหมีเข้ากับชุดนี้ได้ดี"),
]

BIRTHDAYS = ["OCT. 26", "MAR. 23", "DEC. 07", "OCT. 09", "SEP. 01"]

def lum(hexv):
    r, g, b = (int(hexv[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)

def on(hexv):
    """Readable text colour on a fill."""
    return "#FFFFFF" if lum(hexv) < .4 else "#141414"

def datemark(x, base, size, date, fg, dot, anchor="start"):
    mon, day = date.split(". ")
    d1, w1, b1 = L.text_path(mon, size, SYNE); d2, w2, b2 = L.text_path(day, size, SYNE)
    r = size * .085; total = b1[2] + size * .06 + 2 * r + size * .3 + b2[2]
    x0 = x - (total / 2 if anchor == "middle" else 0)
    return (f'<path transform="translate({x0:.1f},{base:.1f})" d="{d1}" fill="{fg}"/>'
            f'<circle cx="{x0 + b1[2] + size * .06 + r:.1f}" cy="{base - r:.1f}" r="{r:.1f}" fill="{dot}"/>'
            f'<path transform="translate({x0 + total - b2[2]:.1f},{base:.1f})" d="{d2}" fill="{fg}"/>')

def board(c):
    """1200 x 800: hero logo panel, avatar, hang tag, five birthday brands, bear, bag."""
    W, H = 1200, 800
    p, ink, dot, deep, fam = c["paper"], c["ink"], c["dot"], c["deep"], c["fam"]
    light = on(deep)
    g = [f'<rect width="{W}" height="{H}" fill="{p}"/>',
         f'<rect x="40" y="40" width="640" height="400" rx="22" fill="{deep}"/>']
    wm, _, _ = L.wordmark(360, 240, 116, light, dot, anchor="middle"); g.append(wm)
    g.append(L.text("our crafted things.", 32, 360, 320, light, SYNE, anchor="middle")[0])
    # avatar
    g.append(f'<circle cx="840" cy="170" r="130" fill="{dot}"/>')
    wm, _, _ = L.wordmark(840, 158, 56, on(dot), on(dot) if lum(dot) > .4 else p, two_lines=True, anchor="middle"); g.append(wm)
    # hang tag
    tx, ty, tw, th = 1010, 60, 150, 270
    g.append(f'<path d="M{tx+22},{ty} H{tx+tw-22} L{tx+tw},{ty+22} V{ty+th} H{tx} V{ty+22} Z" fill="{ink}"/>'
             f'<circle cx="{tx+tw/2}" cy="{ty+34}" r="9" fill="{p}"/>')
    g.append(datemark(tx + tw / 2, ty + 150, 30, "OCT. 26", on(ink), dot, anchor="middle"))
    g.append(L.text("SOI. 02", 24, tx + tw / 2, ty + 200, on(ink), SYNE, anchor="middle")[0])
    g.append(L.text("159 บาท", 22, tx + tw / 2, ty + 240, on(ink), TH, anchor="middle")[0])
    # five birthday brands
    for i, (d, col) in enumerate(zip(BIRTHDAYS, fam)):
        x = 40 + i * 228
        g.append(f'<rect x="{x}" y="480" width="212" height="120" rx="16" fill="{col}"/>')
        g.append(datemark(x + 106, 556, 34, d, on(col), on(col), anchor="middle"))
    # bear (FIVE BEARS) and a bag
    bh = 140; bw = bh * L.BW / L.BH
    g.append(f'<rect x="40" y="630" width="420" height="130" rx="16" fill="{fam[2]}"/>')
    g.append(L.bear(60, 625, bh, fam[0] if fam[0] != fam[2] else ink, dot if dot != fam[0] else ink, ink))
    g.append(L.text("ห้าหมี", 46, 230, 705, on(fam[2]), "Mitr-SemiBold.ttf")[0])
    g.append(L.text("by OCT. 26", 20, 232, 740, on(fam[2]), SYNE, tracking=.06)[0])
    g.append(f'<path d="M560,650 C560,610 640,610 640,650" fill="none" stroke="{ink}" stroke-width="6"/>'
             f'<rect x="520" y="645" width="160" height="125" rx="6" fill="{deep}"/>')
    g.append(datemark(600, 718, 26, "OCT. 26", light, dot, anchor="middle"))
    # swatch strip
    sw = [p, ink, dot, deep] + fam[1:]
    seen = []
    for col in sw:
        if col not in seen: seen.append(col)
    for i, col in enumerate(seen[:7]):
        g.append(f'<rect x="{730 + i * 66}" y="650" width="58" height="110" rx="10" fill="{col}" stroke="#00000022" stroke-width="2"/>')
    return L.svg(W, H, "".join(g), None, "แผงสี OCT. 26")

if __name__ == "__main__":
    for key, *_rest in OPTIONS:
        c = _rest[3]
        open(os.path.join(OUT, f"{key}.svg"), "w").write(board(c))
    print(len(OPTIONS), "boards in", OUT)
