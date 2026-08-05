import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import { motion } from 'framer-motion';
import { Smile, Frown, Meh, Percent } from 'lucide-react';

interface SentimentProps {
  onNavigate: (tab: string) => void;
}

export const SentimentDashboard: React.FC<SentimentProps> = ({ onNavigate }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchSentimentData();
  }, []);

  const fetchSentimentData = async () => {
    try {
      setLoading(true);
      const res = await axios.get('/api/analytics/sentiment');
      setData(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'No dataset loaded.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-8 text-center text-slate-400">Loading Sentiment Analytics...</div>;
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

  const plotlyLayout: any = {
    font: { family: 'Inter, sans-serif', color: '#FFFFFF' },
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    margin: { l: 40, r: 20, t: 40, b: 40 },
    xaxis: { gridcolor: 'rgba(255,255,255,0.05)' },
    yaxis: { gridcolor: 'rgba(255,255,255,0.05)' },
  };

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="glass-card p-6 border-l-4 border-l-purple-500">
          <div className="flex items-center gap-2 text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">
            <Percent className="w-4 h-4 text-purple-400" />
            <span>Total Evaluated</span>
          </div>
          <p className="text-3xl font-black text-white">{data.total_reviews?.toLocaleString()}</p>
          <span className="text-xs text-purple-400">Review entries</span>
        </div>

        <div className="glass-card p-6 border-l-4 border-l-emerald-500">
          <div className="flex items-center gap-2 text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">
            <Smile className="w-4 h-4 text-emerald-400" />
            <span>Positive Share</span>
          </div>
          <p className="text-3xl font-black text-white">{data.positive_pct}%</p>
          <span className="text-xs text-emerald-400">{data.positive?.toLocaleString()} positive</span>
        </div>

        <div className="glass-card p-6 border-l-4 border-l-amber-500">
          <div className="flex items-center gap-2 text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">
            <Meh className="w-4 h-4 text-amber-400" />
            <span>Neutral Share</span>
          </div>
          <p className="text-3xl font-black text-white">{data.neutral_pct}%</p>
          <span className="text-xs text-amber-400">{data.neutral?.toLocaleString()} neutral</span>
        </div>

        <div className="glass-card p-6 border-l-4 border-l-red-500">
          <div className="flex items-center gap-2 text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">
            <Frown className="w-4 h-4 text-red-400" />
            <span>Negative Share</span>
          </div>
          <p className="text-3xl font-black text-white">{data.negative_pct}%</p>
          <span className="text-xs text-red-400">{data.negative?.toLocaleString()} negative</span>
        </div>
      </div>

      {/* Sentiment Charts Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Donut Chart */}
        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-6">
          <h3 className="text-xl font-bold text-white mb-4">Sentiment Breakdown (Pie Chart)</h3>
          <Plot
            data={[
              {
                labels: ['Positive', 'Neutral', 'Negative'],
                values: [data.positive, data.neutral, data.negative],
                type: 'pie',
                hole: 0.4,
                marker: { colors: ['#22C55E', '#FACC15', '#EF4444'] }
              }
            ]}
            layout={{ ...plotlyLayout, title: 'Customer Sentiment Ratio', height: 350 }}
            useResizeHandler
            className="w-full"
          />
        </motion.div>

        {/* Bar Chart */}
        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="glass-card p-6">
          <h3 className="text-xl font-bold text-white mb-4">Sentiment Distribution Counts</h3>
          <Plot
            data={[
              {
                x: ['Positive', 'Neutral', 'Negative'],
                y: [data.positive, data.neutral, data.negative],
                type: 'bar',
                marker: { color: ['#22C55E', '#FACC15', '#EF4444'] }
              }
            ]}
            layout={{ ...plotlyLayout, title: 'Sentiment Entry Volume', height: 350 }}
            useResizeHandler
            className="w-full"
          />
        </motion.div>
      </div>
    </div>
  );
};
