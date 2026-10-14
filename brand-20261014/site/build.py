"""Build the three FIVE BEARS pages from brand.py.

site/brandbook.html  - brand book (name, story, logo, colours, type, voice)
site/launch.html     - launch kit (channels, 30 products with posts, stock, kids at the booth, plan)
site/index.html      - project summary (CLAUDE.md rule), links to everything
Images are published next to each page as logo/... and posters/... (see FILES at the bottom).
"""
import html, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import brand as B

E = html.escape
URLS = json.load(open(os.path.join(HERE, "urls.json"))) if os.path.exists(os.path.join(HERE, "urls.json")) else {}

CSS = """
:root{
  /* Layout: one reading column of cards on cream, like a craft-shop catalogue; wide tables scroll inside their box. */
  --bg:#F7EEE2;--paper:#FFFDF9;--ink:#4A2C1D;--muted:#7A5A45;--line:#E6D3BE;
  --caramel:#B8743A;--heart:#D6453D;--honey:#F0B43C;--peach:#F2A7A0;--sage:#6F9A8D;--cocoa:#4A2C1D;--cream:#F7EEE2;
  --on-accent:#FFFFFF;--chip:#F1E2CF;
  --display:"Mitr","IBM Plex Sans Thai",system-ui,sans-serif;
  --body:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#21150F;--paper:#2C1D15;--ink:#F7EEE2;--muted:#CDB49E;--line:#46311F;--caramel:#D99158;--heart:#EC6A60;--chip:#3A281C;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#21150F;--paper:#2C1D15;--ink:#F7EEE2;--muted:#CDB49E;--line:#46311F;--caramel:#D99158;--heart:#EC6A60;--chip:#3A281C;color-scheme:dark}
*{box-sizing:border-box}
img{max-width:100%;height:auto;display:block}
body{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.65;margin:0;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:0 64px}
.wrap{max-width:860px;margin:0 auto}
h1,h2,h3{font-family:var(--display);font-weight:500;line-height:1.25;text-wrap:balance;margin:0}
h1{font-size:clamp(30px,7vw,46px)}h2{font-size:clamp(23px,5vw,30px)}h3{font-size:19px}
p{margin:0}
a{color:var(--caramel)}
nav.top{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);border-bottom:1px solid var(--line);
  margin:0 calc(-1*max(16px,env(safe-area-inset-left,0px)));padding:10px max(16px,env(safe-area-inset-left,0px));
  display:flex;gap:6px;overflow-x:auto;scrollbar-width:none}
nav.top a{flex:none;font-family:var(--display);font-size:14px;text-decoration:none;color:var(--ink);background:var(--chip);
  border-radius:99px;padding:5px 13px}
nav.top a:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid var(--honey);outline-offset:2px}
section{padding-top:44px;display:flex;flex-direction:column;gap:16px;scroll-margin-top:60px}
.eyebrow{font-family:var(--display);font-size:13px;letter-spacing:.08em;color:var(--caramel)}
.lead{font-size:18px;color:var(--muted);max-width:62ch}
.card{background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:18px}
.paper{background:#FFFDF9;border-radius:18px;padding:18px;display:flex;align-items:center;justify-content:center}
.paper.dark{background:#4A2C1D}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}
.grid.s{grid-template-columns:repeat(auto-fill,minmax(150px,1fr))}
.grid>*{min-width:0}
.cap{font-size:13px;color:var(--muted)}
.mono{font-variant-numeric:tabular-nums}
.chip{display:inline-block;font-size:12.5px;border-radius:99px;padding:2px 10px;background:var(--chip)}
.chip.ok{background:#DCEBE5;color:#2F5A4E}.chip.mid{background:#FBE7C2;color:#7A4E0E}.chip.ext{background:#F8DAD7;color:#8A2A23}
.tbl{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:var(--paper)}
table{border-collapse:collapse;width:100%;font-size:14.5px}
th,td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-family:var(--display);font-weight:500;font-size:13px;color:var(--muted);white-space:nowrap}
td.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
tr:last-child td{border-bottom:0}
ol,ul{margin:0;padding-left:1.3em}
li+li{margin-top:4px}
.copy{font-family:var(--display);font-size:13px;border:1px solid var(--line);background:var(--chip);color:var(--ink);
  border-radius:99px;padding:4px 12px;cursor:pointer}
pre.txt{white-space:pre-wrap;font-family:var(--body);font-size:14.5px;background:var(--bg);border-radius:12px;padding:12px;margin:0}
details{border-top:1px solid var(--line)}
details>summary{cursor:pointer;padding:10px 0;font-family:var(--display);font-size:15px}
.ch{display:flex;flex-direction:column;gap:8px;padding-bottom:12px}
.ch .h{display:flex;justify-content:space-between;align-items:center;gap:8px}
"""

