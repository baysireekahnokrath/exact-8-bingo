"""Build alternatives/index.html: five cool / luxury / sustainability directions side by side."""
import html, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from options import OPTIONS, PREMIUM_PACK

E = html.escape

CSS = """
:root{
  /* Layout: a lookbook. One full-width brand board per option, details in a two-column spec sheet below it. */
  --bg:#F1EEE8;--paper:#FBFAF7;--ink:#1A1814;--muted:#6B655C;--line:#DDD7CD;--accent:#8C4A26;--chip:#E8E3DA;
  --display:"Noto Serif Thai","Bodoni Moda",Georgia,serif;
  --body:"Anuphan","IBM Plex Sans Thai",system-ui,sans-serif;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#141311;--paper:#1D1B18;--ink:#EEEAE2;--muted:#ABA397;--line:#34302A;--accent:#D08B5C;--chip:#2A2723;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#141311;--paper:#1D1B18;--ink:#EEEAE2;--muted:#ABA397;--line:#34302A;--accent:#D08B5C;--chip:#2A2723;color-scheme:dark}
*{box-sizing:border-box}
img{max-width:100%;height:auto;display:block}
body{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.65;margin:0;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:0 72px}
.wrap{max-width:980px;margin:0 auto;display:flex;flex-direction:column;gap:56px}
h1,h2,h3{font-family:var(--display);font-weight:500;line-height:1.25;text-wrap:balance;margin:0}
h1{font-size:clamp(30px,6.5vw,46px)}h2{font-size:clamp(24px,5vw,32px)}h3{font-size:18px}
p{margin:0}
a{color:var(--accent)}
.eyebrow{font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}
.lead{font-size:18px;color:var(--muted);max-width:64ch}
nav.top{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);border-bottom:1px solid var(--line);
  margin:0 calc(-1*max(16px,env(safe-area-inset-left,0px)));padding:10px max(16px,env(safe-area-inset-left,0px));display:flex;gap:6px;overflow-x:auto}
nav.top a{flex:none;font-size:14px;letter-spacing:.06em;text-decoration:none;color:var(--ink);background:var(--chip);border-radius:99px;padding:5px 13px}
nav.top a:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.opt{display:flex;flex-direction:column;gap:18px;scroll-margin-top:64px}
.head{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.num{font-family:var(--display);font-size:15px;color:var(--muted);font-variant-numeric:tabular-nums}
.boards{display:grid;grid-template-columns:minmax(0,2.14fr) minmax(0,1fr);gap:12px}
.boards img{border-radius:6px;width:100%}
.spec{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px}
.spec>div{background:var(--paper);border:1px solid var(--line);border-radius:6px;padding:16px;display:flex;flex-direction:column;gap:8px;min-width:0}
.k{font-size:12.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.sw{display:flex;gap:8px;flex-wrap:wrap}.sw span{display:flex;align-items:center;gap:6px;font-size:13px}
.sw i{width:22px;height:22px;border-radius:50%;border:1px solid var(--line);display:inline-block}
.tbl{overflow-x:auto;border:1px solid var(--line);border-radius:6px;background:var(--paper)}
table{border-collapse:collapse;width:100%;font-size:14.5px}
th,td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-weight:500;font-size:12.5px;letter-spacing:.06em;color:var(--muted);white-space:nowrap}
td.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
tr:last-child td{border-bottom:0}
.risk{font-size:14px;color:var(--muted);border-left:3px solid var(--accent);padding-left:12px}
.pick{background:var(--paper);border:1px solid var(--line);border-radius:6px;padding:20px;display:flex;flex-direction:column;gap:10px}
ul,ol{margin:0;padding-left:1.3em}
@media (max-width:640px){.boards,.spec{grid-template-columns:minmax(0,1fr)}.boards img:last-child{max-width:260px}}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anuphan:wght@400;500&family=Noto+Serif+Thai:wght@400;500&display=swap">')

def option(i, o):
    rows = "".join(
        f'<tr><td>{E(h["name"])}</td><td class="n">{h["base"]}</td><td class="n"><b>{h["price"]:,}</b></td>'
        f'<td class="n">{h["cost"]:.0f}</td><td class="n">{h["margin"]:.0%}</td></tr>' for h in o["heroes"])
    sw = "".join(f'<span><i style="background:{hx}"></i>{E(n)} <span class="k" style="letter-spacing:0">{hx}</span></span>' for n, hx in o["pal"])
    return f"""<section class="opt" id="{o['key']}">
