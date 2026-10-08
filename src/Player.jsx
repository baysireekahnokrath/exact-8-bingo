import { useEffect, useMemo, useState } from "react";
import { GROUPS, MEMBER_BY_ID, membersOf, TOTAL } from "./members.js";
import { LINES, SIZE, lineStatus, toCard } from "./bingo.js";
import {
  getPlayerId,
  lockCard,
  registerPlayer,
  renamePlayer,
  saveCard,
  setMark,
  useDelayedDrawn,
  useGame,
  useValue,
} from "./api.js";

const pid = getPlayerId();
const REVEAL_DELAY = 1500; // รอให้จอใหญ่หมุนลุ้นเสร็จก่อนค่อยโชว์บนมือถือ

export default function Player() {
  const me = useValue(`players/${pid}`);
  const game = useGame();

  if (me === undefined || game === undefined) return <Shell><p className="muted center">กำลังโหลด…</p></Shell>;
  if (!me || !me.name) return <Shell><NameEntry /></Shell>;
  if (!me.locked) {
    if (!game.accepting)
      return (
        <Shell>
          <div className="notice">
            <h2>ปิดรับการ์ดแล้ว</h2>
            <p>ทีมงานปิดรับการ์ดสำหรับรอบนี้แล้ว รอเล่นรอบหน้านะครับ</p>
          </div>
        </Shell>
      );
    return <Shell><CardBuilder me={me} /></Shell>;
  }
  return <Shell><GameCard me={me} game={game} /></Shell>;
}

function Shell({ children }) {
  return <div className="player">{children}</div>;
}

function CardTitle({ name, onRename }) {
  return (
    <div className="card-title">
      <h1>BINGO Plus! - EXACT 8</h1>
      <div className="card-player">
        ชื่อผู้เล่น: <b>{name}</b>
        {onRename && (
          <button className="link" onClick={onRename}>แก้ไข</button>
        )}
      </div>
    </div>
  );
}

// ---------- 1) ใส่ชื่อ ----------
function NameEntry() {
  const [name, setName] = useState("");
  const [busy, setBusy] = useState(false);
  const submit = async (e) => {
    e.preventDefault();
    const n = name.trim();
    if (!n) return;
    setBusy(true);
    await registerPlayer(pid, n);
  };
  return (
    <form className="entry" onSubmit={submit}>
      <div className="entry-logo">BINGO<br /><span>Plus!</span></div>
      <div className="entry-sub">EXACT 8</div>
      <label htmlFor="name">ใส่ชื่อของคุณ</label>
      <input
        id="name"
        value={name}
        maxLength={30}
        autoComplete="off"
        placeholder="เช่น พี่เอก"
        onChange={(e) => setName(e.target.value)}
      />
      <button className="btn primary" disabled={!name.trim() || busy}>เข้าเล่น</button>
    </form>
  );
}

