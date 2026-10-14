"""Build the leather cost & pricing workbook (xlsx -> uploaded to Google Drive as a Google Sheet).

All derived numbers are formulas over the input cells, so the sheet stays live in Google Sheets.
"""
import os
from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "Arial"
BLUE, BLACK, GREEN = "0000FF", "000000", "008000"
HEAD = PatternFill("solid", fgColor="1F3864"); YEL = PatternFill("solid", fgColor="FFF2CC"); SUB = PatternFill("solid", fgColor="D9E1F2")
thin = Side(style="thin", color="BFBFBF"); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
NUM2, NUM0, PCT = '#,##0.00', '#,##0', '0.0%'

def style(c, color=BLACK, bold=False, fill=None, fmt=None, wrap=False, align=None, size=10):
    c.font = Font(name=FONT, color=color, bold=bold, size=size)
    if fill: c.fill = fill
    if fmt: c.number_format = fmt
    c.alignment = Alignment(wrap_text=wrap, vertical="center", horizontal=align)
    c.border = BOX

def header(ws, row, labels, col=1):
    for i, t in enumerate(labels):
        c = ws.cell(row=row, column=col + i, value=t)
        style(c, "FFFFFF", True, HEAD, wrap=True, align="center")
    ws.row_dimensions[row].height = 42

def note(c, text):
    """Sources are written as visible text rows instead of cell comments (keeps the upload small)."""
    return

wb = Workbook()

# ------------------------------------------------------------------ Inputs
S = wb.active; S.title = "ตั้งค่า"
S["A1"] = "ต้นทุนและราคาขาย: สินค้าหนังไม่ต้องเย็บ"; S["A1"].font = Font(name=FONT, bold=True, size=14)
S["A2"] = "ตัวอักษรสีน้ำเงิน = ค่าที่กรอกเอง · พื้นสีเหลือง = ค่าประมาณ ควรวัดหรือชั่งจริงแล้วแก้ · ช่องอื่นเป็นสูตร ไม่ต้องแก้"
S["A2"].font = Font(name=FONT, italic=True, size=10, color="595959")

S["A4"] = "หนังที่ซื้อมา"; S["A4"].font = Font(name=FONT, bold=True, size=12)
header(S, 5, ["ล็อต", "ขนาดเศษ", "ราคา (บาท/กก.)", "ซื้อมา (กก.)", "จ่ายไป (บาท)", "กว้างทั่วไป (ซม.)", "ยาวทั่วไป (ซม.)",
              "ความหนา (มม.)", "ความหนาแน่น (ก./ลบ.ซม.)", "น้ำหนักต่อแผ่น ประมาณ (ก.)", "น้ำหนักต่อแผ่น ชั่งจริง (ก.)",
              "น้ำหนักต่อแผ่นที่ใช้ (ก.)", "แผ่นต่อ กก."])
lots = [("ใหญ่", "บางใหญ่ เกินฝ่ามือ 14–18 × 20 ซม. ขึ้นไป", 95, 20, 16, 22),
        ("เล็ก", "บางเล็ก เท่าฝ่ามือ 10–12 × 16–20 ซม.", 15, 5, 11, 18)]
