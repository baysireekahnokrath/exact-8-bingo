"""Product research for OCT. 26 (15 Oct 2026): what sells, what bags cost elsewhere, and three crossbody
bags built from the current patterns with a cost and price for each.

Costs reuse the cost sheet: small pattern piece 2.784 THB, heart strap 6.212 THB, 20 s per joint at
50 THB/h. Hardware and packaging prices are estimates to check with suppliers.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from brand import PIECE_COST, JOINT_COST, PACK_COST, LOT_CAPACITY

# ---------------------------------------------------------------- what the research says
FINDINGS = [
    ("ของที่ใส่ชื่อได้ขายดีที่สุด", "บทวิเคราะห์ยอดขาย Etsy ปี 2026 พบว่าสินค้าหนังที่ปั๊มชื่อหรือตัวอักษรได้ขายดี เพราะกลายเป็นของขวัญทันที "
     "เช่น กล่องเครื่องประดับหนังใส่ชื่อ ที่มียอดขายกว่า 16,000 ชิ้น", "closo"),
    ("ของชิ้นเล็กคือหมวดหลัก", "ซองใส่บัตร กระเป๋าสตางค์บาง เคสโทรศัพท์ ซองอเนกประสงค์ และปกสมุด เป็นหมวดที่เจอซ้ำในรายการขายดี "
     "ราคากลุ่มนี้บน Etsy ประมาณ 25–80 ดอลลาร์", "etsy"),
    ("กระเป๋าสะพายข้างยังเป็นหมวดใหญ่", "หน้าเพจขายดีของ Etsy มีกระเป๋าสะพายข้างหนังแท้ทำมือ และกระเป๋าทรงเรขาคณิตหรือทรงพัซเซิลอยู่ราว 77–101 ดอลลาร์", "etsy"),
    ("ในไทย หนังแท้ใบเล็กเริ่มราว 890 บาท", "กระเป๋าสะพายข้างหนังแท้ใบเล็กของร้านไทย 890 บาท แบรนด์ไทยระดับกลาง 1,750–3,250 บาท "
     "ส่วนรุ่นที่ขายดีในบทความรีวิวหลายรุ่นเป็นหนัง PU ไม่ใช่หนังแท้", "th"),
    ("กระเป๋าจากเศษหนังมีที่ยืน", "แบรนด์ต่างประเทศขายกระเป๋าสะพายข้างจากเศษหนังหลังการผลิตที่ 54 ดอลลาร์ "
     "และชุดทำกระเป๋าเองแบบตัดชิ้นมาแล้วพร้อมอะไหล่ ขาย 85–110 ดอลลาร์", "upcycle"),
    ("ไม่เจอแบรนด์กระเป๋าหนังแบบต่อชิ้นไม่เย็บที่ชัดเจน", "ที่ใกล้ที่สุดคือ Loewe Puzzle ที่ขาย 2,750 ดอลลาร์ขึ้นไป และชุด DIY ทรงเรขาคณิต "
     "ช่องนี้ยังว่างอยู่สำหรับกระเป๋าที่ต่อจากชิ้นหนังแบบของเรา", "puzzle"),
]
CAVEAT = ("ข้อมูลมาจากการค้นเว็บวันที่ 15 ต.ค. 2569 บางแหล่งเป็นบล็อกหรือบทความรีวิวที่อาจไม่อัปเดต "
          "ไม่มีข้อมูลยอดขายจริงของ Shopee ไทย ก่อนตัดสินใจผลิต ควรเปิดหมวดขายดีใน Shopee และ Etsy ดูเองอีกครั้ง")

# (who, item, price, source key, note)
BAG_PRICES = [
    ("ร้านหนังไทยออนไลน์", "กระเป๋าสะพายข้างหนังแท้ใบเล็ก", "890 บาท", "foryou", "ใบเล็ก คาดเอวได้"),
    ("Tada Real Leather", "กระเป๋าสะพายข้างหนังแท้", "1,750 บาท", "salehere", "แบรนด์ไทย"),
    ("Vanchada", "กระเป๋าสะพายไหล่หนังแท้", "3,250 บาท (ลดจาก 5,500)", "vanchada", "แบรนด์ไทย เย็บมือ"),
    ("Royal Peasantry", "กระเป๋าสะพายข้างจากเศษหนัง", "54 ดอลลาร์", "royal", "เศษหนังหลังการผลิต"),
    ("Etsy หลายร้าน", "กระเป๋าหนังทรงพัซเซิล", "77–101 ดอลลาร์", "etsy_geo", "งานทำมือ"),
    ("POPSEWING", "ชุดทำกระเป๋าสะพายข้างทรงเรขาคณิต", "109.99 ดอลลาร์", "pop", "ชุด DIY ตัดชิ้นและอะไหล่มาให้"),
    ("Loewe", "Puzzle bag", "2,750 ดอลลาร์ขึ้นไป", "loewe", "แบรนด์หรู ต้นแบบของทรงพัซเซิล"),
]

SOURCES = {
    "closo": ("Best Selling Products on Etsy 2026", "https://closo.co/blogs/data-driven-insights-market-analytics/best-selling-products-on-etsy-2026-the-human-premium-era"),
    "etsy": ("Etsy: Top Selling Leather", "https://www.etsy.com/market/top_selling_leather"),
    "etsy_geo": ("Etsy: Leather Geometric Bag", "https://www.etsy.com/market/leather_geometric_bag"),
    "th": ("KTC: กระเป๋าสะพายข้างแบรนด์ไทย 2026", "https://www.ktc.co.th/article/shopping/fashion/bag-thai-brand-popular"),
    "foryou": ("For You Leather: กระเป๋าสะพายข้าง", "https://foryouleather.com/category/15/%E0%B8%81%E0%B8%A3%E0%B8%B0%E0%B9%80%E0%B8%9B%E0%B9%8B%E0%B8%B2%E0%B8%AB%E0%B8%99%E0%B8%B1%E0%B8%87%E0%B8%A7%E0%B8%B1%E0%B8%A7%E0%B9%81%E0%B8%97%E0%B9%89/%E0%B8%81%E0%B8%A3%E0%B8%B0%E0%B9%80%E0%B8%9B%E0%B9%8B%E0%B8%B2%E0%B8%AA%E0%B8%B0%E0%B8%9E%E0%B8%B2%E0%B8%A2%E0%B8%82%E0%B9%89%E0%B8%B2%E0%B8%87"),
    "salehere": ("Sale Here: กระเป๋าหนังแท้แบรนด์ไทย", "https://salehere.co.th/articles/recommend-thai-leather-bag-bands"),
    "vanchada": ("Vanchada", "https://www.vanchada.com/"),
    "royal": ("Royal Peasantry: Patchwork Crossbody", "https://royalpeasantry.com/products/patchwork-crossbody-messenger-bag"),
    "upcycle": ("Royal Peasantry: Patchwork Crossbody", "https://royalpeasantry.com/products/patchwork-crossbody-messenger-bag"),
    "pop": ("POPSEWING: Geometry Crossbody Bag Kit", "https://popsewing.com/products/geometry-crossbody-bag"),
    "puzzle": ("Harrods: LOEWE Puzzle Bag", "https://www.harrods.com/en-us/designers/loewe/puzzle-bag"),
    "loewe": ("Harrods: LOEWE Puzzle Bag", "https://www.harrods.com/en-us/designers/loewe/puzzle-bag"),
}

# ---------------------------------------------------------------- crossbody bags from the patterns
# A heart strap made of five 250 mm heart straps (one per person) replaces a bought strap.
HW = {
    "heart_strap": ("สายหัวใจ 250 มม. × 5 เส้น ต่อกันยาวประมาณ 120 ซม.", 5 * PIECE_COST["01-S250"] + 4 * JOINT_COST),
    "clips": ("ตะขอก้ามปูโลหะ 2 ตัว", 30.0),
    "magnet": ("กระดุมแม่เหล็ก 1 ชุด", 15.0),
    "pouch": ("ถุงผ้าหูรูดพิมพ์โลโก้", 25.0),
    "bought_strap": ("สายหนังสำเร็จพร้อมตะขอ (ถ้าซื้อ)", 200.0),
}

def bag_cost(pieces, code, joints):
    leather = pieces * PIECE_COST[code]
    hw = sum(HW[k][1] for k in ("heart_strap", "clips", "magnet", "pouch"))
    total = leather + joints * JOINT_COST + hw + PACK_COST
    return dict(leather=round(leather, 2), joints=round(joints * JOINT_COST, 2), hw=round(hw, 2),
                pack=round(PACK_COST, 2), total=round(total, 2),
                with_bought=round(total - HW["heart_strap"][1] - HW["clips"][1] + HW["bought_strap"][1], 2),
                minutes=round(joints * 20 / 60 + 10))

# key, name, pattern, module cm, size, parts [(panel, cols, rows)], joints, price, kit price, idea
BAGS = [
    ("box", "กล่องซอย", "04", 6.4, "19.2 × 12.8 × 6.4 ซม.",
     [("หน้า", 3, 2), ("หลัง", 3, 2), ("ก้น", 3, 1), ("ข้าง", 1, 2), ("ข้าง", 1, 2), ("ฝา", 3, 1)], 39, 1290, 890,
     "กระเป๋าทรงกล่องใบเล็ก ใส่มือถือ กระเป๋าตังค์ และกุญแจได้ ฝาเปิดด้านบนปิดด้วยแม่เหล็ก ทรงเดียวกับกล่องของขวัญที่ขายอยู่แล้ว แค่ใหญ่ขึ้น"),
    ("phone", "ซองมือถือวงกลม", "05", 6.4, "12.8 × 19.2 ซม.",
     [("หน้า", 2, 3), ("หลัง", 2, 3)], 22, 890, 690,
     "ซองใส่มือถือสะพายข้าง ใบเล็กสุด ใช้ชิ้นน้อยที่สุด เหมาะเป็นใบแรกที่ลองทำ และเป็นชุดทำเองที่ลูกค้าต่อเสร็จได้ในครึ่งชั่วโมง"),
    ("cube", "ลูกบาศก์ห้าหมี", "06", 6.0, "12 × 12 × 12 ซม.",
     [("หน้า", 2, 2), ("หลัง", 2, 2), ("ข้าง", 2, 2), ("ข้าง", 2, 2), ("ก้น", 2, 2), ("ฝา", 2, 2)], 42, 1190, 790,
     "กระเป๋าลูกบาศก์ใบเล็ก ทรงเล่นสนุก เหมาะกับห้าหมีและเด็กโต แขวนหมีหัวใจที่สายได้"),
]

def bag_rows():
    out = []
    for key, name, code, mod, size, parts, joints, price, kit, idea in BAGS:
        pieces = sum(c * r for _, c, r in parts)
        c = bag_cost(pieces, code, joints)
        out.append(dict(key=key, name=name, code=code, module=mod, size=size, parts=parts, pieces=pieces,
                        joints=joints, price=price, kit=kit, idea=idea, cost=c,
                        margin=(price - c["total"]) / price, per_lot=LOT_CAPACITY["เล็ก"] // pieces))
    return out

BAG_NOTES = [
    "ขนาดคิดจากชิ้นที่ต่อเป็นตารางตรง ระยะชิ้นละ 6.4 ซม. (แบบ 04 และ 05) และ 6 ซม. (แบบ 06) เหมือนกล่องที่ขายอยู่ ต้องทำต้นแบบจริงเพื่อวัดอีกครั้ง",
    "สายหัวใจห้าเส้นต่อกันคือหนึ่งเส้นต่อหนึ่งคนในบ้าน ต้องทดสอบว่ารับน้ำหนักได้ ถ้าไม่ผ่าน ใช้สายสำเร็จแทน ต้นทุนเพิ่มประมาณ 170 บาท",
    "ราคาอะไหล่ (ตะขอ แม่เหล็ก ถุงผ้า สายสำเร็จ) เป็นค่าประมาณ ต้องเช็กกับร้านอะไหล่ก่อน",
    "เศษเล็กหนึ่งล็อตตัดได้ 224 ชิ้น แต่ของไปบูธใช้ไปเกือบหมดแล้ว กระเป๋าจึงเป็นสินค้าของเศษล็อตถัดไป",
    "แพตเทิร์นจะออกแบบใหม่เร็ว ๆ นี้ ระบบเดิมยังใช้ได้ คือกำหนดระยะชิ้น แล้วนับจำนวนชิ้นและรอยต่อตามขนาดกระเป๋า",
]

# ---------------------------------------------------------------- products that tell the story
# (name, story link, stage, personalise, note)
STORY_PRODUCTS = [
    ("พวงกุญแจวันเกิด", "ระบบชื่อ เดือน. วัน ของทั้งครอบครัว", "ต่อเอง", "ปั๊มวันเกิดลูกค้า เช่น MAR. 23",
     "ของขวัญวันเกิดที่ใส่ชื่อได้ ตรงกับสิ่งที่ขายดีที่สุดในงานวิจัย"),
    ("ปกสมุดบันทึกประจำวัน", "Soi 2 From our root ของใช้ในชีวิตประจำวัน", "เย็บง่าย ครบชุด", "ปั๊มชื่อหรือปีบนปก",
     "สมุดที่ใช้ทุกวัน หมวดปกสมุดหนังติดรายการขายดี"),
    ("ซองใส่บัตรรุ่นแรกที่เย็บ", "โตไปด้วยกัน ชุดเย็บที่มีอุปกรณ์ครบ", "เย็บง่าย ครบชุด", "ตัวอักษรย่อ",
     "ซองใส่บัตรเป็นหมวดขายดีอันดับต้น ใช้เป็นชุดเย็บชุดแรก"),
    ("ที่แขวนกุญแจหน้าบ้าน", "ซอยบ้านเรา ป้ายบ้านเลขที่", "ต่อเอง", "ใส่ชื่อครอบครัว",
     "แขวนข้างประตู มีห้าตะขอสำหรับห้าคน"),
    ("หมีวันเกิด", "ห้าหมี หัวใจตรงกลาง", "ต่อเอง", "เขียนชื่อบนหัวใจ",
     "ของขวัญวันเกิดเด็ก ทำต่อจากหมีที่ขายอยู่"),
    ("ซองมือถือวงกลม", "ของใช้ทุกวัน Soi 2", "ชิ้นใหญ่", "เลือกสีชิ้นเองได้",
     "กระเป๋าใบแรก ใช้ชิ้นน้อยที่สุด ดูแบบด้านบน"),
    ("ต้นไม้ครอบครัว", "From our root รากของบ้าน", "งานติดตั้ง", "ใส่ชื่อทุกคนในบ้านลูกค้า",
     "งานแขวนผนังจากชิ้นหนัง ใบไม้หนึ่งใบต่อหนึ่งคน ขายเป็นงานสั่งทำ"),
    ("ผนังซอย", "ป้ายซอยของแบรนด์", "งานติดตั้ง", "ใส่ชื่อร้านของลูกค้า",
     "ผนังหรือฉากกั้นจากชิ้นหนังหลายร้อยชิ้น สำหรับคาเฟ่และร้านค้า"),
]

if __name__ == "__main__":
    for r in bag_rows():
        print(r["name"], r["pieces"], "pcs", r["joints"], "joints", r["cost"], f"margin {r['margin']:.0%}", "per lot", r["per_lot"])
