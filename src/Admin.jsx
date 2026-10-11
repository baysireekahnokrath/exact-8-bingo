import { useMemo, useState } from "react";
import { GROUPS, MEMBER_BY_ID, membersOf, TOTAL } from "./members.js";
import { analyzePlayers, toCard } from "./bingo.js";
import {
  drawNext,
  removePlayer,
  resetAll,
  resetDraws,
  setAccepting,
  undoLastDraw,
  useGame,
  usePlayers,
} from "./api.js";
import Qr from "./Qr.jsx";

export default function Admin() {
  const game = useGame();
  const players = usePlayers();
  const [busy, setBusy] = useState(false);
  const [open, setOpen] = useState(null);
  const drawn = game?.drawn || [];
  const result = useMemo(() => analyzePlayers(players, drawn), [players, drawn]);

  if (!game || players === undefined) return <div className="admin"><p className="muted">กำลังโหลด…</p></div>;

  const joinUrl = location.origin + "/";
  const last = MEMBER_BY_ID[drawn[drawn.length - 1]];
  const drawnSet = new Set(drawn);

  const run = async (fn) => {
    setBusy(true);
    try {
      await fn();
    } finally {
      setTimeout(() => setBusy(false), 1200);
    }
  };

  const rows = [
    ...result.winners.map((p) => ({ ...p, state: "win" })),
    ...result.ready.filter((p) => !p.bingo).map((p) => ({ ...p, state: "ready" })),
    ...result.pending.map((p) => ({ ...p, state: "pending" })),
  ];

  return (
    <div className="admin">
      <header className="adm-head">
        <h1>ทีมงาน · BINGO Plus! EXACT 8</h1>
        <nav>
          <a href="/screen" target="_blank" rel="noreferrer">เปิดจอใหญ่ ↗</a>
          <a href="/" target="_blank" rel="noreferrer">หน้าผู้เล่น ↗</a>
          <a href="/songs/list" target="_blank" rel="noreferrer">🎃 คำขอเพลง ↗</a>
        </nav>
      </header>

      <section className="adm-draw">
        <div className="adm-current">
          <small>ชื่อล่าสุด ({drawn.length}/{TOTAL})</small>
          <div className="adm-name">{last ? last.name : "--"}</div>
          <div>{last ? `กลุ่ม${last.group}` : "ยังไม่เริ่มสุ่ม"}</div>
        </div>
        <div className="adm-buttons">
          <button className="btn primary big" disabled={busy || drawn.length >= TOTAL} onClick={() => run(drawNext)}>
            🎲 สุ่มชื่อ
          </button>
          <button className="btn ghost" disabled={busy || drawn.length === 0} onClick={() => confirm(`ยกเลิกชื่อล่าสุด (${last?.name})?`) && run(undoLastDraw)}>
            ↶ ยกเลิกชื่อล่าสุด
          </button>
        </div>
      </section>

      <section className="adm-grid">
        <div className="adm-panel">
          <h2>ผู้เล่น <small>พร้อม {result.ready.length} · กำลังเลือก {result.pending.length} · BINGO {result.winners.length} · อีก 1 ชื่อ {result.reach.length}</small></h2>
          <table className="adm-table">
            <thead>
              <tr><th>ชื่อ</th><th>สถานะ</th><th></th></tr>
            </thead>
            <tbody>
              {rows.map((p) => (
                <tr key={p.pid} className={p.state}>
                  <td>
                    <button className="link" onClick={() => setOpen(open === p.pid ? null : p.pid)}>{p.name || "(ไม่มีชื่อ)"}</button>
                    {open === p.pid && p.card && <MiniCard card={toCard(p.card)} drawnSet={drawnSet} />}
                  </td>
                  <td>
                    {p.state === "win" && <span className="badge win">BINGO! (ชื่อที่ {p.bingoAt})</span>}
                    {p.state === "ready" && p.needIds.length > 0 && <span className="badge reach">อีก 1: {p.needIds.map((id) => MEMBER_BY_ID[id].name).join(" / ")}</span>}
                    {p.state === "ready" && p.needIds.length === 0 && <span className="muted">พร้อม</span>}
                    {p.state === "pending" && <span className="muted">กำลังเลือก {toCard(p.card).filter(Boolean).length}/25</span>}
                  </td>
                  <td>
                    <button className="link danger" onClick={() => confirm(`ลบผู้เล่น ${p.name}?`) && removePlayer(p.pid)}>ลบ</button>
                  </td>
                </tr>
              ))}
              {rows.length === 0 && <tr><td colSpan={3} className="muted">ยังไม่มีผู้เล่น</td></tr>}
            </tbody>
          </table>
        </div>

        <div className="adm-panel">
          <h2>ลิงก์สำหรับผู้เล่น</h2>
          <div className="adm-qr">
            <Qr url={joinUrl} size={160} />
            <code>{joinUrl}</code>
          </div>

          <h2>ตั้งค่าเกม</h2>
          <label className="toggle">
            <input type="checkbox" checked={game.accepting} onChange={(e) => setAccepting(e.target.checked)} />
            เปิดรับการ์ดผู้เล่นใหม่
          </label>
          <div className="adm-reset">
            <button className="btn ghost" onClick={() => confirm("ล้างชื่อที่สุ่มแล้วทั้งหมด แต่เก็บการ์ดผู้เล่นไว้เล่นรอบใหม่?") && resetDraws(players)}>
              เล่นรอบใหม่ (ใช้การ์ดเดิม)
            </button>
            <button className="btn danger" onClick={() => confirm("ล้างทุกอย่าง? ผู้เล่นทุกคนต้องใส่ชื่อและเลือกการ์ดใหม่") && resetAll(game)}>
              ล้างทั้งหมด
            </button>
          </div>
        </div>
      </section>

      <section className="adm-panel">
        <h2>ชื่อที่สุ่มแล้ว</h2>
        <div className="adm-board">
          {GROUPS.map((g) => (
            <div key={g}>
              <h4>{g}</h4>
              {membersOf(g).map((m) => (
                <span key={m.id} className={drawnSet.has(m.id) ? "on" : ""}>{m.name}</span>
              ))}
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

function MiniCard({ card, drawnSet }) {
  return (
    <div className="mini-card">
      {card.map((id, i) => (
        <span key={i} className={drawnSet.has(id) ? "on" : ""}>{MEMBER_BY_ID[id]?.name || "—"}</span>
      ))}
    </div>
  );
}