for i, (lot, desc, price, kg, w, l) in enumerate(lots):
    r = 6 + i
    vals = [lot, desc, price, kg, f"=C{r}*D{r}", w, l, 1.0, 0.9, f"=F{r}*G{r}*H{r}/10*I{r}", None,
            f'=IF(K{r}="",J{r},K{r})', f"=IF(L{r}=0,0,1000/L{r})"]
    for j, v in enumerate(vals):
        c = S.cell(row=r, column=1 + j, value=v)
        inp = j in (0, 1, 2, 3, 5, 6, 7, 8, 10)
        est = j in (5, 6, 7, 8, 10)
        style(c, BLUE if inp else BLACK, fill=YEL if est else None,
              fmt=None if j < 2 else (NUM2 if j in (2, 4, 9, 11, 12) else '0.0'), wrap=(j == 1))
    note(S.cell(row=r, column=3), "Source: ผู้ใช้แจ้ง 14 ต.ค. 2026")
    note(S.cell(row=r, column=4), "Source: ผู้ใช้แจ้ง 14 ต.ค. 2026")
    note(S.cell(row=r, column=6), "ค่ากลางจากช่วงขนาดที่ผู้ใช้แจ้ง ใช้คำนวณว่าแผ่นหนึ่งวาง die ได้กี่ชิ้น")
    note(S.cell(row=r, column=8), "ค่าประมาณสำหรับหนังบาง แก้เป็นความหนาจริง")
    note(S.cell(row=r, column=9), "ค่าประมาณของหนังทั่วไป 0.8–1.0 ใช้เฉพาะเมื่อยังไม่ได้ชั่งจริง")
    note(S.cell(row=r, column=11), "ชั่งเศษ 10 แผ่น แล้วหารด้วย 10 แล้วกรอกที่นี่ ช่องนี้จะแทนค่าประมาณ")
S["B9"] = "ที่มา: ราคาและน้ำหนักที่ซื้อ ผู้ใช้แจ้ง 14 ต.ค. 2026 · ขนาดทั่วไปใช้ค่ากลางของช่วงที่แจ้ง · ความหนาและความหนาแน่นเป็นค่าประมาณ ชั่งเศษจริง 10 แผ่นแล้วกรอกน้ำหนักเฉลี่ยในคอลัมน์ K"
S["B9"].font = Font(name=FONT, italic=True, size=9, color="595959")
r = 8
S.cell(row=r, column=1, value="รวม"); style(S.cell(row=r, column=1), bold=True, fill=SUB)
for col, f in ((4, "=SUM(D6:D7)"), (5, "=SUM(E6:E7)")):
    c = S.cell(row=r, column=col, value=f); style(c, bold=True, fill=SUB, fmt=NUM2)

S["A10"] = "ค่าแรงและค่าใช้จ่ายอื่น"; S["A10"].font = Font(name=FONT, bold=True, size=12)
header(S, 11, ["รายการ", "ค่า", "หน่วย", "หมายเหตุ"])
params = [
    ("ค่าแรง", 50, "บาท/ชม.", "ตัวอย่าง: 400 บาท/วัน ÷ 8 ชม. แก้เป็นค่าแรงจริง"),
    ("เวลาตัด 1 ครั้ง", 10, "วินาที", "จับเวลาตอนตัดจริงแล้วแก้"),
    ("เวลาประกอบ 1 รอยต่อ", 20, "วินาที", "รวมการร้อยสายหรือสอดปีก 1 จุด"),
    ("เวลาเก็บงานและแพ็ค ต่อสินค้า", 60, "วินาที", "ตรวจงาน ใส่ถุงหรือกล่อง ติดป้าย"),
    ("ระยะห่างระหว่าง die", 3, "มม.", "ระยะที่ต้องเว้นรอบชิ้นงานเวลาวาง die บนเศษหนัง"),
    ("เผื่อเสีย (ตำหนิ ตัดพลาด เศษที่รูปทรงไม่ดี)", 0.20, "%", "ลดจำนวนชิ้นที่ตัดได้ลงตามนี้"),
    ("ราคา die ต่ออัน", 1500, "บาท", "ตัวอย่าง แก้เป็นราคาที่ช่างเสนอ ถ้ายังตัดด้วยเลเซอร์ใส่ 0"),
    ("จำนวนชิ้นที่จะตัดต่อ die", 1000, "ชิ้น", "ใช้เฉลี่ยค่า die ลงในแต่ละชิ้น"),
    ("ค่าธรรมเนียมช่องทางขาย", 0.0, "%", "เช่น ค่าธรรมเนียมแพลตฟอร์มออนไลน์ ขายเองใส่ 0"),
    ("ตัวคูณราคาแนะนำ", 3.0, "เท่าของต้นทุน", "ราคาแนะนำ = ต้นทุนรวม × ตัวคูณ แล้วปัดขึ้น"),
    ("ปัดราคาแนะนำขึ้นทีละ", 10, "บาท", ""),
]
P = {}
for i, (lab, val, unit, nt) in enumerate(params):
    r = 12 + i
    for j, v in enumerate((lab, val, unit, nt)):
        c = S.cell(row=r, column=1 + j, value=v)
        style(c, BLUE if j == 1 else BLACK, fill=YEL if j == 1 else None,
              fmt=(PCT if unit == "%" else ('0.0' if isinstance(val, float) else NUM0)) if j == 1 else None, wrap=(j in (0, 3)))
    P[lab] = f"ตั้งค่า!$B${r}"
    note(S.cell(row=r, column=2), "Source: ค่าตัวอย่างที่ Claude ใส่ไว้ ให้แก้เป็นค่าจริง")
