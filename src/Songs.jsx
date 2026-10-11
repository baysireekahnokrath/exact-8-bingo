import { useMemo, useState } from "react";
import { GROUPS, MEMBER_BY_ID, MEMBERS, membersOf } from "./members.js";
import { addSong, removeSong, setSongDone, useSongs } from "./api.js";
import Qr from "./Qr.jsx";

// หน้าขอเพลง (Halloween): เลือกชื่อตัวเอง → ใส่เพลง → เลือกคนที่อยากให้ร้อง
const ME_KEY = "exact8-songs-me";
const MAX_SINGERS = 6;

const loadMe = () => {
  try {
    return Number(localStorage.getItem(ME_KEY)) || null;
  } catch {
    return null;
  }
};
const saveMe = (id) => {
  try {
    if (id) localStorage.setItem(ME_KEY, String(id));
    else localStorage.removeItem(ME_KEY);
  } catch {}
};

const nameOf = (id) => MEMBER_BY_ID[id]?.name || "?";
// ชื่อเล่นซ้ำกันได้ข้ามกลุ่ม (เช่น พี่ตุ้ม) จึงต่อท้ายด้วยกลุ่ม
const labelOf = (id) => `${nameOf(id)} (${MEMBER_BY_ID[id]?.group})`;
const timeOf = (at) => new Date(at).toLocaleTimeString("th-TH", { hour: "2-digit", minute: "2-digit" });

function Bats() {
  return (
    <div className="hw-bats" aria-hidden="true">
      <span>🦇</span><span>🦇</span><span>🦇</span><span>👻</span><span>🕸️</span>
    </div>
  );
}

function Title({ sub }) {
  return (
    <header className="hw-title">
      <div className="hw-pumpkin">🎃</div>
      <h1>EXACT 8</h1>
      <div className="hw-night">Halloween Song Request</div>
      {sub && <p>{sub}</p>}
    </header>
  );
}

// ---------- เลือกชื่อ (ใช้ทั้งเลือกตัวเองและเลือกคนร้อง) ----------
function MemberPicker({ selected, onPick, disabled = [] }) {
  const [group, setGroup] = useState(GROUPS[0]);
  const [q, setQ] = useState("");
  const list = q.trim() ? MEMBERS.filter((m) => m.name.includes(q.trim())) : membersOf(group);
  return (
    <div className="hw-picker">
      <input className="hw-input" value={q} placeholder="🔍 ค้นหาชื่อ เช่น ตุ้ม" onChange={(e) => setQ(e.target.value)} />
      {!q.trim() && (
        <div className="hw-tabs">
          {GROUPS.map((g) => (
            <button key={g} className={g === group ? "on" : ""} onClick={() => setGroup(g)}>{g}</button>
          ))}
        </div>
      )}
      <div className="hw-names">
        {list.map((m) => (
          <button
            key={m.id}
            className={selected.includes(m.id) ? "on" : ""}
            disabled={disabled.includes(m.id)}
            onClick={() => onPick(m.id)}
          >
            {m.name}
            {q.trim() && <small>{m.group}</small>}
          </button>
        ))}
        {list.length === 0 && <p className="hw-muted">ไม่พบชื่อนี้</p>}
      </div>
    </div>
  );
}

// ---------- หน้าผู้ขอเพลง (มือถือ) ----------
export default function SongRequest() {
  const [me, setMe] = useState(loadMe);
  const pickMe = (id) => {
    saveMe(id);
    setMe(id);
  };

  return (
    <div className="hw">
      <Bats />
      <div className="hw-page">
        {me ? (
          <RequestForm me={me} onChangeMe={() => pickMe(null)} />
        ) : (
          <>
            <Title sub="ขอเพลงที่อยากฟัง แล้วเลือกคนที่อยากให้ขึ้นร้อง!" />
            <section className="hw-card">
              <h2><span className="hw-step">1</span> คุณคือใคร?</h2>
              <MemberPicker selected={[]} onPick={pickMe} />
            </section>
          </>
        )}
      </div>
    </div>
  );
}

