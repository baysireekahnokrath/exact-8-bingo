"""Build ideas/index.html: 20 no-sew product ideas from the rev 20261014 patterns."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from extract import load
from generate import svg_d, SRC, final_slits

READY, PROTO, EXTRA = ("ok", "ลองได้เลย"), ("mid", "ต้องลองต้นแบบ"), ("ext", "ต้องมีชิ้นเสริม")

GROUPS = [
 ("01", "Bear head", "slit 17.91 แนวตั้งกับแนวนอน · หูของหมีอีกตัวเสียบได้ (คอหู 17.41)", [
  (1, "ที่เก็บสายชาร์จหมี", [("01", 1)], "พันสายรอบหัวหมี แล้วเหน็บปลั๊กทั้งสองปลายเข้า slit ใช้ชิ้นเดียว ไม่ต้องมีชิ้นอื่น", "104 × 104 mm", "นักเรียน คนทำงาน ของแถมร้านมือถือ", READY),
  (2, "ที่คั่นหนังสือเหน็บมุมหน้า", [("01", 1)], "slit แนวตั้งกับแนวนอนตั้งฉากกันพอดีกับมุมกระดาษ เหน็บมุมหน้าหนังสือเข้าไป หัวหมีเอียงโผล่ที่มุม", "104 × 104 mm", "ร้านหนังสือ ของขวัญวันครู", PROTO),
  (3, "ป้ายชื่อติดกระเป๋านักเรียน", [("01", 1), ("01-S", 1)], "สายหัวใจร้อยผ่าน slit ทั้งสองแล้วคล้องหูกระเป๋า ปั๊มชื่อเด็กไว้ด้านหลัง", "104 mm + สาย 250", "ผู้ปกครองช่วงเปิดเทอม", EXTRA),
  (4, "ห่วงผ้าเช็ดปากหมี", [("01", 1), ("สายห่วง", 1)], "สายหนังสั้นร้อย slit ทั้งสองเป็นห่วง รัดผ้าเช็ดปากหรือช้อนส้อม", "104 mm", "ร้านอาหาร งานวันเกิดเด็ก", EXTRA),
 ]),
 ("02", "Pinwheel", "slot ยาวครึ่งขอบพับพอดี เหมาะกับการพับกลีบเข้ากลางแบบกังหัน", [
  (5, "ซองอั่งเปาพับกังหัน", [("02", 1)], "พับ 4 กลีบเข้ากลาง ปลายกลีบขัดกันแบบกังหัน ใส่ธนบัตรที่พับให้เหลือไม่เกิน 54 × 54 mm", "54 × 54 mm เมื่อพับ", "ของขวัญองค์กรช่วงตรุษจีน", PROTO),
  (6, "ซองใส่เครื่องประดับ", [("02", 1)], "พับแบบเดียวกัน ใส่แหวนหรือต่างหู แทนกล่องกระดาษ", "54 × 54 mm", "ร้านเครื่องประดับ งานแต่ง", PROTO),
  (7, "ซองการ์ดข้อความติดของขวัญ", [("02", 1)], "ใส่การ์ดขนาด 5 × 5 cm แล้วผูกติดกล่องของขวัญหรือช่อดอกไม้", "54 × 54 mm", "ร้านดอกไม้ ร้านของขวัญ", PROTO),
 ]),
 ("03", "Capsule cross", "ขอบพับ 45 mm · คอปีก 22.0 กับ slit 22.5", [
  (8, "กล่องแหวนขอแต่งงาน", [("03", 6)], "ต่อ 6 ชิ้นเป็นลูกบาศก์ ฝาถอดเปิดได้ทีละรอยต่อ ใช้หนังเกรดพรีเมียม", "45 × 45 × 45 mm", "ร้านเพชร ลูกค้าขอแต่งงาน", PROTO),
  (9, "ลูกเต๋าหนัง", [("03", 6)], "ต่อ 6 ชิ้นเป็นลูกบาศก์ ปั๊มจุดหรือตัวเลขบนแต่ละด้าน", "45 mm", "คาเฟ่บอร์ดเกม ร้านของเล่น", PROTO),
  (10, "ซองใส่ AirTag", [("03", 2)], "ประกบ 2 ชิ้นหน้าหลัง แล้วต่อรอยต่อทั้ง 4 ขอบเป็นซองปิด", "45 × 45 mm", "คนเดินทาง ของขวัญผู้ชาย", PROTO),
  (11, "ชุดตัวต่อหนังสำหรับเด็ก", [("03", 24)], "ชิ้นหลายสีต่อกันได้ทุกขอบ เด็กต่อเป็นลูกบาศก์ สายโซ่ หรือแผ่น ได้เอง", "ชุด 24 ชิ้น", "โรงเรียน ร้านของเล่นเสริมพัฒนาการ", PROTO),
 ]),
 ("04", "Rounded square", "ขอบพับ 63.6 mm · คอปีก 29.5 กับ slit 30.0 · ต่อกับแบบ 05 ได้", [
  (12, "ที่ใส่ปากกาทรงมงกุฎ", [("04", 5)], "ต่อ 5 ชิ้นเป็นกล่องเปิดด้านบน ปีกสามเหลี่ยมของผนังตั้งขึ้นเป็นยอดมงกุฎ", "63.6 mm + ยอด", "ออฟฟิศ ของขวัญองค์กร", PROTO),
  (13, "แผ่นรองจานลายข้าวหลามตัด", [("04", 12)], "ต่อเป็นแผ่น 3 × 4 ชิ้น ปีกสามเหลี่ยมซ้อนกันเป็นลาย ถ้าต่อ 2 × 8 ชิ้นได้ผ้าปูกลางโต๊ะ", "ประมาณ 27 × 36 cm", "ร้านอาหาร โฮมเดคอร์", PROTO),
 ]),
 ("05", "Circle", "ขอบพับ 63.6 mm · คอปีก 29.5 กับ slit 30.0 · ต่อกับแบบ 04 ได้", [
  (14, "ปลอกแก้วกาแฟ", [("05", 4)], "ต่อ 4 ชิ้นเป็นวงรอบแก้ว ปั๊มโลโก้ร้านได้", "รอบวง 255 mm (แก้ว 12 oz)", "คาเฟ่", PROTO),
  (15, "ที่รองแก้วสองชั้นไส้ไม้ก๊อก", [("05", 2), ("ไม้ก๊อก", 1)], "ประกบ 2 ชิ้นโดยมีแผ่นไม้ก๊อกอยู่ข้างใน ต่อรอยต่อทั้ง 4 ขอบ", "63.6 mm (แก้วช็อตหรือเอสเปรสโซ)", "คาเฟ่ บาร์", EXTRA),
  (16, "กระเป๋าเหรียญจิ๋ว", [("05", 2)], "ประกบ 2 ชิ้น ต่อ 3 ขอบ เหลือขอบสุดท้ายไว้เป็นปากซองที่เปิดปิดได้", "63.6 mm", "วัยรุ่น ของที่ระลึก", PROTO),
  (17, "กล่องของขวัญสลับลาย", [("04", 3), ("05", 3)], "ลูกบาศก์ที่ใช้ปีกแหลมของ 04 สลับกับปีกโค้งของ 05 ต่อกันได้เพราะขอบพับ คอปีก และ slit เท่ากัน", "63.6 mm", "ร้านของขวัญ ของขวัญองค์กร", PROTO),
 ]),
 ("06", "Soft cross", "ขอบพับ 60 mm · คอปีก 17.0 กับ slit 17.5", [
  (18, "กล่องของชำร่วยงานแต่ง", [("06", 6)], "ต่อ 6 ชิ้นเป็นลูกบาศก์ ใส่ขนม สบู่ หรือเทียนจิ๋ว สั่งเป็นจำนวนมากได้", "60 × 60 × 60 mm", "งานแต่ง ออแกไนเซอร์", PROTO),
  (19, "ที่ใส่แปรงแต่งหน้า", [("06", 5)], "ต่อ 5 ชิ้นเป็นกล่องเปิดด้านบน ขอบกลีบโค้งนุ่ม", "60 mm", "ร้านเครื่องสำอาง ของขวัญผู้หญิง", PROTO),
  (20, "ของแขวนต้นคริสต์มาส", [("06", 6), ("ริบบิ้น", 1)], "ลูกบาศก์ 6 ชิ้น ใช้หนังหลายสี ผูกริบบิ้นไว้แขวน", "60 mm", "ร้านค้าช่วงปลายปี", EXTRA),
 ]),
]

# n -> (assembly actions at the factory, extra parts note)
PROD = {
 1: (0, "-"), 2: (0, "-"), 3: (2, "สาย 01-S 250 mm"), 4: (2, "สาย 01-S 200 mm"),
 5: (4, "-"), 6: (4, "-"), 7: (4, "-"),
 8: (12, "-"), 9: (12, "-"), 10: (4, "-"), 11: (0, "ลูกค้าต่อเอง · ถุงหรือกล่องใส่ชุด"),
 12: (8, "-"), 13: (17, "-"),
 14: (4, "-"), 15: (4, "แผ่นไม้ก๊อก 60 × 60 mm"), 16: (3, "-"), 17: (12, "-"),
 18: (12, "-"), 19: (8, "-"), 20: (12, "ริบบิ้น"),
}
STRAP = {"01-S": (26.0, 200 * 22), "01-S 250": (32.5, 250 * 22)}   # heart strap: net cm2, nesting box mm2

PICKS = [
 (1, "ใช้หนังชิ้นเดียว ไม่ต้องมีอุปกรณ์เสริม ต้นทุนต่ำที่สุด ขายเป็นของแถมได้"),
 (5, "ใช้หนังชิ้นเดียว และมีช่วงขายชัดเจน ของขวัญองค์กรสั่งทีละมาก"),
 (18, "งานแต่งสั่งเป็นจำนวนมาก ใช้ die ชิ้นเดียว"),
 (11, "ไม่มีใครทำ เหมาะกับ workshop และโรงเรียน ต่อยอดเป็นแบรนด์ของเล่นได้"),
 (8, "ราคาขายต่อชิ้นสูงที่สุดในรายการ"),
]

def minis():
    out = {}
    for p in load(SRC):
        W, H = p["W"], p["H"]
        lines = "".join(f'<line x1="{a[0]:.1f}" y1="{H-a[1]:.1f}" x2="{b[0]:.1f}" y2="{H-b[1]:.1f}"/>' for a, b in ((s["a"], s["b"]) for s in final_slits(p)))
        out[p["code"]] = (f'<svg viewBox="-3 -3 {W+6:.1f} {H+6:.1f}" aria-hidden="true">'
                          f'<path class="cut" d="{svg_d(p["segs"], H)}"/><g class="slit">{lines}</g></svg>')
    return out

def areas():
    from extract import sample
    from shapely.geometry import Polygon
    out = {}
    for p in load(SRC):
        net = Polygon(sample(p["segs"], 200)).area / 100           # cm2
        box = (p["W"] + 3) * (p["H"] + 3)                          # mm2, 3 mm die gap
        out[p["code"]] = (net, box)
    out.update(STRAP)
    return out

def prod_rows(byn, ar):
    import json
    rows, data = [], []
    for code, name, rule, items in GROUPS:
        for n, title, parts, how, size, who, st in items:
            pcs = [(c, q) for c, q in parts if c in ar and c != "01-S"]
            if n == 3:
                pcs.append(("01-S 250", 1))
            if n == 4:
                pcs.append(("01-S", 1))
            net = sum(ar[c][0] * q for c, q in pcs)
            box = sum(ar[c][1] * q for c, q in pcs) / 92903          # sq ft before defects
            strikes = sum(q for c, q in pcs)
            joints, extra = PROD[n]
            data.append({"n": n, "box": round(box, 4), "strikes": strikes, "joints": joints})
            pcs_txt = " + ".join(f"{c}×{q}" for c, q in pcs)
            rows.append(f'<tr data-n="{n}"><td class="num">{n:02d}</td><td>{title}</td><td class="mono">{pcs_txt}</td>'
                        f'<td class="num">{net:.0f}</td><td class="num sq"></td><td class="num">{strikes}</td><td class="num">{joints}</td>'
                        f'<td class="num cost"></td><td>{extra}</td></tr>')
    return "".join(rows), json.dumps(data)

def main():
    m = minis()
    byn = {}
    sections = []
    for code, name, rule, items in GROUPS:
        cards = []
        for n, title, parts, how, size, who, (cls, status) in items:
            byn[n] = title
            chips = "".join(
                f'<span class="chip">{m[c] if c in m else ""}<b>{c}</b> × {q}</span>' for c, q in parts)
            cards.append(f'''<article class="card" id="idea{n}">
        <div class="head"><span class="num">{n:02d}</span><span class="pill {cls}">{status}</span></div>
        <h3>{title}</h3>
        <div class="chips">{chips}</div>
        <p>{how}</p>
        <dl><div><dt>ขนาด</dt><dd>{size}</dd></div><div><dt>ขายให้</dt><dd>{who}</dd></div></dl>
      </article>''')
        sections.append(f'''<section class="group">
    <div class="ghead"><span class="gthumb">{m[code]}</span><div><h2>{code} · {name}</h2><p class="rule">{rule}</p></div></div>
    <div class="cards">
      {"".join(cards)}
    </div>
  </section>''')
    ar = areas()
    byn0 = {n: t for _, _, _, items in GROUPS for n, t, *_ in items}
    prows, pdata = prod_rows(byn0, ar)
    dies = []
    for code, label in [("01", "01 Bear head"), ("01-S", "01-S สายหัวใจ"), ("02", "02 Pinwheel"), ("03", "03 Capsule cross"),
                        ("04", "04 Rounded square"), ("05", "05 Circle"), ("06", "06 Soft cross")]:
        used = [n for _, _, _, items in GROUPS for n, t, parts, *_ in items
                if any(c == code for c, q in parts) or (code == "01-S" and n in (3, 4))]
        net = ar[code][0]
        dies.append(f'<tr><td>{label}</td><td class="num">{net:.1f}</td><td class="num">{len(used)}</td><td class="mono">{", ".join(f"{u:02d}" for u in used)}</td></tr>')
    picks = "".join(f'<li><a href="#idea{n}"><b>{n:02d} {byn[n]}</b></a> <span>{why}</span></li>' for n, why in PICKS)
    t = open(os.path.join(HERE, "template.html")).read()
    t = (t.replace("__PICKS__", picks).replace("__GROUPS__", "\n  ".join(sections))
          .replace("__PRODROWS__", prows).replace("__PRODDATA__", pdata).replace("__DIES__", "".join(dies)))
    open(os.path.join(HERE, "index.html"), "w").write(t)
    print("ok", len(t))

if __name__ == "__main__":
    main()