S["A25"] = "วิธีใช้"; S["A25"].font = Font(name=FONT, bold=True, size=12)
steps = ["1. ชั่งเศษหนังล็อตละ 10 แผ่น แล้วกรอกน้ำหนักเฉลี่ยในช่อง 'น้ำหนักต่อแผ่น ชั่งจริง'",
         "2. ลองตัดจริงแล้วกรอกจำนวนชิ้นต่อแผ่นในแท็บ 'ต้นทุนชิ้นงาน' ถ้าต่างจากที่คำนวณ",
         "3. แก้ค่าแรง เวลา ราคา die และค่าบรรจุภัณฑ์ให้เป็นค่าจริง",
         "4. ใส่ราคาขายจริงในแท็บ 'ราคาขายสินค้า' แล้วดูกำไรต่อชิ้น"]
for i, t in enumerate(steps):
    S.cell(row=26 + i, column=1, value=t).font = Font(name=FONT, size=10)
for col, w in zip("ABCDEFGHIJKLM", (34, 34, 12, 11, 12, 11, 11, 10, 13, 14, 14, 14, 11)):
    S.column_dimensions[col].width = w
S.freeze_panes = "A6"

# ------------------------------------------------------------------ Piece costs
C = wb.create_sheet("ต้นทุนชิ้นงาน")
C["A1"] = "ต้นทุนต่อชิ้นงาน 1 ชิ้น (ตัดจาก die 1 ครั้ง)"; C["A1"].font = Font(name=FONT, bold=True, size=14)
C["A2"] = "เลือกล็อตเศษหนังในคอลัมน์ F ได้ ถ้าลองตัดจริงแล้วได้จำนวนชิ้นต่อแผ่นไม่ตรง ให้กรอกในคอลัมน์ H"
C["A2"].font = Font(name=FONT, italic=True, size=10, color="595959")
header(C, 4, ["แบบ", "ชื่อ", "die กว้าง (มม.)", "die ยาว (มม.)", "หนังสุทธิ (ตร.ซม.)", "ใช้เศษล็อต",
              "ชิ้นต่อแผ่น (คำนวณ)", "ชิ้นต่อแผ่น (ลองตัดจริง)", "ชิ้นต่อแผ่นที่ใช้", "ชิ้นต่อ กก.",
              "ค่าหนังต่อชิ้น (บาท)", "ค่าตัดต่อชิ้น (บาท)", "ค่า die ต่อชิ้น (บาท)", "ต้นทุนต่อชิ้น (บาท)",
              "ตัดได้จากล็อตที่ซื้อ (ชิ้น)", "หมายเหตุ"])
