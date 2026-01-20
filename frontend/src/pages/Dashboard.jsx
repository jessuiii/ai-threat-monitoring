import LiveTable from "../components/LiveTable";
import Alerts from "../components/Alerts";

export default function Dashboard() {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">
        AI Threat Monitoring Dashboard
      </h1>

      <Alerts />
      <LiveTable />
    </div>
  );
}
