"""Birthday deck slides (1920 x 1080), written from one place so colour and type stay on the golden system.

Type steps 16 x phi^(k/2) scaled for a 1080 slide: 26 33 42 53 68 86 110 140.
Spacing is Fibonacci: 13 21 34 55 89 144. Two-column splits are 1 : phi. Palette #2 (Soi Candy).
Images are the brand's own PNGs, uploaded to the deck as assets (/_blob/<id>).

python3 deck/build.py -> deck/project/slides/*.html and deck/project/deck.json
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "project", "slides")

P, I, CO, TO, SU, MI, PI = "#FFF6EC", "#1C1B22", "#2449D8", "#FF5A36", "#FFC23C", "#2EC4A0", "#FF8AC4"
W, MU, MUD, LINE = "#FFFFFF", "#4A4A55", "#C9C4D6", "#F1DCCB"
BODY = "'IBM Plex Sans Thai', Tahoma, sans-serif"
HEAD = "'Anuphan', 'IBM Plex Sans Thai', Tahoma, sans-serif"
MITR = "'Mitr', Tahoma, sans-serif"
JOST = "'Jost', 'Anuphan', sans-serif"

BLOB = {  # uploaded 15 Oct 2026
    "date": "1f82405442426f9927af7dfb7bc849c4", "name": "fdf5d2361b3a46ec4ddabce53499b180",
    "soi": "190ad702c168d58d8f2695b83e111751",
    "love": "8d6ea5ffa0ea089e935345ab55fc75d3", "avatar": "111977978748bb8cf4e65e72dab76bb0",
    "bear": "15387348361d35674b43a64672dbf652", "family": "e9dcaab887265b826410a402138bf25b",
    "p18": "aa023269fbd878a694959a19ac01641d", "p21": "1f12aebd87f38eae6aab682b603d3e18",
    "p23": "7d07d2acfe2ddf2a6b8e9f2c0091611d", "p29": "c88467c3013f59793b12a6a52e8c7cd7",
}
img = lambda k, alt, style: f'<img src="/_blob/{BLOB[k]}" alt="{alt}" style="{style}">'

def section(id_, bg, fg, inner, note, layout="flex-direction:column;justify-content:center", pad="144px"):
    return (f'<section id="{id_}" data-transition="fade" style="background:{bg};color:{fg};font-family:{BODY};'
            f'padding:{pad};display:flex;{layout};gap:55px">\n{inner}\n<aside>{note}</aside>\n</section>\n')

def eyebrow(t, c):
    return f'<p style="font-family:{HEAD};font-size:33px;font-weight:500;letter-spacing:3px;color:{c}">{t}</p>'

def h(t, size=68, font=HEAD, c=None, tag="h2", extra=""):
    col = f";color:{c}" if c else ""
    return f'<{tag} style="font-family:{font};font-size:{size}px;font-weight:600;line-height:1.1{col}{extra}">{t}</{tag}>'

def p(t, size=42, c=None, extra=""):
    col = f";color:{c}" if c else ""
    return f'<p style="font-size:{size}px;line-height:1.5{col}{extra}">{t}</p>'

def card(inner, bg=W, top=None):
    bt = f"border-top:13px solid {top};" if top else f"border:1px solid {LINE};"
    return f'<div style="background:{bg};{bt}border-radius:21px;padding:34px;display:flex;flex-direction:column;gap:13px">{inner}</div>'

S = {}
S["cover"] = section("cover", P, I,
    img("family", "หมีห้าตัว พ่อหมี แม่หมี และลูกหมีสามตัว", "width:987px;height:365px;object-fit:contain") + "\n"
    + h("สุขสันต์วันเกิด แม่หมี", 110, MITR, tag="h1", extra=";text-align:center") + "\n"
    + f'<p style="font-family:{MITR};font-size:42px;font-weight:500;color:{CO};text-align:center">จากพ่อหมี และลูกหมีสามตัว</p>',
    "เปิดสไลด์นี้ค้างไว้ตอนเริ่ม ให้ลูก ๆ ร้องเพลงวันเกิดก่อน แล้วค่อยกดไปหน้าถัดไป",
    "flex-direction:column;justify-content:center;align-items:center")

S["gift"] = section("gift", I, P,
    eyebrow("ของขวัญปีนี้", TO) + "\n" + h("ไม่ได้อยู่ในกล่อง", 140, c=P) + "\n"
    + p("พ่อกับลูก ๆ ทำแบรนด์ให้เธอหนึ่งแบรนด์ ตั้งชื่อตามวันเกิดของเธอ และพาไปออกบูธครั้งแรกวันที่ 23–25 ตุลาคม", 42, MUD, ";max-width:1364px"),
    "หยุดตรงนี้สักครู่ ให้เธอเดาว่าชื่อแบรนด์คืออะไร ใบ้ได้ว่าเป็นตัวเลขที่เธอรู้จักดีที่สุด")

S["name"] = section("name", P, I,
    eyebrow("ชื่อแบรนด์", CO) + "\n"
    + img("name", "OCT. 26", "width:830px;height:254px;object-fit:contain;object-position:left;margin-left:-55px") + "\n"
    + f'<ul style="font-size:42px;line-height:1.5;color:{MU}"><li>O · C · T ย่อจาก our crafted things ของที่เราทำกันเอง</li>'
      '<li>OCT. คือเดือนตุลาคม</li><li>26 คือวันเกิดของเธอ</li></ul>',
    "ให้ลูก ๆ อ่านชื่อพร้อมกัน อ็อก ยี่สิบหก ชื่อนี้วาดเองจากวงกลมและเส้นตรง ส่วน OCT. กับ 26 แบ่งกันตามสัดส่วนทองคำ ชื่ออื่นที่คิดมาทั้งหมด 55 ชื่ออยู่ในหน้าทางเลือกแบรนด์")

S["date"] = section("date", CO, P,
    eyebrow("แบรนด์นี้เกิดวันเดียวกับเธอ", SU) + "\n"
    + img("date", "26.10", "width:911px;height:411px;object-fit:contain") + "\n"
    + p("ลูก ๆ ขายวันแรกที่บูธ 23–25 ตุลาคม แล้ว OCT. 26 เกิดอย่างเป็นทางการในวันเกิดของเธอ ทุกปีในวันนี้ ร้านจะออกของรุ่นพิเศษหนึ่งชุด", 42, "#E3E8FB", ";text-align:center;max-width:1597px"),
    "ถ้าพรีเซนต์ก่อนวันงาน บอกว่าวันที่ 26 เราจะฉลองสองงานพร้อมกัน",
    "flex-direction:column;justify-content:center;align-items:center", "89px 144px")

S["arch"] = section("arch", P, I,
    h("หนึ่งบ้าน หนึ่งซอย และหมีห้าตัว") + "\n"
    + '<div style="display:grid;grid-template-columns:1fr 1fr;gap:55px">'
    + card(img("soi", "ป้าย SOI. 02", "width:100%;height:233px;object-fit:contain;object-position:left")
           + h("OCT. 26 · SOI. 02", 53, tag="h3")
           + p("From our root คอลเลกชันแรก ของใช้ทุกวัน 23 แบบ จากบ้านในซอย 2 ที่ทุกอย่างเริ่มต้น", 33, MU))
    + card(img("love", "ป้าย Love ห้าหมี FIVE BEARS", "width:100%;height:233px;object-fit:contain;object-position:left")
           + h("ห้าหมี by OCT. 26 · Love", 53, tag="h3")
           + p("ซับแบรนด์ของครอบครัวและเด็ก คอลเลกชันแรกคือ Love หัวหมีกับสายหัวใจ 7 แบบ", 33, MU))
    + "</div>",
    "ห้าหมีเป็นซับแบรนด์ ใช้ร้านและบัญชีเดียวกับ OCT. 26 แยกเป็นหมวดในร้าน",
    "flex-direction:column;justify-content:center", "89px 144px")

S["heart"] = section("heart", TO, W,
    f'<div style="flex:none;width:610px;height:610px;background:{P};border-radius:50%;display:flex;align-items:center;justify-content:center">'
    + img("bear", "หมีห้าหมี มีหัวใจสีแดงตรงกลาง", "width:377px;height:377px;object-fit:contain") + "</div>\n"
    + '<div style="flex:1;display:flex;flex-direction:column;gap:34px">'
    + h("หัวใจตรงกลางคือเธอ", 86, MITR)
    + p("หมีของห้าหมีคือบล็อกตัดหนังแบบ 01 ของจริง ร่องสองเส้นเป็นแก้ม และหัวใจตรงกลางคือแม่หมี คอลเลกชันแรกของห้าหมีจึงชื่อ Love", 42)
    + "</div>",
    "ถ้ามีชิ้นหนังแบบ 01 อยู่ในมือ ยื่นให้เธอจับดูตอนพูดสไลด์นี้",
    "flex-direction:row;align-items:center")

STORY = [("26 ตุลาคม", "แบรนด์ตั้งชื่อตามวันเกิดของเธอ และเกิดในวันเดียวกัน"),
         ("our crafted things", "ของที่เราทำกันเอง พ่อทำบล็อก ลูก ๆ ประกอบและขาย"),
         ("เริ่มจากเศษหนัง", "เศษหนังแท้เท่าฝ่ามือ ตัดด้วยบล็อกของพ่อ ต่อกันเป็นของใช้ทีละชิ้น"),
         ("From our root", "ทุกอย่างเริ่มที่บ้านในซอย 2 คอลเลกชันแรกจึงชื่อ SOI. 02 และหัวหมีชิ้นแรกกลายเป็นห้าหมี")]
S["story"] = section("story", P, I,
    h("เรื่องของ OCT. 26") + "\n" + '<div style="display:grid;grid-template-columns:1fr 1fr;gap:34px">'
    + "".join(card(h(t, 42, JOST if t.isascii() else HEAD, CO, "h3") + p(d, 33, MU)) for t, d in STORY) + "</div>",
    "เรื่องเล่าฉบับเต็มอยู่ใน Brand Book ใช้เป็นข้อความโพสต์แรกของเพจได้เลย")

FAM = [("พ่อหมี", CO, "โคบอลต์ · ออกแบบและผลิต"), ("แม่หมี", TO, "มะเขือเทศ · หัวใจของบ้าน"),
       ("ลูกหมีคนโต", SU, "ทานตะวัน · หัวหน้าร้าน"), ("ลูกหมีคนกลาง", MI, "มิ้นต์ · นักสาธิต"),
       ("ลูกหมีคนเล็ก", PI, "ชมพูขนม · ผู้ต้อนรับ")]
S["family"] = section("family", W, I,
    h("ห้าหมี ห้าสี", 68, MITR) + "\n"
    + img("family", "หมีห้าตัวเรียงจากพ่อหมีถึงลูกหมีคนเล็ก", "width:100%;height:377px;object-fit:contain") + "\n"
    + '<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:21px">'
    + "".join(f'<div style="display:flex;flex-direction:column;gap:5px;border-top:13px solid {c};padding-top:21px">'
              f'<p style="font-family:{MITR};font-size:33px;font-weight:500">{n}</p><p style="font-size:26px;color:{MU}">{d}</p></div>'
              for n, c, d in FAM) + "</div>",
    "ให้ลูกแต่ละคนพูดชื่อสีและหน้าที่ของตัวเอง สีของแต่ละคนจะเป็นสีของแบรนด์วันเกิดของคนนั้นด้วย",
    "flex-direction:column;justify-content:center", "89px 144px")

POST = [("p18", "โปสเตอร์กล่องของชำร่วยงานแต่ง 159 บาท คอลเลกชัน SOI. 02"),
        ("p21", "โปสเตอร์ชุดที่รองแก้ว 4 ลาย 179 บาท คอลเลกชัน SOI. 02"),
        ("p23", "โปสเตอร์ราวหมีห้าตัว 349 บาท ห้าหมี Love"),
        ("p29", "โปสเตอร์ที่ห้อยกระเป๋าหมีหัวใจ 129 บาท ห้าหมี Love")]
S["products"] = section("products", P, I,
    '<div style="display:flex;flex-direction:column;gap:13px">' + h("สินค้า 30 แบบ จาก 6 แพตเทิร์น")
    + p("SOI. 02 สองแผ่นซ้าย ห้าหมี Love สองแผ่นขวา ทุกตัวมีโปสเตอร์ How-to และข้อความโพสต์ 5 ช่องทาง", 33, MU) + "</div>\n"
    + '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:21px">'
    + "".join(img(k, a, "width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:13px") for k, a in POST) + "</div>",
    "ราวหมีห้าตัวคือสินค้าตัวเอกของห้าหมี หมีห้าตัวต่อหูเข้าแก้มกันเป็นราว เหมือนบ้านเรา",
    "flex-direction:column;justify-content:center", "89px 144px")

KIDS = [("หัวหน้าร้าน", "ลูกหมีคนโต", SU, ["ดูแลกล่องเงินและ QR", "ทอนเงิน จดยอดขาย", "ส่งถุง พูดขอบคุณ"]),
        ("นักสาธิต", "ลูกหมีคนกลาง", MI, ["ต่อหนังให้ลูกค้าดู", "ให้ลูกค้าลองดึงว่าไม่หลุด", "ชวนดูชุดต่อเอง"]),
        ("ผู้ต้อนรับ", "ลูกหมีคนเล็ก", PI, ["ยิ้ม ทักทาย ยื่นการ์ด", "ชวนเด็ก ๆ ลองต่อ", "แจกสติกเกอร์หมี"])]
S["kids"] = section("kids", P, I,
    h("ลูกหมีขายของเอง", 68, MITR) + "\n" + '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:34px">'
    + "".join(card(f'<h3 style="font-family:{MITR};font-size:42px;font-weight:500">{t}</h3>'
                   + p(who, 26, CO) + f'<ul style="font-size:33px;line-height:1.4;color:{MU}">' + "".join(f"<li>{x}</li>" for x in li) + "</ul>",
                   top=c) for t, who, c, li in KIDS) + "</div>\n"
    + p("พ่อหรือแม่อยู่ที่บูธตลอด · ทำกะละ 45 นาที · ปิดยอดทุกเย็น ลูก ๆ ได้ 10% เข้ากระปุก", 33, MU),
    "หน้าที่ปรับตามวัยของลูกได้ ประโยคที่ใช้ทักทายและปิดการขายอยู่ใน Launch Kit")

CH = [("Facebook Page", "OCT. 26"), ("Instagram", "@oct26.crafted"), ("TikTok", "@oct26.crafted"),
      ("YouTube", "@oct26.crafted"), ("Shopee", "ร้าน OCT. 26")]
S["channels"] = section("channels", W, I,
    f'<div style="display:grid;grid-template-columns:1fr 1.618fr;gap:89px;align-items:center;width:100%">'
    + img("avatar", "รูปโปรไฟล์ OCT. 26", "width:100%;height:550px;object-fit:contain")
    + '<div style="display:flex;flex-direction:column;gap:34px">' + h("ห้าช่องทาง ชื่อเดียวกัน")
    + f'<table style="font-size:33px;color:{I}"><tr><th style="width:45%">ช่องทาง</th><th style="width:55%">ชื่อ</th></tr>'
    + "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in CH) + "</table>"
    + p("รูปโปรไฟล์ ปก และข้อความแนะนำร้านทำไว้ครบแล้ว รอเปิดบัญชีในชื่อพ่อหรือแม่", 26, MU) + "</div></div>",
    "ต้องเช็กก่อนว่าชื่อ oct26.crafted ยังว่างทุกช่องทาง ห้าหมีไม่ต้องเปิดบัญชีแยก ใช้หมวดในร้าน",
    "flex-direction:row;align-items:center")

import sys; sys.path.insert(0, os.path.dirname(HERE)); import brand as B
_T = B.event_totals()
NUM = [(f"{_T['units']:,}", "ชิ้น จากเศษหนังที่ซื้อมา"), (f"{_T['sales']:,.0f}", "บาท ถ้าขายหมดทั้งสามวัน"),
       (f"{_T['cost']:,.0f}", "บาท ต้นทุนของทั้งหมด")]
S["numbers"] = section("numbers", I, P,
    h("ของที่เตรียมไปบูธ", 68, MITR, P) + "\n" + '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:55px">'
    + "".join(f'<div style="display:flex;flex-direction:column;gap:8px"><p style="font-family:{JOST};font-size:140px;font-weight:500;line-height:1.1;color:{SU};font-variant-numeric:tabular-nums">{n}</p>'
              f'<p style="font-size:33px;color:{MUD}">{d}</p></div>' for n, d in NUM) + "</div>\n"
    + p("ต้นทุนรวมหนัง ค่าตัด ค่าบล็อกเฉลี่ย ค่าประกอบ แพ็ค และบรรจุภัณฑ์ ยังไม่รวมค่าบูธ ค่าพิมพ์ และค่าบล็อกที่ต้องสั่งใหม่", 26, MUD),
    "ตัวเลขมาจากราคาแนะนำในชุดเปิดตัว และสูตรต้นทุนเดียวกับ Google Sheet")

PLAN = [("14 ต.ค.", "เลือกชื่อ OCT. 26 สั่งทำบล็อกที่ยังไม่มี", ""), ("15 ต.ค.", "เปิดห้าช่องทาง ส่งไฟล์ไปร้านพิมพ์", ""),
        ("16–18 ต.ค.", "ตัดหนัง ลูก ๆ ช่วยประกอบ ถ่ายรูป ซ้อมขาย", ""), ("19–20 ต.ค.", "ลงสินค้า Shopee โพสต์ How-to วันละตัว", ""),
        ("21–22 ต.ค.", "แพ็คของ ติดราคา จัดบูธจำลองที่บ้าน", ""), ("23–25 ต.ค.", "ออกบูธครั้งแรกของ OCT. 26", "#FFE3F1"),
        ("26 ต.ค.", "วันเกิดเธอ และวันเกิด OCT. 26 สรุปยอด แบ่งเข้ากระปุกลูก ๆ", "#E3E8FB")]
S["plan"] = section("plan", P, I,
    h("เก้าวันถึงบูธ", 68, MITR) + "\n"
    + f'<table style="font-size:33px;color:{I}"><tr><th style="width:22%">วัน</th><th style="width:78%">ทำอะไร</th></tr>'
    + "".join(f'<tr{f' style="background:{bg}"' if bg else ""}><td>{d}</td><td>{t}</td></tr>' for d, t, bg in PLAN) + "</table>",
    "แผนรายวันแบบละเอียดอยู่ใน Launch Kit")

S["close"] = section("close", P, I,
    img("bear", "หมีห้าหมีกับหัวใจสีแดง", "width:233px;height:233px;object-fit:contain") + "\n"
    + h("สุขสันต์วันเกิดนะ แม่หมี", 110, MITR, TO, "h1", ";text-align:center") + "\n"
    + p("OCT. 26 เป็นของเธอ ขอบคุณที่เป็นหัวใจของบ้าน ที่ทำให้เราห้าคนต่อกันด้วยรัก", 42, None, ";text-align:center;max-width:1364px") + "\n"
    + f'<p style="font-family:{MITR};font-size:33px;font-weight:500;color:{CO};text-align:center">รักนะ จากพ่อหมี และลูกหมีสามตัว</p>',
    "ประโยคนี้เป็นร่าง แก้เป็นคำพูดของคุณเองได้ในโหมดแก้ไข แล้วให้ลูก ๆ ยื่นราวหมีห้าตัวชิ้นแรกให้แม่หมีตอนจบ",
    "flex-direction:column;justify-content:center;align-items:center")

DECK = {"v": 4, "createdOnFiles": {"v": 1, "at": "2026-10-14T16:05:00Z"}, "lists": "css", "title": "สุขสันต์วันเกิด 26.10",
        "order": ["cover", "gift", "name", "date", "arch", "heart", "story", "family", "products", "kids", "channels", "numbers", "plan", "close"],
        "sections": {"s1": {"description": "ของขวัญวันเกิด: แบรนด์ที่ตั้งชื่อตามวันเกิดของเธอ", "start": "cover"},
                     "s2": {"description": "ตัวตนของแบรนด์: OCT. 26 คอลเลกชัน SOI. 02 และซับแบรนด์ห้าหมี", "start": "name"},
                     "s3": {"description": "ร้านพร้อมขาย: สินค้า ลูก ๆ ขายของ ช่องทาง และตัวเลข", "start": "products"},
                     "s4": {"description": "แผนถึงวันออกบูธ และคำอวยพร", "start": "plan"}},
        "faces": {"mitr": {"family": "Mitr", "href": "https://fonts.googleapis.com/css2?family=Mitr:wght@400;500;600&display=swap"},
                  "ibm-plex-sans-thai": {"family": "IBM Plex Sans Thai", "href": "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;600&display=swap"},
                  "anuphan": {"family": "Anuphan", "href": "https://fonts.googleapis.com/css2?family=Anuphan:wght@500;600&display=swap"},
                  "jost": {"family": "Jost", "href": "https://fonts.googleapis.com/css2?family=Jost:wght@400;500&display=swap"}},
        "designSystems": []}

if __name__ == "__main__":
    assert set(S) == set(DECK["order"])
    for k, v in S.items():
        open(os.path.join(OUT, k + ".html"), "w").write(v)
    json.dump(DECK, open(os.path.join(HERE, "project", "deck.json"), "w"), ensure_ascii=False)
    print(len(S), "slides")