pieces = [("01", "Bear head", 104.36, 104.36, 63.7, "ใหญ่"),
          ("01-S 200", "สายหัวใจ 200 mm", 200, 22, 26.0, "ใหญ่"),
          ("01-S 250", "สายหัวใจ 250 mm", 250, 22, 32.5, "ใหญ่"),
          ("02", "Pinwheel", 90, 90, 57.3, "เล็ก"),
          ("03", "Capsule cross", 90, 90, 52.1, "เล็ก"),
          ("04", "Rounded square", 90, 90, 80.8, "เล็ก"),
          ("05", "Circle", 90, 90, 63.6, "เล็ก"),
          ("06", "Soft cross", 90, 90, 48.1, "เล็ก")]
gap, waste, rate = P["ระยะห่างระหว่าง die"], P["เผื่อเสีย (ตำหนิ ตัดพลาด เศษที่รูปทรงไม่ดี)"], P["ค่าแรง"]
cut, dprice, dqty = P["เวลาตัด 1 ครั้ง"], P["ราคา die ต่ออัน"], P["จำนวนชิ้นที่จะตัดต่อ die"]
dv = DataValidation(type="list", formula1='"ใหญ่,เล็ก"', allow_blank=False); C.add_data_validation(dv)
for i, (code, name, dw, dh, area, lot) in enumerate(pieces):
    r = 5 + i
    m = f"MATCH($F{r},ตั้งค่า!$A$6:$A$7,0)"
    W, L = f"INDEX(ตั้งค่า!$F$6:$F$7,{m})*10", f"INDEX(ตั้งค่า!$G$6:$G$7,{m})*10"
    calc = (f"=MAX(INT({W}/(C{r}+{gap}))*INT({L}/(D{r}+{gap})),"
            f"INT({W}/(D{r}+{gap}))*INT({L}/(C{r}+{gap})))")
    vals = [code, name, dw, dh, area, lot, calc, None,
            f'=IF(H{r}="",G{r},H{r})',
            f"=I{r}*INDEX(ตั้งค่า!$M$6:$M$7,{m})*(1-{waste})",
            f"=IF(J{r}=0,0,INDEX(ตั้งค่า!$C$6:$C$7,{m})/J{r})",
            f"={cut}/3600*{rate}",
            f"=IF({dqty}=0,0,{dprice}/{dqty})",
            f"=K{r}+L{r}+M{r}",
            f"=INT(J{r}*INDEX(ตั้งค่า!$D$6:$D$7,{m}))",
            f'=IF(I{r}=0,"เศษล็อตนี้สั้นหรือแคบเกินไป ตัดชิ้นนี้ไม่ได้","")']
    for j, v in enumerate(vals):
        c = C.cell(row=r, column=1 + j, value=v)
        fmt = {2: '0.0', 3: '0.0', 4: '0.0', 6: NUM0, 7: NUM0, 8: NUM0, 9: '0.0', 10: NUM2, 11: NUM2, 12: NUM2, 13: NUM2, 14: NUM0}.get(j)
        style(c, BLUE if j in (5, 7) else BLACK, bold=(j == 13), fill=YEL if j == 7 else None, fmt=fmt, wrap=(j == 15))
    dv.add(f"F{r}")
note(C["E5"], "Source: คำนวณจากเส้นตัดในไฟล์ DXF ชุด rev 20261014")
note(C["C5"], "Source: ขนาดกรอบของ die จากไฟล์ DXF ชุด rev 20261014")
for col, w in zip("ABCDEFGHIJKLMNOP", (10, 18, 10, 10, 11, 10, 11, 12, 11, 10, 12, 11, 11, 12, 12, 34)):
    C.column_dimensions[col].width = w
C["A14"] = "ที่มา: ขนาด die และพื้นที่หนังสุทธิคำนวณจากไฟล์ DXF ชุด rev 20261014 · ชิ้นต่อแผ่นคำนวณจากขนาดเศษทั่วไปในแท็บ 'ตั้งค่า' บวกระยะห่าง die"
C["A14"].font = Font(name=FONT, italic=True, size=9, color="595959")
C.freeze_panes = "C5"

