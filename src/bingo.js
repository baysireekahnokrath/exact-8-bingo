// กติกาบิงโก: ครบ 5 ช่องเรียงกัน แนวนอน / แนวตั้ง / แนวทแยง
export const SIZE = 5;

export const LINES = (() => {
  const lines = [];
  for (let r = 0; r < SIZE; r++) lines.push([0, 1, 2, 3, 4].map((c) => r * SIZE + c));
  for (let c = 0; c < SIZE; c++) lines.push([0, 1, 2, 3, 4].map((r) => r * SIZE + c));
  lines.push([0, 6, 12, 18, 24]);
  lines.push([4, 8, 12, 16, 20]);
  return lines;
})();

// Firebase Realtime Database อาจคืน array มาเป็น object หรือ array ที่มีรู ให้แปลงกลับเป็น array เสมอ
export function toList(val) {
  if (!val) return [];
  if (Array.isArray(val)) return val.filter((v) => v !== null && v !== undefined);
  return Object.keys(val)
    .sort((a, b) => Number(a) - Number(b))
    .map((k) => val[k]);
}

export function toCard(val) {
  const out = Array(SIZE * SIZE).fill(null);
  if (!val) return out;
  for (const [k, v] of Object.entries(val)) {
    const i = Number(k);
    if (i >= 0 && i < out.length && v) out[i] = Number(v);
  }
  return out;
}

// เช็กการ์ดเทียบกับเงื่อนไข isHit(cellIndex)
export function lineStatus(isHit) {
  let bingo = false;
  const needs = new Set(); // ช่องที่ขาดอีก 1 ช่องจะได้บิงโก
  for (const line of LINES) {
    const missing = line.filter((i) => !isHit(i));
    if (missing.length === 0) bingo = true;
    else if (missing.length === 1) needs.add(missing[0]);
  }
  return { bingo, needs: [...needs] };
}

// วิเคราะห์การ์ดจากรายชื่อที่สุ่มออกแล้ว (ใช้บนจอใหญ่/หน้าทีมงาน)
// drawOrder: Map(memberId -> ลำดับที่ถูกสุ่ม เริ่มที่ 1)
export function analyzeCard(card, drawOrder) {
  const { bingo, needs } = lineStatus((i) => drawOrder.has(card[i]));
  let bingoAt = null;
  if (bingo) {
    for (const line of LINES) {
      if (line.every((i) => drawOrder.has(card[i]))) {
        const at = Math.max(...line.map((i) => drawOrder.get(card[i])));
        if (bingoAt === null || at < bingoAt) bingoAt = at;
      }
    }
  }
  return { bingo, bingoAt, needIds: needs.map((i) => card[i]) };
}

// สรุปผลผู้เล่นทุกคนจากรายชื่อที่สุ่มออกแล้ว
export function analyzePlayers(players, drawn) {
  const drawOrder = new Map(drawn.map((id, i) => [id, i + 1]));
  const ready = [];
  const pending = [];
  for (const p of players || []) {
    if (!p.locked) {
      pending.push(p);
      continue;
    }
    const card = toCard(p.card);
    ready.push({ ...p, ...analyzeCard(card, drawOrder) });
  }
  const winners = ready
    .filter((p) => p.bingo)
    .sort((a, b) => a.bingoAt - b.bingoAt || (a.lockedAt || 0) - (b.lockedAt || 0));
  const reach = ready
    .filter((p) => !p.bingo && p.needIds.length > 0)
    .sort((a, b) => b.needIds.length - a.needIds.length || (a.name || "").localeCompare(b.name || "", "th"));
  return { ready, pending, winners, reach };
}
