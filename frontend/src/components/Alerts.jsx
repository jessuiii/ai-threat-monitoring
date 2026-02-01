import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { AlertTriangle, ShieldCheck } from "lucide-react";
import { Card, CardHeader } from "./ui/Card";

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
    <Card className="h-full border-red-500/20 shadow-[0_0_20px_rgba(239,68,68,0.1)]">
      <CardHeader
        title="Active Threats"
        subtitle="Real-time detected anomalies"
        className="mb-4"
      />

      <div className="space-y-3">
        <AnimatePresence mode="popLayout">
          {alerts.length === 0 ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex flex-col items-center justify-center py-8 text-gray-500 gap-2"
            >
              <ShieldCheck className="w-8 h-8 text-green-500/50" />
              <p className="text-sm">No active threats detected</p>
            </motion.div>
          ) : (
            alerts.map((a, i) => (
              <motion.div
                key={`${a.src_ip}-${i}`}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 flex items-center gap-3"
              >
                <div className="p-2 rounded-full bg-red-500/20 text-red-400">
                  <AlertTriangle className="w-4 h-4" />
                </div>
                <div>
                  <h4 className="text-white text-sm font-semibold">{a.attack_type}</h4>
                  <p className="text-xs text-red-300 font-mono">{a.src_ip}</p>
                </div>
              </motion.div>
            ))
          )}
        </AnimatePresence>
      </div>
    </Card>
  );
}