FONT_LINK = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;600&family=Mitr:wght@400;500;600&display=swap">')

COPY_JS = """<script>
document.addEventListener('click',e=>{const b=e.target.closest('.copy');if(!b)return;
const t=document.getElementById(b.dataset.for);const s=t.innerText;
const done=()=>{const o=b.textContent;b.textContent='คัดลอกแล้ว';setTimeout(()=>b.textContent=o,1400)};
const sel=()=>{const r=document.createRange();r.selectNodeContents(t);const w=getSelection();w.removeAllRanges();w.addRange(r);b.textContent='เลือกข้อความแล้ว กดคัดลอก'};
try{navigator.clipboard.writeText(s).then(done,sel)}catch(_){sel()}});
</script>"""

def head(title):
    return (f'<title>{E(title)}</title><meta name="claude:viewport-fit-sides" content="cover">{FONT_LINK}<style>{CSS}</style>')

def copybox(id_, text, label="คัดลอก"):
    return (f'<div class="ch"><div class="h"><span class="cap">{label}</span><button class="copy" data-for="{id_}">คัดลอก</button></div>'
            f'<pre class="txt" id="{id_}">{E(text)}</pre></div>')

def status_chip(s):
    return {B.READY: "ok", B.PROTO: "mid", B.EXTRA: "ext"}[s]

def link(key, text):
    u = URLS.get(key)
    return f'<a href="{u}">{text}</a>' if u else text

