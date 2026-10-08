import { useEffect, useRef, useState } from "react";
import { isLocalMode, store } from "./store.js";
import { MEMBERS } from "./members.js";
import { toList } from "./bingo.js";

// ---------- hooks ----------
export function useValue(path) {
  const [value, setValue] = useState(undefined); // undefined = ยังโหลดไม่เสร็จ
  useEffect(() => store.subscribe(path, setValue), [path]);
  return value;
}

export function useGame() {
  const raw = useValue("game");
  if (raw === undefined) return undefined;
  const g = raw || {};
  return {
    round: g.round || 1,
    drawn: toList(g.drawn).map(Number),
    current: g.current || null,
    accepting: g.accepting !== false,
  };
}

export function usePlayers() {
  const raw = useValue("players");
  if (raw === undefined) return undefined;
  return Object.entries(raw || {}).map(([pid, p]) => ({ pid, ...p }));
}

export function useConnected() {
  const [ok, setOk] = useState(true);
  useEffect(() => store.onConnection(setOk), []);
  return ok;
}

// แสดงชื่อที่สุ่มใหม่ช้ากว่าจริงเล็กน้อย ให้จอใหญ่หมุนลุ้นเสร็จก่อน (ใช้บนมือถือผู้เล่น)
export function useDelayedDrawn(game, delayMs) {
  const [shown, setShown] = useState(null);
  const drawn = game?.drawn;
  const key = drawn ? drawn.join(",") : null;
  const shownRef = useRef(null);
  shownRef.current = shown;
  useEffect(() => {
    if (!drawn) return;
    const prev = shownRef.current;
    if (prev === null || drawn.length <= prev.length) {
      setShown(drawn);
      return;
    }
    const t = setTimeout(() => setShown(drawn), delayMs);
    return () => clearTimeout(t);
  }, [key]); // eslint-disable-line react-hooks/exhaustive-deps
  return shown;
}

// ---------- ผู้เล่น ----------
export function getPlayerId() {
  // โหมดทดสอบ: แยกผู้เล่นตามแท็บ เพื่อลองหลายคนในเครื่องเดียว
  const KEY = "exact8-bingo-pid";
  let pid = null;
  try {
    const s = isLocalMode ? sessionStorage : localStorage;
    pid = s.getItem(KEY);
    if (!pid) {
      pid = "p" + Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
      s.setItem(KEY, pid);
    }
  } catch {
    pid = pid || "p" + Math.random().toString(36).slice(2, 10);
  }
  return pid;
}

export const registerPlayer = (pid, name) =>
  store.set(`players/${pid}`, { name, joinedAt: Date.now(), card: null, locked: false });
export const renamePlayer = (pid, name) => store.update(`players/${pid}`, { name });
export const saveCard = (pid, card) => store.set(`players/${pid}/card`, card.map((v) => v || 0));
export const lockCard = (pid, card) =>
  store.update(`players/${pid}`, { card, locked: true, lockedAt: Date.now() });
export const setMark = (pid, cell, on) => store.set(`players/${pid}/marks/c${cell}`, on ? true : null);
export const removePlayer = (pid) => store.remove(`players/${pid}`);

// ---------- ทีมงาน ----------
export async function drawNext() {
  let picked = null;
  await store.transaction("game", (g) => {
    g = g || {};
    const drawn = toList(g.drawn).map(Number);
    const remaining = MEMBERS.filter((m) => !drawn.includes(m.id));
    if (remaining.length === 0) return undefined;
    const m = remaining[Math.floor(Math.random() * remaining.length)];
    picked = m.id;
    return { ...g, drawn: [...drawn, m.id], current: { id: m.id, n: drawn.length + 1, at: Date.now() } };
  });
  return picked;
}

export async function undoLastDraw() {
  await store.transaction("game", (g) => {
    g = g || {};
    const drawn = toList(g.drawn).map(Number);
    if (drawn.length === 0) return undefined;
    drawn.pop();
    const last = drawn[drawn.length - 1];
    return { ...g, drawn, current: last ? { id: last, n: drawn.length, at: Date.now() } : null };
  });
}

export const setAccepting = (on) => store.update("game", { accepting: on });

// ล้างชื่อที่สุ่มแล้ว แต่เก็บการ์ดผู้เล่นไว้ (ล้างช่องที่ผู้เล่นแตะด้วย)
export function resetDraws(players) {
  const patch = { "game/drawn": null, "game/current": null };
  for (const p of players || []) patch[`players/${p.pid}/marks`] = null;
  return store.update("", patch);
}

// ล้างทุกอย่าง ผู้เล่นต้องใส่ชื่อและเลือกการ์ดใหม่
export function resetAll(game) {
  return store.update("", {
    players: null,
    game: { round: (game?.round || 1) + 1, accepting: true },
  });
}
