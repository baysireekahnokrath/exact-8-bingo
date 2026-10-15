"""Build the three OCT. 26 pages from brand.py.

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
  /* Layout: one reading column of cards, every size from phi. Type steps 16 x phi^(k/2); spacing Fibonacci 5 8 13 21 34 55 89;
     reading column 987px (a Fibonacci number); two-column splits 61.8 / 38.2. Palette #2, chosen 15 Oct 2026. */
  --bg:#FFF6EC;--paper:#FFFFFF;--ink:#1C1B22;--muted:#4A4A55;--line:#F1DCCB;
  --cobalt:#2449D8;--tomato:#FF5A36;--sun:#FFC23C;--mint:#2EC4A0;--pink:#FF8AC4;--leather:#B8743A;
  --caramel:var(--cobalt);--heart:#E2401C;--brick:var(--tomato);--love:var(--pink);--honey:var(--sun);--peach:var(--pink);--sage:var(--mint);
  --cocoa:var(--ink);--cream:var(--bg);--leaf:var(--cobalt);--chestnut:var(--ink);
  --on-accent:#FFFFFF;--chip:#FBE9DA;
  --t-1:12.6px;--t0:16px;--t1:20.4px;--t2:25.9px;--t3:32.9px;--t4:41.9px;
  --s1:5px;--s2:8px;--s3:13px;--s4:21px;--s5:34px;--s6:55px;--s7:89px;
  --logo:"Jost","Anuphan",system-ui,sans-serif;
  --display:"Anuphan","IBM Plex Sans Thai",system-ui,sans-serif;
  --body:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#14131A;--paper:#1F1E27;--ink:#FFF6EC;--muted:#C9C4D6;--line:#34323F;--cobalt:#7C97FF;--caramel:#7C97FF;--heart:#FF7A5C;--chip:#2A2833;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#14131A;--paper:#1F1E27;--ink:#FFF6EC;--muted:#C9C4D6;--line:#34323F;--cobalt:#7C97FF;--caramel:#7C97FF;--heart:#FF7A5C;--chip:#2A2833;color-scheme:dark}
*{box-sizing:border-box}
img{max-width:100%;height:auto;display:block}
body{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:var(--t0);line-height:1.618;margin:0;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:0 var(--s7)}
.wrap{max-width:987px;margin:0 auto}
h1,h2,h3{font-family:var(--display);font-weight:600;line-height:1.236;text-wrap:balance;margin:0}
h1{font-size:clamp(var(--t3),7vw,var(--t4))}h2{font-size:clamp(var(--t2),5vw,var(--t3))}h3{font-size:var(--t1)}
p{margin:0}
a{color:var(--cobalt)}
nav.top{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);border-bottom:1px solid var(--line);
  margin:0 calc(-1*max(16px,env(safe-area-inset-left,0px)));padding:var(--s3) max(16px,env(safe-area-inset-left,0px));
  display:flex;gap:var(--s2);overflow-x:auto;scrollbar-width:none}
nav.top a{flex:none;font-family:var(--display);font-size:14px;text-decoration:none;color:var(--ink);background:var(--chip);
  border-radius:var(--s4);padding:var(--s1) var(--s3)}
nav.top a:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid var(--tomato);outline-offset:2px}
section{padding-top:var(--s6);display:flex;flex-direction:column;gap:var(--s4);scroll-margin-top:var(--s7)}
.eyebrow{font-family:var(--logo);font-weight:500;font-size:var(--t-1);letter-spacing:.12em;text-transform:uppercase;color:var(--cobalt)}
.lead{font-size:var(--t1);color:var(--muted);max-width:61.8ch}
.card{background:var(--paper);border:1px solid var(--line);border-radius:var(--s4);padding:var(--s4)}
.paper{background:#FFFFFF;border-radius:var(--s4);padding:var(--s4);display:flex;align-items:center;justify-content:center}
.paper.dark{background:#2449D8}
.grid{display:grid;gap:var(--s3);grid-template-columns:repeat(auto-fill,minmax(233px,1fr))}
.grid.s{grid-template-columns:repeat(auto-fill,minmax(144px,1fr))}
.grid>*{min-width:0}
.cap{font-size:var(--t-1);color:var(--muted)}
.mono{font-variant-numeric:tabular-nums}
.chip{display:inline-block;font-size:var(--t-1);border-radius:var(--s4);padding:2px var(--s3);background:var(--chip)}
.chip.ok{background:#D7F3EA;color:#0E6B55}.chip.mid{background:#FFF0C7;color:#7A5200}.chip.ext{background:#FFE1D9;color:#A0300F}
.tbl{overflow-x:auto;border:1px solid var(--line);border-radius:var(--s3);background:var(--paper)}
table{border-collapse:collapse;width:100%;font-size:14.5px}
th,td{text-align:left;padding:var(--s2) var(--s3);border-bottom:1px solid var(--line);vertical-align:top}
th{font-family:var(--display);font-weight:500;font-size:var(--t-1);color:var(--muted);white-space:nowrap}
td.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
tr:last-child td{border-bottom:0}
ol,ul{margin:0;padding-left:1.3em}
li+li{margin-top:var(--s1)}
.copy{font-family:var(--display);font-size:var(--t-1);border:1px solid var(--line);background:var(--chip);color:var(--ink);
  border-radius:var(--s4);padding:var(--s1) var(--s3);cursor:pointer}
pre.txt{white-space:pre-wrap;font-family:var(--body);font-size:14.5px;background:var(--bg);border-radius:var(--s3);padding:var(--s3);margin:0}
details{border-top:1px solid var(--line)}
details>summary{cursor:pointer;padding:var(--s3) 0;font-family:var(--display);font-size:15px}
.ch{display:flex;flex-direction:column;gap:var(--s2);padding-bottom:var(--s3)}
.ch .h{display:flex;justify-content:space-between;align-items:center;gap:var(--s2)}
"""

FONT_LINK = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anuphan:wght@500;600&family=IBM+Plex+Sans+Thai:wght@400;600&family=Mitr:wght@400;500;600&family=Jost:wght@400;500&display=swap">')

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
def fig(f, cap, cls="", ratio="4/3"):
    return (f'<figure class="card" style="margin:0;display:flex;flex-direction:column;gap:10px"><div class="paper {cls}" style="aspect-ratio:{ratio}">'
            f'<img src="logo/{f}.svg" alt="{E(cap)}" style="max-height:100%;max-width:100%"></div>'
            f'<figcaption class="cap">{E(cap)} · <span class="mono">logo/svg/{f}.svg</span></figcaption></figure>')

def swatches(keys):
    return "".join(
        f'<div class="card" style="padding:0;overflow:hidden"><div style="height:76px;background:{hx}"></div><div style="padding:10px 12px">'
        f'<b style="font-family:var(--display);font-weight:500">{E(th)}</b> <span class="mono cap">{hx}</span><p class="cap">{E(use)}</p></div></div>'
        for k, th, hx, use in B.PALETTE if k in keys)

