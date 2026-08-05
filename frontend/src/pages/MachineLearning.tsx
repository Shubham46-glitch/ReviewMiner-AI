import React, { useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import { motion } from 'framer-motion';
import { Cpu, Award, CheckCircle2, AlertCircle, Play } from 'lucide-react';

interface MLProps {
  onNavigate: (tab: string) => void;
}

export const MachineLearning: React.FC<MLProps> = ({ onNavigate }) => {
  const [loading, setLoading] = useState(false);
  const [mlResult, setMlResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleTrain = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await axios.post('/api/ml/train');
      setMlResult(res.data.results);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to train ML model.');
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

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* ML Pipeline Banner */}
      <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-8 border-purple-500/20">
        <div className="flex items-center gap-3 mb-2">
          <Cpu className="w-6 h-6 text-purple-400" />
          <h2 className="text-2xl font-bold text-white">Supervised Machine Learning Pipeline</h2>
        </div>
        <p className="text-slate-400 text-sm mb-6">
          Train a Multinomial Naive Bayes classification model using TF-IDF vector features extracted from active dataset text records.
        </p>

        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4 text-xs font-semibold text-slate-300">
            <span className="px-3 py-1.5 rounded-lg bg-purple-500/20 border border-purple-500/30 text-purple-300">TF-IDF Features</span>
            <span>→</span>
            <span className="px-3 py-1.5 rounded-lg bg-cyan-500/20 border border-cyan-500/30 text-cyan-300">80/20 Train-Test Split</span>
            <span>→</span>
            <span className="px-3 py-1.5 rounded-lg bg-emerald-500/20 border border-emerald-500/30 text-emerald-300">Multinomial Naive Bayes</span>
          </div>

          <button
            onClick={handleTrain}
            disabled={loading}
            className="flex items-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-purple-600 to-cyan-500 hover:from-purple-500 hover:to-cyan-400 text-white font-bold text-sm shadow-lg shadow-purple-500/30 transition-all disabled:opacity-50"
          >
            <Play className="w-4 h-4 fill-white" />
            <span>{loading ? 'Training Model...' : 'Train Naive Bayes Model Now'}</span>
          </button>
        </div>

        {error && (
          <div className="mt-4 p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-sm flex items-center gap-3">
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}
      </motion.div>

      {/* ML Evaluation Metrics */}
      {mlResult && (
        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="glass-card p-6 border-l-4 border-l-purple-500">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Accuracy Score</span>
              <p className="text-3xl font-black text-white mt-1">{(mlResult.metrics.accuracy * 100).toFixed(1)}%</p>
              <span className="text-xs text-purple-400">Overall correctness</span>
            </div>

            <div className="glass-card p-6 border-l-4 border-l-cyan-500">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Precision Score</span>
              <p className="text-3xl font-black text-white mt-1">{(mlResult.metrics.precision * 100).toFixed(1)}%</p>
              <span className="text-xs text-cyan-400">Weighted precision</span>
            </div>

            <div className="glass-card p-6 border-l-4 border-l-emerald-500">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Recall Score</span>
              <p className="text-3xl font-black text-white mt-1">{(mlResult.metrics.recall * 100).toFixed(1)}%</p>
              <span className="text-xs text-emerald-400">Weighted recall</span>
            </div>

            <div className="glass-card p-6 border-l-4 border-l-amber-500">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">F1 Score</span>
              <p className="text-3xl font-black text-white mt-1">{(mlResult.metrics.f1_score * 100).toFixed(1)}%</p>
              <span className="text-xs text-amber-400">Harmonic mean score</span>
            </div>
          </div>

          {/* Confusion Matrix Heatmap */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="glass-card p-6">
              <h3 className="text-xl font-bold text-white mb-4">Confusion Matrix Heatmap</h3>
              <Plot
                data={[
                  {
                    z: mlResult.confusion_matrix.matrix,
                    x: mlResult.confusion_matrix.labels,
                    y: mlResult.confusion_matrix.labels,
                    type: 'heatmap',
                    colorscale: 'Purples'
                  }
                ]}
                layout={{ ...plotlyLayout, title: 'Predicted vs Actual Labels', height: 350 }}
                useResizeHandler
                className="w-full"
              />
            </div>

            {/* Classification Report */}
            <div className="glass-card p-6 overflow-x-auto">
              <h3 className="text-xl font-bold text-white mb-4">Classification Metrics Report</h3>
              <table className="w-full text-left text-sm text-slate-300 border-collapse">
                <thead>
                  <tr className="border-b border-white/10 text-xs font-bold text-purple-400 uppercase">
                    <th className="p-3">Class</th>
                    <th className="p-3">Precision</th>
                    <th className="p-3">Recall</th>
                    <th className="p-3">F1-Score</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(mlResult.classification_report).map(([cls, scores]: [string, any]) => {
                    if (typeof scores !== 'object') return null;
                    return (
                      <tr key={cls} className="border-b border-white/5 hover:bg-slate-800/40">
                        <td className="p-3 font-semibold text-white">{cls}</td>
                        <td className="p-3 text-cyan-400">{scores.precision?.toFixed(4)}</td>
                        <td className="p-3 text-emerald-400">{scores.recall?.toFixed(4)}</td>
                        <td className="p-3 text-purple-400">{scores['f1-score']?.toFixed(4)}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
};
