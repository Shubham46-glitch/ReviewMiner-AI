import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { TrendingUp, Download, CheckCircle, AlertOctagon, Lightbulb } from 'lucide-react';

interface BIProps {
  onNavigate: (tab: string) => void;
}

export const BusinessIntelligence: React.FC<BIProps> = ({ onNavigate }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchBIData();
  }, []);

  const fetchBIData = async () => {
    try {
      setLoading(true);
      const res = await axios.get('/api/analytics/business-intelligence');
      setData(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'No dataset loaded.');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = () => {
    window.open('/api/analytics/export-pdf', '_blank');
  };

  if (loading) return <div className="p-8 text-center text-slate-400">Generating Executive BI Report...</div>;
  if (error) {
    return (
      <div className="p-8 max-w-xl mx-auto text-center">
        <div className="glass-card p-8">
          <p className="text-red-400 font-semibold mb-4">{error}</p>
          <button onClick={() => onNavigate('upload')} className="px-6 py-3 rounded-xl bg-purple-600 text-white font-bold text-sm">
            Upload Dataset
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* Header Banner */}
      <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-8 border-purple-500/20 flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <TrendingUp className="w-6 h-6 text-purple-400" />
            <h2 className="text-2xl font-bold text-white">Executive Business Intelligence</h2>
          </div>
          <p className="text-slate-400 text-sm">
            Data-driven strategic insights, customer complaint extraction, and automated operational recommendations.
          </p>
        </div>

        <button
          onClick={handleDownloadPDF}
          className="flex items-center gap-2 px-6 py-3.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-500 hover:from-emerald-500 hover:to-teal-400 text-white font-bold text-sm shadow-lg shadow-emerald-500/20 transition-all"
        >
          <Download className="w-4 h-4" />
          <span>Export Executive PDF Report</span>
        </button>
      </motion.div>

      {/* Satisfaction KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="glass-card p-6 border-l-4 border-l-cyan-500">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Satisfaction Index</span>
          <p className="text-3xl font-black text-cyan-400 mt-1">{data.customer_satisfaction_pct}%</p>
          <span className="text-xs text-slate-400">Weighted score</span>
        </div>

        <div className="glass-card p-6 border-l-4 border-l-emerald-500">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Positive Drivers</span>
          <p className="text-3xl font-black text-emerald-400 mt-1">{data.positive_pct}%</p>
          <span className="text-xs text-slate-400">Happy feedback share</span>
        </div>

        <div className="glass-card p-6 border-l-4 border-l-red-500">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Dissatisfaction Rate</span>
          <p className="text-3xl font-black text-red-400 mt-1">{data.negative_pct}%</p>
          <span className="text-xs text-slate-400">Complaint ratio</span>
        </div>

        <div className="glass-card p-6 border-l-4 border-l-amber-500">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Neutral Ratio</span>
          <p className="text-3xl font-black text-amber-400 mt-1">{data.neutral_pct}%</p>
          <span className="text-xs text-slate-400">Indifferent feedback</span>
        </div>
      </div>

      {/* Positive & Negative Drivers Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="glass-card p-6 border-t-4 border-t-emerald-500">
          <div className="flex items-center gap-2 mb-4">
            <CheckCircle className="w-5 h-5 text-emerald-400" />
            <h3 className="text-lg font-bold text-white">Most Appreciated Customer Features</h3>
          </div>
          <div className="flex flex-wrap gap-2">
            {data.top_positive_features?.map((feat: string, idx: number) => (
              <span key={idx} className="px-3.5 py-1.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 font-semibold text-sm">
                ✨ {feat}
              </span>
            ))}
          </div>
        </div>

        <div className="glass-card p-6 border-t-4 border-t-red-500">
          <div className="flex items-center gap-2 mb-4">
            <AlertOctagon className="w-5 h-5 text-red-400" />
            <h3 className="text-lg font-bold text-white">Top Customer Complaints & Friction Points</h3>
          </div>
          <div className="flex flex-wrap gap-2">
            {data.top_complaints?.map((comp: string, idx: number) => (
              <span key={idx} className="px-3.5 py-1.5 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 font-semibold text-sm">
                ⚠️ {comp}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Automated Recommendations */}
      <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-8">
        <div className="flex items-center gap-2 mb-6">
          <Lightbulb className="w-6 h-6 text-amber-400" />
          <h3 className="text-xl font-bold text-white">Strategic AI Action Recommendations</h3>
        </div>

        <div className="space-y-4">
          {data.recommendations?.map((rec: string, idx: number) => (
            <div key={idx} className="p-4 rounded-xl bg-purple-500/10 border-l-4 border-l-purple-500 border border-purple-500/20 text-slate-200 font-medium text-sm">
              {rec}
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};
