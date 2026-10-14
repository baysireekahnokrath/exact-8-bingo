import json, subprocess
H = {"bold": True, "bg": "#6B4226", "fg": "#FFFFFF", "wrap": "wrap", "valign": "middle"}
M = '#,##0.00;(#,##0.00);"-"'
B = '#,##0;(#,##0);"-"'
P = '0.0%;(0.0%);"-"'
IN = "#0000FF"; Y = "#FFF2B3"
specs = {
 1627285359: {"rules": [
   {"range": "A1", "bold": True, "size": 14},
   {"range": "A2", "italic": True},
   {"range": "A4", "bold": True, "size": 12}, {"range": "A11", "bold": True, "size": 12}, {"range": "A25", "bold": True, "size": 12},
   dict(H, range="A5:M5"), dict(H, range="A12:D12"),
   {"range": "C6:D7", "fg": IN}, {"range": "F6:I7", "fg": IN, "bg": Y}, {"range": "K6:K7", "fg": IN, "bg": Y},
   {"range": "B13:B14", "fg": IN}, {"range": "B15:B18", "fg": IN, "bg": Y}, {"range": "B19:B23", "fg": IN},
   {"range": "E6:E8", "number": B}, {"range": "C6:C7", "number": B}, {"range": "J6:J7", "number": "0.0"},
   {"range": "L6:L7", "number": "0.0"}, {"range": "M6:M7", "number": "#,##0.0"},
   {"range": "B13", "number": M}, {"range": "B20:B21", "number": P},
   {"range": "A8:M8", "bold": True},
   {"range": "A5:M8", "borders": "#BFBFBF"}, {"range": "A12:D23", "borders": "#BFBFBF"},
   {"range": "A9:M9", "italic": True}],
   "col_widths": {"A": 210, "B": 230, "C:M": 110},
   "row_heights": {"5": 42}},
 101: {"rules": [
   {"range": "A1", "bold": True, "size": 14}, {"range": "A2", "italic": True},
   dict(H, range="A4:P4"),
   {"range": "F5:F12", "fg": IN}, {"range": "H5:H12", "fg": IN},
   {"range": "C5:E12", "number": "0.0"}, {"range": "J5:J12", "number": "0.0"},
   {"range": "K5:N12", "number": M}, {"range": "O5:O12", "number": B},
   {"range": "N5:N12", "bold": True}, {"range": "A5:A12", "bold": True},
   {"range": "A4:P12", "borders": "#BFBFBF"},
   {"range": "B14:P14", "bold": True}, {"range": "P14", "number": B}],
   "freeze": {"rows": 4, "columns": 2},
   "col_widths": {"A": 80, "B": 150, "C:O": 100, "P": 320},
   "row_heights": {"4": 42}},
 102: {"rules": [
   {"range": "A1", "bold": True, "size": 14}, {"range": "A2", "italic": True},
   {"range": "B3", "bold": True}, {"range": "C3:J3", "number": M, "bg": "#F3E9DF"},
   dict(H, range="A4:Y4"),
   {"range": "C5:J24", "fg": IN, "align": "center"}, {"range": "M5:M24", "fg": IN},
   {"range": "P5:Q24", "fg": IN, "bg": Y}, {"range": "T5:T24", "fg": IN, "bg": Y},
   {"range": "K5:K24", "number": M}, {"range": "N5:R24", "number": M},
   {"range": "S5:U24", "number": B}, {"range": "V5:W24", "number": M}, {"range": "X5:X24", "number": P},
   {"range": "R5:R24", "bold": True}, {"range": "W5:W24", "bold": True},
   {"range": "A4:Y24", "borders": "#BFBFBF"}, {"range": "B26", "italic": True}],
   "freeze": {"rows": 4, "columns": 2},
   "col_widths": {"A": 40, "B": 230, "C:X": 95, "Y": 320},
   "row_heights": {"4": 48}},
}
import os, glob; S = glob.glob(os.path.expanduser("~/.claude/skills/**/google-workspace/scripts/sheets_helper.py"), recursive=True)[0]
reqs = []
for sid, spec in specs.items():
    json.dump(spec, open(f"spec_{sid}.json", "w"), ensure_ascii=False)
    out = subprocess.run(["python3", S, "format", f"spec_{sid}.json", "--sheet-id", str(sid)], capture_output=True, text=True, check=True).stdout
    r = json.loads(out); reqs += r["requests"] if isinstance(r, dict) else r
reqs.append({"setDataValidation": {"range": {"sheetId": 101, "startRowIndex": 4, "endRowIndex": 12, "startColumnIndex": 5, "endColumnIndex": 6},
  "rule": {"condition": {"type": "ONE_OF_LIST", "values": [{"userEnteredValue": "ใหญ่"}, {"userEnteredValue": "เล็ก"}]}, "strict": True, "showCustomUi": True}}})
json.dump(reqs, open("fmt_requests.json", "w"), ensure_ascii=False)
print(len(reqs)); print(json.dumps(reqs[:3], ensure_ascii=False)[:800])
