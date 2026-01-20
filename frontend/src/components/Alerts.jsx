import { useEffect, useState } from "react";

export default function Alerts() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const interval = setInterval(async () => {
      const res = await fetch("http://localhost:8000/events");
      const data = await res.json();

      const high = data.filter(
        e => e.prediction.includes("🚨") || e.threat_distance > 0.4
      );

      setAlerts(high.slice(0, 5));
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-red-50 border border-red-300 rounded p-4">
      <h2 className="text-lg font-semibold text-red-700">
        Active Threat Alerts
      </h2>

      {alerts.length === 0 && (
        <p className="text-sm text-red-600">No active threats</p>
      )}

      {alerts.map((a, i) => (
        <div key={i} className="text-sm text-red-800 mt-1">
          🚨 {a.src_ip} | Risk: {a.confidence.toFixed(2)}
        </div>
      ))}
    </div>
  );
}