# ---------------------------------------------------------------- brand book
def brandbook():
    b = B.BRAND
    names = "".join(
        f'<div class="card" style="display:flex;flex-direction:column;gap:6px{";border:2px solid var(--caramel)" if tag else ""}">'
        f'<h3>{E(n)}</h3>{f"<span class=chip>{tag}</span>" if tag else ""}<p class="cap" style="font-size:14px">{E(why)}</p></div>'
        for n, tag, why in B.NAME_OPTIONS)
    story = "".join(f'<div class="card"><h3>{E(h)}</h3><p style="margin-top:6px">{E(t)}</p></div>' for h, t in B.STORY_LONG)
    fam = "".join(
        f'<div class="card" style="display:flex;gap:12px;align-items:center"><span style="flex:none;width:40px;height:40px;border-radius:50%;'
        f'background:{B.C[k]};border:1px solid var(--line)"></span><div><b style="font-family:var(--display);font-weight:500">{E(n)}</b>'
        f'<p class="cap">{E(r)}</p></div></div>' for n, k, r in B.FAMILY)
    sw = "".join(
        f'<div class="card" style="padding:0;overflow:hidden"><div style="height:84px;background:{hx}"></div><div style="padding:10px 12px">'
        f'<b style="font-family:var(--display);font-weight:500">{E(th)}</b> <span class="mono cap">{hx}</span><p class="cap">{E(use)}</p></div></div>'
        for k, th, hx, use in B.PALETTE)
    voice = "".join(
        f'<div class="card" style="display:flex;flex-direction:column;gap:8px"><h3>{E(h)}</h3><p class="cap" style="font-size:14px">{E(d)}</p>'
        f'<p><span class="chip ok">ใช้</span> {E(do)}</p><p><span class="chip ext">เลี่ยง</span> <s>{E(dont)}</s></p></div>'
        for h, d, do, dont in B.VOICE)
    logos = [("logo-stacked", "โลโก้หลัก แนวตั้ง", ""), ("logo-horizontal", "แนวนอน ใช้หัวเว็บ ป้ายบูธ", ""),
             ("logo-stacked-reverse", "บนพื้นเข้ม", "dark"), ("logo-horizontal-mono", "สีเดียว ใช้ปั๊มเลเซอร์ ตรายาง", ""),
             ("mark", "ตัวหมี ใช้เดี่ยว ๆ", ""), ("sticker-3cm", "สติกเกอร์ปิดถุง 3 ซม.", "")]
    logo_cards = "".join(
        f'<figure class="card" style="margin:0;display:flex;flex-direction:column;gap:10px"><div class="paper {cls}" style="aspect-ratio:4/3">'
        f'<img src="logo/{f}.svg" alt="{E(cap)}" style="max-height:100%;max-width:100%"></div>'
        f'<figcaption class="cap">{E(cap)} · <span class="mono">logo/svg/{f}.svg</span></figcaption></figure>' for f, cap, cls in logos)
    apps = [("avatar-1080.png", "รูปโปรไฟล์ทุกช่องทาง 1080 × 1080"), ("cover-facebook-1640x624.png", "ปก Facebook 1640 × 624"),
            ("cover-youtube-2560x1440.png", "ปก YouTube 2560 × 1440"), ("cover-shopee-1200x600.png", "ปกร้าน Shopee 1200 × 600")]
    app_cards = "".join(
        f'<figure class="card" style="margin:0;display:flex;flex-direction:column;gap:8px"><img src="logo/{f}" alt="{E(c)}" style="border-radius:10px;border:1px solid var(--line)">'
        f'<figcaption class="cap">{E(c)}</figcaption></figure>' for f, c in apps)
    return f"""{head("ห้าหมี Brand Book")}
<div class="wrap">
<nav class="top" aria-label="หัวข้อ"><a href="#name">ชื่อ</a><a href="#story">เรื่องเล่า</a><a href="#logo">โลโก้</a><a href="#family">ครอบครัวหมี</a>
<a href="#color">สี</a><a href="#type">ตัวอักษร</a><a href="#voice">น้ำเสียง</a><a href="#use">ตัวอย่างใช้งาน</a></nav>
<header style="padding-top:28px;display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));align-items:center">
 <div class="paper" style="aspect-ratio:1"><img src="logo/logo-stacked.svg" alt="โลโก้ห้าหมี FIVE BEARS" style="max-height:100%"></div>
 <div style="display:flex;flex-direction:column;gap:12px;min-width:0"><span class="eyebrow">BRAND BOOK · ฉบับแรก 14 ต.ค. 2569</span>
 <h1>{b['th']} · {b['en']}</h1><p class="lead">{E(b['line'])}</p>
 <p>คู่มือนี้ใช้กับทุกอย่างที่มีชื่อห้าหมี ตั้งแต่ป้ายบูธ ถุง สติกเกอร์ ไปจนถึงโพสต์ในโซเชียล ให้ทุกชิ้นดูเป็นแบรนด์เดียวกัน</p></div>
</header>

<section id="name"><span class="eyebrow">ชื่อแบรนด์</span><h2>ห้าหมี เพราะบ้านเรามีห้าคน</h2>
<p class="lead">ตัวเลือกห้าชื่อที่คิดไว้ ชื่อที่มีกรอบคือชื่อที่แนะนำ และใช้ทำโลโก้กับทุกไฟล์ในชุดนี้</p>
<div class="grid">{names}</div>
<p class="cap">ก่อนพิมพ์ของจำนวนมาก เช็กว่าชื่อ @{b['handle']} ยังว่างในทุกช่องทาง และค้นชื่อในฐานข้อมูลเครื่องหมายการค้าของกรมทรัพย์สินทางปัญญา ถ้าเปลี่ยนชื่อ แก้ใน brand.py ที่เดียวแล้วสร้างไฟล์ใหม่ได้ทั้งชุด</p></section>

<section id="story"><span class="eyebrow">STORY TELLING</span><h2>เรื่องของห้าหมี</h2>
<p class="lead">{E(B.STORY_SHORT)}</p>
<div class="grid">{story}</div>
<div class="card">{copybox("bio", B.STORY_BIO, "ประโยคแนะนำตัวสั้น ใช้เป็น bio")}</div></section>

<section id="logo"><span class="eyebrow">โลโก้</span><h2>หมีตัวนี้คือบล็อกตัดจริง</h2>
<p class="lead">รูปหมีในโลโก้คือเส้นตัดของแบบ 01 ที่หมุน 45 องศาให้หูอยู่ด้านบน ร่องสองเส้นของบล็อกกลายเป็นแก้ม และหัวใจตรงกลางคือแม่หมี</p>
<div class="grid">{logo_cards}</div>
<div class="card"><h3>กติกาการใช้โลโก้</h3><ul style="margin-top:8px">
<li>เว้นที่ว่างรอบโลโก้อย่างน้อยเท่าความกว้างหูหมีหนึ่งข้าง</li>
<li>โลโก้หลักเล็กที่สุดกว้าง 25 มม. ถ้าเล็กกว่านั้นใช้ตัวหมีอย่างเดียว เล็กสุด 10 มม.</li>
<li>บนพื้นเข้มใช้ไฟล์ reverse บนหนังหรือตรายางใช้ไฟล์สีเดียว</li>
<li>ห้ามบีบ ยืด หมุน ใส่เงา หรือเปลี่ยนสีหัวใจเป็นสีอื่นนอกจากแดงหัวใจหรือครีม</li>
<li>ไฟล์ SVG ทุกไฟล์แปลงตัวอักษรเป็นเส้นแล้ว ส่งร้านพิมพ์ได้เลยโดยไม่ต้องมีฟอนต์</li></ul></div></section>

<section id="family"><span class="eyebrow">ครอบครัวหมี</span><h2>หมีห้าตัว ห้าสี</h2>
<div class="paper"><img src="logo/family.svg" alt="หมีห้าตัวเรียงจากพ่อหมีถึงลูกหมีคนเล็ก"></div>
<div class="grid">{fam}</div>
<p class="cap">สีประจำตัวใช้กับป้ายชื่อพนักงานลูกหมี ถุง และสีพื้นของโพสต์ ลูกแต่ละคนเลือกสีของตัวเองใหม่ได้ ขอให้อยู่ในชุดสีด้านล่าง</p></section>

<section id="color"><span class="eyebrow">สี</span><h2>ชุดสี</h2>
<div class="grid s">{sw}</div>
<p class="cap">สัดส่วนโดยประมาณ ครีม 60% คาราเมลกับโกโก้ 30% แดงหัวใจและสีลูกหมี 10% ใช้แดงหัวใจกับราคาและปุ่มสั่งซื้อเท่านั้น</p></section>

<section id="type"><span class="eyebrow">ตัวอักษร</span><h2>สองฟอนต์ ฟรีจาก Google Fonts</h2>
<div class="grid">
<div class="card"><p class="cap">หัวข้อ · {B.FONTS['head'][0]}</p><p style="font-family:var(--display);font-size:38px;font-weight:600;line-height:1.2">ห้าหมี 349 บาท</p><p class="cap">{E(B.FONTS['head'][1])}</p></div>
<div class="card"><p class="cap">เนื้อความ · {B.FONTS['body'][0]}</p><p style="font-size:18px">เศษหนังแท้ต่อกันด้วยปีกและร่อง ไม่ใช้กาว ไม่ต้องเย็บสักเข็ม</p><p class="cap">{E(B.FONTS['body'][1])}</p></div>
</div></section>

<section id="voice"><span class="eyebrow">น้ำเสียง</span><h2>พูดแบบห้าหมี</h2><div class="grid">{voice}</div></section>

<section id="use"><span class="eyebrow">ตัวอย่างใช้งาน</span><h2>รูปโปรไฟล์และปก</h2>
<p class="cap">บนมือถือ กดค้างที่รูปเพื่อบันทึก ไฟล์ทั้งหมดอยู่ในโฟลเดอร์ brand-20261014/logo ของโปรเจกต์</p>
<div class="grid">{app_cards}</div>
<figure class="card" style="margin:0;display:flex;flex-direction:column;gap:8px"><img src="posters/21-post.png" alt="ตัวอย่างโปสเตอร์ How-to ราวหมีห้าตัว" style="border-radius:10px;max-width:420px">
<figcaption class="cap">โปสเตอร์ How-to ใช้แบบเดียวกันทั้ง 30 ตัว ดูทั้งหมดใน {link("launch", "ชุดเปิดตัว")}</figcaption></figure></section>
</div>{COPY_JS}"""

