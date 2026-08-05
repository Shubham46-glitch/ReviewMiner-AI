import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Cloud, Tag } from 'lucide-react';

interface WordCloudProps {
  onNavigate: (tab: string) => void;
}

export const WordCloudAnalytics: React.FC<WordCloudProps> = ({ onNavigate }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchWordcloudData();
  }, []);

  const fetchWordcloudData = async () => {
    try {
      setLoading(true);
      const res = await axios.get('/api/analytics/wordclouds');
      setData(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'No dataset loaded.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-8 text-center text-slate-400">Generating Word Cloud Analytics...</div>;
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
      {/* Overall Word Cloud */}
      <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-8">
        <div className="flex items-center gap-2 mb-4">
          <Cloud className="w-6 h-6 text-purple-400" />
          <h3 className="text-xl font-bold text-white">Overall Dataset Word Cloud</h3>
        </div>
        {data.wordcloud_overall ? (
          <img src={data.wordcloud_overall} alt="Overall Word Cloud" className="w-full rounded-xl border border-white/10 shadow-lg" />
        ) : (
          <p className="text-slate-400 text-sm">Insufficient text vocabulary to generate word cloud.</p>
        )}
      </motion.div>

      {/* Positive & Negative Word Clouds */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="glass-card p-6 border-t-4 border-t-emerald-500">
          <h3 className="text-lg font-bold text-emerald-400 mb-4">Positive Reviews Word Cloud</h3>
          {data.wordcloud_positive ? (
            <img src={data.wordcloud_positive} alt="Positive Word Cloud" className="w-full rounded-xl border border-white/10" />
          ) : (
            <p className="text-slate-400 text-sm">No positive text data available.</p>
          )}
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="glass-card p-6 border-t-4 border-t-red-500">
          <h3 className="text-lg font-bold text-red-400 mb-4">Negative Reviews Word Cloud</h3>
          {data.wordcloud_negative ? (
            <img src={data.wordcloud_negative} alt="Negative Word Cloud" className="w-full rounded-xl border border-white/10" />
          ) : (
            <p className="text-slate-400 text-sm">No negative text data available.</p>
          )}
        </motion.div>
      </div>

      {/* Top Keywords Table */}
      <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="glass-card p-8">
        <div className="flex items-center gap-2 mb-4">
          <Tag className="w-5 h-5 text-cyan-400" />
          <h3 className="text-xl font-bold text-white">Top 20 Most Frequent Keywords</h3>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {data.top_keywords?.map((kw: any, idx: number) => (
            <div key={idx} className="p-4 rounded-xl bg-slate-900/60 border border-white/5 flex items-center justify-between">
              <span className="text-sm font-semibold text-slate-200">{kw.word}</span>
              <span className="px-2.5 py-1 rounded-full bg-purple-500/20 text-purple-300 text-xs font-bold">
                {kw.frequency}
              </span>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};
