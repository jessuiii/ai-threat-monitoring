import { useEffect, useState } from "react";
import { Card, CardHeader } from "./ui/Card";
import { Copy, CheckCircle2 } from "lucide-react";

const BACKEND_URL = "http://localhost:8000/events";

export default function LiveTable() {
  const [events, setEvents] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${BACKEND_URL}?t=${Date.now()}`);
        if (!res.ok) throw new Error("Backend not reachable");

        const data = await res.json();
        console.log("🔥 LiveTable Fetched:", data.length, "events", data[0]); // DEBUG
        setEvents(data);
        setError(null);
      } catch (err) {
        setError(err.message);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <Card>
      <div className="flex items-center justify-between mb-6">
        <CardHeader
          title="Live Network Events"
          subtitle="Raw packet stream analysis"
          className="mb-0"
        />
        {error && (
          <span className="text-red-400 text-xs bg-red-500/10 px-2 py-1 rounded border border-red-500/20">
            {error}
          </span>
        )}
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left">
          <thead className="text-xs text-gray-400 uppercase bg-white/5">
            <tr>
              <th className="px-4 py-3 rounded-tl-lg">Source IP</th>
              <th className="px-4 py-3">Rate</th>
              <th className="px-4 py-3">Packets</th>
              <th className="px-4 py-3">Bytes</th>
              <th className="px-4 py-3">Service</th>
              <th className="px-4 py-3">Attack Type</th>
              <th className="px-4 py-3">Confidence</th>
              <th className="px-4 py-3 rounded-tr-lg">Quantum Risk</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {events.length === 0 && (
              <tr>
                <td colSpan="7" className="px-4 py-8 text-center text-gray-500">
                  Waiting for traffic stream...
                </td>
              </tr>
            )}

            {events.map((e, idx) => (
              <tr
                key={idx}
                className="hover:bg-white/5 transition-colors group"
              >
                <td className="px-4 py-3 font-mono text-cyan-300">{e.src_ip}</td>
                <td className="px-4 py-3 text-gray-300">{Number(e.rate ?? 0).toFixed(2)}</td>
                <td className="px-4 py-3 text-gray-300">{e.spkts}</td>
                <td className="px-4 py-3 text-gray-300">{e.sbytes}</td>
                <td className="px-4 py-3 font-mono text-cyan-200/70">{e.service || "-"}</td>
                <td className="px-4 py-3">
                  <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${e.attack_type === 'Normal'
                    ? 'bg-green-500/10 text-green-400 border border-green-500/20'
                    : 'bg-red-500/10 text-red-400 border border-red-500/20'
                    }`}>
                    {e.attack_type}
                  </span>
                </td>
                <td className="px-4 py-3 text-gray-300">
                  <div className="w-full bg-white/10 rounded-full h-1.5 max-w-[80px]">
                    <div
                      className="bg-cyan-500 h-1.5 rounded-full"
                      style={{ width: `${(e.confidence ?? 0) * 100}%` }}
                    />
                  </div>
                </td>
                <td className="px-4 py-3">
                  <span className={`text-xs ${(e.threat_distance ?? 0) > 0.5 ? 'text-red-400' : 'text-gray-400'
                    }`}>
                    {(e.threat_distance ?? 0).toFixed(3)}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}
