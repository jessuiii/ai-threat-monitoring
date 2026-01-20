export default function Alerts() {
  return (
    <div className="bg-red-50 border border-red-300 rounded p-4">
      <h2 className="text-lg font-semibold text-red-700">
        Threat Alerts
      </h2>

      <p className="text-sm text-red-600">
        Alerts will appear here when the threat distance
        drops below the defined threshold.
      </p>
    </div>
  );
}