def brandbook():
    b = B.BRAND
    meaning = [("O · C · T", "our · crafted · things ของที่เราทำกันเอง ไม่ได้สั่งโรงงาน"),
               ("OCT.", "ตุลาคม เดือนที่แบรนด์เกิด และเดือนที่ลูก ๆ ออกบูธครั้งแรก"),
               ("26", "วันเกิดของแม่ แบรนด์เกิดวันเดียวกัน 26 ตุลาคม 2569"),
               ("อ่านว่า", f"{b['say']} เขียนตัวใหญ่ มีจุดหลัง OCT และเว้นวรรคก่อน 26 ทุกครั้ง")]
    import importlib.util
    _sp = importlib.util.spec_from_file_location("logolab_build", os.path.join(ROOT, "logolab", "build.py"))
    LL = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(LL)
    golden_rows = "".join(f'<tr><td>{E(a)}</td><td class="mono">{E(c)}</td></tr>' for a, c in [
        ("ตัวอักษรโลโก้", "เส้น = ความสูง ÷ φ⁴ · จุด = เส้น × φ · ตัวเลขกว้าง = ความสูง ÷ φ"),
        ("OCT. 26 ทั้งคำ", "OCT. กับช่องว่าง : 26 = φ² : 1 · ทั้งคำกว้าง 5 เท่าของความสูง"),
        ("ป้ายห้อยสัญลักษณ์", "กว้าง : สูง = 1 : φ · ฐานเลข 26 อยู่ที่เส้นแบ่งทองคำ"),
        ("ป้ายคอลเลกชัน", "กว้าง : สูง = φ : 1 (SOI. 02) และ φ² : 1 (Love)"),
        ("ขนาดตัวอักษรบนเว็บ", " · ".join(f"{v:g}" for v in B.GOLDEN["type"]) + " px (16 × φ^(k/2))"),
        ("ระยะห่าง", " · ".join(str(v) for v in B.GOLDEN["space"]) + " px (ฟีโบนัชชี)"),
        ("โปสเตอร์", "ขอบ 89 · ช่องไฟ 13 / 21 / 34 / 55 · หัวข้อ 89 · ราคา 233 px"),
        ("งานพิมพ์ (มม.)", " · ".join(f"{k} {' × '.join(str(x) for x in v)}" for k, v in B.GOLDEN["print_mm"].items())),
        ("สัดส่วนสี", "พื้น 61.8% · หมึกและโคบอลต์ 23.6% · มะเขือเทศและสีครอบครัว 14.6%"),
        ("ที่ว่างรอบโลโก้", "อย่างน้อย จุด × φ ทุกด้าน"),
        ("ป้ายห้อยในกรอบสี่เหลี่ยม", "สูง = ด้านกรอบ ÷ φ (รูปโปรไฟล์ ไอคอน สติกเกอร์)")])
    mean = "".join(f'<div class="card"><h3 style="font-family:var(--logo);font-weight:500">{E(h)}</h3><p style="margin-top:6px">{E(t)}</p></div>' for h, t in meaning)
    arch = "".join(
        f'<div class="card" style="display:flex;flex-direction:column;gap:6px;{"border:2px solid var(--brick)" if i == 0 else ""}">'
        f'<span class="eyebrow">{E(lv)}</span><h3>{E(nm)}</h3><p class="cap" style="font-size:14px">{E(what)}</p><p style="font-size:14.5px">{E(note)}</p></div>'
        for i, (lv, nm, what, note) in enumerate(B.ARCH))
    answer = "".join(f'<div class="card"><h3>{E(h)}</h3><p style="margin-top:6px">{E(t)}</p></div>' for h, t in B.SUB_ANSWER)
    story = "".join(f'<div class="card"><h3>{E(h)}</h3><p style="margin-top:6px">{E(t)}</p></div>' for h, t in B.STORY_LONG)
    fam = "".join(
        f'<div class="card" style="display:flex;gap:12px;align-items:center"><span style="flex:none;width:40px;height:40px;border-radius:50%;'
        f'background:{B.C[k]};border:1px solid var(--line)"></span><div><b style="font-family:var(--display);font-weight:500">{E(n)}</b>'
        f'<p class="cap">{E(r)}</p></div></div>' for n, k, r in B.FAMILY)
    voice = "".join(
        f'<div class="card" style="display:flex;flex-direction:column;gap:8px"><h3>{E(h)}</h3><p class="cap" style="font-size:14px">{E(d)}</p>'
        f'<p><span class="chip ok">ใช้</span> {E(do)}</p><p><span class="chip ext">เลี่ยง</span> <s>{E(dont)}</s></p></div>'
        for h, d, do, dont in B.VOICE)
    LOGOS = [  # the four logos, one at a time, never side by side
        ("1", "OCT. 26", "oct-wordmark", "โลโก้หลัก ชื่อเต็ม",
         "แบ็คดรอปบูธ ถุง การ์ด ป้ายห้อย หัวเว็บ ปก Facebook และ Shopee ท้ายโปสเตอร์ ปั๊มลงหนัง"),
        ("2", "ป้ายห้อย 26", "oct-mark", "สัญลักษณ์ ตอนพื้นที่เล็กหรือเป็นสี่เหลี่ยม",
         "รูปโปรไฟล์ทุกช่องทาง ไอคอนเว็บ สติกเกอร์ปิดถุง ที่ที่เล็กจนชื่อเต็มอ่านไม่ออก"),
        ("3", "ห้าหมี FIVE BEARS", "fivebears", "โลโก้ซับแบรนด์",
         "ทุกอย่างของห้าหมี ป้ายห้อย Love โต๊ะห้าหมีที่บูธ"),
        ("4", "หมีหัวใจ", "bear", "สัญลักษณ์ห้าหมี",
         "สติกเกอร์แจกเด็ก ป้ายเล็ก รูปโปรไฟล์ถ้าวันหนึ่งห้าหมีแยกบัญชี")]
    logo_rows = "".join(f'<tr><td><b>{n}. {E(nm)}</b><br><span class="cap">{E(role)}</span></td><td>{E(use)}</td></tr>' for n, nm, f, role, use in LOGOS)
    def versions(f, has_rev=True):
        out = [fig(f, "บนพื้นสว่าง")]
        if has_rev: out.append(fig(f + "-reverse", "บนพื้นเข้ม", "dark"))
        out.append(fig(f + "-mono", "สีเดียว ปั๊มหนัง ตรายาง พิมพ์สีเดียว"))
        return "".join(out)
    oct_logos = (f'<h3>1. OCT. 26</h3><div class="grid">{versions("oct-wordmark")}</div>'
                 f'<h3>2. ป้ายห้อย 26</h3><div class="grid">{versions("oct-mark")}'
                 + fig("avatar-1080", "ใช้จริง: รูปโปรไฟล์ 1080 × 1080") + fig("oct-sticker-34mm", "ใช้จริง: สติกเกอร์ปิดถุง 34 มม.") + "</div>")
    bear_logos = (f'<h3>3. ห้าหมี FIVE BEARS</h3><div class="grid">{versions("fivebears")}</div>'
                  f'<h3>4. หมีหัวใจ</h3><div class="grid">{fig("bear", "สี")}{fig("bear-mono", "สีเดียว ใช้ได้ทั้งพื้นสว่างและพื้นเข้ม")}'
                  + fig("fivebears-sticker-34mm", "ใช้จริง: สติกเกอร์แจกเด็ก 34 มม.") + "</div>")
    colls = "".join(
        f'<div class="card" style="display:flex;flex-direction:column;gap:10px"><div class="paper" style="aspect-ratio:5/3"><img src="logo/{img}.svg" alt="ป้ายคอลเลกชัน {E(c["name"])}"></div>'
        f'<span class="eyebrow">{E(c["brand"])} · คอลเลกชันแรก</span><h3>{E(c["name"])}</h3><p class="cap" style="font-size:14px">{E(c["line"])}</p>'
        f'<p style="font-size:14.5px">{E(c["why"])}</p>'
        f'<p class="cap">{sum(p["coll"] == k for p in B.PRODUCTS)} แบบ · '
        f'{E(", ".join(p["name"] for p in B.PRODUCTS if p["coll"] == k)[:150])}…</p></div>'
        for k, img, c in (("soi2", "soi2-sign", B.COLLECTIONS["soi2"]), ("love", "love-badge", B.COLLECTIONS["love"])))
    fonts = "".join(
        f'<div class="card"><p class="cap">{E(role)} · {E(nm)}</p><p style="font-family:{css};font-size:{sz}px;font-weight:{w};line-height:1.25">{E(sample)}</p><p class="cap">{E(use)}</p></div>'
        for role, (nm, use), css, sz, w, sample in [
            ("ภาษาอังกฤษ", B.FONTS["latin"], "var(--logo)", 34, 500, "our crafted things."),
            ("หัวข้อภาษาไทย", B.FONTS["head"], "var(--display)", 34, 500, "กล่องของชำร่วย 159 บาท"),
            ("ห้าหมี", B.FONTS["sub"], "'Mitr',sans-serif", 32, 600, "ราวหมีห้าตัว 349 บาท"),
            ("เนื้อความ", B.FONTS["body"], "var(--body)", 18, 400, "เศษหนังแท้ต่อกันด้วยปีกและร่อง ทุกชิ้นสีไม่ซ้ำกัน")])
    apps = [("avatar-1080.png", "รูปโปรไฟล์ทุกช่องทาง 1080 × 1080"), ("cover-facebook-1640x624.png", "ปก Facebook 1640 × 624"),
            ("cover-youtube-2560x1440.png", "ปก YouTube 2560 × 1440"), ("cover-shopee-1200x600.png", "ปกร้าน Shopee 1200 × 600")]
    app_cards = "".join(
        f'<figure class="card" style="margin:0;display:flex;flex-direction:column;gap:8px"><img src="logo/{f}" alt="{E(c)}" style="border-radius:10px;border:1px solid var(--line)">'
        f'<figcaption class="cap">{E(c)}</figcaption></figure>' for f, c in apps)
    return f"""{head("OCT. 26 Brand Book")}
<div class="wrap">
<nav class="top" aria-label="หัวข้อ"><a href="#name">ชื่อ</a><a href="#arch">โครงสร้างแบรนด์</a><a href="#story">เรื่องเล่า</a><a href="#logo">โลโก้</a><a href="#golden">สัดส่วนทองคำ</a>
<a href="#collections">คอลเลกชัน</a><a href="#fivebears">ห้าหมี</a><a href="#color">สี</a><a href="#type">ตัวอักษร</a><a href="#voice">น้ำเสียง</a><a href="#use">ตัวอย่างใช้งาน</a></nav>
<header style="padding-top:28px;display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));align-items:center">
 <div class="paper" style="aspect-ratio:1"><img src="logo/oct-wordmark.svg" alt="โลโก้ OCT. 26" style="max-height:100%"></div>
 <div style="display:flex;flex-direction:column;gap:12px;min-width:0"><span class="eyebrow">BRAND BOOK · ฉบับสัดส่วนทองคำ · 15 ต.ค. 2569</span>
 <h1>คู่มือแบรนด์ OCT. 26</h1><p class="lead">{E(b['tag_en'])} {E(b['tag_th'])} · {E(b['line'])}</p>
 <p>คู่มือนี้ใช้กับทุกอย่างที่มีชื่อ OCT. 26 และซับแบรนด์ห้าหมี ตั้งแต่ป้ายบูธ ถุง สติกเกอร์ ไปจนถึงโพสต์ในโซเชียล</p></div>
</header>

<section id="name"><span class="eyebrow">ชื่อแบรนด์</span><h2>OCT. 26 ชื่อที่ซ่อนวันเกิดของเธอ</h2>
<div class="grid">{mean}</div>
<p class="cap">ค้นเว็บเมื่อ 14 ต.ค. 2569 ไม่เจอแบรนด์เครื่องหนังหรือบัญชีไทยชื่อ OCT. 26 แต่มีแบรนด์เครื่องหนังที่ขึ้นต้นด้วย Oct อยู่แล้ว (Octovo, Octogony) การค้นเว็บไม่ใช่การค้นเครื่องหมายการค้า ก่อนพิมพ์จำนวนมาก ค้นในฐานข้อมูลกรมทรัพย์สินทางปัญญา และเช็กว่า @{b['handle']} ยังว่างทุกช่องทาง ชื่ออื่นที่คิดไว้ทั้งหมดอยู่ใน {link("alternatives", "หน้าทางเลือกแบรนด์")}</p></section>

<section id="arch"><span class="eyebrow">โครงสร้างแบรนด์</span><h2>แบรนด์หลัก คอลเลกชัน และซับแบรนด์</h2>
<p class="lead">หมีห้าตัวเป็นซับแบรนด์ได้ ใช้ชื่อเต็มว่า ห้าหมี FIVE BEARS by OCT. 26</p>
<div class="grid">{arch}</div>
<div class="grid">{answer}</div></section>

<section id="story"><span class="eyebrow">STORY TELLING</span><h2>เรื่องของ OCT. 26</h2>
<p class="lead">{E(B.STORY_SHORT)}</p>
<div class="grid">{story}</div>
<div class="card">{copybox("bio", B.STORY_BIO, "ประโยคแนะนำตัวสั้น ใช้เป็น bio")}</div></section>

<section id="logo"><span class="eyebrow">โลโก้</span><h2>สี่โลโก้ ใช้ทีละตัว</h2>
<p class="lead">ทั้งบ้านมีโลโก้แค่สี่ตัว แบรนด์ละสอง คือชื่อเต็มหนึ่งตัว กับสัญลักษณ์ตอนพื้นที่เล็กหนึ่งตัว ใช้ทีละตัวเสมอ ไม่วางป้ายห้อยคู่กับชื่อ เพราะป้ายก็บอก 26 อยู่แล้ว คนจะเห็นแค่ OCT. 26 กับป้าย 26 ซ้ำ ๆ จนจำได้</p>
<div class="tbl"><table><thead><tr><th>โลโก้</th><th>ใช้ที่ไหน</th></tr></thead><tbody>{logo_rows}</tbody></table></div>
<p>ตัวอักษรวาดเองจากวงกลมและเส้นตรง ไม่ใช่ฟอนต์ จุดสีมะเขือเทศเป็นส่วนเดียวที่ใหญ่กว่าเส้น จึงเป็นสิ่งที่คนจำ ป้ายห้อยสัดส่วน 1 : φ ฐานของเลข 26 อยู่ตรงเส้นแบ่งทองคำ ทุกโลโก้มีสามแบบ บนพื้นสว่าง บนพื้นเข้ม และสีเดียว</p>
{oct_logos}
<div class="card"><h3>กติกาการใช้โลโก้</h3><ul style="margin-top:8px">
<li>เขียนชื่อในข้อความว่า OCT. 26 ตัวใหญ่ มีจุด และเว้นวรรคหนึ่งครั้ง ชื่อบัญชีใช้ {E(b['handle'])}</li>
<li>เว้นที่ว่างรอบโลโก้อย่างน้อย จุด × φ ทุกด้าน</li>
<li>ใช้ทีละตัว ไม่วางป้ายห้อยคู่กับชื่อ OCT. 26 ในพื้นที่เดียวกัน</li>
<li>OCT. 26 เล็กสุดกว้าง 34 มม. ถ้าเล็กกว่านั้นใช้ป้ายห้อย ซึ่งเล็กสุดสูง 8 มม.</li>
<li>our crafted things. เป็นข้อความ ไม่ใช่ส่วนหนึ่งของโลโก้ วางใต้ชื่อได้เมื่อหน้างานมีที่ เช่น ปกโซเชียลและการ์ด</li>
<li>จุดเป็นสีมะเขือเทศเสมอ ยกเว้นงานสีเดียว แบรนด์วันเกิดแต่ละแบรนด์ใช้สีของเจ้าของวันเกิด ห้ามบีบ ยืด หมุน หรือใส่เงา</li>
<li>ไฟล์ SVG ทุกไฟล์แปลงตัวอักษรเป็นเส้นแล้ว ส่งร้านพิมพ์ได้เลยโดยไม่ต้องมีฟอนต์</li></ul></div></section>

<section id="golden"><span class="eyebrow">สัดส่วนทองคำ</span><h2>ทุกอย่างมาจาก φ = 1.618</h2>
<p class="lead">ขนาดของทุกชิ้น ตั้งแต่ความหนาเส้นในโลโก้ จนถึงขนาดถุงกระดาษ คำนวณจากตัวเลขเดียว ทุกส่วนจึงสัมพันธ์กันเอง ตาคนจึงรู้สึกว่าลงตัว</p>
<div class="paper">{LL.wordmark_construction()}</div>
<div class="paper" style="max-width:377px">{LL.tag_construction()}</div>
<div class="tbl"><table><tbody>{golden_rows}</tbody></table></div>
<p class="cap">ภาพเส้นโครงและการทดสอบตั้งแต่ 16 พิกเซลถึงบิลบอร์ดอยู่ใน {link("logolab", "Logo Lab")}</p></section>

<section id="collections"><span class="eyebrow">คอลเลกชัน</span><h2>SOI. 02 และ Love</h2>
<div class="grid">{colls}</div></section>

<section id="fivebears"><span class="eyebrow">ซับแบรนด์</span><h2>ห้าหมี FIVE BEARS by OCT. 26</h2>
<p class="lead">หมีในโลโก้คือเส้นตัดของแบบ 01 ที่หมุน 45 องศา ร่องสองเส้นเป็นแก้ม หัวใจตรงกลางคือแม่ ใช้กับสินค้าคอลเลกชัน Love และทุกอย่างที่ทำให้เด็ก</p><p class="cap">แบบ 01 หามาจากอินเทอร์เน็ต ใช้ช่วงเปิดตัวได้ แต่ต้องวาดหมีใหม่จากแพตเทิร์นของเราเองก่อนยื่นจดเครื่องหมายการค้า</p>
<div class="paper"><img src="logo/family.svg" alt="หมีห้าตัว สีเดียวกับแบรนด์วันเกิดของแต่ละคน"></div>
<div class="grid">{fam}</div>
{bear_logos}
<p class="cap">ห้าหมีมีบรรทัด by OCT. 26 เสมอ ยกเว้นตัวหมีเดี่ยวและสติกเกอร์ ที่เล็กเกินจะอ่าน</p></section>

<section id="color"><span class="eyebrow">สี · เลือกแล้ว ชุดที่ 2</span><h2>สีสด สะดุดตา หนึ่งคนหนึ่งสี</h2><p class="lead">เลือกแล้ววันที่ 15 ต.ค. 2569 จากหน้าสุ่มสี ชุดที่ 2 แต่ละสีของครอบครัวเป็นสีของคนหนึ่งคน ใช้กับแบรนด์วันเกิดและหมีของคนนั้น</p>
<h3>สีหลัก</h3><div class="grid s">{swatches(B.MASTER_KEYS)}</div>
<p class="cap">สัดส่วนตาม φ: พื้นครีมนม 61.8% หมึกและโคบอลต์ 23.6% มะเขือเทศและสีครอบครัว 14.6% ตัวหนังสือเล็กใช้หมึกหรือโคบอลต์ มะเขือเทศใช้กับจุด ราคา และปุ่ม</p>
<h3>สีครอบครัว</h3><div class="grid s">{swatches([k for k, *_ in B.PALETTE if k not in B.MASTER_KEYS])}</div></section>

<section id="type"><span class="eyebrow">ตัวอักษร</span><h2>ตัวอักษรโลโก้ที่วาดเอง และสี่ฟอนต์จาก Google Fonts</h2>
<div class="paper"><img src="logo/oct-wordmark.svg" alt="ตัวอักษรโลโก้ OCT. Geometric" style="max-height:89px"></div><p class="cap">{E(B.FONTS["logo"][0])} · {E(B.FONTS["logo"][1])}</p>
<div class="grid">{fonts}</div></section>

<section id="voice"><span class="eyebrow">น้ำเสียง</span><h2>พูดแบบ OCT. 26</h2><div class="grid">{voice}</div></section>

<section id="use"><span class="eyebrow">ตัวอย่างใช้งาน</span><h2>รูปโปรไฟล์ ปก และโปสเตอร์</h2>
<p class="cap">บนมือถือ กดค้างที่รูปเพื่อบันทึก ไฟล์ทั้งหมดอยู่ในโฟลเดอร์ brand-20261014/logo ของโปรเจกต์</p>
<div class="grid">{app_cards}</div>
<div class="grid">
<figure class="card" style="margin:0;display:flex;flex-direction:column;gap:8px"><img src="posters/18-post.png" alt="ตัวอย่างโปสเตอร์ SOI. 02 กล่องของชำร่วยงานแต่ง" style="border-radius:10px">
<figcaption class="cap">โปสเตอร์ SOI. 02 ขอบ 89 ช่องไฟฟีโบนัชชี</figcaption></figure>
<figure class="card" style="margin:0;display:flex;flex-direction:column;gap:8px"><img src="posters/21-post.png" alt="ตัวอย่างโปสเตอร์ห้าหมี Love ราวหมีห้าตัว" style="border-radius:10px">
<figcaption class="cap">โปสเตอร์ห้าหมี Love · ดูทั้ง 30 ตัวใน {link("launch", "ชุดเปิดตัว")}</figcaption></figure></div></section>
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
        coll = (f'<span class="chip" style="background:{"#FFE3F1" if p["coll"] == "love" else "#E3E8FB"};color:{"#A3215F" if p["coll"] == "love" else "#1A35A3"}">'
                f'{E(p["line"])}</span>')
        cards += f"""<article class="card" id="p{n}" style="display:grid;gap:14px;grid-template-columns:minmax(0,min(180px,36%)) minmax(0,1fr)">
