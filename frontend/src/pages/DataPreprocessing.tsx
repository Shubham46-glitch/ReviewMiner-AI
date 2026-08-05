import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Sparkles, ArrowRight, CheckCircle } from 'lucide-react';

interface PreprocessingProps {
  onNavigate: (tab: string) => void;
}

export const DataPreprocessing: React.FC<PreprocessingProps> = ({ onNavigate }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPreprocessingData();
  }, []);

  const fetchPreprocessingData = async () => {
    try {
      setLoading(true);
      const res = await axios.get('/api/analytics/preprocessing');
      setData(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'No dataset loaded.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-slate-400">Loading Preprocessing Pipeline...</div>;
  }

  if (error) {
    return (
      <div className="p-8 max-w-xl mx-auto text-center space-y-4">
        <div className="glass-card p-8 border-purple-500/20">
          <p className="text-red-400 font-semibold mb-4">{error}</p>
          <button
            onClick={() => onNavigate('upload')}
            className="px-6 py-3 rounded-xl bg-purple-600 text-white font-bold text-sm"
          >
            Go to Dataset Upload
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* Pipeline Overview Card */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-8 border-purple-500/20"
      >
        <div className="flex items-center gap-3 mb-2">
          <Sparkles className="w-6 h-6 text-purple-400" />
          <h2 className="text-2xl font-bold text-white">Natural Language Preprocessing Pipeline</h2>
        </div>
        <p className="text-slate-400 text-sm mb-6">
          The raw text has been transformed using the following NLP cleaning pipeline steps:
        </p>

        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {[
            "1. Lowercase Conversion",
            "2. Remove Punctuation",
            "3. Remove Numbers",
            "4. Remove Stopwords",
            "5. NLTK Lemmatization"
          ].map((step, idx) => (
            <div key={idx} className="p-3 rounded-xl bg-slate-900/60 border border-white/5 text-center">
              <CheckCircle className="w-4 h-4 text-emerald-400 mx-auto mb-2" />
              <span className="text-xs font-semibold text-slate-300">{step}</span>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-card p-6 border-l-4 border-l-red-500">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Original Raw Words</span>
          <p className="text-3xl font-black text-white mt-1">{data.original_total_words?.toLocaleString()}</p>
          <span className="text-xs text-red-400">Raw messy text tokens</span>
        </div>

        <div className="glass-card p-6 border-l-4 border-l-emerald-500">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Cleaned Optimized Tokens</span>
          <p className="text-3xl font-black text-white mt-1">{data.cleaned_total_tokens?.toLocaleString()}</p>
          <span className="text-xs text-emerald-400">Normalized NLP vocabulary</span>
        </div>

        <div className="glass-card p-6 border-l-4 border-l-cyan-500">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Noise Reduction %</span>
          <p className="text-3xl font-black text-white mt-1">{data.reduction_pct}%</p>
          <span className="text-xs text-cyan-400">Stopwords & punctuation removed</span>
        </div>
      </div>

      {/* Before vs After Comparison Table */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="glass-card p-8"
      >
        <h3 className="text-xl font-bold text-white mb-4">Before vs After Text Transformation</h3>
        <p className="text-slate-400 text-sm mb-6">
          Side-by-side comparison of original raw review text against the cleaned NLP tokens:
        </p>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300 border-collapse">
            <thead>
              <tr className="border-b border-white/10 text-xs font-bold text-purple-400 uppercase">
                <th className="p-3 w-1/2">Original Raw Text</th>
                <th className="p-3 w-1/2">Cleaned & Lemmatized Tokens</th>
              </tr>
            </thead>
            <tbody>
              {data.comparison_preview?.map((row: any, i: number) => (
                <tr key={i} className="border-b border-white/5 hover:bg-slate-800/40">
                  <td className="p-3 text-slate-400 font-normal">{row.Text}</td>
                  <td className="p-3 text-emerald-400 font-medium bg-emerald-500/5">{row.Cleaned_Text}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="mt-8 text-right">
          <button
            onClick={() => onNavigate('eda')}
            className="inline-flex items-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-purple-600 to-cyan-500 text-white font-bold text-sm shadow-lg shadow-purple-500/30"
          >
            <span>Proceed to Exploratory Data Analysis (EDA)</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </motion.div>
    </div>
  );
};
