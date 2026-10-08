import { useEffect, useMemo, useRef, useState } from "react";
import { GROUPS, MEMBERS, MEMBER_BY_ID, membersOf, TOTAL } from "./members.js";
import { analyzePlayers } from "./bingo.js";
import { drawNext, useGame, usePlayers } from "./api.js";
import { initAudio, playFanfare, playTick, playWin, speak, speakMember } from "./sound.js";
import Qr from "./Qr.jsx";

const ROLL_TICKS = 18;
const ROLL_MS = 65;

export default function Screen() {
  const game = useGame();
  const players = usePlayers();
  const [shownDrawn, setShownDrawn] = useState(null);
  const [rollId, setRollId] = useState(null);
  const [rolling, setRolling] = useState(false);
  const [busy, setBusy] = useState(false);
  const [sfxOn, setSfxOn] = useState(true);
  const [voiceOn, setVoiceOn] = useState(true);
  const [audioArmed, setAudioArmed] = useState(false);
  const [celebrate, setCelebrate] = useState(null);
  const shownRef = useRef(null);
  shownRef.current = shownDrawn;
  const prefs = useRef({});
  prefs.current = { sfxOn, voiceOn };

  const armAudio = () => {
    initAudio();
    setAudioArmed(true);
  };

  // หมุนลุ้นทุกครั้งที่มีชื่อใหม่ (ไม่ว่าจะกดสุ่มจากเครื่องไหน)
  const key = game ? game.drawn.join(",") : null;
  useEffect(() => {
    if (!game) return;
    const prev = shownRef.current;
    const drawn = game.drawn;
    if (prev === null || drawn.length <= prev.length) {
      setShownDrawn(drawn);
      setRolling(false);
      return;
    }
    const pool = MEMBERS.filter((m) => !prev.includes(m.id));
    const last = drawn[drawn.length - 1];
    let n = 0;
    setRolling(true);
    const iv = setInterval(() => {
      setRollId(pool[Math.floor(Math.random() * pool.length)].id);
      if (prefs.current.sfxOn) playTick();
      if (++n >= ROLL_TICKS) {
        clearInterval(iv);
        setRolling(false);
        setShownDrawn(drawn);
        if (prefs.current.sfxOn) playWin();
        if (prefs.current.voiceOn) setTimeout(() => speakMember(MEMBER_BY_ID[last]), 380);
      }
    }, ROLL_MS);
    return () => clearInterval(iv);
  }, [key]); // eslint-disable-line react-hooks/exhaustive-deps

  const drawn = shownDrawn || [];
  const drawnSet = useMemo(() => new Set(drawn), [drawn]);
  const result = useMemo(() => analyzePlayers(players, drawn), [players, drawn]);

  // ฉลองผู้ชนะใหม่
  const seenWinners = useRef(null);
  useEffect(() => {
    if (shownDrawn === null || players === undefined) return;
    const ids = result.winners.map((w) => w.pid);
    if (seenWinners.current === null) {
      seenWinners.current = new Set(ids);
      return;
    }
    const fresh = result.winners.filter((w) => !seenWinners.current.has(w.pid));
    seenWinners.current = new Set(ids);
    if (fresh.length === 0) return;
    setCelebrate(fresh.map((w) => w.name));
    const delay = prefs.current.voiceOn ? 1800 : 300;
    setTimeout(() => {
      if (prefs.current.sfxOn) playFanfare();
      if (prefs.current.voiceOn) setTimeout(() => speak(`บิงโก! ${fresh.map((w) => w.name).join(" ")}`), 1200);
    }, delay);
  }, [result, shownDrawn, players]);

  useEffect(() => {
    if (!celebrate) return;
    const t = setTimeout(() => setCelebrate(null), 9000);
    return () => clearTimeout(t);
  }, [celebrate]);

  const doDraw = async () => {
    if (busy || rolling || drawn.length >= TOTAL) return;
    armAudio();
    setBusy(true);
    try {
      await drawNext();
    } finally {
      setTimeout(() => setBusy(false), ROLL_TICKS * ROLL_MS + 300);
    }
  };

  useEffect(() => {
    const onKey = (e) => {
      if (e.code === "Space" || e.code === "Enter") {
        e.preventDefault();
        doDraw();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  });

  if (!game || players === undefined) return <div className="screen"><p className="center muted">กำลังโหลด…</p></div>;

  const joinUrl = location.origin + "/";
  const lobby = drawn.length === 0 && !rolling;
  const current = rolling ? MEMBER_BY_ID[rollId] : MEMBER_BY_ID[drawn[drawn.length - 1]];

  return (
    <div className="screen">
      <header className="scr-head">
        <h1>BINGO Plus! <span>EXACT 8</span></h1>
        <div className="scr-stats">
          <span>ผู้เล่นพร้อม <b>{result.ready.length}</b>{result.pending.length > 0 && <> · กำลังเลือก {result.pending.length}</>}</span>
          <span>สุ่มแล้ว <b>{drawn.length}</b>/{TOTAL}</span>
          {!audioArmed && <button className="arm-audio" onClick={armAudio}>🔊 คลิกเพื่อเปิดเสียง</button>}
          <label><input type="checkbox" checked={sfxOn} onChange={(e) => setSfxOn(e.target.checked)} /> เสียง</label>
          <label><input type="checkbox" checked={voiceOn} onChange={(e) => setVoiceOn(e.target.checked)} /> อ่านชื่อ</label>
        </div>
      </header>

      <main className="scr-main">
        <section className="stage">
          {lobby ? (
            <div className="lobby">
              <Qr url={joinUrl} size={340} />
              <div className="lobby-text">
                <h2>สแกนเพื่อเข้าร่วมเกม</h2>
                <p className="url">{joinUrl.replace(/^https?:\/\//, "").replace(/\/$/, "")}</p>
                <ol>
                  <li>ใส่ชื่อของคุณ</li>
                  <li>เลือกชื่อเพื่อนกลุ่มละ 5 คนลงตาราง</li>
                  <li>กด OK แล้วรอลุ้น!</li>
                </ol>
                <div className="joined">
                  {result.ready.map((p) => <span key={p.pid} className="chip ready">{p.name}</span>)}
                  {result.pending.map((p) => <span key={p.pid} className="chip">{p.name}</span>)}
                </div>
              </div>
            </div>
          ) : (
            <div className={`draw-card ${rolling ? "rolling" : "revealed"}`}>
              <div className="group-badge">{current ? `กลุ่ม${current.group}` : ""}</div>
              <div className="big-name" key={rolling ? "r" : drawn.length}>{current?.name || "--"}</div>
              <div className="draw-no">{rolling ? "กำลังสุ่ม…" : `ลำดับที่ ${drawn.length} / ${TOTAL}`}</div>
            </div>
          )}
          <button className="btn draw" onClick={doDraw} disabled={busy || rolling || drawn.length >= TOTAL}>
            {drawn.length >= TOTAL ? "สุ่มครบแล้ว" : lobby ? "เริ่มเกม · สุ่มชื่อแรก" : "สุ่มชื่อถัดไป"} <small>(Space)</small>
          </button>
        </section>

        <aside className="side">
          <div className="panel winners">
            <h3>🏆 BINGO!</h3>
            {result.winners.length === 0 && <p className="muted">ยังไม่มีผู้ชนะ</p>}
            <ol>
              {result.winners.map((w) => (
                <li key={w.pid}><b>{w.name}</b> <small>ชื่อที่ {w.bingoAt}</small></li>
              ))}
            </ol>
          </div>
          <div className="panel reach">
            <h3>🔥 ลุ้น! อีก 1 ชื่อ <span className="count">{result.reach.length}</span></h3>
            {result.reach.length === 0 && <p className="muted">ยังไม่มี</p>}
            <ul>
              {result.reach.map((p) => (
                <li key={p.pid}>
                  <b>{p.name}</b>
                  <span className="needs">รอ {p.needIds.map((id) => MEMBER_BY_ID[id].name).join(" / ")}</span>
                </li>
              ))}
            </ul>
          </div>
          {!lobby && (
            <div className="panel mini-qr">
              <Qr url={joinUrl} size={96} />
              <span>มาช้า? สแกนเข้าร่วมได้</span>
            </div>
          )}
        </aside>
      </main>

      <section className="board">
        {GROUPS.map((g) => (
          <div key={g} className="board-col">
            <h4>{g}</h4>
            <div className="board-names">
              {membersOf(g).map((m) => (
                <span key={m.id} className={drawnSet.has(m.id) ? "on" : ""}>{m.name}</span>
              ))}
            </div>
          </div>
        ))}
      </section>

      {celebrate && (
        <div className="celebrate" onClick={() => setCelebrate(null)}>
          <div className="bingo-word">BINGO!</div>
          <div className="celebrate-names">{celebrate.map((n) => <div key={n}>{n}</div>)}</div>
        </div>
      )}
    </div>
  );
}