<a href="posters/{n:02d}-post.png" target="_blank" rel="noopener"><img src="posters/thumb/{n:02d}.jpg" alt="โปสเตอร์ {E(p['name'])}" loading="lazy" style="border-radius:10px;border:1px solid var(--line)"></a>
<div style="display:flex;flex-direction:column;gap:6px;min-width:0"><span class="cap mono">#{n:02d}</span><h3>{E(p['name'])}{hero}</h3>
<p class="cap" style="font-size:14px">{E(p['pieces_txt'])}{(' + ' + E(p['extra'][0])) if p['extra'] else ''}</p>
<p class="mono"><b style="font-family:var(--display);font-size:20px;color:var(--heart)">{p['price']} บาท</b>
 <span class="cap">ต้นทุน {p['cost']:.2f} · กำไร {p['profit']:.0f} ({p['margin']:.0%}) · เตรียมไปงาน {p['stock']} ชิ้น</span></p>
<p>{coll} <span class="chip {status_chip(p['status'])}">{p['status']}</span></p>
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
    return f"""{head("OCT. 26 Launch Kit")}
<div class="wrap">
<nav class="top" aria-label="หัวข้อ"><a href="#plan">แผนถึงวันงาน</a><a href="#social">โซเชียลและ Shopee</a><a href="#products">สินค้า 30 ตัว</a>
<a href="#stock">สต็อกไปงาน</a><a href="#kids">ลูก ๆ ขายของ</a><a href="#print">ของต้องพิมพ์</a><a href="#more">แนะนำเพิ่ม</a></nav>
<header style="padding-top:28px;display:flex;flex-direction:column;gap:12px"><span class="eyebrow">LAUNCH KIT · บูธ 23–25 ต.ค. 2569</span>
<h1>OCT. 26 พร้อมออกบูธ</h1>
<p class="lead">ทุกอย่างที่ต้องทำก่อนวันงาน ข้อความโพสต์ของสินค้า 30 ตัวสำหรับ 5 ช่องทาง และคู่มือให้ลูก ๆ ขายของเอง สินค้าแบ่งเป็นคอลเลกชัน SOI. 02 และห้าหมี Love กดปุ่มคัดลอกแล้ววางในแอปได้เลย</p>
<div class="grid s">
<div class="card"><p class="cap">สินค้า</p><b style="font-family:var(--display);font-size:28px">30 แบบ</b></div>
<div class="card"><p class="cap">เตรียมไปงาน</p><b style="font-family:var(--display);font-size:28px" class="mono">{tot['units']} ชิ้น</b></div>
<div class="card"><p class="cap">ถ้าขายหมด</p><b style="font-family:var(--display);font-size:28px" class="mono">{tot['sales']:,.0f} บาท</b></div>
<div class="card"><p class="cap">ต้นทุนของทั้งหมด</p><b style="font-family:var(--display);font-size:28px" class="mono">{tot['cost']:,.0f} บาท</b></div>
</div>
<p class="cap">ต้นทุนคิดแบบเดียวกับ {link("sheet", "Google Sheet ต้นทุน")} (หนัง ค่าตัด 1.50 ค่าบล็อกเฉลี่ย 0.95 ค่าประกอบ ค่าแพ็ค บรรจุภัณฑ์ 5 บาท) ยังไม่รวมค่าบูธ ค่าพิมพ์ และค่าบล็อกที่ต้องสั่งใหม่</p>
</header>

<section id="plan"><span class="eyebrow">แผนถึงวันงาน · 9 วันถึงบูธ</span><h2>14 ถึง 26 ตุลาคม</h2>
<div class="tbl"><table><tbody>{tl}</tbody></table></div>
<p class="cap">งานที่ช้าที่สุดคือบล็อกตัด ถ้ายังไม่มีบล็อกแบบไหน ให้สั่งวันนี้ แบบที่ได้ไม่ทันให้ขายแบบสั่งจองผ่าน Shopee แทน</p></section>

<section id="social"><span class="eyebrow">โซเชียลมีเดียและร้าน Shopee</span><h2>ห้าช่องทาง ชื่อเดียวกัน</h2>
<p class="lead">ทุกช่องใช้ชื่อ @{B.BRAND['handle']} รูปโปรไฟล์และปกอยู่ใน {link("brandbook", "Brand Book")} บัญชีต้องเปิดในชื่อพ่อหรือแม่ เพราะทุกแพลตฟอร์มกำหนดอายุขั้นต่ำ 13 ปี และ Shopee ต้องใช้บัตรประชาชนกับบัญชีธนาคาร</p>
<div class="grid">{ch}</div>
<div class="card"><h3>9 โพสต์แรก</h3><ol style="margin-top:6px">
<li>ทำไมชื่อ OCT. 26 (ใช้ข้อความใน Brand Book + โลโก้ OCT. 26)</li><li>เปิดตัวคอลเลกชัน SOI. 02 และห้าหมี Love (ป้าย SOI. 02 กับป้าย Love)</li><li>แนะนำลูกสามคน และหน้าที่ที่บูธ</li>
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

<section id="kids"><span class="eyebrow">ลูก ๆ ขายของ</span><h2>สามหน้าที่ ทำได้ตามวัย</h2>
<div class="grid">{roles}</div>
<h3>ประโยคที่ซ้อมไว้</h3><div class="tbl"><table><tbody>{scripts}</tbody></table></div>
<div class="card"><h3>กติกาบูธ</h3><ul style="margin-top:6px">{rules}</ul></div></section>

<section id="print"><span class="eyebrow">ของต้องพิมพ์</span><h2>สั่งร้านพิมพ์ภายใน 15 ต.ค.</h2>
<div class="tbl"><table><thead><tr><th>รายการ</th><th>จำนวน</th><th>หมายเหตุ</th></tr></thead><tbody>{prints}</tbody></table></div></section>

<section id="more"><span class="eyebrow">ข้อ 7 · แนะนำเพิ่ม</span><h2>สิ่งที่ควรทำต่อ</h2><div class="grid">{more}</div></section>
</div>{COPY_JS}"""