# ------------------------------------------------------------------ Products
R = wb.create_sheet("ราคาขายสินค้า")
R["A1"] = "ราคาขายและกำไรต่อสินค้า"; R["A1"].font = Font(name=FONT, bold=True, size=14)
R["A2"] = "ใส่ราคาขายจริงในคอลัมน์ T ถ้าเว้นว่าง จะใช้ราคาแนะนำ · แถว 3 ดึงต้นทุนต่อชิ้นมาจากแท็บ 'ต้นทุนชิ้นงาน'"
R["A2"].font = Font(name=FONT, italic=True, size=10, color="595959")
codes = ["01", "01-S 200", "01-S 250", "02", "03", "04", "05", "06"]
R.cell(row=3, column=2, value="ต้นทุนต่อชิ้น (บาท)"); style(R.cell(row=3, column=2), bold=True, fill=SUB)
for k in range(8):
    c = R.cell(row=3, column=3 + k, value=f"='ต้นทุนชิ้นงาน'!N{5 + k}"); style(c, GREEN, fill=SUB, fmt=NUM2)
header(R, 4, ["#", "สินค้า"] + [f"ใช้แบบ {x} (ชิ้น)" for x in codes] +
       ["ค่าชิ้นงาน (บาท)", "ครั้งที่ตัด", "รอยต่อ", "ค่าประกอบ (บาท)", "ค่าเก็บงานและแพ็ค (บาท)", "ชิ้นเสริม (บาท)",
        "บรรจุภัณฑ์ (บาท)", "ต้นทุนรวม (บาท)", "ราคาแนะนำ (บาท)", "ราคาขาย (กรอก)", "ราคาที่ใช้ (บาท)",
        "ค่าธรรมเนียม (บาท)", "กำไรต่อชิ้น (บาท)", "กำไร %", "หมายเหตุ"])
# n, name, {code: qty}, joints, extra baht, packaging baht
prods = [
    (1, "ที่เก็บสายชาร์จหมี", {"01": 1}, 0, 0, 5), (2, "ที่คั่นหนังสือเหน็บมุมหน้า", {"01": 1}, 0, 0, 5),
    (3, "ป้ายชื่อติดกระเป๋านักเรียน", {"01": 1, "01-S 250": 1}, 2, 0, 5), (4, "ห่วงผ้าเช็ดปากหมี", {"01": 1, "01-S 200": 1}, 2, 0, 5),
    (5, "ซองอั่งเปาพับกังหัน", {"02": 1}, 4, 0, 5), (6, "ซองใส่เครื่องประดับ", {"02": 1}, 4, 0, 5),
    (7, "ซองการ์ดข้อความติดของขวัญ", {"02": 1}, 4, 0, 5),
    (8, "กล่องแหวนขอแต่งงาน", {"03": 6}, 12, 0, 5), (9, "ลูกเต๋าหนัง", {"03": 6}, 12, 0, 5),
    (10, "ซองใส่ AirTag", {"03": 2}, 4, 0, 5), (11, "ชุดตัวต่อหนังสำหรับเด็ก (24 ชิ้น)", {"03": 24}, 0, 10, 5),
    (12, "ที่ใส่ปากกาทรงมงกุฎ", {"04": 5}, 8, 0, 5), (13, "แผ่นรองจานลายข้าวหลามตัด", {"04": 12}, 17, 0, 5),
    (14, "ปลอกแก้วกาแฟ", {"05": 4}, 4, 0, 5), (15, "ที่รองแก้วสองชั้นไส้ไม้ก๊อก", {"05": 2}, 4, 10, 5),
    (16, "กระเป๋าเหรียญจิ๋ว", {"05": 2}, 3, 0, 5), (17, "กล่องของขวัญสลับลาย", {"04": 3, "05": 3}, 12, 0, 5),
    (18, "กล่องของชำร่วยงานแต่ง", {"06": 6}, 12, 0, 5), (19, "ที่ใส่แปรงแต่งหน้า", {"06": 5}, 8, 0, 5),
    (20, "ของแขวนต้นคริสต์มาส", {"06": 6}, 12, 3, 5),
]
EXTRA_NOTE = {11: "ถุงใส่ชุดตัวต่อ (ตัวอย่าง)", 15: "แผ่นไม้ก๊อก 60 × 60 mm (ตัวอย่าง)", 20: "ริบบิ้น (ตัวอย่าง)"}
first, last = 5, 5 + len(prods) - 1
jsec, psec, fee, mult, rnd = (P["เวลาประกอบ 1 รอยต่อ"], P["เวลาเก็บงานและแพ็ค ต่อสินค้า"],
                              P["ค่าธรรมเนียมช่องทางขาย"], P["ตัวคูณราคาแนะนำ"], P["ปัดราคาแนะนำขึ้นทีละ"])
