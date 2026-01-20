import { useEffect, useState } from "react";

const BACKEND_URL = "http://localhost:8000/events";

export default function Alerts() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch(BACKEND_URL);
        if (!res.ok) return;

        const data = await res.json();

        // 🔥 ONLY non‑normal attacks
        const activeThreats = data.filter(
          e => e.attack_type && e.attack_type.toLowerCase() !== "normal"
        );

        // Keep only latest unique IPs
        const uniqueByIP = Object.values(
          activeThreats.reduce((acc, e) => {
            acc[e.src_ip] = e;
            return acc;
          }, {})
        );

        setAlerts(uniqueByIP.slice(0, 5));
      } catch {
        // silent fail
      }
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-red-50 border border-red-300 rounded p-4">
      <h2 className="text-lg font-semibold text-red-700">
        Active Threat Alerts
      </h2>

      {alerts.length === 0 && (
        <p className="text-sm text-red-600">
          No active threats
        </p>
      )}

      {alerts.map((a, i) => (
        <div
          key={i}
          className="text-sm text-red-800 mt-2 font-semibold"
        >
          🚨 {a.src_ip}
        </div>
      ))}
    </div>
  );
}