# ---------------------------------------------------------------- brand bible
BIBLE_CSS = """
.ch-head{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.ch-no{font-family:var(--logo);font-weight:500;font-size:15px;color:var(--brick);letter-spacing:.06em}
.big{font-family:var(--display);font-weight:600;font-size:clamp(24px,5.6vw,34px);line-height:1.35;text-wrap:balance}
.quote{border-left:4px solid var(--brick);padding:4px 0 4px 16px;font-size:18px}
.duo{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr))}
.duo>*{min-width:0}
.tile{display:flex;flex-direction:column;gap:4px}
.tile b{font-family:var(--logo);font-weight:500;font-size:26px;color:var(--brick);font-variant-numeric:tabular-nums}
.slider{display:grid;grid-template-columns:5.5em 1fr 5.5em;align-items:center;gap:10px;font-size:14px}
.slider .r{text-align:right}
.track{position:relative;height:6px;border-radius:3px;background:var(--line)}
.track i{position:absolute;top:50%;width:18px;height:18px;margin:-9px 0 0 -9px;border-radius:50%;border:2px solid var(--paper)}
.key{display:inline-flex;align-items:center;gap:6px;font-size:13px;color:var(--muted)}
.key i{width:12px;height:12px;border-radius:50%;display:inline-block}
.bar{display:flex;height:34px;border-radius:10px;overflow:hidden}
.bar span{display:flex;align-items:center;justify-content:center;color:#fff;font-size:13px;font-variant-numeric:tabular-nums;min-width:0}
.thumbs{display:flex;gap:8px;flex-wrap:wrap}
.thumbs figure{margin:0;width:72px;display:flex;flex-direction:column;gap:2px}
.thumbs img{border-radius:6px;border:1px solid var(--line)}
.thumbs figcaption{font-size:11px;color:var(--muted);line-height:1.3}
.tl{display:grid;grid-template-columns:7.5em 1fr;gap:0 14px}
.tl>div{padding:10px 0;border-bottom:1px solid var(--line);min-width:0}
.tl .d{font-family:var(--logo);font-weight:500;font-size:13.5px;font-variant-numeric:tabular-nums}
.tag{display:inline-block;font-size:12px;border-radius:99px;padding:1px 9px;margin-left:6px}
.tag.oct{background:#E3E8FB;color:#1A35A3}.tag.bear{background:#FFE3F1;color:#A3215F}
.check{list-style:none;padding:0;display:grid;gap:6px}
.check li{display:flex;gap:10px;align-items:flex-start}
.check li::before{content:"";flex:none;width:16px;height:16px;margin-top:4px;border:2px solid var(--brick);border-radius:4px}
"""

