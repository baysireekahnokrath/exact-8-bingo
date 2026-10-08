// เสียง effect และเสียงอ่านชื่อภาษาไทย (ยกมาจากโปรแกรมสุ่มเดิม)
let audioCtx = null;
let voices = [];

if ("speechSynthesis" in window) {
  voices = window.speechSynthesis.getVoices();
  window.speechSynthesis.onvoiceschanged = () => {
    voices = window.speechSynthesis.getVoices();
  };
}

export function initAudio() {
  if (!audioCtx) {
    const Ctx = window.AudioContext || window.webkitAudioContext;
    if (!Ctx) return;
    audioCtx = new Ctx();
  }
  if (audioCtx.state === "suspended") audioCtx.resume();
}

export const audioReady = () => !!audioCtx && audioCtx.state === "running";

function tone(type, freq, start, dur, vol, endFreq) {
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.type = type;
  osc.frequency.setValueAtTime(freq, start);
  if (endFreq) osc.frequency.exponentialRampToValueAtTime(endFreq, start + dur);
  gain.gain.setValueAtTime(vol, start);
  gain.gain.exponentialRampToValueAtTime(0.001, start + dur);
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start(start);
  osc.stop(start + dur);
}

export function playTick() {
  if (!audioCtx) return;
  tone("sine", 520, audioCtx.currentTime, 0.04, 0.12, 140);
}

export function playWin() {
  if (!audioCtx) return;
  [523.25, 659.25, 783.99, 1046.5].forEach((f, i) =>
    tone("triangle", f, audioCtx.currentTime + i * 0.07, 0.35, 0.2)
  );
}

export function playFanfare() {
  if (!audioCtx) return;
  const notes = [523.25, 659.25, 783.99, 1046.5, 783.99, 1046.5, 1318.5];
  const times = [0, 0.12, 0.24, 0.36, 0.6, 0.72, 0.9];
  notes.forEach((f, i) => tone("square", f, audioCtx.currentTime + times[i], i === notes.length - 1 ? 0.9 : 0.22, 0.12));
}

// ปรับคำอ่านเฉพาะบางชื่อให้ระบบอ่านถูก
function phonetic(str) {
  const map = {
    "อเส": "อะเส",
    "พี่ป๊อด": "พี่ป้อด",
    "พี่ปัชชี่": "พี่ปัดชี่",
    "พี่พสิษฐ์": "พี่พะสิด",
  };
  return map[str] || str;
}

export function speak(text) {
  if (!("speechSynthesis" in window)) return;
  window.speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = "th-TH";
  u.rate = 0.85;
  u.pitch = 1.12;
  if (voices.length === 0) voices = window.speechSynthesis.getVoices();
  const thai = voices.filter((v) => v.lang.toLowerCase().includes("th"));
  const female =
    thai.find((v) => /female|narisa|premwadee|kanya|siri/i.test(v.name)) || thai[0];
  if (female) u.voice = female;
  window.speechSynthesis.speak(u);
}

export const speakMember = (m) => speak(`${phonetic(m.name)} - ${phonetic(m.group)}`);
