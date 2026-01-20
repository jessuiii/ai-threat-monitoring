import { useEffect, useState } from "react";

const BACKEND_URL = "http://localhost:8000/events";

export default function LiveTable() {
  const [events, setEvents] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch(BACKEND_URL);
        if (!res.ok) throw new Error("Backend not reachable");

        const data = await res.json();
        setEvents(data);
        setError(null);
      } catch (err) {
        setError(err.message);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-white rounded shadow p-4">
      <h2 className="text-lg font-semibold mb-3">
        Live Network Events
      </h2>

      {error && (
        <p className="text-red-600 text-sm mb-2">
          {error}
        </p>
      )}

      <div className="overflow-x-auto">
        <table className="w-full text-sm border">
          <thead className="bg-gray-200">
            <tr>
              <th className="p-2 border">Source IP</th>
              <th className="p-2 border">Rate</th>
              <th className="p-2 border">Packets</th>
              <th className="p-2 border">Bytes</th>
              <th className="p-2 border">Attack Type</th>
              <th className="p-2 border">Confidence</th>
              <th className="p-2 border">Threat Distance</th>
            </tr>
          </thead>

          <tbody>
            {events.length === 0 && (
              <tr>
                <td colSpan="7" className="p-3 text-center">
                  Waiting for traffic…
                </td>
              </tr>
            )}

            {events.map((e, idx) => (
              <tr key={idx} className="odd:bg-gray-50">
                <td className="p-2 border">{e.src_ip}</td>
                <td className="p-2 border">
                  {Number(e.rate ?? 0).toFixed(2)}
                </td>
                <td className="p-2 border">{e.spkts}</td>
                <td className="p-2 border">{e.sbytes}</td>
                <td className="p-2 border font-medium">
                  {e.attack_type}
                </td>
                <td className="p-2 border">
                  {(e.confidence ?? 0).toFixed(3)}
                </td>
                <td className="p-2 border">
                  {(e.threat_distance ?? 0).toFixed(3)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