def bible():
    import bible as V
    byn = {p["n"]: p for p in B.PRODUCTS}
    def ch(no, id_, eyebrow, title, body):
        return (f'<section id="{id_}"><div class="ch-head"><span class="ch-no">{no:02d}</span><span class="eyebrow">{E(eyebrow)}</span></div>'
                f'<h2>{E(title)}</h2>{body}</section>')
    def svgimg(f, alt, cls="paper", ratio=None):
        st = f' style="aspect-ratio:{ratio}"' if ratio else ""
        return f'<div class="{cls}"{st}><img src="bible/{f}.svg" alt="{E(alt)}" style="max-height:100%"></div>'
    values = "".join(
        f'<div class="card" style="display:flex;flex-direction:column;gap:8px"><h3>{E(v)} <span class="cap" style="font-family:var(--logo);font-weight:500">{E(en)}</span></h3>'
        f'<p><span class="chip ok">เราทำ</span> {E(do)}</p><p><span class="chip ext">เราไม่ทำ</span> {E(dont)}</p></div>' for v, en, do, dont in V.VALUES)
    core = (f'<p class="big">{E(V.ESSENCE[0])} <span style="font-family:var(--logo);color:var(--brick)">{E(V.ESSENCE[1])}</span></p>'
            f'<div class="card"><span class="eyebrow">เหตุผลที่มีแบรนด์นี้</span><p style="margin-top:6px;font-size:17px">{E(V.PURPOSE)}</p>'
            f'<p class="cap" style="margin-top:8px">ฉบับสั้น · {E(V.PURPOSE_SHORT)}</p></div>'
            f'<div class="duo"><div class="card"><span class="eyebrow">ภาพในอีก 5 ปี</span><p style="margin-top:6px">{E(V.VISION)}</p></div>'
            f'<div class="card"><span class="eyebrow">สิ่งที่ทำทุกวัน</span><ol style="margin-top:6px">{"".join(f"<li>{E(m)}</li>" for m in V.MISSION)}</ol></div></div>'
            f'<p class="quote"><b>คำสัญญากับลูกค้า</b><br>{E(V.PROMISE)}</p>'
            f'<p class="cap">ตัวเลือกอื่น · {" · ".join(E(x) for x in V.PROMISE_ALT)}</p>'
            f'<h3>คุณค่า {len(V.VALUES)} ข้อ</h3><div class="duo">{values}</div>')
    proof = "".join(f'<div class="card tile"><b>{E(n)}</b><span class="cap" style="font-size:14px">{E(t)}</span></div>' for n, t in V.PROOF)
    alts = "".join(
        f'<div class="card" style="display:flex;flex-direction:column;gap:6px{";border:2px solid var(--brick)" if o == "OCT. 26" else ""}">'
        f'<h3>{E(o)}</h3><span class="cap mono">{E(pr)}</span><p><span class="chip ok">ได้</span> {E(get)}</p><p><span class="chip ext">ขาด</span> {E(miss)}</p></div>'
        for o, pr, get, miss in V.ALTERNATIVES)
    pos = (f'<p class="quote">{E(V.POSITIONING)}</p><div class="grid s">{proof}</div>'
           f'<div class="duo">{svgimg("map", "แผนที่ตำแหน่ง OCT. 26 เทียบกับทางเลือกอื่น", ratio="9/7")}'
           f'<div class="card"><h3>ถ้าไม่ซื้อเรา ลูกค้าซื้ออะไร</h3><p class="cap" style="font-size:14px;margin-top:4px">แผนที่ด้านข้างเทียบสองเรื่อง ต่อเองได้หรือไม่ และมีเรื่องเล่าหรือไม่ OCT. 26 อยู่มุมขวาบนคนเดียว</p></div></div>'
           f'<div class="grid">{alts}</div>'
           f'<p class="cap">แถวสุดท้ายบอกจุดอ่อนของเราเองด้วย ใช้ตอบลูกค้าที่ถามตรง ๆ ช่วงราคาของทางเลือกอื่นเป็นค่าประมาณจากที่เห็นทั่วไป ควรเช็กกับร้านจริงก่อนใช้ในการขาย</p>')
    personas = ""
    for who, need, ns, chn, line in V.PERSONAS:
        th = "".join(f'<figure><img src="posters/thumb/{n:02d}.jpg" alt="{E(byn[n]["name"])}" loading="lazy"><figcaption>{E(byn[n]["name"])} · {byn[n]["price"]}</figcaption></figure>' for n in ns)
        personas += (f'<div class="card" style="display:flex;flex-direction:column;gap:8px"><h3>{E(who)}</h3><p class="cap" style="font-size:14px">{E(need)}</p>'
                     f'<p class="quote" style="font-size:15.5px">“{E(line)}”</p><p class="cap">เจอได้ที่ {E(chn)}</p><div class="thumbs">{th}</div></div>')
    arche = "".join(f'<div class="card"><span class="eyebrow">{E(b_)}</span><h3 style="margin-top:4px">{E(a)}</h3><p style="margin-top:6px">{E(t)}</p></div>' for b_, a, t in V.ARCHETYPE)
    sliders = "".join(
        f'<div class="slider"><span>{E(l)}</span><div class="track"><i style="left:{(o-1)*25}%;background:var(--brick)" title="OCT. 26"></i>'
        f'<i style="left:{(f-1)*25}%;background:var(--love)" title="ห้าหมี"></i></div><span class="r">{E(r)}</span></div>' for l, r, o, f in V.SLIDERS)
    isnot = "".join(f'<div class="tbl"><table><thead><tr><th>{E(k)} เป็น</th><th>แต่ไม่</th></tr></thead><tbody>'
                    + "".join(f'<tr><td><b>{E(a)}</b></td><td><s>{E(b_)}</s></td></tr>' for a, b_ in v) + '</tbody></table></div>'
                    for k, v in V.IS_NOT.items())
    samples = "".join(f'<tr><td><b>{E(t)}</b></td><td>{E(o)}</td><td>{E(f)}</td></tr>' for t, o, f in V.VOICE_SAMPLES)
    person = (f'<div class="duo">{arche}</div><div class="card" style="display:flex;flex-direction:column;gap:14px">'
              f'<div style="display:flex;gap:16px;flex-wrap:wrap"><span class="key"><i style="background:var(--brick)"></i>OCT. 26</span>'
              f'<span class="key"><i style="background:var(--love)"></i>ห้าหมี</span></div>{sliders}</div>'
              f'<div class="duo">{isnot}</div><h3>เรื่องเดียวกัน สองน้ำเสียง</h3>'
              f'<div class="tbl"><table><thead><tr><th>เรื่อง</th><th>OCT. 26</th><th>ห้าหมี</th></tr></thead><tbody>{samples}</tbody></table></div>')
    pillars = "".join(
        f'<div class="card" style="display:flex;flex-direction:column;gap:8px"><span class="eyebrow">เสาที่ {i}</span><h3>{E(h)}</h3><p class="cap">{E(sub)}</p>'
        f'<ul>{"".join(f"<li>{E(x)}</li>" for x in pr)}</ul><p class="quote" style="font-size:15px">“{E(ex)}”</p></div>'
        for i, (h, sub, pr, ex) in enumerate(V.PILLARS, 1))
    tags = "".join(f'<tr><td><b>{E(w)}</b></td><td style="font-family:var(--logo);font-weight:500">{E(en)}</td><td>{E(th)}</td><td class="cap">{E(use)}</td></tr>' for w, en, th, use in V.TAGLINES)
    pitch = "".join(f'<div class="card">{copybox(f"pitch{i}", t, f"{d} · {who}")}</div>' for i, (d, who, t) in enumerate(V.PITCH))
    lex = "".join(f'<tr><td><span class="chip ok">ใช้</span> {E(u)}</td><td><span class="chip ext">เลี่ยง</span> {E(a)}</td><td class="cap">{E(w)}</td></tr>' for u, a, w in V.LEXICON)
    msg = (f'<h3>สามเสาของสาร</h3><div class="grid">{pillars}</div><h3>สโลแกน</h3>'
           f'<div class="tbl"><table><thead><tr><th>ใช้กับ</th><th>อังกฤษ</th><th>ไทย</th><th>ที่ใช้</th></tr></thead><tbody>{tags}</tbody></table></div>'
           f'<h3>เล่าแบรนด์ในหนึ่งนาที</h3><div class="grid">{pitch}</div>'
           f'<h3>คำที่ใช้ คำที่เลี่ยง</h3><div class="tbl"><table><tbody>{lex}</tbody></table></div>')
    naming = "".join(f'<div class="card" style="display:flex;flex-direction:column;gap:6px"><span class="eyebrow">{E(a)}</span><h3>{E(rule)}</h3>'
                     f'<p style="font-size:14.5px">{E(how)}</p><p class="mono" style="font-family:var(--logo);font-weight:500;color:var(--brick)">{E(ex)}</p></div>' for a, rule, how, ex in V.NAMING)
    codes = " · ".join(f'<span class="mono">{V.product_code(p)}</span> {E(p["name"])}' for p in B.PRODUCTS)
    names = (f'<div class="grid">{naming}</div>'
             f'<details><summary>รหัสสินค้าทั้ง 30 ตัว</summary><p style="font-size:14px;padding-bottom:12px">{codes}</p></details>')
    dist = "".join(f'<div class="card" style="display:flex;flex-direction:column;gap:6px"><h3>{E(a)}</h3><p class="cap" style="font-size:14px">{E(w)}</p>'
                   f'<p style="font-size:14.5px"><b>ใช้ที่</b> {E(where)}</p><p style="font-size:14.5px"><b>กติกา</b> {E(pr)}</p></div>' for a, w, where, pr in V.DISTINCTIVE)
    photo = "".join(f'<div class="card"><h3>{E(h)}</h3><p class="cap" style="font-size:14px;margin-top:4px">{E(t)}</p></div>' for h, t in V.PHOTO_RULES)
    shots = "".join(f'<tr><td><b>{E(a)}</b></td><td>{E(b_)}</td><td class="cap">{E(c)}</td></tr>' for a, b_, c in V.SHOTS)
    visual = (f'<p class="lead">ลูกค้าจำแบรนด์จากสิ่งที่เห็นซ้ำ ๆ ห้าอย่างนี้คือสิ่งที่ต้องอยู่ในทุกงาน และห้ามเปลี่ยนเล่น</p>'
              f'<div class="grid">{dist}</div>'
              f'<h3>ลายปีกและร่อง</h3>{svgimg("pattern", "ลายพื้นจากชิ้นหนังจริงห้าแบบของ SOI. 02", ratio="3/2")}'
              f'<p class="cap">ลายจากเส้นตัดจริงของแพตเทิร์น 02–06 ใช้กับกระดาษห่อ พื้นหลังโพสต์ และผนังบูธ ไฟล์ bible/svg/pattern.svg</p>'
              f'<h3>ภาพถ่าย</h3><div class="grid">{photo}</div>'
              f'<div class="tbl"><table><thead><tr><th>ภาพ</th><th>ถ่ายอย่างไร</th><th>ใช้ที่</th></tr></thead><tbody>{shots}</tbody></table></div>')
    touch = "".join(
        f'<figure class="card" style="margin:0;display:flex;flex-direction:column;gap:10px">{svgimg(f, n) if f else ""}'
        f'<figcaption><h3>{E(n)}</h3><p class="cap" style="font-size:14px">{E(sz)} · {E(mat)}</p><p class="cap">{E(use)}</p></figcaption></figure>'
        for n, sz, mat, use, f in V.TOUCH)
    pack = (f'<div class="grid">{touch}</div><div class="card"><h3>ลำดับเมื่อลูกค้าเปิดถุง</h3><ol style="margin-top:6px">{"".join(f"<li>{E(x)}</li>" for x in V.UNBOX)}</ol></div>'
            f'<div class="card" style="border:2px solid var(--brick)"><h3>งบบรรจุภัณฑ์</h3><p style="margin-top:6px">{E(V.PACK_BUDGET)}</p></div>'
            f'<p class="cap">ป้ายห้อยตัวอย่างใช้สินค้าจริง {E(V.product_code(byn[18]))} และ {E(V.product_code(byn[23]))} ช่องสี่เหลี่ยมบนการ์ดคือที่วาง QR ของ Instagram เมื่อเปิดบัญชีแล้ว</p>')
    journey = "".join(f'<div class="card"><span class="eyebrow">{i}. {E(a)}</span><p style="margin-top:4px">{E(b_)}</p><p class="cap">{E(c)}</p></div>'
                      for i, (a, b_, c) in enumerate(V.JOURNEY, 1))
    booth = (f'<div class="duo">{svgimg("booth", "ผังบูธ โต๊ะ SOI. 02 ทางซ้าย โต๊ะห้าหมี Love ทางขวา จุดสาธิตหน้าโต๊ะ", ratio="76/70")}'
             f'<div style="display:flex;flex-direction:column;gap:10px;min-width:0">{journey}</div></div>'
             f'<p class="cap">ผังนี้สมมติบูธขนาด 2 × 2 เมตร ถ้าบูธจริงต่างไป ให้คงหลักเดิม แยกสองคอลเลกชันซ้ายขวา และวางของให้ลองดึงไว้ด้านหน้าเสมอ</p>')
    mix = "".join(f'<span style="flex:{p} 1 0;background:var(--{"love" if c == "heart" else c})" title="{E(n)}">{p}%</span>' for n, p, d, c in V.CONTENT_MIX)
    mixl = "".join(f'<tr><td><b>{E(n)}</b></td><td class="n">{p}%</td><td>{E(d)}</td></tr>' for n, p, d, c in V.CONTENT_MIX)
    week = "".join(f'<div class="card tile"><b style="font-family:var(--display);font-size:20px;color:var(--ink)">{E(d)}</b><span class="cap" style="font-size:14px">{E(t)}</span></div>' for d, t in V.WEEK)
    tone = "".join(f'<tr><td><b>{E(c)}</b></td><td>{E(t)}</td><td class="cap">{E(w)}</td></tr>' for c, t, w in V.CHANNEL_TONE)
    content = (f'<div class="bar" role="img" aria-label="สัดส่วนคอนเทนต์">{mix}</div>'
               f'<div class="tbl"><table><tbody>{mixl}</tbody></table></div><h3>สัปดาห์หนึ่ง</h3><div class="grid s">{week}</div>'
               f'<h3>น้ำเสียงแต่ละช่องทาง</h3><div class="tbl"><table><thead><tr><th>ช่องทาง</th><th>พูดอย่างไร</th><th>คนที่เจอ</th></tr></thead><tbody>{tone}</tbody></table></div>')
    year = "".join(f'<div class="d">{E(d)}</div><div><b>{E(t)}</b><span class="tag {k}">{"OCT. 26" if k == "oct" else "ห้าหมี"}</span><p class="cap" style="font-size:14px">{E(x)}</p></div>'
                   for d, t, x, k in V.YEAR)
    ritual = (f'<div class="duo"><div class="tl">{year}</div>{svgimg("edition", "การ์ดรุ่นวันเกิด OCT. 26 – No. 42 ชิ้นที่ 07 จาก 42", ratio="1")}</div>'
              f'<p class="cap">วันที่ของเทศกาลที่ไม่ตายตัว เช่น ตรุษจีน ให้เช็กปฏิทินปีนั้นก่อนวางแผนผลิต</p>')
    roles = "".join(f'<tr><td><b>{E(a)}</b></td><td>{E(b_)}</td></tr>' for a, b_ in V.ROLES)
    checks = "".join(f"<li>{E(c)}</li>" for c in V.CHECKLIST)
    health = "".join(f'<tr><td><b>{E(a)}</b></td><td>{E(b_)}</td><td class="cap" style="white-space:nowrap">{E(c)}</td></tr>' for a, b_, c in V.HEALTH)
    care = (f'<div class="tbl"><table><thead><tr><th>ใคร</th><th>ดูแลอะไร</th></tr></thead><tbody>{roles}</tbody></table></div>'
            f'<p class="cap">นี่คืองานประจำนอกบูธ เป็นข้อเสนอ ปรับได้ตามที่ทั้งบ้านตกลงกัน ส่วนหน้าที่ที่บูธ (ต้อนรับ สาธิต รับเงิน) อยู่ใน {link("launch", "Launch Kit")}</p>'
            f'<div class="card"><h3>เช็กก่อนโพสต์ทุกครั้ง</h3><ul class="check" style="margin-top:8px">{checks}</ul></div>'
            f'<h3>วัดว่าแบรนด์โตไหม</h3><div class="tbl"><table><thead><tr><th>ดูอะไร</th><th>วัดอย่างไร</th><th>บ่อยแค่ไหน</th></tr></thead><tbody>{health}</tbody></table></div>'
            f'<p class="cap">ทุกอย่างในคู่มือนี้แก้ได้ที่ไฟล์ brand-20261014/bible.py และ brand.py แล้วสร้างหน้าใหม่ ลิงก์เดิมไม่เปลี่ยน</p>')
    def dm(d, big=False):
        mon, day = d.split(". ")
        return (f'<span style="font-family:var(--logo);font-weight:500;font-size:{30 if big else 22}px;white-space:nowrap">{E(mon)}'
                f'<span style="color:var(--brick)">.</span> {E(day)}</span>')
    fam = "".join(f'<div class="card" style="display:flex;flex-direction:column;gap:4px{";border:2px solid var(--brick)" if main else ""}">'
                  f'{dm(d, main)}<b style="font-family:var(--display);font-weight:500">{E(who)}</b><span class="cap">{E(st)}</span></div>'
                  for d, who, st, main in V.FAMILY_BRANDS)
    ladder = "".join(f'<div class="card" style="display:flex;flex-direction:column;gap:6px"><span class="eyebrow">ขั้นที่ {i} · {E(when)}</span><h3>{E(st)}</h3>'
                     f'<p style="font-size:14.5px">{E(what)}</p><p class="cap">ลูก ๆ ทำ: {E(kids)}</p><p class="cap">ตัวอย่าง: {E(ex)}</p></div>'
                     for i, (st, what, kids, ex, when) in enumerate(V.GROWTH, 1))
    family = (f'<p class="lead">OCT. 26 เป็นบ้านหลังใหญ่ที่เรียบ ทุกคนในบ้านมีแบรนด์วันเกิดของตัวเองได้ ห้าหมีคือทั้งห้าคนรวมกัน</p>'
              f'<div class="grid s">{fam}</div><div class="card"><ul>{"".join(f"<li>{E(r)}</li>" for r in V.FAMILY_RULES)}</ul></div>'
              f'<h3>แบรนด์โตไปพร้อมลูก ๆ</h3><div class="grid">{ladder}</div>'
              f'<p class="cap">กระเป๋าสะพายข้างสามแบบจากแพตเทิร์นที่มี พร้อมต้นทุนและราคาเทียบตลาด อยู่ใน {link("productlab", "หน้าวิจัยสินค้า")}</p>'
              f'<div class="card" style="border:2px solid var(--brick)"><h3>เรื่องแพตเทิร์น</h3><p style="margin-top:6px">{E(V.PATTERN_NOTE)}</p></div>')
    import importlib.util
    spec = importlib.util.spec_from_file_location("colorlab_build", os.path.join(ROOT, "colorlab", "build.py"))
    CL = importlib.util.module_from_spec(spec); spec.loader.exec_module(CL)
    colors = (f'<p class="lead">เลือกแล้ว ชุดที่ 2 Soi Candy กระดาษครีม หมึกเกือบดำ น้ำเงินโคบอลต์ และแดงมะเขือเทศ ทุกไฟล์ใช้ชุดนี้แล้ว ส่วนทางเลือกอื่นยังเก็บไว้ใน {link("colorlab", "Color Lab")}</p>'
              f'<div class="grid s">' + "".join(
                  f'<figure class="card" style="margin:0;padding:8px;display:flex;flex-direction:column;gap:6px"><img src="colorlab/{k}.svg" alt="แผงสี {E(n)}" style="border-radius:8px">'
                  f'<figcaption class="cap"><b>{E(n)}</b> · {E(fam_)}</figcaption></figure>' for k, fam_, n, *_ in CL.OPTIONS) + '</div>'
              f'<p class="cap">สัดส่วนสีบนงานหนึ่งชิ้น กระดาษ 61.8 หมึก 23.6 สีเด่น 14.6 สีหนัง B8743A เป็นสีวัสดุ ไม่ใช่สีพิมพ์ แก้สีใน brand.py ที่เดียว ทุกไฟล์เปลี่ยนตาม</p>')
    chapters = [("core", "หัวใจแบรนด์", "ทำไมต้องมี OCT. 26", core),
                ("family", "ครอบครัวแบรนด์", "แบรนด์วันเกิดของทุกคน และทางเติบโต", family),
                ("position", "ตำแหน่งแบรนด์", "เราต่างจากทางเลือกอื่นอย่างไร", pos),
                ("people", "ลูกค้า", "สี่กลุ่มที่เราขายให้", personas and f'<div class="duo">{personas}</div>'),
                ("personality", "บุคลิก", "ถ้า OCT. 26 เป็นคน", person),
                ("message", "สาร", "พูดอะไร และพูดอย่างไร", msg),
                ("naming", "ระบบชื่อ", "ตั้งชื่อคอลเลกชันและสินค้า", names),
                ("color", "สีแบรนด์", "เลือกแล้ว ชุดที่ 2 Soi Candy", colors),
                ("visual", "ภาษาภาพ", "สิ่งที่ลูกค้าจะจำได้", visual),
                ("pack", "บรรจุภัณฑ์", "ป้ายห้อย การ์ด และถุง", pack),
                ("booth", "บูธ", "ห้าขั้นจากทางเดินถึงลูกค้า", booth),
                ("content", "คอนเทนต์", "โพสต์อะไร สัปดาห์ละเท่าไร", content),
                ("year", "ปีแรก", "วันสำคัญของแบรนด์ ต.ค. 69 ถึง ต.ค. 70", ritual),
                ("care", "ดูแลแบรนด์", "ใครดูแลอะไร และเช็กอะไร", care)]
    nav = "".join(f'<a href="#{i}">{E(e)}</a>' for i, e, _, _ in chapters)
    body = "".join(ch(n, i, e, t, b_) for n, (i, e, t, b_) in enumerate(chapters, 1))
    return f"""{head("OCT. 26 Brand Bible")}<style>{BIBLE_CSS}</style>
<div class="wrap">
<nav class="top" aria-label="บท">{nav}</nav>
<header style="padding-top:28px;display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));align-items:center">
 <div class="paper dark" style="aspect-ratio:1"><img src="logo/oct-wordmark-reverse.svg" alt="โลโก้ OCT. 26 บนพื้นน้ำเงินโคบอลต์" style="max-height:100%"></div>
 <div style="display:flex;flex-direction:column;gap:12px;min-width:0"><span class="eyebrow">BRAND BIBLE · ฉบับที่ 2 · 15 ต.ค. 2569</span>
 <h1 style="font-family:var(--logo);font-weight:500">OCT. 26</h1>
 <p class="lead">คู่มือว่าแบรนด์นี้คิด พูด และทำอย่างไร ใช้คู่กับ {link("brandbook", "Brand Book")} ที่เก็บโลโก้ สี และไฟล์ ส่วนข้อความโพสต์และสินค้าอยู่ใน {link("launch", "Launch Kit")}</p>
 <p class="cap">{len(chapters)} บท อ่านจบประมาณ 20 นาที ฉบับนี้ปรับตามความเห็นของเจ้าของแบรนด์ 19 ข้อ</p></div>
</header>
{body}
</div>{COPY_JS}"""

