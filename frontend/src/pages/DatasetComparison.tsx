import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import { motion } from 'framer-motion';
import { Layers, Upload } from 'lucide-react';

interface ComparisonProps {
  onNavigate: (tab: string) => void;
}

export const DatasetComparison: React.FC<ComparisonProps> = ({ onNavigate }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchComparison();
  }, []);

  const fetchComparison = async () => {
    try {
      setLoading(true);
      const res = await axios.get('/api/dataset/compare');
      setData(res.data);
    } catch (err) {
      setData({ can_compare: false, message: "Upload at least 2 datasets to compare." });
    } finally {
      setLoading(false);
    }
  };

  const plotlyLayout: any = {
    font: { family: 'Inter, sans-serif', color: '#FFFFFF' },
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    margin: { l: 40, r: 20, t: 40, b: 40 },
    xaxis: { gridcolor: 'rgba(255,255,255,0.05)' },
    yaxis: { gridcolor: 'rgba(255,255,255,0.05)' },
  };

  if (loading) return <div className="p-8 text-center text-slate-400">Loading Multi-Dataset Comparison...</div>;

  if (!data?.can_compare) {
    return (
      <div className="p-8 max-w-xl mx-auto text-center space-y-4">
        <div className="glass-card p-8 border-purple-500/20">
          <Layers className="w-12 h-12 text-purple-400 mx-auto mb-4" />
          <h3 className="text-xl font-bold text-white mb-2">Multi-Dataset Comparison Engine</h3>
          <p className="text-slate-400 text-sm mb-6">
            Upload at least 2 different CSV/TXT datasets to compare sentiment ratios, review volumes, and trend insights side-by-side.
          </p>
          <button
            onClick={() => onNavigate('upload')}
            className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-sm transition-all"
          >
            <Upload className="w-4 h-4" />
            <span>Upload Another Dataset</span>
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-8 border-purple-500/20">
        <div className="flex items-center gap-3 mb-2">
          <Layers className="w-6 h-6 text-purple-400" />
          <h2 className="text-2xl font-bold text-white">Multi-Dataset Comparison Dashboard</h2>
        </div>
        <p className="text-slate-400 text-sm">
          Comparing {data.datasets.length} active uploaded datasets side-by-side:
        </p>
      </motion.div>

      {/* Comparison Grouped Bar Chart */}
      <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-6">
        <h3 className="text-xl font-bold text-white mb-4">Sentiment Breakdown Comparison (%)</h3>
        <Plot
          data={[
            {
              x: data.datasets.map((d: any) => d.dataset_name),
              y: data.datasets.map((d: any) => d.positive_pct),
              name: 'Positive %',
              type: 'bar',
              marker: { color: '#22C55E' }
            },
            {
              x: data.datasets.map((d: any) => d.dataset_name),
              y: data.datasets.map((d: any) => d.neutral_pct),
              name: 'Neutral %',
              type: 'bar',
              marker: { color: '#FACC15' }
            },
            {
              x: data.datasets.map((d: any) => d.dataset_name),
              y: data.datasets.map((d: any) => d.negative_pct),
              name: 'Negative %',
              type: 'bar',
              marker: { color: '#EF4444' }
            }
          ]}
          layout={{ ...plotlyLayout, barmode: 'group', height: 380 }}
          useResizeHandler
          className="w-full"
        />
      </motion.div>

      {/* Comparison Table */}
      <div className="glass-card p-8 overflow-x-auto">
        <h3 className="text-xl font-bold text-white mb-4">Dataset Comparison Matrix</h3>
        <table className="w-full text-left text-sm text-slate-300 border-collapse">
          <thead>
            <tr className="border-b border-white/10 text-xs font-bold text-purple-400 uppercase">
              <th className="p-3">Dataset Name</th>
              <th className="p-3">Total Records</th>
              <th className="p-3">Positive Share</th>
              <th className="p-3">Negative Share</th>
              <th className="p-3">Avg Text Length</th>
            </tr>
          </thead>
          <tbody>
            {data.datasets.map((d: any, i: number) => (
              <tr key={i} className="border-b border-white/5 hover:bg-slate-800/40">
                <td className="p-3 font-semibold text-white">{d.dataset_name}</td>
                <td className="p-3">{d.total_records.toLocaleString()}</td>
                <td className="p-3 text-emerald-400 font-bold">{d.positive_pct}%</td>
                <td className="p-3 text-red-400 font-bold">{d.negative_pct}%</td>
                <td className="p-3 text-cyan-400">{d.avg_text_length} chars</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
