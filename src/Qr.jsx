import { useEffect, useState } from "react";
import QRCode from "qrcode";

export default function Qr({ url, size = 240 }) {
  const [src, setSrc] = useState(null);
  useEffect(() => {
    QRCode.toDataURL(url, { margin: 1, width: size * 2, color: { dark: "#0f172a", light: "#ffffff" } }).then(setSrc);
  }, [url, size]);
  return (
    <div className="qr" style={{ width: size, height: size }}>
      {src && <img src={src} alt={`QR code: ${url}`} width={size} height={size} />}
    </div>
  );
}
