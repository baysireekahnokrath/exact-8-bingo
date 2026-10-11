// แปลงรายชื่อ CSV → ไฟล์ .vcf (vCard 3.0) ไฟล์เดียว ให้ทุกคน import เข้ามือถือได้ทั้ง iOS และ Android
//
// ใช้:  npm run contacts -- [ไฟล์ CSV] [ไฟล์ปลายทาง .vcf]
// ค่าเริ่มต้น: contacts/contacts.csv → contacts/EXACT8-contacts.vcf
//
// คอลัมน์ CSV (แถวแรกเป็นหัวตาราง ตาม contacts/contacts.example.csv):
//   ชื่อเล่น, ชื่อ, นามสกุล, เบอร์โทร, กลุ่ม, อีเมล, หมายเหตุ
// ต้องมีอย่างน้อย ชื่อเล่น หรือ ชื่อ และ เบอร์โทร (ใส่หลายเบอร์คั่นด้วย / ได้)

import { readFileSync, writeFileSync } from "node:fs";

// คำนำหน้าชื่อในมือถือ ทำให้ค้นหา "EXACT8" แล้วเจอเพื่อนทั้งรุ่น
const PREFIX = "EXACT8";
const ORG = "EXACT 8";

const [src = "contacts/contacts.csv", out = "contacts/EXACT8-contacts.vcf"] = process.argv.slice(2);

function parseCsv(text) {
  const rows = [];
  let row = [], field = "", quoted = false;
  text = text.replace(/^\uFEFF/, ""); // BOM จาก Excel / Google Sheets
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (quoted) {
      if (c === '"' && text[i + 1] === '"') { field += '"'; i++; }
      else if (c === '"') quoted = false;
      else field += c;
    } else if (c === '"') quoted = true;
    else if (c === ",") { row.push(field); field = ""; }
    else if (c === "\n" || c === "\r") {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(field); rows.push(row); row = []; field = "";
    } else field += c;
  }
  if (field || row.length) { row.push(field); rows.push(row); }
  return rows.filter((r) => r.some((f) => f.trim()));
}

// 081-234-5678 / 0812345678 / +66 81 234 5678 → +66812345678
function normalizePhone(raw) {
  let p = raw.replace(/[^\d+]/g, "");
  if (p.startsWith("+")) return p;
  if (p.startsWith("66") && p.length === 11) return "+" + p;
  if (p.startsWith("0") && (p.length === 10 || p.length === 9)) return "+66" + p.slice(1);
  return p;
}

const esc = (s) => s.replace(/\\/g, "\\\\").replace(/\n/g, "\\n").replace(/([,;])/g, "\\$1");

const COLS = {
  nick: ["ชื่อเล่น", "nickname"],
  first: ["ชื่อ", "first name", "firstname"],
  last: ["นามสกุล", "last name", "lastname"],
  phone: ["เบอร์โทร", "เบอร์", "phone", "mobile"],
  group: ["กลุ่ม", "group"],
  email: ["อีเมล", "email"],
  note: ["หมายเหตุ", "note"],
};

const [header, ...rows] = parseCsv(readFileSync(src, "utf8"));
const idx = {};
for (const [key, names] of Object.entries(COLS)) {
  idx[key] = header.findIndex((h) => names.includes(h.trim().toLowerCase()));
}
if (idx.phone < 0 || (idx.nick < 0 && idx.first < 0)) {
  console.error(`หัวตารางใน ${src} ต้องมีคอลัมน์ "เบอร์โทร" และ "ชื่อเล่น" หรือ "ชื่อ"`);
  process.exit(1);
}

const cards = [];
const problems = [];
rows.forEach((r, i) => {
  const get = (k) => (idx[k] >= 0 ? (r[idx[k]] || "").trim() : "");
  const nick = get("nick"), first = get("first"), last = get("last");
  const phones = get("phone").split("/").map((p) => p.trim()).filter(Boolean).map(normalizePhone);
  const line = i + 2;
  if (!nick && !first) return problems.push(`แถว ${line}: ไม่มีชื่อ`);
  if (!phones.length) problems.push(`แถว ${line} (${nick || first}): ไม่มีเบอร์โทร`);
  phones.forEach((p) => {
    if (!/^\+66[1-9]\d{7,8}$/.test(p) && !/^\+(?!66)\d{8,15}$/.test(p)) problems.push(`แถว ${line} (${nick || first}): เบอร์ "${p}" ดูไม่ถูกต้อง`);
  });

  // ชื่อที่โชว์ในมือถือ: "EXACT8 พี่คิตตี้ สมหญิง ใจดี"
  // ใส่ทั้งหมดไว้ในช่องชื่อ (N) เพื่อให้ iPhone และ Android แสดงเหมือนกัน
  const display = [PREFIX, nick, first, last].filter(Boolean).join(" ");
  const group = get("group"), email = get("email"), note = get("note");
  const lines = [
    "BEGIN:VCARD",
    "VERSION:3.0",
    `N:;${esc(display)};;;`,
    `FN:${esc(display)}`,
    nick && `NICKNAME:${esc(nick)}`,
    `ORG:${esc(ORG)}${group ? ";" + esc(group) : ""}`,
    ...phones.map((p) => `TEL;TYPE=CELL:${p}`),
    email && `EMAIL;TYPE=INTERNET:${esc(email)}`,
    `CATEGORIES:${esc(ORG)}`,
    note && `NOTE:${esc(note)}`,
    "END:VCARD",
  ].filter(Boolean);
  cards.push(lines.join("\r\n"));
});

writeFileSync(out, cards.join("\r\n") + "\r\n", "utf8");
console.log(`✅ สร้าง ${out} แล้ว: ${cards.length} รายชื่อ`);
if (problems.length) {
  console.log(`\n⚠️  ตรวจสอบ ${problems.length} จุด:`);
  problems.forEach((p) => console.log("   - " + p));
}
