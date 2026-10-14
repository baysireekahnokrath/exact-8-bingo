"""Five alternative brand directions: cool, luxury, sustainability.

Same products, same dies, same family. What changes is the name, the look and the price level.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from brand import PRODUCTS

PREMIUM_PACK = 40.0   # rigid box, tissue, foil sticker: estimate per item, replaces the 5 THB bag

def hero(n, price):
    p = next(q for q in PRODUCTS if q["n"] == n)
    cost = round(p["cost"] - 5 + PREMIUM_PACK, 2)
    return dict(n=n, name=p["name"], price=price, cost=cost, margin=(price - cost) / price, base=p["price"])

OPTIONS = [
 dict(key="remnant", name="REMNANT", th="เรมแนนท์", mean="Remnant แปลว่า เศษที่เหลือ บอกตรง ๆ ว่าทำจากเศษหนัง แต่พูดแบบแบรนด์แฟชั่น",
      tag_en="Nothing wasted. Nothing stitched.", tag_th="ไม่ทิ้ง ไม่เย็บ",
      vibe="Quiet luxury แบบมินิมอล ขาวงาช้าง ดำ และสีคอนยัค เหมือนร้านเครื่องหนังในแกลเลอรี",
      story="เศษหนังเกรดดีจากโรงงาน คัดทีละชิ้น ทุกชิ้นมีหมายเลขกำกับ ครอบครัวเป็นคนคัดและประกอบ เล่าเรื่องลูก ๆ ได้ในโพสต์เบื้องหลัง ไม่ต้องอยู่บนโลโก้",
      who="คนทำงานอายุ 25–40 ที่ซื้อของขวัญราคา 300–900 บาท ร้านคอนเซปต์สโตร์",
      heroes=[hero(8, 690), hero(10, 390), hero(29, 490)],
      pal=[("Ink", "#151311"), ("Bone", "#ECE6DC"), ("Cognac", "#8C4A26"), ("Ash", "#8F877C")],
      bg="#151311", fg="#ECE6DC", acc="#B8693A",
      font=("alt/BodoniModa-Medium.ttf", "Bodoni Moda"), thfont=("alt/NotoSerifThai-Regular.ttf", "Noto Serif Thai"),
      tracking=.32, handle="remnant.bkk",
      risk="คำว่า Remnant มีคนใช้ตั้งชื่อร้านอยู่บ้างในต่างประเทศ ต้องเติมคำให้เป็นของเรา เช่น REMNANT BKK และค้นเครื่องหมายการค้าก่อน"),
 dict(key="unsewn", name="UNSEWN", th="อันโซน", mean="Unsewn แปลว่า ไม่ได้เย็บ คือจุดขายที่ไม่มีใครเหมือน ทั้งชิ้นไม่มีด้ายสักเส้น",
      tag_en="Leather, held by design.", tag_th="หนังแท้ ยึดกันด้วยการออกแบบ",
      vibe="Craft luxury สีโอ๊ต เขียวมะกอก และสีแทน ตัวอักษรเซริฟบางแบบสตูดิโอญี่ปุ่นหรือสแกนดิเนเวีย",
      story="งานออกแบบล้วน ๆ ปีกกับร่องที่ต่างกันครึ่งมิลลิเมตรคือเทคนิคของพ่อ ทุกชิ้นถอดซ่อมได้ เปลี่ยนชิ้นเดียวไม่ต้องทิ้งทั้งอัน ลูก ๆ เป็นทีมประกอบ",
      who="สายดีไซน์และของแต่งบ้าน ร้านเฟอร์นิเจอร์ คาเฟ่ ของขวัญองค์กรระดับพรีเมียม",
      heroes=[hero(17, 590), hero(12, 490), hero(14, 350)],
      pal=[("Olive", "#3E4A3D"), ("Oat", "#E9E2D3"), ("Tan", "#B9875A"), ("Clay", "#9A5B3F")],
      bg="#E9E2D3", fg="#3E4A3D", acc="#B9875A",
      font=("alt/CormorantGaramond-Medium.ttf", "Cormorant Garamond"), thfont=("alt/NotoSerifThai-Regular.ttf", "Noto Serif Thai"),
      tracking=.28, handle="unsewn.studio",
      risk="อ่านออกเสียงยากสำหรับคนไทยบางคน ต้องใส่คำอ่านภาษาไทยในโลโก้รอง"),
 dict(key="interlock", name="INTERLOCK", th="อินเตอร์ล็อก", mean="Interlock แปลว่า ล็อกเข้าหากัน คือกลไกของทุกชิ้นในร้าน ฟังดูเท่และเป็นเทคนิค",
      tag_en="Cut. Lock. Done.", tag_th="ตัด ล็อก จบ",
      vibe="Cool และสตรีท สีดำ เทาคอนกรีต และส้มสัญญาณ ฟอนต์หนาแบบโปสเตอร์ ใช้เส้นตัดของบล็อกเป็นลายกราฟิก",
      story="โชว์งานออกแบบแบบวิศวกร เส้นตัดสีดำ ร่องสีแดง ขนาดเป็นมิลลิเมตร ขายชุดต่อเองให้คนชอบ DIY ลูก ๆ ถ่ายคลิปต่อแข่งเวลาลง TikTok",
      who="วัยรุ่นถึงวัยทำงาน สาย DIY ของเล่นดีไซน์ คนชอบงานกราฟิก",
      heroes=[hero(11, 890), hero(9, 290), hero(10, 350)],
      pal=[("Carbon", "#141517"), ("Concrete", "#C9C7C2"), ("Signal", "#FF5A1F"), ("Paper", "#F3F2EE")],
      bg="#141517", fg="#F3F2EE", acc="#FF5A1F",
      font=("alt/Archivo-ExtraBold.ttf", "Archivo"), thfont=("alt/ChakraPetch-SemiBold.ttf", "Chakra Petch"),
      tracking=.04, handle="interlock.lab",
      risk="Interlock เป็นคำทั่วไปที่ใช้ในหลายวงการ จดเครื่องหมายเดี่ยว ๆ ยาก ควรใช้คู่กับโลโก้หรือเป็น INTERLOCK LAB"),
 dict(key="aftercut", name="AFTERCUT", th="อาฟเตอร์คัท", mean="After cut คือสิ่งที่เหลือหลังการตัด แบรนด์ที่เกิดจากเศษหลังการตัดกระเป๋าและรองเท้า",
      tag_en="Made from what's left after the cut.", tag_th="ทำจากสิ่งที่เหลือหลังการตัด",
      vibe="Sustainability ชัดเจน สีเขียวป่า หิน และทองแดง สัญลักษณ์ใบไม้ที่มีร่องตัดเป็นเส้นใบ",
      story="นับเป็นตัวเลขได้ว่าช่วยเศษหนังไว้กี่กิโลแล้ว บอกบนป้ายทุกชิ้น วัสดุเดียว ไม่มีด้าย ไม่มีกาว ครอบครัวเป็นคนเก็บ คัด และประกอบ",
      who="สายรักษ์โลก คาเฟ่และร้านที่ทำเรื่องยั่งยืน ของขวัญองค์กรสาย ESG",
      heroes=[hero(14, 290), hero(15, 220), hero(30, 290)],
      pal=[("Forest", "#1F3A2E"), ("Stone", "#DDD8CC"), ("Copper", "#B0703C"), ("Moss", "#6E7F5A")],
      bg="#1F3A2E", fg="#DDD8CC", acc="#C9844A",
      font=("alt/Syne-Bold.ttf", "Syne"), thfont=("alt/Anuphan-Medium.ttf", "Anuphan"),
      tracking=.08, handle="aftercut.th",
      risk="เรื่องรักษ์โลกต้องมีตัวเลขจริง เช่น ซื้อเศษมากี่กิโล ใช้ไปกี่กิโล ห้ามเคลมเกินจริง"),
 dict(key="quint", name="QUINT", th="ควินท์", mean="Quint มาจากภาษาละติน แปลว่า ห้า ยังเป็นเรื่องครอบครัวห้าคน แต่เล่าแบบแบรนด์หรู คนรู้ความหมายเฉพาะคนที่ถาม",
      tag_en="Five hands. One craft.", tag_th="ห้ามือ หนึ่งงานฝีมือ",
      vibe="Heritage luxury สีน้ำเงินเที่ยงคืน แชมเปญ และเบอร์กันดี ตัวอักษรโรมันคลาสสิก โลโก้เป็นร่องห้าเส้นรอบวง",
      story="ร่องห้าเส้นในโลโก้คือคนห้าคนในบ้าน ใช้ได้ทั้งของขวัญแต่งงานและองค์กร ยังเป็นของขวัญถึงภรรยาได้เหมือนเดิม แค่พูดเบากว่า",
      who="คู่แต่งงาน งานหมั้น ของขวัญผู้ใหญ่ ของขวัญองค์กรสั่งจำนวนมาก",
      heroes=[hero(8, 890), hero(18, 290), hero(13, 990)],
      pal=[("Midnight", "#1B2233"), ("Champagne", "#E8DCC4"), ("Burgundy", "#6E2233"), ("Gold", "#B89B62")],
      bg="#1B2233", fg="#E8DCC4", acc="#B89B62",
      font=("alt/Cinzel-Medium.ttf", "Cinzel"), thfont=("alt/NotoSerifThai-Regular.ttf", "Noto Serif Thai"),
      tracking=.3, handle="quint.atelier",
      risk="ชื่อสั้นและหรู แต่คนไทยไม่รู้ความหมาย ต้องเล่าเรื่องห้าคนในทุกจุดขาย ทั้งป้ายและการ์ด"),
]