<div class="head"><span class="num">{i:02d}</span><h2>{E(o['name'])}</h2><span style="color:var(--muted)">{E(o['th'])}</span></div>
<div class="boards"><img src="img/{o['key']}-board.png" alt="โลโก้ {E(o['name'])} บนสีหลักของแบรนด์" width="1200" height="720">
<img src="img/{o['key']}-tag.png" alt="ป้ายห้อยสินค้า {E(o['name'])} ตัวอย่างกับ{E(o['heroes'][0]['name'])}" width="560" height="860"></div>
<div class="spec">
<div><span class="k">ความหมาย</span><p>{E(o['mean'])}</p><p><b>{E(o['tag_en'])}</b><br>{E(o['tag_th'])}</p></div>
<div><span class="k">ลุค</span><p>{E(o['vibe'])}</p><div class="sw">{sw}</div>
<p class="k" style="letter-spacing:.04em;text-transform:none">ฟอนต์ {E(o['font'][1])} · ภาษาไทย {E(o['thfont'][1])} · @{E(o['handle'])}</p></div>
<div><span class="k">เรื่องครอบครัวอยู่ตรงไหน</span><p>{E(o['story'])}</p></div>
<div><span class="k">ขายใคร</span><p>{E(o['who'])}</p></div>
</div>
<div class="tbl"><table><thead><tr><th>สินค้าหลัก</th><th>ราคาห้าหมี</th><th>ราคาแบรนด์นี้</th><th>ต้นทุน</th><th>กำไร</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="risk">{E(o['risk'])}</p>
</section>"""

def page():
    nav = "".join(f'<a href="#{o["key"]}">{E(o["name"])}</a>' for o in OPTIONS)
    comp = [("REMNANT", "มินิมอล หรูเงียบ", "เล่าในโพสต์เบื้องหลัง", "กลาง", "300–700"),
            ("UNSEWN", "งานฝีมือ ดีไซน์", "ลูก ๆ เป็นทีมประกอบ", "กลาง", "350–600"),
            ("INTERLOCK", "เท่ สตรีท DIY", "คลิปลูกต่อแข่งเวลา", "ยาก ต้องใช้คู่โลโก้", "290–890"),
            ("AFTERCUT", "รักษ์โลกชัดที่สุด", "ครอบครัวเก็บและคัดเศษ", "กลาง", "220–290"),
            ("QUINT", "หรูคลาสสิก", "ห้าร่อง = ห้าคนในบ้าน", "น่าจะง่ายกว่า ไม่ใช่คำทั่วไป", "290–990"),
            ("KHAD", "เท่แบบไทยร่วมสมัย", "คำที่พูดกันในบ้าน", "กลาง ต้องจดคู่โลโก้", "259–290"),
            ("SANSFIL", "หรูแบบผู้หญิง", "แบรนด์ที่ตั้งให้แม่หมี", "กลาง", "290–790"),
            ("POINT FIVE", "เท่แบบวิศวกร", "ห้า = ห้าคน, 0.5 = งานของพ่อ", "กลาง ต้องค้นหมวดเครื่องหนัง", "390–790"),
            ("PRANEET", "หรูแบบไทย", "ดอกห้ากลีบ = ห้าคน", "ยาก คำทั่วไป ต้องจดคู่โลโก้", "190–890"),
            ("MONO/HIDE", "ยั่งยืนแบบดิบ", "ลูก ๆ แกะชิ้นให้ดูว่ามีแต่หนัง", "กลาง ต้องจดคู่ HIDE", "250–450")]
    crow = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td><td class='n'>{e}</td></tr>" for a, b, c, d, e in comp)
    opts = ('<p class="eyebrow">ชุดที่ 1</p>' + "".join(option(i, o) for i, o in enumerate(OPTIONS[:5], 1))
            + '<p class="eyebrow">ชุดที่ 2</p>' + "".join(option(i, o) for i, o in enumerate(OPTIONS[5:], 6)))
    return f"""<title>ทางเลือกแบรนด์ Luxury</title><meta name="claude:viewport-fit-sides" content="cover">{FONTS}<style>{CSS}</style>