// ---------- 2) เลือกชื่อลงตาราง ----------
function CardBuilder({ me }) {
  const card = useMemo(() => toCard(me.card), [me.card]);
  const [picking, setPicking] = useState(null); // cell index
  const [confirming, setConfirming] = useState(false);
  const filled = card.filter(Boolean).length;

  const put = (cell, id) => {
    const next = [...card];
    next[cell] = id;
    saveCard(pid, next);
  };

  const fillRandom = () => {
    const next = [...card];
    for (let c = 0; c < SIZE; c++) {
      const used = new Set();
      for (let r = 0; r < SIZE; r++) if (next[r * SIZE + c]) used.add(next[r * SIZE + c]);
      const pool = membersOf(GROUPS[c]).filter((m) => !used.has(m.id)).sort(() => Math.random() - 0.5);
      for (let r = 0; r < SIZE; r++) if (!next[r * SIZE + c]) next[r * SIZE + c] = pool.pop().id;
    }
    saveCard(pid, next);
  };

  const rename = () => {
    const n = prompt("แก้ไขชื่อผู้เล่น", me.name);
    if (n && n.trim()) renamePlayer(pid, n.trim().slice(0, 30));
  };

  return (
    <>
      <div className="paper">
        <CardTitle name={me.name} onRename={rename} />
        <p className="hint">แตะช่องว่างเพื่อเลือกชื่อ — คอลัมน์ละ 1 กลุ่ม กลุ่มละ 5 คน</p>
        <Grid
          card={card}
          renderCell={(id, i) => (
            <button className={`cell ${id ? "filled" : "empty"}`} onClick={() => setPicking(i)}>
              {id ? MEMBER_BY_ID[id].name : "+"}
            </button>
          )}
        />
        <p className="footnote">* ใส่ชื่อเพื่อนกลุ่มละ 5 คน / บิงโกแถวตรงหรือแนวทแยงครบ 5 ช่องรับรางวัล *</p>
      </div>

      <div className="builder-actions">
        <button className="btn ghost" onClick={fillRandom} disabled={filled === 25}>🎲 สุ่มเติมช่องที่เหลือ</button>
        <button className="btn ghost" onClick={() => confirm("ล้างการ์ดทั้งหมด?") && saveCard(pid, Array(25).fill(0))} disabled={filled === 0}>ล้าง</button>
      </div>

      <div className="sticky-bar">
        <span className="progress"><b>{filled}</b>/25 ช่อง</span>
        <button className="btn primary" disabled={filled < 25} onClick={() => setConfirming(true)}>
          {filled < 25 ? `ใส่อีก ${25 - filled} ช่อง` : "OK ยืนยันการ์ด"}
        </button>
      </div>

      {picking !== null && (
        <Picker cell={picking} card={card} onPick={(id) => { put(picking, id); setPicking(null); }} onClose={() => setPicking(null)} />
      )}

      {confirming && (
        <Modal onClose={() => setConfirming(false)}>
          <h2>ยืนยันการ์ด?</h2>
          <p>กด OK แล้วจะแก้ไขชื่อในตารางไม่ได้อีก</p>
          <div className="modal-actions">
            <button className="btn ghost" onClick={() => setConfirming(false)}>กลับไปแก้</button>
            <button className="btn primary" onClick={() => lockCard(pid, card)}>OK</button>
          </div>
        </Modal>
      )}
    </>
  );
}

function Picker({ cell, card, onPick, onClose }) {
  const col = cell % SIZE;
  const row = Math.floor(cell / SIZE);
  const group = GROUPS[col];
  const usedInCol = new Set();
  for (let r = 0; r < SIZE; r++) if (r !== row && card[r * SIZE + col]) usedInCol.add(card[r * SIZE + col]);
  return (
    <Modal onClose={onClose} sheet>
      <h2>กลุ่ม{group} <small>แถวที่ {row + 1}</small></h2>
      <div className="pick-list">
        {membersOf(group).map((m) => {
          const used = usedInCol.has(m.id);
          const current = card[cell] === m.id;
          return (
            <button
              key={m.id}
              className={`pick ${current ? "current" : ""}`}
              disabled={used}
              onClick={() => onPick(m.id)}
            >
              {m.name}
              {used && <small>ใช้แล้ว</small>}
            </button>
          );
        })}
      </div>
      <div className="modal-actions">
        {card[cell] ? <button className="btn ghost" onClick={() => onPick(0)}>ลบช่องนี้</button> : <span />}
        <button className="btn ghost" onClick={onClose}>ปิด</button>
      </div>
    </Modal>
  );
}