# ---------------------------------------------------------------- launch kit
def launch():
    tot = B.event_totals(); use, big, small = B.piece_usage()
    cap_total = sum(B.LOT_CAPACITY.values())
    tl = "".join(f'<tr><td style="white-space:nowrap"><b>{d}</b> <span class="cap">{w}</span></td><td>{E(t)}</td></tr>' for d, w, t in B.TIMELINE)
    ch = ""
    for i, (nm, handle, url, setup, bio) in enumerate(B.CHANNELS):
        ch += (f'<div class="card" style="display:flex;flex-direction:column;gap:8px;min-width:0"><h3>{nm}</h3>'
               f'<p><span class="chip">{E(handle)}</span></p><p class="cap" style="font-size:14px">{E(setup)}</p>'
               f'{copybox(f"bio{i}", bio, "ข้อความแนะนำร้าน")}</div>')
    cards = ""
    for p in B.PRODUCTS:
        n = p["n"]
        shots, tcap = B.script_tiktok(p); ytt, ytd = B.youtube(p); spt, spd = B.shopee(p)
        shot_txt = "\n".join(f"{t}  {a}  ({b_})" for t, a, b_ in shots)
        hero = ' <span class="chip" style="background:var(--heart);color:var(--on-accent)">สินค้าหลัก</span>' if n in B.HEROES else ""
        cards += f"""<article class="card" id="p{n}" style="display:grid;gap:14px;grid-template-columns:minmax(0,min(180px,36%)) minmax(0,1fr)">
<a href="posters/{n:02d}-post.png" target="_blank" rel="noopener"><img src="posters/thumb/{n:02d}.jpg" alt="โปสเตอร์ {E(p['name'])}" loading="lazy" style="border-radius:10px;border:1px solid var(--line)"></a>
<div style="display:flex;flex-direction:column;gap:6px;min-width:0"><span class="cap mono">#{n:02d}</span><h3>{E(p['name'])}{hero}</h3>
<p class="cap" style="font-size:14px">{E(p['pieces_txt'])}{(' + ' + E(p['extra'][0])) if p['extra'] else ''}</p>
<p class="mono"><b style="font-family:var(--display);font-size:20px;color:var(--heart)">{p['price']} บาท</b>
 <span class="cap">ต้นทุน {p['cost']:.2f} · กำไร {p['profit']:.0f} ({p['margin']:.0%}) · เตรียมไปงาน {p['stock']} ชิ้น</span></p>
<p><span class="chip {status_chip(p['status'])}">{p['status']}</span></p>
<p class="cap"><a href="posters/{n:02d}-post.png" target="_blank" rel="noopener">โปสเตอร์ 1080 × 1350</a> · <a href="posters/{n:02d}-story.png" target="_blank" rel="noopener">story 1080 × 1920</a></p></div>
<div style="grid-column:1/-1;min-width:0">
<details><summary>Facebook</summary>{copybox(f"fb{n}", B.caption_fb(p), "โพสต์ + แนบโปสเตอร์ 1080 × 1350")}</details>
<details><summary>Instagram</summary>{copybox(f"ig{n}", B.caption_ig(p), "แคปชัน + โปสเตอร์ หรือคลิป Reels")}</details>
<details><summary>TikTok</summary>{copybox(f"tts{n}", shot_txt, "สคริปต์ถ่าย 15 วินาที ใช้ภาพปก story")}{copybox(f"ttc{n}", tcap, "แคปชัน")}</details>
<details><summary>YouTube Shorts</summary>{copybox(f"ytt{n}", ytt, "ชื่อคลิป")}{copybox(f"ytd{n}", ytd, "คำอธิบาย")}</details>
<details><summary>Shopee</summary>{copybox(f"spt{n}", spt, "ชื่อสินค้า")}{copybox(f"spd{n}", spd, "รายละเอียดสินค้า")}</details>
</div></article>"""
    stock = "".join(
        f'<tr><td class="mono">{p["n"]:02d}</td><td>{E(p["name"])}</td><td class="n">{p["price"]}</td><td class="n">{p["stock"]}</td>'
        f'<td class="n">{p["stock"]*p["npieces"]}</td><td class="n">{p["stock"]*p["price"]:,}</td></tr>'
        for p in sorted(B.PRODUCTS, key=lambda q: -q["stock"] * q["price"]))
    roles = "".join(
        f'<div class="card" style="display:flex;flex-direction:column;gap:6px;border-top:6px solid {B.C[c]}"><h3>{E(w)}</h3>'
        f'<span class="cap">{E(n)}</span><ul>{"".join(f"<li>{E(x)}</li>" for x in jobs)}</ul></div>' for n, w, c, jobs in B.KIDS_ROLES)
    scripts = "".join(f'<tr><td style="white-space:nowrap"><b>{E(a)}</b></td><td>“{E(b_)}”</td></tr>' for a, b_ in B.SCRIPTS)
    rules = "".join(f"<li>{E(r)}</li>" for r in B.BOOTH_RULES)
    prints = "".join(f'<tr><td>{E(a)}</td><td class="n">{E(q)}</td><td>{E(n)}</td></tr>' for a, q, n in B.PRINT_LIST)
    more = "".join(f'<div class="card"><h3>{E(a)}</h3><p class="cap" style="font-size:14px;margin-top:4px">{E(b_)}</p></div>' for a, b_ in B.MORE)
    usage = " · ".join(f"{B.PIECE_NAME[k]} {v}" for k, v in sorted(use.items()))
    return f"""{head("ห้าหมี Launch Kit")}
<div class="wrap">
<nav class="top" aria-label="หัวข้อ"><a href="#plan">แผน 9 วัน</a><a href="#social">โซเชียลและ Shopee</a><a href="#products">สินค้า 30 ตัว</a>
<a href="#stock">สต็อกไปงาน</a><a href="#kids">ลูกหมีขายของ</a><a href="#print">ของต้องพิมพ์</a><a href="#more">แนะนำเพิ่ม</a></nav>
<header style="padding-top:28px;display:flex;flex-direction:column;gap:12px"><span class="eyebrow">LAUNCH KIT · บูธ 23–25 ต.ค. 2569</span>
<h1>ห้าหมี พร้อมออกบูธ</h1>
<p class="lead">ทุกอย่างที่ต้องทำก่อนวันงาน ข้อความโพสต์ของสินค้า 30 ตัวสำหรับ 5 ช่องทาง และคู่มือให้ลูกหมีขายของเอง กดปุ่มคัดลอกแล้ววางในแอปได้เลย</p>
<div class="grid s">
<div class="card"><p class="cap">สินค้า</p><b style="font-family:var(--display);font-size:28px">30 แบบ</b></div>
<div class="card"><p class="cap">เตรียมไปงาน</p><b style="font-family:var(--display);font-size:28px" class="mono">{tot['units']} ชิ้น</b></div>
<div class="card"><p class="cap">ถ้าขายหมด</p><b style="font-family:var(--display);font-size:28px" class="mono">{tot['sales']:,.0f} บาท</b></div>
<div class="card"><p class="cap">ต้นทุนของทั้งหมด</p><b style="font-family:var(--display);font-size:28px" class="mono">{tot['cost']:,.0f} บาท</b></div>
</div>
<p class="cap">ต้นทุนคิดแบบเดียวกับ {link("sheet", "Google Sheet ต้นทุน")} (หนัง ค่าตัด 1.50 ค่าบล็อกเฉลี่ย 0.95 ค่าประกอบ ค่าแพ็ค บรรจุภัณฑ์ 5 บาท) ยังไม่รวมค่าบูธ ค่าพิมพ์ และค่าบล็อกที่ต้องสั่งใหม่</p>
</header>

<section id="plan"><span class="eyebrow">แผน 9 วัน</span><h2>14 ถึง 26 ตุลาคม</h2>
<div class="tbl"><table><tbody>{tl}</tbody></table></div>
<p class="cap">งานที่ช้าที่สุดคือบล็อกตัด ถ้ายังไม่มีบล็อกแบบไหน ให้สั่งวันนี้ แบบที่ได้ไม่ทันให้ขายแบบสั่งจองผ่าน Shopee แทน</p></section>

<section id="social"><span class="eyebrow">โซเชียลมีเดียและร้าน Shopee</span><h2>ห้าช่องทาง ชื่อเดียวกัน</h2>
<p class="lead">ทุกช่องใช้ชื่อ @{B.BRAND['handle']} รูปโปรไฟล์และปกอยู่ใน {link("brandbook", "Brand Book")} บัญชีต้องเปิดในชื่อพ่อหรือแม่ เพราะทุกแพลตฟอร์มกำหนดอายุขั้นต่ำ 13 ปี และ Shopee ต้องใช้บัตรประชาชนกับบัญชีธนาคาร</p>
<div class="grid">{ch}</div>
<div class="card"><h3>9 โพสต์แรก</h3><ol style="margin-top:6px">
<li>เรื่องของห้าหมี (ใช้ข้อความใน Brand Book + รูปครอบครัวหมี)</li><li>แนะนำลูกหมีสามตัว และหน้าที่ที่บูธ</li>
{"".join(f"<li>How-to {E(next(p['name'] for p in B.PRODUCTS if p['n']==h))}</li>" for h in B.HEROES[:6])}
<li>เจอกันที่บูธ 23–25 ต.ค. พร้อมแผนที่และเลขบูธ</li></ol></div></section>

<section id="products"><span class="eyebrow">สินค้า 30 ตัว</span><h2>โปสเตอร์และโพสต์ทุกช่องทาง</h2>
<p class="lead">แตะรูปเพื่อเปิดโปสเตอร์ขนาดเต็ม แต่ละตัวมีภาพ story 1080 × 1920 สำหรับ TikTok, Reels และ Shorts อยู่ในโฟลเดอร์ posters/png</p>
<p class="cap"><span class="chip ok">{B.READY}</span> ตัดแล้วขายได้เลย · <span class="chip mid">{B.PROTO}</span> ต่อตัวอย่างหนึ่งชิ้นก่อนผลิต · <span class="chip ext">{B.EXTRA}</span> ต้องซื้อของเสริม</p>
{cards}</section>

<section id="stock"><span class="eyebrow">สต็อกไปงาน</span><h2>{tot['units']} ชิ้น จากหนังที่มี</h2>
<p class="lead">ใช้ชิ้นหนัง {big + small} จาก {cap_total} ชิ้นที่ตัดได้จากเศษที่ซื้อมา (เศษใหญ่ 505 + เศษเล็ก 224) ชิ้นแบบ 02–06 ที่เกินจากเศษเล็ก {max(0, small - B.LOT_CAPACITY['เล็ก'])} ชิ้นให้ตัดจากเศษใหญ่</p>
<p class="cap">{usage}</p>
<div class="tbl"><table><thead><tr><th>#</th><th>สินค้า</th><th>ราคา</th><th>จำนวน</th><th>ชิ้นหนัง</th><th>ยอดถ้าขายหมด</th></tr></thead><tbody>{stock}</tbody></table></div>
<p class="cap">เวลาประกอบรวมประมาณ {tot['assembly_h']:.1f} ชม. และแพ็คอีก {tot['pack_h']:.1f} ชม. แบ่งให้ลูก ๆ ช่วยวันเสาร์อาทิตย์ที่ 17–18 ต.ค. ได้</p></section>

<section id="kids"><span class="eyebrow">ลูกหมีขายของ</span><h2>สามหน้าที่ ทำได้ตามวัย</h2>
<div class="grid">{roles}</div>
<h3>ประโยคที่ซ้อมไว้</h3><div class="tbl"><table><tbody>{scripts}</tbody></table></div>
<div class="card"><h3>กติกาบูธ</h3><ul style="margin-top:6px">{rules}</ul></div></section>

<section id="print"><span class="eyebrow">ของต้องพิมพ์</span><h2>สั่งร้านพิมพ์ภายใน 15 ต.ค.</h2>
<div class="tbl"><table><thead><tr><th>รายการ</th><th>จำนวน</th><th>หมายเหตุ</th></tr></thead><tbody>{prints}</tbody></table></div></section>

<section id="more"><span class="eyebrow">ข้อ 7 · แนะนำเพิ่ม</span><h2>สิ่งที่ควรทำต่อ</h2><div class="grid">{more}</div></section>
</div>{COPY_JS}"""

