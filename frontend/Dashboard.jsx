import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Section({ title, children }) {
  return (
    <div className="bg-white rounded shadow p-4 mb-4">
      <h2 className="text-xl font-bold mb-2">{title}</h2>
      {children}
    </div>
  );
}

export default function Dashboard({ token, user, onLogout }) {
  const [logs, setLogs] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [selectedLog, setSelectedLog] = useState(null);
  const [explanation, setExplanation] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:8000/dashboard/logs', { headers: { Authorization: `Bearer ${token}` } })
      .then(res => setLogs(res.data));
    axios.get('http://localhost:8000/dashboard/alerts', { headers: { Authorization: `Bearer ${token}` } })
      .then(res => setAlerts(res.data));
  }, [token]);

  const handleSelectLog = (log) => {
    setSelectedLog(log);
    setExplanation(null);
    axios.get(`http://localhost:8000/dashboard/explanations/${log.id}`, { headers: { Authorization: `Bearer ${token}` } })
      .then(res => setExplanation(res.data));
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold text-blue-700">Threat Monitoring Dashboard</h1>
        <div>
          <span className="mr-4">{user.sub} ({user.role})</span>
          <button className="bg-red-500 text-white px-3 py-1 rounded" onClick={onLogout}>Logout</button>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Section title="Recent Alerts">
          <ul>
            {alerts.map(a => (
              <li key={a.id} className="mb-2">
                <span className={`font-bold ${a.severity === 'High' ? 'text-red-600' : a.severity === 'Medium' ? 'text-yellow-600' : 'text-green-600'}`}>{a.severity}</span>
                : {a.message} <span className="text-xs text-gray-500">({new Date(a.created_at).toLocaleString()})</span>
              </li>
            ))}
          </ul>
        </Section>
        <Section title="Recent Logs">
          <ul>
            {logs.map(l => (
              <li key={l.id} className="mb-2 cursor-pointer hover:underline" onClick={() => handleSelectLog(l)}>
                Log #{l.id} ({l.source}) <span className="text-xs text-gray-500">{new Date(l.timestamp).toLocaleString()}</span>
              </li>
            ))}
          </ul>
        </Section>
      </div>
      {selectedLog && (
        <Section title={`Log #${selectedLog.id} Explanation`}>
          {explanation ? (
            <div>
              <div>Prediction: <b>{explanation.predicted_label}</b> (Confidence: {(explanation.confidence * 100).toFixed(1)}%)</div>
              <div className="mt-2">
                <b>Feature Importances:</b>
                <ul className="list-disc ml-6">
                  {explanation.explanation && Object.entries(explanation.explanation).map(([k, v]) => (
                    <li key={k}>{k}: {v.toFixed(3)}</li>
                  ))}
                </ul>
              </div>
            </div>
          ) : <div>Loading explanation...</div>}
        </Section>
      )}
    </div>
  );
}