function RequestForm({ me, onChangeMe }) {
  const songs = useSongs();
  const [song, setSong] = useState("");
  const [singers, setSingers] = useState([]);
  const [picking, setPicking] = useState(false);
  const [busy, setBusy] = useState(false);
  const [toast, setToast] = useState("");
  const mine = (songs || []).filter((s) => s.by === me);
  const m = MEMBER_BY_ID[me];

  const toggleSinger = (id) =>
    setSingers((cur) => (cur.includes(id) ? cur.filter((x) => x !== id) : cur.length < MAX_SINGERS ? [...cur, id] : cur));

  const submit = async (e) => {
    e.preventDefault();
    if (!song.trim() || singers.length === 0) return;
    setBusy(true);
    try {
      await addSong({ by: me, song: song.trim().slice(0, 120), singers, at: Date.now() });
      setSong("");
      setSingers([]);
      setToast("🎃 ส่งคำขอเพลงแล้ว!");
      setTimeout(() => setToast(""), 2500);
    } catch {
      setToast("ส่งไม่สำเร็จ ลองใหม่อีกครั้ง");
      setTimeout(() => setToast(""), 3000);
    }
    setBusy(false);
  };

  return (
    <>
      <Title />
      <div className="hw-me">
        👻 สวัสดี <b>{m?.name}</b> <small>({m?.group})</small>
        <button className="hw-link" onClick={onChangeMe}>ไม่ใช่ฉัน</button>
      </div>

      <form className="hw-card" onSubmit={submit}>
        <h2><span className="hw-step">2</span> เพลงที่อยากฟัง 🎵</h2>
        <input
          className="hw-input"
          value={song}
          maxLength={120}
          placeholder="ชื่อเพลง – ศิลปิน"
          onChange={(e) => setSong(e.target.value)}
        />

        <h2><span className="hw-step">3</span> อยากให้ใครร้อง? 🎤</h2>
        <div className="hw-chips">
          {singers.map((id) => (
            <button type="button" key={id} className="hw-chip" onClick={() => toggleSinger(id)}>
              {nameOf(id)} <small>{MEMBER_BY_ID[id].group}</small> ✕
            </button>
          ))}
          <button type="button" className="hw-add" onClick={() => setPicking(true)}>
            + {singers.length ? "เพิ่มคนร้อง" : "เลือกคนร้อง"}
          </button>
        </div>

        <button className="hw-btn" disabled={!song.trim() || singers.length === 0 || busy}>
          {busy ? "กำลังส่ง…" : "ส่งคำขอเพลง 🦇"}
        </button>
      </form>

      {mine.length > 0 && (
        <section className="hw-card">
          <h2>เพลงที่ฉันขอ <small>({mine.length})</small></h2>
          <ul className="hw-mine">
            {mine.map((s) => (
              <li key={s.sid} className={s.done ? "done" : ""}>
                <div>
                  <b>{s.song}</b>
                  <span>🎤 {s.singers.map(labelOf).join(", ")}</span>
                </div>
                {s.done ? (
                  <em>ร้องแล้ว ✓</em>
                ) : (
                  <button className="hw-link" onClick={() => confirm(`ยกเลิกเพลง "${s.song}"?`) && removeSong(s.sid)}>ยกเลิก</button>
                )}
              </li>
            ))}
          </ul>
        </section>
      )}

      {picking && (
        <div className="hw-sheet-bg" onClick={() => setPicking(false)}>
          <div className="hw-sheet" onClick={(e) => e.stopPropagation()}>
            <h2>เลือกคนร้อง <small>{singers.length}/{MAX_SINGERS} คน</small></h2>
            <MemberPicker selected={singers} onPick={toggleSinger} />
            <button className="hw-btn" onClick={() => setPicking(false)}>เสร็จ ({singers.length} คน)</button>
          </div>
        </div>
      )}
      {toast && <div className="hw-toast">{toast}</div>}
    </>
  );
}

// ---------- จอรวมคำขอเพลง (พิธีกร / จอใหญ่) ----------
export function SongBoard() {
  const songs = useSongs();
  const url = `${location.origin}/songs`;
  const ranking = useMemo(() => {
    const count = {};
    for (const s of songs || []) if (!s.done) for (const id of s.singers) count[id] = (count[id] || 0) + 1;
    return Object.entries(count).sort((a, b) => b[1] - a[1]).slice(0, 10);
  }, [songs]);
  const list = [...(songs || [])].sort((a, b) => (a.done ? 1 : 0) - (b.done ? 1 : 0));
  const waiting = list.filter((s) => !s.done).length;

  return (
    <div className="hw hw-board">
      <Bats />
      <header className="hw-board-head">
        <div>
          <h1>🎃 EXACT 8 <span>Halloween Song Request</span></h1>
          <p>รอร้อง <b>{waiting}</b> เพลง · ทั้งหมด <b>{list.length}</b> คำขอ</p>
        </div>
        <div className="hw-board-qr">
          <Qr url={url} size={110} />
          <span>สแกนเพื่อขอเพลง<br /><b>{url.replace(/^https?:\/\//, "")}</b></span>
        </div>
      </header>

      <div className="hw-board-main">
        <section className="hw-card hw-queue">
          <h2>🎵 คิวเพลง</h2>
          {songs === undefined && <p className="hw-muted">กำลังโหลด…</p>}
          {songs && list.length === 0 && <p className="hw-muted">ยังไม่มีคำขอเพลง 👻</p>}
          <ol>
            {list.map((s) => (
              <li key={s.sid} className={s.done ? "done" : ""}>
                <label className="hw-done" title="ร้องแล้ว">
                  <input type="checkbox" checked={!!s.done} onChange={(e) => setSongDone(s.sid, e.target.checked)} />
                </label>
                <div className="hw-song">
                  <b>{s.song}</b>
                  <span>
                    🎤 <em>{s.singers.map(labelOf).join(", ")}</em>
                    <small> · ขอโดย {labelOf(s.by)} {timeOf(s.at)}</small>
                  </span>
                </div>
                <button className="hw-link" onClick={() => confirm(`ลบเพลง "${s.song}"?`) && removeSong(s.sid)}>ลบ</button>
              </li>
            ))}
          </ol>
        </section>

        <section className="hw-card hw-rank">
          <h2>👑 ถูกขอให้ร้องมากที่สุด</h2>
          {ranking.length === 0 && <p className="hw-muted">ยังไม่มี</p>}
          <ol>
            {ranking.map(([id, n]) => (
              <li key={id}>
                <span>{nameOf(id)} <small>{MEMBER_BY_ID[id].group}</small></span>
                <b>{n}</b>
              </li>
            ))}
          </ol>
        </section>
      </div>
    </div>
  );
}