# ---------------------------------------------------------------- color lab
def colorlab():
    import importlib.util
    spec = importlib.util.spec_from_file_location("colorlab_build", os.path.join(ROOT, "colorlab", "build.py"))
    CL = importlib.util.module_from_spec(spec); spec.loader.exec_module(CL)
    # our own read of each option, 1..3: eye-catching, looks premium, fits FIVE BEARS, fits real leather
    SCORE = {"oct": (1, 2, 3, 3), "candy": (3, 1, 3, 2), "tropic": (3, 2, 2, 2), "saddle": (1, 3, 1, 3),
             "oxblood": (1, 3, 1, 2), "grandjoke": (3, 3, 2, 2), "pistachio": (3, 2, 3, 2)}
    dots = lambda n: "".join(f'<i style="display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:3px;background:{"var(--brick)" if i < n else "var(--line)"}"></i>' for i in range(3))
    cards, rows, nav = "", "", ""
    for key, fam, name, idea, c, note in sorted(CL.OPTIONS, key=lambda o: o[0] != "candy"):
        won = key == "candy"
        sw = [("พื้น", c["paper"]), ("ตัวหนังสือ", c["ink"]), ("จุด", c["dot"]), ("สีหลัก", c["deep"])]
        sw += [(d, col) for d, col in zip(CL.BIRTHDAYS, c["fam"])]
        swh = "".join(f'<div style="display:flex;flex-direction:column;gap:2px;min-width:0"><span style="height:34px;border-radius:6px;border:1px solid var(--line);background:{h}"></span>'
                      f'<span class="cap mono" style="font-size:11px">{E(l)}<br>{h}</span></div>' for l, h in sw)
        cards += (f'<article class="card" id="{key}" style="display:flex;flex-direction:column;gap:10px;scroll-margin-top:60px{";border:3px solid var(--cobalt)" if won else ""}">'
                  f'<img src="colorlab/{key}.svg" alt="แผงสี {E(name)} บนโลโก้ ป้ายห้อย ห้าแบรนด์วันเกิด และห้าหมี" style="border-radius:10px">'
                  f'<div><span class="chip">{E(fam)}</span>{' <span class="chip" style="background:var(--cobalt);color:#fff">เลือกแล้ว ชุดที่ 2</span>' if won else ""}</div><h3 style="font-family:var(--logo);font-weight:500;font-size:22px">{E(name)}</h3>'
                  f'<p>{E(idea)}</p><div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(64px,1fr));gap:8px">{swh}</div>'
                  f'<p class="cap" style="font-size:14px">{E(note)}</p></article>')
        e, p, f, l = SCORE[key]
        nw = ' style="white-space:nowrap"'
        rows += f'<tr><td><a href="#{key}"><b>{E(name)}</b></a></td><td{nw}>{dots(e)}</td><td{nw}>{dots(p)}</td><td{nw}>{dots(f)}</td><td{nw}>{dots(l)}</td></tr>'
        nav += f'<a href="#{key}">{E(name)}</a>'
    ask = ["ยืนห่างโต๊ะ 5 เมตร แบบไหนเห็นก่อน", "วางชิ้นหนังจริงบนสีพื้น หนังดูสวยขึ้นหรือจมหาย",
           "ลูก ๆ ชอบแบบไหน และห้าหมีดูน่ารักในแบบไหน", "สีนี้จะใช้กับแบรนด์วันเกิดของทุกคนได้ไหม",
           "ราคาที่อยากขายในอีกสองปี สีนี้รับได้ไหม", "พิมพ์ป้ายห้อยจริงสองแบบที่ชอบที่สุด แล้วค่อยตัดสิน"]
    return f"""{head("OCT. 26 Color Lab")}
<div class="wrap">
<nav class="top" aria-label="ทางเลือกสี">{nav}<a href="#compare">เทียบ</a><a href="#ask">คำถาม</a></nav>
<header style="padding-top:28px;display:flex;flex-direction:column;gap:12px"><span class="eyebrow">COLOR LAB · 15 ต.ค. 2569 · เลือกแล้ว ชุดที่ 2</span>
<h1>สีของ OCT. 26 เลือกแล้ว Soi Candy</h1>
<p class="lead">บ้านเราเลือกชุดที่ 2 Soi Candy แล้ว เมื่อ 15 ต.ค. 2569 ทุกไฟล์ของแบรนด์ใช้ชุดนี้ ทางเลือกอื่นเก็บไว้ด้านล่างเพื่อเทียบ</p>
<p class="cap">ทุกแผงใช้ของชุดเดียวกัน โลโก้ รูปโปรไฟล์ ป้ายห้อย ห้าแบรนด์วันเกิด ห้าหมี และถุง เปลี่ยนแค่สี จะได้เทียบกันได้ตรง ๆ</p>
<p class="cap">สามแนวที่ขอ สีสดสะดุดตา หรูแบบเงียบ และหรูแบบตลก แนวละสองแบบ บวกสีตั้งต้นเดิม แต่ละแบบให้สีห้าสีกับห้าแบรนด์วันเกิดไว้ด้วย</p></header>
<section id="options" style="padding-top:28px"><div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(min(100%,380px),1fr))">{cards}</div></section>
<section id="compare"><span class="eyebrow">เทียบ</span><h2>แต่ละแบบเด่นเรื่องไหน</h2>
<div class="tbl"><table><thead><tr><th>แบบ</th><th>สะดุดตา</th><th>ดูหรู</th><th>ห้าหมี</th><th>หนังจริง</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="cap">คะแนนเป็นความเห็นของเรา สามจุดคือเด่นที่สุด ใช้เป็นจุดเริ่มคุย ไม่ใช่คำตอบ</p></section>
<section id="ask"><span class="eyebrow">ก่อนเลือก</span><h2>คำถามที่ควรคุยกันที่บ้าน</h2>
<div class="card"><ol>{"".join(f"<li>{E(q)}</li>" for q in ask)}</ol></div>
<p class="cap">อยากดูสีแบบไม่มีชื่อแบรนด์มาชวนเอนเอียง หรืออยากสุ่มชุดใหม่ ใช้ {link("palettes", "หน้าสุ่มสี")}</p>
<p class="cap">เลือกได้แล้ว บอกชื่อแบบมาได้เลย หรือผสมกันก็ได้ เช่น พื้นของแบบหนึ่งกับจุดของอีกแบบ แล้วจะสร้างโลโก้ โปสเตอร์ และทุกหน้าใหม่ด้วยสีนั้น กลับไปที่ {link("bible", "Brand Bible")}</p></section>
</div>"""