<nav class="top" aria-label="ทางเลือก">{nav}<a href="#pick">คำแนะนำ</a></nav>
<div class="wrap">
<header style="padding-top:28px;display:flex;flex-direction:column;gap:14px">
<span class="eyebrow">Brand directions · 14 ต.ค. 2569</span>
<h1>สิบทางเลือก แนวเท่ หรู และยั่งยืน</h1>
<p class="lead">สินค้า บล็อกตัด และครอบครัวเดิมทั้งหมด สิ่งที่เปลี่ยนคือชื่อ ลุค และระดับราคา ทุกโลโก้ในหน้านี้เป็นไฟล์จริงที่แปลงตัวอักษรเป็นเส้นแล้ว ส่วนป้ายห้อยเป็นตัวอย่างการใช้งานบนสินค้า</p>
<p style="font-size:14px;color:var(--muted)">ต้นทุนในตารางใช้สูตรเดียวกับ Google Sheet แต่เปลี่ยนถุง 5 บาทเป็นกล่องพรีเมียมประมาณ {PREMIUM_PACK:.0f} บาท ราคาแบรนด์หรูต้องมาพร้อมงานเก็บขอบหนัง การคัดหนังเกรดดี และบรรจุภัณฑ์ที่ดีขึ้น</p>
</header>
{opts}
<section class="opt"><h2>เทียบกันทั้งสิบ</h2>
<div class="tbl"><table><thead><tr><th>แบรนด์</th><th>โทน</th><th>เรื่องครอบครัว</th><th>จดชื่อ</th><th>ราคาสินค้าหลัก (บาท)</th></tr></thead><tbody>{crow}</tbody></table></div></section>
<section class="opt pick" id="pick"><span class="eyebrow">คำแนะนำ</span><h2>POINT FIVE ถ้าอยากได้ทั้งเท่และหรูในชื่อเดียว</h2>
<p>POINT FIVE คือ 0.5 มม. ระยะที่ปีกเล็กกว่าร่อง ซึ่งเป็นงานออกแบบของพ่อจริง ๆ และคำว่า ไฟว์ ยังเท่ากับคนห้าคนในบ้าน ชื่อเดียวเล่าได้ทั้งความแม่นยำของงานและเรื่องครอบครัว ใช้ drawing ที่มีอยู่แล้วเป็นกราฟิกได้ทันที</p>
<p>ถ้าอยากให้ชื่อแบรนด์เป็นของขวัญถึงภรรยาโดยตรง เลือก SANSFIL ที่สโลแกนจบด้วยคำว่า ด้วยความรัก หรือ QUINT ที่หรูแบบคลาสสิก ถ้าเรื่องรักษ์โลกคือจุดขายหลัก MONO/HIDE พูดเรื่องวัสดุเดียวได้ชัดกว่า AFTERCUT แต่ต้องตัดสินค้าที่มีไม้ก๊อก ห่วงโลหะ และริบบิ้นออกจากไลน์นี้</p>
<p>สำหรับบูธวันที่ 23–25 ต.ค. ที่ลูก ๆ ขายเอง ห้าหมียังเหมาะที่สุด ทางที่ใช้ได้ทั้งสองแบบคือให้ห้าหมีเป็นไลน์ของลูก ๆ และของราคาเบา แล้วเปิดแบรนด์หรูที่เลือกเป็นไลน์พรีเมียมใน Shopee งานแต่ง และองค์กร โดยใช้บล็อกชุดเดียวกัน</p>
<ol><li>คัดให้เหลือ 2–3 ชื่อ แล้วเช็กชื่อบัญชีและค้นฐานข้อมูลเครื่องหมายการค้าของกรมทรัพย์สินทางปัญญา</li>
<li>เลือกหนึ่งชื่อ หรือเลือกโครงสองไลน์</li>
<li>บอกผม แล้วผมจะทำโลโก้ชุดเต็ม Brand Book โปสเตอร์ 30 ตัว และสไลด์ในลุคนั้นให้ใหม่ทั้งชุด</li></ol></section>
</div>"""

if __name__ == "__main__":
    open(os.path.join(HERE, "index.html"), "w").write(page())
    print("ok")
