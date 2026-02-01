import { useEffect, useState } from "react";
import { Activity, ShieldAlert, Zap, Server } from 'lucide-react';
import StatCard from '../components/StatCard';
import Alerts from '../components/Alerts';
import LiveTable from '../components/LiveTable';

const BACKEND_URL = "http://localhost:8000/events";

export default function Dashboard() {
  const [data, setData] = useState([]);
  const [stats, setStats] = useState({
    totalPackets: 0,
    threatCount: 0,
    avgRate: 0,
  });

  useEffect(() => {
    const Interval = setInterval(async () => {
      try {
        const res = await fetch(BACKEND_URL);
        if (!res.ok) return;
        const events = await res.json();

        setData(events);

        // Update Stats
        const threats = events.filter(e => e.attack_type !== 'Normal');
        setStats({
          totalPackets: events.reduce((acc, curr) => acc + (curr.spkts || 0), 0),
          threatCount: threats.length,
          avgRate: events.length > 0
            ? (events.reduce((acc, curr) => acc + (curr.rate || 0), 0) / events.length).toFixed(2)
            : 0
        });

      } catch (err) {
        console.error("Fetch error:", err);
      }
    }, 2000);

    return () => clearInterval(Interval);
  }, []);

  return (
    <div className="space-y-6">
      {/* Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <StatCard
          title="Active Threats"
          value={stats.threatCount}
          icon={ShieldAlert}
          trend={stats.threatCount > 0 ? 'up' : 'down'}
        />
        <StatCard
          title="Total Packets"
          value={stats.totalPackets.toLocaleString()}
          icon={Server}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Alerts Section - Spanning 1 column */}
        <div className="lg:col-span-1">
          <Alerts />
        </div>

        {/* Live Table Section - Spanning 2 columns to fill the row alongside Alerts */}
        <div className="lg:col-span-2">
          <LiveTable />
        </div>
      </div>
    </div>
  );
}