# ---------------------------------------------------------------- product lab
def productlab():
    sys.path.insert(0, os.path.join(ROOT, "research"))
    import research as R
    src = lambda k: f'<a href="{R.SOURCES[k][1]}" target="_blank" rel="noopener">{E(R.SOURCES[k][0])}</a>'
    finds = "".join(f'<div class="card" style="display:flex;flex-direction:column;gap:6px"><h3>{E(h)}</h3><p style="font-size:14.5px">{E(t)}</p><p class="cap">ที่มา: {src(k)}</p></div>'
                    for h, t, k in R.FINDINGS)
    prices = "".join(f'<tr><td><b>{E(w)}</b><br>{E(it)}<br><span class="cap">{E(n)} · {src(k)}</span></td><td class="n" style="white-space:normal;min-width:6.5em">{E(p)}</td></tr>'
                     for w, it, p, k, n in R.BAG_PRICES)
    bags = ""
    for b in R.bag_rows():
        c = b["cost"]
        parts = " · ".join(f"{E(n)} {cc}×{rr}" for n, cc, rr in b["parts"])
        bags += (f'<article class="card" style="display:flex;flex-direction:column;gap:10px">'
                 f'<img src="research/bag-{b["key"]}.svg" alt="ภาพด้านหน้ากระเป๋า {E(b["name"])}" style="border-radius:10px">'
                 f'<h3>{E(b["name"])}</h3><p>{E(b["idea"])}</p>'
                 f'<p class="cap" style="font-size:14px">แบบ {b["code"]} ระยะชิ้น {b["module"]} ซม. · {E(parts)} · รวม {b["pieces"]} ชิ้น รอยต่อ {b["joints"]} จุด · ประกอบประมาณ {c["minutes"]} นาที</p>'
                 f'<div class="tbl"><table><tbody>'
                 f'<tr><td>ชิ้นหนัง</td><td class="n">{c["leather"]:.0f}</td></tr><tr><td>ค่าประกอบ</td><td class="n">{c["joints"]:.0f}</td></tr>'
                 f'<tr><td>สายหัวใจ ตะขอ แม่เหล็ก ถุงผ้า</td><td class="n">{c["hw"]:.0f}</td></tr>'
                 f'<tr><td><b>ต้นทุนรวม</b></td><td class="n"><b>{c["total"]:.0f} บาท</b></td></tr>'
                 f'<tr><td>ถ้าซื้อสายสำเร็จแทน</td><td class="n">{c["with_bought"]:.0f} บาท</td></tr></tbody></table></div>'
                 f'<p><b style="font-family:var(--logo);font-size:24px;color:var(--brick)">{b["price"]:,} บาท</b> <span class="cap">สำเร็จ · กำไรขั้นต้น {b["margin"]:.0%}</span></p>'
                 f'<p class="cap">ชุดทำเอง {b["kit"]:,} บาท · เศษเล็กหนึ่งล็อตทำได้ {b["per_lot"]} ใบ</p></article>')
    story = "".join(f'<div class="card" style="display:flex;flex-direction:column;gap:6px"><span class="eyebrow">{E(stage)}</span><h3>{E(n)}</h3>'
                    f'<p class="cap" style="font-size:14px">เรื่องที่เล่า: {E(link_)}</p><p style="font-size:14.5px">{E(note)}</p><p class="cap">ใส่ชื่อได้: {E(pers)}</p></div>'
                    for n, link_, stage, pers, note in R.STORY_PRODUCTS)
    srcs = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{E(t)}</a></li>' for t, u in dict(R.SOURCES.values()).items())
    return f"""{head("OCT. 26 Product Lab")}
<div class="wrap">
<nav class="top" aria-label="หัวข้อ"><a href="#market">ตลาด</a><a href="#prices">ราคาเทียบ</a><a href="#bags">กระเป๋าสามแบบ</a><a href="#story">สินค้าที่เล่าเรื่อง</a><a href="#sources">ที่มา</a></nav>
<header style="padding-top:28px;display:flex;flex-direction:column;gap:12px"><span class="eyebrow">PRODUCT LAB · 15 ต.ค. 2569</span>
<h1>ขายอะไรดี และกระเป๋าสะพายข้างทำได้ไหม</h1>
<p class="lead">ทำได้ และมีช่องว่างในตลาด กระเป๋าหนังแท้ใบเล็กในไทยเริ่มราว 890 บาท ส่วนกระเป๋าที่ต่อจากชิ้นหนังแบบของเรายังไม่เจอแบรนด์ไหนทำจริงจัง กระเป๋าสามแบบด้านล่างใช้แพตเทิร์นที่มี ต้นทุน 140–180 บาท ขาย 890–1,290 บาท</p></header>
<section id="market"><span class="eyebrow">ตลาดบอกอะไร</span><h2>สินค้าหนังที่ขายดี</h2><div class="grid">{finds}</div><p class="cap">{E(R.CAVEAT)}</p></section>
<section id="prices"><span class="eyebrow">ราคาเทียบ</span><h2>กระเป๋าคล้ายกันขายเท่าไร</h2>
<div class="tbl"><table><thead><tr><th>ใคร · อะไร · ที่มา</th><th>ราคา</th></tr></thead><tbody>{prices}</tbody></table></div>
<p class="cap">ราคาดอลลาร์เป็นราคาขายต่างประเทศ ไม่ได้แปลงเป็นบาท เพราะค่าเงินเปลี่ยนทุกวัน ราคาที่ลดแล้วอาจกลับไปราคาปกติ</p></section>
<section id="bags"><span class="eyebrow">ออกแบบจากแพตเทิร์นที่มี</span><h2>กระเป๋าสะพายข้างสามแบบ</h2>
<div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr))">{bags}</div>
<div class="card"><h3>ต้องรู้ก่อนทำ</h3><ul style="margin-top:6px">{"".join(f"<li>{E(n)}</li>" for n in R.BAG_NOTES)}</ul></div>
<p class="cap">แนะนำให้เริ่มที่ซองมือถือวงกลม ใช้ 12 ชิ้น ทำต้นแบบได้ในวันเดียว ถ้าขายได้ค่อยทำกระเป๋าทรงกล่องกับกระเป๋าลูกบาศก์ห้าหมี</p></section>
<section id="story"><span class="eyebrow">ข้อ 16</span><h2>สินค้าที่เล่าเรื่องของแบรนด์</h2>
<p class="lead">เมื่อชื่อและเรื่องเล่าลงตัว สินค้าควรพาเรื่องไปด้วย แปดชิ้นนี้ผูกกับวันเกิด ซอยบ้าน รากของครอบครัว และห้าหมี และเรียงตามทางเติบโตใน {link("bible", "Brand Bible")}</p>
<div class="grid">{story}</div></section>
<section id="sources"><span class="eyebrow">ที่มา</span><h2>แหล่งข้อมูล</h2><div class="card"><ul>{srcs}</ul></div></section>
</div>"""

# ---------------------------------------------------------------- summary (CLAUDE.md)
AUDIT = [
    ("Soi 2 ดูบ้าน ๆ และหน้าตาไม่เข้ากับ OCT. 26 (ป้ายถนนสีน้ำตาลกับตัวไทย ๒)",
     "เปลี่ยนเป็น SOI. 02 เขียนด้วยไวยากรณ์เดียวกับ OCT. 26 ป้ายพื้นเข้ม ตัวอักษรเดียวกับโลโก้ ความหมายซอยบ้านยังอยู่ในเรื่องเล่า"),
    ("คำสัญญาว่า ไม่ต้องเย็บ ยังหลงอยู่ในเช็กลิสต์ก่อนโพสต์ ทั้งที่อนาคตจะมีชุดเย็บ",
     "เปลี่ยนเป็น บอกวิธีทำตรงกับชิ้นนั้น โปสเตอร์และโพสต์ของสินค้าชุดแรกยังบอกว่าไม่ต้องเย็บ เพราะชิ้นนั้นไม่ต้องเย็บจริง"),
    ("กติกาถ่ายรูปยังแนะนำกระดาษคราฟต์ ขัดกับเรื่องไม่เอาคราฟต์",
     "เปลี่ยนเป็นโต๊ะไม้เรียบ ผ้าลินิน หรือกระดาษสีพื้นของแบรนด์"),
    ("บรรจุภัณฑ์ใหม่ (ถุงกระดาษด้าน ถุงผ้า) แพงกว่างบ 5 บาทต่อชิ้นในชีตต้นทุน",
     "แยกเป็นต่อชิ้น (ป้ายห้อยและซอง 5 บาท) กับต่อออเดอร์ (ถุงและการ์ด) และเสนอยอดขั้นต่ำต่อออเดอร์"),
    ("Brand Bible บอกว่าทุกชิ้นมีป้ายห้อย แต่รายการของที่ต้องพิมพ์ไม่มีป้ายห้อย",
     "เพิ่มป้ายห้อย 350 ใบในรายการพิมพ์ และในแผนวันที่ 21 ต.ค."),
    ("Brand Book บอกว่าโลโก้หมีและโปสเตอร์ใช้ต่อได้ทั้งหมด แต่ Brand Bible บอกว่าแพตเทิร์นมาจากอินเทอร์เน็ต",
     "ทั้งสองที่บอกตรงกันแล้ว ใช้ช่วงเปิดตัวได้ วาดหมีใหม่จากแพตเทิร์นของเราก่อนจดเครื่องหมายการค้า"),
    ("Brand Book นำเสนอสีตุลาคมเหมือนสรุปแล้ว และกำหนดว่าจุดต้องเป็นส้มอิฐเสมอ",
     "ติดป้ายว่าเป็นชุดตั้งต้น และให้จุดใช้สีของแบรนด์ ซึ่งแบรนด์วันเกิดแต่ละแบรนด์เลือกเองได้ ต่อมา 15 ต.ค. เลือกชุดที่ 2 แล้ว"),
    ("ภาพในอีก 5 ปีบอกว่าทุกคนต้องมีแบรนด์วันเกิด แต่กติกาบอกว่าเปิดเมื่อเจ้าของพร้อม",
     "เขียนใหม่เป็น ใครพร้อมเมื่อไร ก็มีแบรนด์ของตัวเอง"),
    ("น้ำเสียงใน Brand Book บอกว่าห้าหมีพูดน่ารักได้มากกว่า แต่ Brand Bible บอกว่าห้าหมีช่างพูดและขี้เล่นสุด ๆ",
     "Brand Book ใช้คำเดียวกันแล้ว สองเสียงหนึ่งบ้าน"),
    ("หน้าที่ลูก ๆ ใน Brand Bible ต่างจากหน้าที่ที่บูธใน Launch Kit",
     "ระบุชัดว่าอันหนึ่งคืองานประจำนอกบูธ อีกอันคือหน้าที่ที่บูธ ทั้งสองอย่างใช้คู่กันได้"),
    ("Launch Kit เขียนว่าแผน 9 วัน แต่แผนยาวถึงวันที่ 26",
     "เปลี่ยนเป็น แผนถึงวันงาน · 9 วันถึงบูธ"),
    ("ชื่อกระเป๋า กล่องซอย ขัดกับกติกาตั้งชื่อสินค้าที่ให้บอกว่าใช้ทำอะไรก่อน",
     "เปลี่ยนเป็น กระเป๋าทรงกล่อง และ กระเป๋าลูกบาศก์ห้าหมี"),
]

