import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import { motion } from 'framer-motion';
import { FileText, AlignLeft, Copy, AlertTriangle } from 'lucide-react';

interface EDAProps {
  onNavigate: (tab: string) => void;
}

export const EDA: React.FC<EDAProps> = ({ onNavigate }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchEDAData();
  }, []);

  const fetchEDAData = async () => {
    try {
      setLoading(true);
      const res = await axios.get('/api/analytics/eda');
      setData(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'No dataset loaded.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-8 text-center text-slate-400">Loading EDA Analytics...</div>;
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
            <FileText className="w-4 h-4 text-purple-400" />
            <span>Total Reviews</span>
          </div>
          <p className="text-3xl font-black text-white">{data.total_reviews?.toLocaleString()}</p>
          <span className="text-xs text-purple-400">Total text records</span>
        </div>

        <div className="glass-card p-6 border-l-4 border-l-cyan-500">
          <div className="flex items-center gap-2 text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">
            <AlignLeft className="w-4 h-4 text-cyan-400" />
            <span>Avg Review Length</span>
          </div>
          <p className="text-3xl font-black text-white">{data.avg_length} chars</p>
          <span className="text-xs text-cyan-400">Average character length</span>
        </div>

        <div className="glass-card p-6 border-l-4 border-l-amber-500">
          <div className="flex items-center gap-2 text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">
            <Copy className="w-4 h-4 text-amber-400" />
            <span>Duplicate Records</span>
          </div>
          <p className="text-3xl font-black text-white">{data.duplicate_count}</p>
          <span className="text-xs text-amber-400">Redundant rows</span>
        </div>

        <div className="glass-card p-6 border-l-4 border-l-emerald-500">
          <div className="flex items-center gap-2 text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">
            <AlertTriangle className="w-4 h-4 text-emerald-400" />
            <span>Missing Values</span>
          </div>
          <p className="text-3xl font-black text-white">{data.missing_count}</p>
          <span className="text-xs text-emerald-400">Incomplete records</span>
        </div>
      </div>

      {/* Review Length Distribution Chart */}
      <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-6">
        <h3 className="text-xl font-bold text-white mb-4">Review Character Length Distribution</h3>
        <Plot
          data={[
            {
              x: data.lengths_distribution,
              type: 'histogram',
              marker: { color: '#7C3AED' },
              name: 'Length'
            }
          ]}
          layout={{ ...plotlyLayout, title: 'Character Count Histogram', height: 320 }}
          useResizeHandler
          className="w-full"
        />
      </motion.div>

      {/* Top Words & N-Grams Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Unigrams */}
        <div className="glass-card p-6">
          <h3 className="text-lg font-bold text-white mb-4">Top 15 Single Words (Unigrams)</h3>
          <Plot
            data={[
              {
                x: data.top_unigrams.map((item: any) => item.frequency),
                y: data.top_unigrams.map((item: any) => item.word),
                type: 'bar',
                orientation: 'h',
                marker: { color: '#06B6D4' }
              }
            ]}
            layout={{ ...plotlyLayout, yaxis: { autorange: 'reversed' }, height: 350 }}
            useResizeHandler
            className="w-full"
          />
        </div>

        {/* Bigrams */}
        <div className="glass-card p-6">
          <h3 className="text-lg font-bold text-white mb-4">Top 15 Bigrams (2-word phrases)</h3>
          <Plot
            data={[
              {
                x: data.top_bigrams.map((item: any) => item.frequency),
                y: data.top_bigrams.map((item: any) => item.word),
                type: 'bar',
                orientation: 'h',
                marker: { color: '#7C3AED' }
              }
            ]}
            layout={{ ...plotlyLayout, yaxis: { autorange: 'reversed' }, height: 350 }}
            useResizeHandler
            className="w-full"
          />
        </div>

        {/* Trigrams */}
        <div className="glass-card p-6">
          <h3 className="text-lg font-bold text-white mb-4">Top 15 Trigrams (3-word phrases)</h3>
          <Plot
            data={[
              {
                x: data.top_trigrams.map((item: any) => item.frequency),
                y: data.top_trigrams.map((item: any) => item.word),
                type: 'bar',
                orientation: 'h',
                marker: { color: '#22C55E' }
              }
            ]}
            layout={{ ...plotlyLayout, yaxis: { autorange: 'reversed' }, height: 350 }}
            useResizeHandler
            className="w-full"
          />
        </div>
      </div>
    </div>
  );
};
