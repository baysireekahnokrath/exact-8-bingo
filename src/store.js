// ชั้นเก็บข้อมูลกลาง: ใช้ Firebase Realtime Database ถ้ามี config
// ถ้าไม่มี ใช้ localStorage แทน (sync ข้ามแท็บในเครื่องเดียว สำหรับทดสอบ)
import { initializeApp } from "firebase/app";
import * as db from "firebase/database";
import { firebaseConfig } from "./firebaseConfig.js";

const forceLocal = new URLSearchParams(location.search).has("local");
export const isLocalMode = !firebaseConfig || forceLocal;

let impl;

if (!isLocalMode) {
  const database = db.getDatabase(initializeApp(firebaseConfig));
  // ?emu = ใช้ Firebase Emulator ในเครื่อง (สำหรับนักพัฒนาทดสอบเท่านั้น)
  if (new URLSearchParams(location.search).has("emu")) db.connectDatabaseEmulator(database, "127.0.0.1", 9000);
  const r = (path) => (path ? db.ref(database, path) : db.ref(database));
  impl = {
    subscribe(path, cb) {
      return db.onValue(r(path), (snap) => cb(snap.val()));
    },
    set: (path, val) => db.set(r(path), val),
    update: (path, val) => db.update(r(path), val),
    remove: (path) => db.remove(r(path)),
    async transaction(path, fn) {
      const res = await db.runTransaction(r(path), fn);
      return res.committed ? res.snapshot.val() : undefined;
    },
    onConnection(cb) {
      return db.onValue(r(".info/connected"), (snap) => cb(snap.val() === true));
    },
  };
} else {
  const KEY = "exact8-bingo-local-db";
  const listeners = new Set();
  const load = () => {
    try {
      return JSON.parse(localStorage.getItem(KEY)) || {};
    } catch {
      return {};
    }
  };
  let tree = load();
  const parts = (path) => path.split("/").filter(Boolean);
  const getAt = (path) => parts(path).reduce((n, k) => (n == null ? null : n[k] ?? null), tree);
  const clean = (v) => (v === undefined ? null : JSON.parse(JSON.stringify(v ?? null)));
  const setAt = (path, val) => {
    const ks = parts(path);
    if (ks.length === 0) {
      tree = clean(val) || {};
      return;
    }
    let n = tree;
    for (const k of ks.slice(0, -1)) {
      if (typeof n[k] !== "object" || n[k] === null) n[k] = {};
      n = n[k];
    }
    const last = ks[ks.length - 1];
    if (val === null || val === undefined) delete n[last];
    else n[last] = clean(val);
  };
  const notify = () => listeners.forEach((l) => l.cb(clean(getAt(l.path))));
  const commit = () => {
    localStorage.setItem(KEY, JSON.stringify(tree));
    notify();
  };
  window.addEventListener("storage", (e) => {
    if (e.key !== KEY) return;
    tree = load();
    notify();
  });
  impl = {
    subscribe(path, cb) {
      const l = { path, cb };
      listeners.add(l);
      setTimeout(() => cb(clean(getAt(path))), 0);
      return () => listeners.delete(l);
    },
    async set(path, val) {
      tree = load();
      setAt(path, val);
      commit();
    },
    async update(path, val) {
      tree = load();
      for (const [k, v] of Object.entries(val)) setAt(`${path}/${k}`, v);
      commit();
    },
    async remove(path) {
      tree = load();
      setAt(path, null);
      commit();
    },
    async transaction(path, fn) {
      tree = load();
      const next = fn(clean(getAt(path)));
      if (next === undefined) return undefined;
      setAt(path, next);
      commit();
      return clean(next);
    },
    onConnection(cb) {
      setTimeout(() => cb(true), 0);
      return () => {};
    },
  };
}

export const store = impl;