// ---------- 3) เล่นเกม ----------
function GameCard({ me, game }) {
  const card = useMemo(() => toCard(me.card), [me.card]);
  const drawn = useDelayedDrawn(game, REVEAL_DELAY) || [];
  const drawnSet = useMemo(() => new Set(drawn), [drawn]);
  const marks = me.marks || {};
  const isMarked = (i) => !!marks[`c${i}`];
  const { bingo, needs } = lineStatus(isMarked);
  const bingoCells = new Set(LINES.filter((l) => l.every(isMarked)).flat());
  const [toast, setToast] = useState(null);
  const [showBingo, setShowBingo] = useState(false);
  const [seenBingo, setSeenBingo] = useState(false);
  const [showHistory, setShowHistory] = useState(false);

  useEffect(() => {
    if (bingo && !seenBingo) {
      setShowBingo(true);
      setSeenBingo(true);
      navigator.vibrate?.([200, 100, 200, 100, 400]);
    }
    if (!bingo) setSeenBingo(false);
  }, [bingo, seenBingo]);

  useEffect(() => {
    if (!toast) return;
    const t = setTimeout(() => setToast(null), 1800);
    return () => clearTimeout(t);
  }, [toast]);

  const latestId = drawn[drawn.length - 1];
  const latest = latestId ? MEMBER_BY_ID[latestId] : null;

  const tap = (i) => {
    const id = card[i];
    if (isMarked(i)) return setMark(pid, i, false);
    if (!drawnSet.has(id)) {
      setToast(`${MEMBER_BY_ID[id].name} ยังไม่ถูกเรียกชื่อ`);
      navigator.vibrate?.(60);
      return;
    }
    setMark(pid, i, true);
  };

  return (
    <>
      <div className={`now ${latest ? "" : "waiting"}`} key={latestId || "none"}>
        {latest ? (
          <>
            <div className="now-label">ชื่อล่าสุด (ลำดับที่ {drawn.length}/{TOTAL})</div>
            <div className="now-name">{latest.name}</div>
            <div className="now-group">กลุ่ม{latest.group}</div>
          </>
        ) : (
          <>
            <div className="now-name small">รอทีมงานเริ่มสุ่มชื่อ…</div>
            <div className="now-group">การ์ดของคุณพร้อมแล้ว ✓</div>
          </>
        )}
      </div>

      <div className="paper">
        <CardTitle name={me.name} />
        <Grid
          card={card}
          renderCell={(id, i) => (
            <button
              className={`cell ${isMarked(i) ? "marked" : ""} ${bingoCells.has(i) ? "win" : ""} ${needs.includes(i) ? "need" : ""}`}
              onClick={() => tap(i)}
            >
              <span>{MEMBER_BY_ID[id]?.name}</span>
            </button>
          )}
        />
        <p className="footnote">แตะชื่อที่ถูกเรียกเพื่อทำเครื่องหมาย ได้ 5 ช่องเรียงกันเป็นผู้ชนะ!</p>
      </div>

      <div className="status-line">
        {bingo ? (
          <span className="badge win">🎉 BINGO! แจ้งทีมงานได้เลย</span>
        ) : needs.length > 0 ? (
          <span className="badge reach">🔥 อีก 1 ชื่อ! ลุ้น {[...new Set(needs.map((i) => MEMBER_BY_ID[card[i]].name))].join(" / ")}</span>
        ) : (
          <span className="muted">แตะไปแล้ว {Object.keys(marks).length} ช่อง</span>
        )}
      </div>

      <button className="btn ghost wide" onClick={() => setShowHistory((s) => !s)}>
        {showHistory ? "ซ่อน" : "ดู"}ชื่อที่ถูกเรียกแล้ว ({drawn.length})
      </button>
      {showHistory && (
        <div className="history">
          {[...drawn].reverse().map((id, k) => (
            <span key={id} className={card.includes(id) ? "mine" : ""}>
              <small>{drawn.length - k}.</small> {MEMBER_BY_ID[id].name} <small>({MEMBER_BY_ID[id].group})</small>
            </span>
          ))}
          {drawn.length === 0 && <p className="muted">ยังไม่มี</p>}
        </div>
      )}

      {toast && <div className="toast">{toast}</div>}
      {showBingo && (
        <div className="bingo-overlay" onClick={() => setShowBingo(false)}>
          <div className="bingo-word">BINGO!</div>
          <p>ยินดีด้วย {me.name}! ชื่อของคุณขึ้นจอใหญ่แล้ว</p>
          <small>แตะเพื่อปิด</small>
        </div>
      )}
    </>
  );
}

function Grid({ card, renderCell }) {
  return (
    <div className="grid">
      {GROUPS.map((g) => (
        <div key={g} className="grid-head">{g}</div>
      ))}
      {card.map((id, i) => (
        <div key={i} className="grid-cell">{renderCell(id, i)}</div>
      ))}
    </div>
  );
}

function Modal({ children, onClose, sheet }) {
  return (
    <div className="modal-bg" onClick={onClose}>
      <div className={`modal ${sheet ? "sheet" : ""}`} onClick={(e) => e.stopPropagation()}>
        {children}
      </div>
    </div>
  );
}