for i, (n, name, use, joints, extra, pack) in enumerate(prods):
    r = first + i
    row = [n, name] + [use.get(cd) for cd in codes] + [
        f"=SUMPRODUCT($C$3:$J$3,C{r}:J{r})", f"=SUM(C{r}:J{r})", joints,
        f"=M{r}*{jsec}/3600*{rate}", f"={psec}/3600*{rate}", extra, pack,
        f"=K{r}+N{r}+O{r}+P{r}+Q{r}", f"=CEILING(R{r}*{mult},{rnd})", None,
        f'=IF(T{r}="",S{r},T{r})', f"=U{r}*{fee}", f"=U{r}-R{r}-V{r}", f"=IF(U{r}=0,0,W{r}/U{r})",
        f"=IF(AND(E{r}>0,'ต้นทุนชิ้นงาน'!I7=0),\"สาย 250 mm ตัดจากเศษขนาดนี้ไม่ได้ ต้องใช้เศษยาว 25.5 ซม. ขึ้นไป\",\"\")"]
    for j, v in enumerate(row):
        c = R.cell(row=r, column=1 + j, value=v)
        inp = j in range(2, 10) or j in (12, 15, 16, 19)
        fmt = NUM0 if j in (0, 11, 12) or 2 <= j <= 9 else (PCT if j == 23 else (None if j in (1, 24) else NUM2))
        style(c, BLUE if inp else BLACK, bold=j in (17, 22), fill=YEL if j in (15, 16, 19) else None, fmt=fmt, wrap=(j in (1, 24)))
    if n in EXTRA_NOTE:
        note(R.cell(row=r, column=16), f"Source: {EXTRA_NOTE[n]} ค่าตัวอย่าง แก้เป็นราคาจริง")
note(R["Q5"], "Source: ค่าบรรจุภัณฑ์ตัวอย่าง 5 บาท แก้เป็นราคาจริงของแต่ละสินค้า")
note(R["M5"], "จำนวนรอยต่อที่ต้องประกอบที่โรงงาน (สอดปีกหรือร้อยสาย 1 จุด = 1)")
for col, w in zip("ABCDEFGHIJKLMNOPQRSTUVWXY", (5, 30, 9, 9, 9, 9, 9, 9, 9, 9, 11, 8, 8, 10, 11, 10, 11, 12, 12, 12, 12, 11, 12, 9, 40)):
    R.column_dimensions[col].width = w
R["A26"] = "ที่มา: ชิ้นเสริมและบรรจุภัณฑ์เป็นค่าตัวอย่าง (ถุงชุดตัวต่อ 10 · ไม้ก๊อก 10 · ริบบิ้น 3 · บรรจุภัณฑ์ 5 บาท) ให้แก้เป็นราคาจริง · รอยต่อ = จุดที่ต้องสอดปีกหรือร้อยสายที่โรงงาน"
R["A26"].font = Font(name=FONT, italic=True, size=9, color="595959")
R.freeze_panes = "C5"

out = os.path.join(HERE, "leather-cost-pricing.xlsx")
wb.save(out); print(out, os.path.getsize(out))
