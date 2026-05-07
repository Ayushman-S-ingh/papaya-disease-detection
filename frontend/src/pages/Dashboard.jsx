// src/pages/Dashboard.jsx
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { predictionService } from "../services/predictionService";
import Navbar from "../components/common/Navbar";

export default function Dashboard() {
  const { user } = useAuth();
  const [summary, setSummary] = useState(null);
  const [recent,  setRecent]  = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      predictionService.getSummary(),
      predictionService.getHistory({ per_page: 5 }),
    ])
      .then(([sumData, histData]) => {
        setSummary(sumData);
        setRecent(histData.predictions || []);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const sev_emoji = { none: "✅", low: "🟡", medium: "🟠", high: "🔴", critical: "🚨" };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-6xl mx-auto px-4 py-8">
        {/* Welcome */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Welcome back, {user?.name?.split(" ")[0]} 👋</h1>
            <p className="text-gray-500 mt-1">Here's your farm health summary</p>
          </div>
          <Link to="/predict"
            className="px-6 py-3 bg-green-600 text-white rounded-xl font-semibold hover:bg-green-700 transition flex items-center gap-2">
            🔍 New Scan
          </Link>
        </div>

        {/* Stats cards */}
        {loading ? (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="bg-white rounded-2xl p-5 shadow-sm animate-pulse h-24" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <StatCard icon="🌿" label="Total Scans"      value={summary?.total_predictions || 0} color="green" />
            <StatCard icon="🎯" label="Avg Confidence"   value={`${summary?.avg_confidence || 0}%`} color="blue" />
            <StatCard icon="🦠" label="Diseases Found"
              value={Object.keys(summary?.disease_distribution || {}).filter(k => k !== "Healthy Leaf").length}
              color="orange" />
            <StatCard icon="✅" label="Healthy Scans"
              value={summary?.disease_distribution?.["Healthy Leaf"] || 0}
              color="purple" />
          </div>
        )}

        {/* Quick actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <QuickAction to="/predict"   icon="📸" title="Scan Leaf"        desc="Upload or photograph a leaf" color="green" />
          <QuickAction to="/history"   icon="📋" title="View History"     desc="Browse all your scans" color="blue" />
          <QuickAction to="/analytics" icon="📊" title="Disease Analytics" desc="Charts and trends" color="purple" />
        </div>

        {/* Recent predictions */}
        <div className="bg-white rounded-2xl shadow-sm">
          <div className="p-6 border-b border-gray-100 flex items-center justify-between">
            <h2 className="font-bold text-gray-900 text-lg">Recent Predictions</h2>
            <Link to="/history" className="text-green-600 text-sm hover:underline">View all →</Link>
          </div>
          <div className="divide-y divide-gray-50">
            {recent.length === 0 ? (
              <div className="p-8 text-center text-gray-400">
                No scans yet. <Link to="/predict" className="text-green-600 hover:underline">Upload your first leaf image</Link>
              </div>
            ) : recent.map(p => (
              <div key={p.id} className="p-5 flex items-center gap-4 hover:bg-gray-50 transition">
                <span className="text-2xl">{sev_emoji[p.severity] || "🌿"}</span>
                <div className="flex-1 min-w-0">
                  <p className="font-semibold text-gray-900 truncate">{p.disease_name}</p>
                  <p className="text-sm text-gray-400">{new Date(p.created_at).toLocaleDateString()}</p>
                </div>
                <div className="text-right">
                  <p className="font-bold text-gray-900">{p.confidence}%</p>
                  <p className="text-xs text-gray-400">confidence</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}

function StatCard({ icon, label, value, color }) {
  const colors = {
    green:  "bg-green-50 text-green-700",
    blue:   "bg-blue-50 text-blue-700",
    orange: "bg-orange-50 text-orange-700",
    purple: "bg-purple-50 text-purple-700",
  };
  return (
    <div className="bg-white rounded-2xl p-5 shadow-sm">
      <div className={`w-10 h-10 rounded-xl flex items-center justify-center text-xl mb-3 ${colors[color]}`}>{icon}</div>
      <p className="text-2xl font-bold text-gray-900">{value}</p>
      <p className="text-sm text-gray-500 mt-1">{label}</p>
    </div>
  );
}

function QuickAction({ to, icon, title, desc, color }) {
  const borders = { green: "border-green-200 hover:border-green-400", blue: "border-blue-200 hover:border-blue-400", purple: "border-purple-200 hover:border-purple-400" };
  return (
    <Link to={to} className={`bg-white rounded-2xl p-5 shadow-sm border-2 border-transparent ${borders[color]} transition group`}>
      <div className="text-3xl mb-2">{icon}</div>
      <p className="font-bold text-gray-900">{title}</p>
      <p className="text-sm text-gray-500 mt-1">{desc}</p>
    </Link>
  );
}