def summary():
    tot = B.event_totals()
    rows = [("Logo Lab", "logolab", "สรุปแล้ว เหลือสี่โลโก้ ใช้ทีละตัว: OCT. 26 ป้ายห้อย 26 ห้าหมี และหมีหัวใจ"),
            ("Color Lab", "colorlab", "เลือกแล้ว ชุดที่ 2 Soi Candy ทางเลือกอื่นเก็บไว้เทียบ"),
            ("สุ่มสีแบบไม่มีชื่อแบรนด์", "palettes", "สุ่มสีสามแนวบนตัวอย่างที่ไม่มีโลโก้ ล็อกสี เก็บชุดที่ชอบ คัดลอกรหัสสี"),
            ("Product Lab", "productlab", "สินค้าหนังที่ขายดี ราคากระเป๋าเทียบตลาด กระเป๋าสะพายข้างสามแบบจากแพตเทิร์น และสินค้าที่เล่าเรื่อง"),
            ("Brand Bible", "bible", "14 บท ตั้งแต่เหตุผลที่มีแบรนด์ ครอบครัวแบรนด์วันเกิด สี บุคลิก สาร ระบบชื่อ บรรจุภัณฑ์ บูธ คอนเทนต์ จนถึงปีแรก"),
            ("Brand Book", "brandbook", "ชื่อ เรื่องเล่า โลโก้ชุดใหม่ ระบบสัดส่วนทองคำ สีชุดที่ 2 ฟอนต์ น้ำเสียง"),
            ("Launch Kit", "launch", "แผนถึงวันงาน โซเชียล Shopee สินค้า 30 ตัวแบ่งตามคอลเลกชัน พร้อมโพสต์ 5 ช่องทาง คู่มือลูก ๆ ขายของ"),
            ("สไลด์ของขวัญวันเกิด", "deck", "พรีเซนต์ OCT. 26 ให้เธอในวันเกิด 26.10"),
            ("Google Sheet ต้นทุน", "sheet", "ต้นทุน ราคาขาย กำไร 3 แท็บ"),
            ("ทางเลือกแบรนด์ทั้งหมด", "alternatives", "55 ชื่อที่คิดมา OCT. 26 ติดป้าย เลือกแล้ว")]
    links = "".join(f'<div class="card"><h3>{link(k, E(t))}</h3><p class="cap" style="font-size:14px;margin-top:4px">{E(d)}</p></div>' for t, k, d in rows)
    files = [("brand-20261014/brand.py", "ข้อมูลทั้งหมดของแบรนด์ แก้ที่นี่ที่เดียว"),
             ("brand-20261014/logo/svg, logo/png", "โลโก้ 22 ไฟล์ OCT. 26 ป้าย SOI. 02 ป้าย Love และห้าหมี แปลงตัวอักษรเป็นเส้นแล้ว"),
             ("brand-20261014/posters/png", "โปสเตอร์ How-to 30 ตัว × 2 ขนาด (60 ไฟล์)"),
             ("brand-20261014/bible.py, bible/svg", "เนื้อหา Brand Bible และภาพประกอบ 8 ไฟล์ (ป้ายห้อย การ์ด ถุง ลาย ผังบูธ)"),
             ("brand-20261014/colorlab", "แผงสีเจ็ดแบบ แก้สีแต่ละแบบได้ใน colorlab/build.py"),
             ("brand-20261014/research", "ข้อมูลวิจัยสินค้า ต้นทุนกระเป๋า และภาพกระเป๋าสามแบบ"),
             ("brand-20261014/site", "ต้นฉบับหน้าเว็บทั้งหก"),
             ("brand-20261014/deck", "ต้นฉบับสไลด์"),
             ("brand-20261014/alternatives", "ทางเลือกแบรนด์ 55 แบบ โลโก้และป้ายห้อย")]
    ftable = "".join(f'<tr><td class="mono" style="white-space:nowrap">{E(f)}</td><td>{E(d)}</td></tr>' for f, d in files)
    return f"""{head("OCT. 26 สรุปโปรเจกต์")}
<div class="wrap"><header style="padding-top:28px;display:flex;flex-direction:column;gap:14px">
<span class="eyebrow">สรุปโปรเจกต์ · อัปเดต 15 ต.ค. 2569</span><h1>OCT. 26 ก่อนออกบูธ 23–25 ต.ค.</h1>
<div class="paper" style="aspect-ratio:16/7"><img src="logo/oct-wordmark.svg" alt="โลโก้ OCT. 26" style="max-height:100%"></div>
<p class="lead">ชื่อแบรนด์ เรื่องเล่า โลโก้และ brand book ช่องทางโซเชียลกับ Shopee สินค้า 30 ตัวพร้อมโปสเตอร์และโพสต์ทุกช่องทาง คู่มือให้ลูก ๆ ขายเอง และสไลด์สำหรับวันเกิดเธอ</p></header>
<section><span class="eyebrow">คำตอบ</span><h2>หมี 5 ตัวเป็นซับแบรนด์ได้</h2>
<p class="lead">OCT. 26 เป็นแบรนด์หลัก SOI. 02 เป็นคอลเลกชันแรก และห้าหมี FIVE BEARS by OCT. 26 เป็นซับแบรนด์ที่มีคอลเลกชันแรกชื่อ Love</p>
<div class="grid">
<div class="card" style="display:flex;flex-direction:column;gap:10px"><div class="paper" style="aspect-ratio:5/3"><img src="logo/soi2-sign.svg" alt="ป้าย SOI. 02"></div><h3>OCT. 26 · SOI. 02</h3><p class="cap">ตั้งชื่อตามซอยบ้านเรา ของใช้ทุกวัน {sum(p["coll"] == "soi2" for p in B.PRODUCTS)} แบบ จากแพตเทิร์น 02–06</p></div>
<div class="card" style="display:flex;flex-direction:column;gap:10px"><div class="paper" style="aspect-ratio:5/3"><img src="logo/love-badge.svg" alt="ป้าย Love ห้าหมี"></div><h3>ห้าหมี by OCT. 26 · Love</h3><p class="cap">หัวหมีและสายหัวใจ {sum(p["coll"] == "love" for p in B.PRODUCTS)} แบบ จากแพตเทิร์น 01</p></div></div>
<div class="grid">{"".join(f'<div class="card"><h3>{E(h)}</h3><p class="cap" style="font-size:14px;margin-top:4px">{E(t)}</p></div>' for h, t in B.SUB_ANSWER)}</div></section>
<section><span class="eyebrow">ตรวจทั้งชุด · 15 ต.ค. 2569</span><h2>สิ่งที่ขัดกันเอง และแก้แล้ว</h2>
<div class="tbl"><table><thead><tr><th>เจออะไร</th><th>แก้อย่างไร</th></tr></thead><tbody>{"".join(f"<tr><td>{E(a)}</td><td>{E(b_)}</td></tr>" for a, b_ in AUDIT)}</tbody></table></div></section>
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
<li>ชื่อ @{B.BRAND['handle']} ยังว่างทุกช่องทาง ถ้าไม่ว่าง เลือกชื่อใหม่แล้วแก้ใน brand.py ที่เดียว</li>
<li>ค้นชื่อ OCT. 26 และห้าหมีในฐานข้อมูลเครื่องหมายการค้า ก่อนพิมพ์ของจำนวนมาก</li>
<li>มีบล็อกแบบไหนแล้วบ้าง แบบที่ยังไม่มีต้องสั่งวันนี้</li>
<li>สินค้าที่ติดป้าย “ลองต้นแบบก่อน” ต่อตัวอย่างหนึ่งชิ้นทุกตัว ก่อนลงขายใน Shopee</li>
<li>ใส่ชื่องานและเลขบูธแทน [ชื่องาน] ในข้อความโพสต์</li>
<li>สายหัวใจ 250 มม. ต้องใช้เศษยาว 25.5 ซม. ขึ้นไป ถ้าเศษสั้นกว่า ป้ายชื่อกระเป๋าใช้สาย 200 แทน</li>
<li>ราคาขายเป็นราคาแนะนำ แก้ได้ในคอลัมน์ราคาขายของ Google Sheet</li>
<li>พิมพ์ป้ายห้อยตัวอย่าง 55 × 89 มม. หนึ่งแผ่น ดูสีโคบอลต์และมะเขือเทศบนกระดาษจริงก่อนสั่งพิมพ์จำนวนมาก</li>
<li>เช็กว่าแพตเทิร์น 01–06 ที่หามา เจ้าของอนุญาตให้ขายได้ และเริ่มออกแบบแพตเทิร์นของเราเอง</li>
<li>ขอใบเสนอราคาป้ายห้อย ถุงกระดาษด้าน และถุงผ้า แล้วตั้งยอดขั้นต่ำต่อออเดอร์ใน Shopee</li></ol></div></section>
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
    for name, fn in (("brandbook.html", brandbook), ("launch.html", launch), ("bible.html", bible), ("colorlab.html", colorlab), ("productlab.html", productlab), ("index.html", summary)):
        open(os.path.join(HERE, name), "w").write(fn())
    print("built", URLS)
