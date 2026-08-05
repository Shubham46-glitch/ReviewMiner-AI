import React, { useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import { motion } from 'framer-motion';
import { Sparkles, Send, CheckCircle2, AlertCircle } from 'lucide-react';

export const Prediction: React.FC = () => {
  const [reviewText, setReviewText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handlePredict = async () => {
    if (!reviewText.trim()) return;
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('text', reviewText);

    try {
      const res = await axios.post('/api/ml/predict', formData);
      setResult(res.data.prediction);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to predict review sentiment.');
    } finally {
      setLoading(false);
    }
  };

  const sampleReviews = [
    "The product quality is superb and delivery was lightning fast! Highly recommend.",
    "Average item. Works fine but nothing special for the price tag.",
    "Terrible customer service! Item arrived damaged and emails were completely ignored."
  ];

  const plotlyLayout: any = {
    font: { family: 'Inter, sans-serif', color: '#FFFFFF' },
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    margin: { l: 40, r: 20, t: 40, b: 40 },
    xaxis: { gridcolor: 'rgba(255,255,255,0.05)', range: [0, 100] },
    yaxis: { gridcolor: 'rgba(255,255,255,0.05)' },
  };

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* Review Input Box */}
      <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-8 border-purple-500/20">
        <div className="flex items-center gap-3 mb-2">
          <Sparkles className="w-6 h-6 text-purple-400" />
          <h2 className="text-2xl font-bold text-white">Live Sentiment Predictor</h2>
        </div>
        <p className="text-slate-400 text-sm mb-6">
          Enter any product review, feedback comment, or text string to predict its sentiment using the trained Machine Learning pipeline:
        </p>

        {/* Sample Review Quick Buttons */}
        <div className="flex flex-wrap gap-2 mb-4">
          <span className="text-xs font-bold text-slate-400 self-center mr-2">Try Sample:</span>
          {sampleReviews.map((sample, idx) => (
            <button
              key={idx}
              onClick={() => setReviewText(sample)}
              className="text-xs px-3 py-1.5 rounded-lg bg-slate-900/60 border border-white/10 hover:border-purple-500 text-slate-300 transition-colors"
            >
              Sample {idx + 1}
            </button>
          ))}
        </div>

        <textarea
          value={reviewText}
          onChange={(e) => setReviewText(e.target.value)}
          placeholder="Write or paste review text here..."
          rows={4}
          className="w-full bg-slate-900 border border-white/10 rounded-2xl p-4 text-white placeholder-slate-500 focus:outline-none focus:border-purple-500 transition-colors mb-4"
        />

        <div className="text-right">
          <button
            onClick={handlePredict}
            disabled={loading || !reviewText.trim()}
            className="inline-flex items-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-purple-600 to-cyan-500 hover:from-purple-500 hover:to-cyan-400 text-white font-bold text-sm shadow-lg shadow-purple-500/30 transition-all disabled:opacity-50"
          >
            <Send className="w-4 h-4" />
            <span>{loading ? 'Analyzing Sentiment...' : 'Predict Sentiment Now'}</span>
          </button>
        </div>

        {error && (
          <div className="mt-4 p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-sm flex items-center gap-3">
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}
      </motion.div>

      {/* Prediction Result Display */}
      {result && (
        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Sentiment Result Card */}
            <div className={`glass-card p-8 text-center border-l-8 ${
              result.sentiment === 'Positive' ? 'border-l-emerald-500' :
              result.sentiment === 'Negative' ? 'border-l-red-500' : 'border-l-amber-500'
            }`}>
              <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">Predicted Sentiment</span>
              <h1 className={`text-4xl font-black mt-2 ${
                result.sentiment === 'Positive' ? 'text-emerald-400' :
                result.sentiment === 'Negative' ? 'text-red-400' : 'text-amber-400'
              }`}>
                {result.sentiment === 'Positive' ? '😊 POSITIVE' :
                 result.sentiment === 'Negative' ? '😡 NEGATIVE' : '😐 NEUTRAL'}
              </h1>
              <p className="text-lg font-bold text-cyan-400 mt-2">Confidence: {result.confidence}%</p>
              <span className="text-xs text-slate-400 block mt-4">Model: {result.model_used}</span>
            </div>

            {/* Probability Graph */}
            <div className="glass-card p-6">
              <h3 className="text-lg font-bold text-white mb-4">Class Probability Breakdown (%)</h3>
              <Plot
                data={[
                  {
                    x: Object.values(result.probabilities) as any,
                    y: Object.keys(result.probabilities) as any,
                    type: 'bar',
                    orientation: 'h',
                    marker: { color: ['#22C55E', '#FACC15', '#EF4444'] }
                  }
                ]}
                layout={{ ...plotlyLayout, height: 220 }}
                useResizeHandler
                className="w-full"
              />
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
};
