import Player from "./Player.jsx";
import Screen from "./Screen.jsx";
import Admin from "./Admin.jsx";
import SongRequest, { SongBoard } from "./Songs.jsx";
import { isLocalMode } from "./store.js";
import { useConnected } from "./api.js";

export default function App() {
  const path = location.pathname.replace(/\/+$/, "");
  const connected = useConnected();
  const PAGES = { "/screen": Screen, "/admin": Admin, "/songs": SongRequest, "/songs/list": SongBoard };
  const Page = PAGES[path] || Player;
  return (
    <>
      {isLocalMode && <div className="mode-banner">โหมดทดสอบ: ยังไม่ได้เชื่อม Firebase (ข้อมูลอยู่ในเบราว์เซอร์นี้เท่านั้น)</div>}
      {!connected && <div className="mode-banner warn">กำลังเชื่อมต่ออินเทอร์เน็ต…</div>}
      <Page />
    </>
  );
}
