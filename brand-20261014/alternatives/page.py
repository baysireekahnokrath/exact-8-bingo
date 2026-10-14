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
.chipx{font-size:13px;background:var(--chip);border-radius:99px;padding:3px 11px}
.ini{display:flex;gap:10px;flex-wrap:wrap}.ini label{display:flex;flex-direction:column;gap:4px;font-size:13px;color:var(--muted)}
.ini input{width:56px;height:56px;font-size:26px;text-align:center;text-transform:uppercase;border:1px solid var(--line);border-radius:12px;background:var(--bg);color:var(--ink);font-family:var(--body)}
.ini input:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.word{font-size:20px;font-weight:500;letter-spacing:.12em;background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:6px 12px;font-variant-numeric:tabular-nums}
.taken{font-size:13px;letter-spacing:.04em;background:#8E2B23;color:#FBF6EE;border-radius:99px;padding:2px 10px}
.risk{font-size:14px;color:var(--muted);border-left:3px solid var(--accent);padding-left:12px}
.pick{background:var(--paper);border:1px solid var(--line);border-radius:6px;padding:20px;display:flex;flex-direction:column;gap:10px}
ul,ol{margin:0;padding-left:1.3em}
@media (max-width:640px){.boards,.spec{grid-template-columns:minmax(0,1fr)}.boards img:last-child{max-width:260px}}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anuphan:wght@400;500&family=Noto+Serif+Thai:wght@400;500&display=swap">')

def concept_card(o):
    if not o.get("concept"):
        return ""
    chips = "".join(f'<span class="chipx">{E(m)}</span>' for m in o["more"])
    return (f'<div class="pick" style="gap:8px"><span class="k">แนวคิด · {E(o["concept"])}</span><p>{E(o["approach"])}</p>'
            f'<p class="k" style="text-transform:none;letter-spacing:.02em">{E(o.get("more_label", "ชื่ออื่นในแนวเดียวกัน"))}</p><div class="sw">{chips}</div></div>')

INITIALS_TOOL = """<div class="pick" id="tool" style="gap:12px"><span class="k">ลองตั้งชื่อจากอักษรแรกของห้าคน</span>
<p>พิมพ์อักษรตัวแรกของชื่อแต่ละคน (อังกฤษหรือไทยก็ได้) หน้านี้จะเรียงให้ครบทุกแบบ แบบที่สลับสระกับพยัญชนะ อ่านออกเสียงง่าย จะขึ้นก่อน ตัวอักษรที่ใส่ไว้ตอนนี้เป็นตัวอย่าง</p>
<div class="ini">
<label>พ่อ<input id="ini1" maxlength="1" value="P"></label><label>แม่<input id="ini2" maxlength="1" value="A"></label>
<label>คนโต<input id="ini3" maxlength="1" value="N"></label><label>คนกลาง<input id="ini4" maxlength="1" value="I"></label>
<label>คนเล็ก<input id="ini5" maxlength="1" value="K"></label></div>
<p class="k" id="ini-count" style="text-transform:none;letter-spacing:0"></p>
<div class="sw" id="ini-out"></div>
<details><summary class="k" style="cursor:pointer;text-transform:none;letter-spacing:0">ดูทุกแบบ</summary><p id="ini-all" style="font-size:14px;line-height:2;word-spacing:.6em"></p></details>
</div>
<script>
(function(){
const V=new Set("AEIOUY".split(""));
const isV=c=>V.has(c)||/[\u0E30-\u0E45\u0E47-\u0E4E]/.test(c);
function perms(a){if(a.length<2)return[a];const out=[];a.forEach((x,i)=>perms(a.slice(0,i).concat(a.slice(i+1))).forEach(p=>out.push([x].concat(p))));return out}
function score(w){let s=0,run=1;for(let i=1;i<w.length;i++){const a=isV(w[i-1]),b=isV(w[i]);if(a!==b){s+=2;run=1}else{run++;s-=run>2?3:1}}return s+(isV(w[0])?0:1)}
function draw(){
 const L=[1,2,3,4,5].map(n=>(document.getElementById("ini"+n).value||"").trim().toUpperCase()).filter(Boolean);
 const out=document.getElementById("ini-out"),all=document.getElementById("ini-all"),cnt=document.getElementById("ini-count");
 if(L.length<2){out.textContent="ใส่อักษรอย่างน้อยสองตัว";all.textContent="";cnt.textContent="";return}
 const words=[...new Set(perms(L).map(p=>p.join("")))].sort((a,b)=>score(b)-score(a)||a.localeCompare(b));
 cnt.textContent="ทั้งหมด "+words.length+" แบบ · 12 แบบที่อ่านง่ายที่สุด";
 out.innerHTML="";words.slice(0,12).forEach(w=>{const s=document.createElement("span");s.className="word";s.textContent=w;out.appendChild(s)});
 all.textContent=words.join(" ");
}
document.querySelectorAll(".ini input").forEach(i=>i.addEventListener("input",draw));draw();
})();
</script>"""

def option(i, o):
    rows = "".join(
        f'<tr><td>{E(h["name"])}</td><td class="n">{h["base"]}</td><td class="n"><b>{h["price"]:,}</b></td>'
        f'<td class="n">{h["cost"]:.0f}</td><td class="n">{h["margin"]:.0%}</td></tr>' for h in o["heroes"])
    sw = "".join(f'<span><i style="background:{hx}"></i>{E(n)} <span class="k" style="letter-spacing:0">{hx}</span></span>' for n, hx in o["pal"])
    return f"""<section class="opt" id="{o['key']}">
<div class="head"><span class="num">{i:02d}</span><h2>{E(o['name'])}</h2><span style="color:var(--muted)">{E(o['th'])}</span>{'<span class="taken">มีคนใช้แล้ว</span>' if o.get('taken') else ''}</div>
<div class="boards"><img src="img/{o['key']}-board.png" alt="โลโก้ {E(o['name'])} บนสีหลักของแบรนด์" width="1200" height="720">
<img src="img/{o['key']}-tag.png" alt="ป้ายห้อยสินค้า {E(o['name'])} ตัวอย่างกับ{E(o['heroes'][0]['name'])}" width="560" height="860"></div>
{concept_card(o)}<div class="spec">
<div><span class="k">ความหมาย</span><p>{E(o['mean'])}</p><p><b>{E(o['tag_en'])}</b><br>{E(o['tag_th'])}</p></div>
<div><span class="k">ลุค</span><p>{E(o['vibe'])}</p><div class="sw">{sw}</div>
<p class="k" style="letter-spacing:.04em;text-transform:none">ฟอนต์ {E(o['font'][1])} · ภาษาไทย {E(o['thfont'][1])} · @{E(o['handle'])}</p></div>
<div><span class="k">เรื่องครอบครัวอยู่ตรงไหน</span><p>{E(o['story'])}</p></div>
<div><span class="k">ขายใคร</span><p>{E(o['who'])}</p></div>
</div>
<div class="tbl"><table><thead><tr><th>สินค้าหลัก</th><th>ราคาห้าหมี</th><th>ราคาแบรนด์นี้</th><th>ต้นทุน</th><th>กำไร</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="risk">{E(o['risk'])}</p>
{INITIALS_TOOL if o['key'] == 'initials' else ''}
</section>"""

def page():
    nav = "".join(f'<a href="#{o["key"]}">{E(o["name"])}</a>' for o in OPTIONS[50:55] + OPTIONS[45:50] + OPTIONS[35:40] + OPTIONS[40:45] + OPTIONS[25:30] + OPTIONS[30:35] + OPTIONS[20:25] + OPTIONS[15:20] + OPTIONS[10:15] + OPTIONS[:10])
    comp = [("REMNANT", "มินิมอล หรูเงียบ", "เล่าในโพสต์เบื้องหลัง", "กลาง", "300–700"),
            ("UNSEWN", "งานฝีมือ ดีไซน์", "ลูก ๆ เป็นทีมประกอบ", "กลาง", "350–600"),
            ("INTERLOCK", "เท่ สตรีท DIY", "คลิปลูกต่อแข่งเวลา", "ยาก ต้องใช้คู่โลโก้", "290–890"),
            ("AFTERCUT", "รักษ์โลกชัดที่สุด", "ครอบครัวเก็บและคัดเศษ", "กลาง", "220–290"),
            ("QUINT", "หรูคลาสสิก", "ห้าร่อง = ห้าคนในบ้าน", "น่าจะง่ายกว่า ไม่ใช่คำทั่วไป", "290–990"),
            ("KHAD", "เท่แบบไทยร่วมสมัย", "คำที่พูดกันในบ้าน", "กลาง ต้องจดคู่โลโก้", "259–290"),
            ("SANSFIL", "หรูแบบผู้หญิง", "แบรนด์ที่ตั้งให้แม่หมี", "กลาง", "290–790"),
            ("POINT FIVE", "เท่แบบวิศวกร", "ห้า = ห้าคน, 0.5 = งานของพ่อ", "กลาง ต้องค้นหมวดเครื่องหนัง", "390–790"),
            ("PRANEET", "หรูแบบไทย", "ดอกห้ากลีบ = ห้าคน", "มีคนใช้แล้ว", "190–890"),
            ("MONO/HIDE", "ยั่งยืนแบบดิบ", "ลูก ๆ แกะชิ้นให้ดูว่ามีแต่หนัง", "กลาง ต้องจดคู่ HIDE", "250–450"),
            ("ละเมียด LAMIAD", "หรูแบบไทย ต่อจาก PRANEET", "ดอกห้ากลีบ = ห้าคน", "ค้นเว็บไม่เจอแบรนด์ชื่อนี้", "190–890"),
            ("เบญจ BENJA", "เบญจรงค์ร่วมสมัย", "เบญจ = ห้า ห้าสีห้าคน", "คำทั่วไป เจอชื่อซ้ำในกระเป๋าและเฟอร์นิเจอร์", "490–590"),
            ("บรรจง BANJONG", "ลายรดน้ำ ดำทอง", "พ่อออกแบบ ลูกประกอบ", "ชื่อคนทั่วไป ต้องจดคู่โลโก้", "290–790"),
            ("กนก KANOK", "ลายไทย แดงทอง", "ช่างไทยรุ่นใหม่ในบ้าน", "ชื่อคนทั่วไป ใกล้ Kanita", "150–590"),
            ("หัตถ์ HATTHA", "ศิลาดล", "ห้าคู่มือ", "ค้นเว็บไม่เจอแบรนด์ชื่อนี้", "290–790"),
            ("ประจำ PRAJAM", "หม้อห้อมร่วมสมัย", "ของประจำตัวของทุกคนในบ้าน", "ค้นเว็บไม่เจอ คำทั่วไป จดคู่โลโก้", "129–219"),
            ("คู่ใจ KOOJAI", "อบอุ่นแบบบ้าน", "หัวใจสองดวง = พ่อกับแม่", "ค้นเว็บไม่เจอแบรนด์ชื่อนี้", "169–229"),
            ("ใช้ดี CHAIDEE", "สดใส เป็นมิตร", "ลูก ๆ ทดลองใช้ทุกชิ้น", "เจอ Chaidee Mansion คนละหมวด", "99–299"),
            ("วันวัน WANWAN", "สดชื่นยามเช้า", "กิจวัตรของลูก ๆ", "ใกล้ Wanpi แบรนด์หนังมาเลเซีย", "99–259"),
            ("คุ้นมือ KHUNMUE", "หนังที่ผ่านการใช้", "ลูก ๆ ถือในรูปก่อนหลัง", "ค้นเว็บไม่เจอ ใกล้ FEEMUE", "159–229"),
            ("bit.", "มินิมอลเครื่องเขียน", "จุดแดง = แม่หมี", "คำทั่วไป จดทั้งชุด", "79–249"),
            ("kit.", "เท่แบบเครื่องมือ", "keep it together", "คำทั่วไป จดทั้งชุด", "199–590"),
            ("hold.", "บ้านแบบญี่ปุ่น", "ถ่ายของในบ้านเราเอง", "คำทั่วไป จดทั้งชุด", "199–290"),
            ("left.", "สีหนังเต็มพื้น", "f = five ห้าคน", "คำทั่วไป แปลว่าซ้ายได้", "99–390"),
            ("pal.", "น่ารักแบบเพื่อน", "ลูก ๆ ตั้งชื่อให้ของ", "มีกระเป๋ารุ่น Pal ของ Fill in the Bag", "129–189"),
            ("tab.", "สะอาดแบบเครื่องมือ", "ลูก ๆ สาธิต tab เข้า slot", "ค้นเว็บไม่เจอ คำทั่วไป จดทั้งชุด", "199–290"),
            ("fit.", "สดใส ซองพับ", "พับแข่งเวลา", "คำทั่วไป คนนึกถึงฟิตเนส", "89–159"),
            ("kin.", "อบอุ่นกลางคืน", "kin = ครอบครัว", "ใกล้ &Kin แบรนด์เสื้อผ้า", "189–390"),
            ("one.", "ดิบและเรียบ", "อ่านว่า วัน", "คำทั่วไปมาก จดทั้งชุด", "89–299"),
            ("mom.", "อ่อนโยน", "แบรนด์ของแม่หมี", "คำทั่วไป ขายผู้ชายยาก", "159–390"),
            ("MAISON OURS", "ปารีส หมีเดิม", "ours = หมี และ ของเรา", "ใกล้ Les Ours และ Maison des Ours", "190–590"),
            ("MAISON CINQ", "ปารีสคลาสสิก", "cinq = ห้า", "คนไทยอ่านยาก ใกล้ Sept Cinq", "250–590"),
            ("MAISON TUCK", "สตูดิโอมินิมอล", "เทคนิคของพ่อ", "ค้นเว็บไม่เจอแบรนด์ชื่อนี้", "350–790"),
            ("MAISON FOLD", "กระดาษพับ", "ซองพับทั้งตระกูล", "ใกล้ The Fold (อังกฤษ)", "150–290"),
            ("MAISON MEND", "ยั่งยืนแบบหรู", "ลูก ๆ เปลี่ยนชิ้นให้ลูกค้า", "ค้นเว็บไม่เจอ (มีเครื่องหมายเก่า Mendessolle)", "290–490"),
            ("mai. ใหม่", "ใบไม้ใหม่", "เศษเก่า กลายเป็นของใหม่", "ค้นเว็บไม่เจอแบรนด์เครื่องหนัง", "159–219"),
            ("dee. ดี", "เช้าวันจันทร์", "ลูก ๆ ให้คะแนน ดี", "ใกล้ร้านหนัง หนังสวยดี", "129–229"),
            ("lek. เล็ก", "เครื่องเขียน", "ของชิ้นเล็กให้ลูก ๆ ขาย", "Lek Gallery, Lek Massage คนละหมวด", "59–99"),
            ("fun. ฝัน", "ฝันกลางคืน", "ไลน์ของเด็ก", "คำทั่วไปมาก", "129–590"),
            ("jai. ใจ", "แดงเต็มพื้น", "ใจ = แม่หมี", "เคยมีข่าวแบรนด์ชื่อ Jai ต้องค้นละเอียด", "129–299"),
            ("dad. แดด", "ตระกูล mom.", "drawing ของพ่อ", "คำทั่วไป จดทั้งชุด", "129–290"),
            ("kid. คิด", "ตระกูล mom.", "ลูก ๆ เป็นนักออกแบบ", "คำทั่วไป แบรนด์เด็กใช้เยอะ", "189–590"),
            ("sis.", "ตระกูล mom.", "ลูกสาวสองคน", "คำแสลงทั่วไป", "159–189"),
            ("fam.", "ตระกูล mom.", "ห้าคนรอบตัวฉัน", "คำแสลงทั่วไป", "299–390"),
            ("us.", "ตระกูล mom.", "พ่อกับแม่เป็นคู่แรก", "คำทั่วไปมาก ชื่อบัญชีหายาก", "159–390"),
            ("CLICKER", "ศัพท์ช่างหนัง", "พ่อกดบล็อกตัดเอง", "ค้นเว็บไม่เจอแบรนด์ชื่อนี้", "250–390"),
            ("MAKE DO", "สำนวนอังกฤษ", "สอนลูกให้ใช้สิ่งที่มี", "ใกล้ Make Smith, MW Makes", "390–490"),
            ("23·10", "วันสำคัญ", "วันแรกที่ลูกขายเอง", "ตัวเลขจดยาก ต้องจดเป็นโลโก้", "199–490"),
            ("อักษรแรกห้าคน", "ชื่อทุกคนในบ้าน", "มีตัวอักษรของทุกคน", "น่าจะจดง่ายที่สุด เพราะเป็นคำที่ตั้งขึ้นใหม่", "189–390"),
            ("SOI 5", "สถานที่", "ซอยบ้านเรา", "คำทั่วไป ต้องจดเป็นโลโก้ป้ายซอย", "59–189"),
            ("ทน", "ไม้เข้มกับหนัง · กลับหัว = ทน", "คอลเลกชันไม้เนื้อแข็ง ต่อกับ ฌ เฌอ", "คำทั่วไป จดเป็นโลโก้", "199–290"),
            ("ร เรือ", "แม่น้ำ · กลับหัว = ร", "ห้าคนอยู่ลำเดียวกัน", "ตัวอักษรเดียว จดเป็นโลโก้", "89–159"),
            ("บท", "หน้ากระดาษ · กลับหัว = นก", "แบรนด์พี่น้องของ ฌ เฌอ", "คำทั่วไป จดเป็นโลโก้", "59–390"),
            ("ด เด็ก", "สวน · กลับหัว = บ ใบไม้", "ลูกหมีสามตัวคือเด็ก", "ตัวอักษรเดียว ต้องวาดหัวให้ชัด", "189–590"),
            ("มด", "ดินทราย · กลับหัว = บก", "ครอบครัวมดงาน", "ต้องวาด ม ใหม่ให้อ่านกลับหัวได้", "199–590")]
    crow = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td><td class='n'>{e}</td></tr>" for a, b, c, d, e in comp)
    set11 = ('<p class="eyebrow">ชุดที่ 11 · ใหม่ · วิธีคิดแบบ ฌ เฌอ</p>'
            '<div class="pick" style="gap:10px"><h2>สามชั้นของวิธีคิด ฌ เฌอ</h2>'
            '<ol><li><b>ชื่อ</b> ตัวอักษรไทยหรือคำสั้นที่ความหมายตรงกับแบรนด์ แบบ ฌ เฌอ แปลว่าต้นไม้</li>'
            '<li><b>โลโก้</b> วาดตัวอักษรให้เส้นซ่อนรูปสินค้า แบบโต๊ะที่มีเก้าอี้สอดอยู่ข้างใต้ ของเราซ่อนปีกหนังที่สอดเข้าร่อง</li>'
            '<li><b>คอลเลกชัน</b> กลับหัวแล้วอ่านเป็นอีกคำ คำนั้นเป็นธีมชื่อคอลเลกชัน แบบ ฌ เฌอ กลับหัวเป็น นก</li></ol>'
            '<p>ผมลองหมุนตัวอักษรไทยทุกตัวในฟอนต์ไม่มีหัวจริง ๆ คู่ที่อ่านได้ชัดคือ ท กับ น, บ กับ ก, ด กลายเป็น บ, ม กลายเป็น ก และ ร ยังเป็น ร คำที่หมุนแล้วอ่านได้จริงคือ ทน (ยังเป็น ทน) และ บท (กลายเป็น นก) ตารางด้านล่างใช้ตอนวาดต่อได้</p>'
            '<div class="boards" style="grid-template-columns:minmax(0,1fr) minmax(0,1fr)"><img src="img/thai-rotation.png" alt="ตัวอักษรไทย 44 ตัว แถวบนตั้งตรง แถวล่างหมุน 180 องศา" width="1650" height="1200">'
            '<img src="img/thai-ambigram-test.png" alt="ทดสอบคำ ด ร ทน มด บท กบ บก ทบ นก หมุน 180 องศาในสามฟอนต์" width="2070" height="900"></div>'
            '<p class="k" style="text-transform:none;letter-spacing:0">ซ้าย ตัวอักษรทุกตัวตั้งตรงและกลับหัว (Kanit) · ขวา ทดสอบคำในฟอนต์ Kanit, Mitr และ Anuphan กรอบแดงคือกลับหัว</p></div>'
            + "".join(option(i, o) for i, o in enumerate(OPTIONS[50:55], 51)))
    set10 = ('<p class="eyebrow">ชุดที่ 10 · ห้าแนวคิดใหม่</p>'
            '<p style="font-size:14px;color:var(--muted)">แต่ละแนวคิดเป็นวิธีตั้งชื่อแบบใหม่ ไม่ใช่แค่ชื่อเดียว มีชื่อตัวอย่างที่ทำโลโก้ให้แล้ว และชื่ออื่นในแนวเดียวกันให้เลือกต่อ</p>'
            + "".join(option(i, o) for i, o in enumerate(OPTIONS[45:50], 46)))
    set8 = ('<p class="eyebrow">ชุดที่ 8 · แบบ one. อ่านเป็นคำไทยได้</p>'
            '<p style="font-size:14px;color:var(--muted)">คำอังกฤษสั้น ๆ ที่อ่านออกเสียงแล้วเป็นคำไทยที่มีความหมาย เหมือน one. ที่อ่านว่า วัน</p>'
            + "".join(option(i, o) for i, o in enumerate(OPTIONS[35:40], 36)))
    set9 = ('<p class="eyebrow">ชุดที่ 9 · แบบ mom. ครบทั้งครอบครัว</p>'
            '<p style="font-size:14px;color:var(--muted)">ใช้ฟอนต์เดียวกับ mom. ทุกตัว จึงใช้เป็นไลน์สินค้าย่อยของแบรนด์เดียวกันได้ ทั้ง dad. kid. sis. fam. us.</p>'
            + "".join(option(i, o) for i, o in enumerate(OPTIONS[40:45], 41)))
    set6 = ('<p class="eyebrow">ชุดที่ 6 · แบบ dot เพิ่มอีก 5</p>'
            + "".join(option(i, o) for i, o in enumerate(OPTIONS[25:30], 26)))
    set7 = ('<p class="eyebrow">ชุดที่ 7 · แบบ Maison Keep</p>'
            '<p style="font-size:14px;color:var(--muted)">Maison ตามด้วยคำเดียวที่เป็นหัวใจของแบรนด์ ราคาและต้นทุนคิดแบบไลน์พรีเมียม กล่อง 40 บาท</p>'
            + "".join(option(i, o) for i, o in enumerate(OPTIONS[30:35], 31)))
    set5 = ('<p class="eyebrow">ชุดที่ 5 · แบบ dot: diary object thing</p>'
            '<p style="font-size:14px;color:var(--muted)">ชื่อตัวพิมพ์เล็กสั้น ๆ ที่ทุกตัวอักษรย่อมาจากคำหนึ่งคำ และใช้จุดเป็นโลโก้ ทำตามรูปแบบการตั้งชื่อ ไม่ได้ใช้ชื่อเดิม ราคาและต้นทุนคิดแบบชุดของใช้ทุกวัน กล่องคราฟต์ 15 บาท</p>'
            + "".join(option(i, o) for i, o in enumerate(OPTIONS[20:25], 21)))
    set4 = ('<p class="eyebrow">ชุดที่ 4 · ของใช้ในชีวิตประจำวัน</p>'
            '<p style="font-size:14px;color:var(--muted)">ชุดนี้ราคาอยู่ระหว่างห้าหมีกับแบรนด์หรู ต้นทุนใช้กล่องคราฟต์และสติกเกอร์ประมาณ 15 บาท แทนกล่องพรีเมียม 40 บาท</p>'
            + "".join(option(i, o) for i, o in enumerate(OPTIONS[15:20], 16)))
    set3 = ('<p class="eyebrow">ชุดที่ 3 · แนวเดียวกับ PRANEET</p>'
            + "".join(option(i, o) for i, o in enumerate(OPTIONS[10:15], 11)))
    opts = ('<p class="eyebrow">ชุดที่ 1</p>' + "".join(option(i, o) for i, o in enumerate(OPTIONS[:5], 1))
            + '<p class="eyebrow">ชุดที่ 2</p>' + "".join(option(i, o) for i, o in enumerate(OPTIONS[5:10], 6)))
    return f"""<title>ทางเลือกแบรนด์ Luxury</title><meta name="claude:viewport-fit-sides" content="cover">{FONTS}<style>{CSS}</style>
<nav class="top" aria-label="ทางเลือก">{nav}<a href="#pick">คำแนะนำ</a></nav>
<div class="wrap">
<header style="padding-top:28px;display:flex;flex-direction:column;gap:14px">
<span class="eyebrow">Brand directions · 14 ต.ค. 2569</span>
<h1>ห้าสิบห้าทางเลือก กับสิบเอ็ดวิธีตั้งชื่อแบรนด์</h1>
<p class="lead">สินค้า บล็อกตัด และครอบครัวเดิมทั้งหมด สิ่งที่เปลี่ยนคือชื่อ ลุค และระดับราคา ทุกโลโก้ในหน้านี้เป็นไฟล์จริงที่แปลงตัวอักษรเป็นเส้นแล้ว ส่วนป้ายห้อยเป็นตัวอย่างการใช้งานบนสินค้า</p>
<p style="font-size:14px;color:var(--muted)">ต้นทุนในตารางใช้สูตรเดียวกับ Google Sheet แต่เปลี่ยนถุง 5 บาทเป็นกล่องพรีเมียมประมาณ {PREMIUM_PACK:.0f} บาท ราคาแบรนด์หรูต้องมาพร้อมงานเก็บขอบหนัง การคัดหนังเกรดดี และบรรจุภัณฑ์ที่ดีขึ้น</p>
</header>
{set11}
<section class="opt pick" id="pick"><span class="eyebrow">คำแนะนำรอบนี้</span><h2>ทน ถ้าใช้วิธีคิดแบบ ฌ เฌอ</h2>
<p>ทน กลับหัวแล้วยังอ่านว่า ทน ตรงทุกฟอนต์ที่ลอง ไม่ต้องดัดตัวอักษรก็อ่านได้ ความหมายตรงกับความจริงของสินค้า ไม่มีด้ายให้ขาด ไม่มีกาวให้ลอก และคอลเลกชันชื่อไม้เนื้อแข็งต่อกับ ฌ เฌอ ที่แปลว่าต้นไม้ได้ เป็นแบรนด์พี่น้องที่มีเหตุผลรองรับ</p>
<p>ถ้าอยากให้สองแบรนด์เชื่อมกันชัดที่สุด เลือก บท เพราะกลับหัวแล้วเป็น นก คำเดียวกับที่ ฌ เฌอ กลับหัวแล้วได้ และสินค้าตัวแรกคือที่คั่นหนังสือ ซึ่งคั่นบทพอดี ส่วน มด ต้องวาดหัว ม ใหม่ก่อนถึงจะอ่านกลับหัวเป็น บก ได้</p>
<p>ผมพิสูจน์การอ่านกลับหัวด้วยฟอนต์จริงให้แล้ว ส่วนการซ่อนรูปสินค้าในเส้นตัวอักษรเขียนเป็นแนวทางไว้ในแต่ละแบรนด์ ต้องวาดด้วยมือแบบที่ทำกับ ฌ เฌอ</p>
<ol><li>เลือก 1–2 คำ แล้วสเก็ตช์ตัวอักษรที่ซ่อนปีกหนังกับร่อง</li><li>ค้นเครื่องหมายการค้า (คำทั่วไปต้องจดเป็นโลโก้) และชื่อบัญชี</li>
<li>ส่งสเก็ตช์มา ผมทำเป็นเวกเตอร์ Brand Book โปสเตอร์ 30 ตัว และสไลด์ให้ทั้งชุด</li></ol></section>
{set10}

{set8}
{set9}

{set6}
{set7}

{set5}

{set4}

{set3}

{opts}
<section class="opt"><h2>เทียบกันทั้งห้าสิบห้า</h2>
<div class="tbl"><table><thead><tr><th>แบรนด์</th><th>โทน</th><th>เรื่องครอบครัว</th><th>จดชื่อ</th><th>ราคาสินค้าหลัก (บาท)</th></tr></thead><tbody>{crow}</tbody></table></div></section>

</div>"""

if __name__ == "__main__":
    open(os.path.join(HERE, "index.html"), "w").write(page())
    print("ok")