# ---------------------------------------------------------------- summary (CLAUDE.md)
def summary():
    tot = B.event_totals()
    rows = [("Brand Book", "brandbook", "ชื่อ เรื่องเล่า โลโก้ สี ฟอนต์ น้ำเสียง"),
            ("Launch Kit", "launch", "แผน 9 วัน โซเชียล Shopee สินค้า 30 ตัว พร้อมโพสต์ 5 ช่องทาง คู่มือลูกหมีขายของ"),
            ("สไลด์ของขวัญวันเกิด", "deck", "พรีเซนต์ทั้งหมดให้แม่หมี"),
            ("Google Sheet ต้นทุน", "sheet", "ต้นทุน ราคาขาย กำไร 3 แท็บ"),
            ("ทางเลือกแบรนด์ Luxury", "alternatives", "อีก 20 ชื่อ แนวเท่ หรู ยั่งยืน และของใช้ทุกวัน พร้อมโลโก้และราคา")]
    links = "".join(f'<div class="card"><h3>{link(k, E(t))}</h3><p class="cap" style="font-size:14px;margin-top:4px">{E(d)}</p></div>' for t, k, d in rows)
    files = [("brand-20261014/brand.py", "ข้อมูลทั้งหมดของแบรนด์ แก้ที่นี่ที่เดียว"),
             ("brand-20261014/logo/svg, logo/png", "โลโก้ 13 ไฟล์ แปลงตัวอักษรเป็นเส้นแล้ว"),
             ("brand-20261014/posters/png", "โปสเตอร์ How-to 30 ตัว × 2 ขนาด (60 ไฟล์)"),
             ("brand-20261014/site", "ต้นฉบับหน้าเว็บทั้งสาม"),
             ("brand-20261014/deck", "ต้นฉบับสไลด์"),
             ("brand-20261014/alternatives", "ทางเลือกแบรนด์ 20 แบบ โลโก้และป้ายห้อย")]
    ftable = "".join(f'<tr><td class="mono" style="white-space:nowrap">{E(f)}</td><td>{E(d)}</td></tr>' for f, d in files)
    return f"""{head("ห้าหมี สรุปโปรเจกต์")}
<div class="wrap"><header style="padding-top:28px;display:flex;flex-direction:column;gap:14px">
<span class="eyebrow">สรุปโปรเจกต์ · 14 ต.ค. 2569</span><h1>แบรนด์ห้าหมี ก่อนออกบูธ 23–25 ต.ค.</h1>
<div class="paper"><img src="logo/family.svg" alt="หมีห้าตัว"></div>
<p class="lead">ชื่อแบรนด์ เรื่องเล่า โลโก้และ brand book ช่องทางโซเชียลกับ Shopee สินค้า 30 ตัวพร้อมโปสเตอร์และโพสต์ทุกช่องทาง คู่มือให้ลูก ๆ ขายเอง และสไลด์สำหรับวันเกิดแม่หมี</p></header>
<section><h2>เปิดดู</h2><div class="grid">{links}</div></section>
<section><h2>ตัวเลขสำคัญ</h2><div class="grid s">
<div class="card"><p class="cap">สินค้า</p><b style="font-family:var(--display);font-size:26px">30 แบบ</b></div>
<div class="card"><p class="cap">โปสเตอร์</p><b style="font-family:var(--display);font-size:26px">60 ภาพ</b></div>
<div class="card"><p class="cap">ข้อความโพสต์</p><b style="font-family:var(--display);font-size:26px">210 ชิ้น</b></div>
<div class="card"><p class="cap">ของไปงาน</p><b style="font-family:var(--display);font-size:26px" class="mono">{tot['units']} ชิ้น</b></div>
<div class="card"><p class="cap">ยอดถ้าขายหมด</p><b style="font-family:var(--display);font-size:26px" class="mono">{tot['sales']:,.0f} ฿</b></div>
<div class="card"><p class="cap">ต้นทุนของ</p><b style="font-family:var(--display);font-size:26px" class="mono">{tot['cost']:,.0f} ฿</b></div></div></section>
<section><h2>ไฟล์</h2><div class="tbl"><table><tbody>{ftable}</tbody></table></div></section>
<section><h2>ต้องเช็กก่อน</h2><div class="card"><ol>
<li>ชื่อ @{B.BRAND['handle']} ยังว่างทุกช่องทาง ถ้าไม่ว่าง เลือกชื่อใหม่แล้วแก้ใน brand.py</li>
<li>มีบล็อกแบบไหนแล้วบ้าง แบบที่ยังไม่มีต้องสั่งวันนี้</li>
<li>สินค้าที่ติดป้าย “ลองต้นแบบก่อน” ต่อตัวอย่างหนึ่งชิ้นทุกตัว ก่อนลงขายใน Shopee</li>
<li>ใส่ชื่องานและเลขบูธแทน [ชื่องาน] ในข้อความโพสต์</li>
<li>สายหัวใจ 250 มม. ต้องใช้เศษยาว 25.5 ซม. ขึ้นไป ถ้าเศษสั้นกว่า ป้ายชื่อกระเป๋าใช้สาย 200 แทน</li>
<li>ราคาขายเป็นราคาแนะนำ แก้ได้ในคอลัมน์ราคาขายของ Google Sheet</li></ol></div></section>
</div>"""

FILES = {}
def assets():
    """Published path -> source path, shared by all three pages."""
    out = {}
    for f in os.listdir(os.path.join(ROOT, "logo", "svg")):
        out[f"logo/{f}"] = os.path.join(ROOT, "logo", "svg", f)
    for f in os.listdir(os.path.join(ROOT, "logo", "png")):
        out[f"logo/{f}"] = os.path.join(ROOT, "logo", "png", f)
    return out

if __name__ == "__main__":
    for name, fn in (("brandbook.html", brandbook), ("launch.html", launch), ("index.html", summary)):
        open(os.path.join(HERE, name), "w").write(fn())
    print("built", URLS)
