import React, { useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import { motion } from 'framer-motion';
import { Sparkles, Send, AlertCircle } from 'lucide-react';

export const Prediction: React.FC = () => {
  const [reviewText, setReviewText] = useState('staff is not friendly');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handlePredict = async () => {
    if (!reviewText.trim()) {
      setError("Please enter a review to classify.");
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('text', reviewText);

    try {
      const res = await axios.post('/api/ml/predict', formData);
      if (res.data.status === 'error') {
        setError(res.data.detail);
      } else {
        setResult(res.data);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Sentiment model is not ready. Train the sentiment classification model before making predictions.');
    } finally {
      setLoading(false);
    }
  };

  const sampleReviews = [
    { label: "Positive", text: "The product quality is excellent and delivery was very fast. Highly recommend!" },
    { label: "Neutral", text: "The product arrived yesterday and I have used it twice." },
    { label: "Negative", text: "staff is not friendly" }
  ];

  const plotlyLayout: any = {
    font: { family: 'Inter, sans-serif', color: '#FFFFFF' },
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    margin: { l: 75, r: 25, t: 30, b: 40 },
    xaxis: { gridcolor: 'rgba(255,255,255,0.05)', range: [0, 100] },
    yaxis: { gridcolor: 'rgba(255,255,255,0.05)' },
  };

  const sent = result?.predicted_sentiment || result?.sentiment || '';
  const isPos = sent.toLowerCase().includes('pos') || sent === '5' || sent === '4';
  const isNeg = sent.toLowerCase().includes('neg') || sent === '1' || sent === '2';

  const displaySent = isPos ? 'POSITIVE' : isNeg ? 'NEGATIVE' : 'NEUTRAL';
  const displayEmoji = isPos ? '🟢' : isNeg ? '🔴' : '🟡';
  const colorClass = isPos ? 'text-emerald-400 border-l-emerald-500' : isNeg ? 'text-red-400 border-l-red-500' : 'text-amber-400 border-l-amber-500';

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* Review Input Box */}
      <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-8 border-purple-500/20">
        <div className="flex items-center gap-3 mb-2">
          <Sparkles className="w-6 h-6 text-purple-400" />
          <div>
            <h2 className="text-2xl font-bold text-white">AI Sentiment Prediction</h2>
            <p className="text-slate-400 text-sm mt-0.5">
              Enter a review or comment and let the trained model predict its sentiment.
            </p>
          </div>
        </div>

        {/* Sample Review Quick Buttons */}
        <div className="flex flex-wrap items-center gap-2 my-4">
          <span className="text-xs font-bold text-slate-400 mr-2">Try Sample:</span>
          {sampleReviews.map((sample, idx) => (
            <button
              key={idx}
              onClick={() => {
                setReviewText(sample.text);
                setResult(null);
                setError(null);
              }}
              className="text-xs px-3 py-1.5 rounded-lg bg-slate-900/80 border border-white/10 hover:border-purple-500 text-slate-300 transition-colors"
            >
              {sample.label} Sample
            </button>
          ))}
        </div>

        <textarea
          value={reviewText}
          onChange={(e) => {
            setReviewText(e.target.value);
            setResult(null);
            setError(null);
          }}
          placeholder="Write or paste a review here..."
          rows={4}
          className="w-full bg-slate-900/90 border border-white/10 rounded-2xl p-4 text-white placeholder-slate-500 focus:outline-none focus:border-purple-500 transition-colors mb-4 text-sm"
        />

        <div className="flex items-center justify-between">
          <div>
            {error && (
              <div className="p-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-xs flex items-center gap-2">
                <AlertCircle className="w-4 h-4 flex-shrink-0" />
                <span>{error}</span>
              </div>
            )}
          </div>

          <button
            onClick={handlePredict}
            disabled={loading || !reviewText.trim()}
            className="inline-flex items-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-purple-600 to-cyan-500 hover:from-purple-500 hover:to-cyan-400 text-white font-bold text-sm shadow-lg shadow-purple-500/30 transition-all disabled:opacity-50"
          >
            <Send className="w-4 h-4" />
            <span>{loading ? 'Predicting Sentiment...' : 'Predict Sentiment'}</span>
          </button>
        </div>
      </motion.div>

      {/* Prediction Result Display */}
      {result && (
        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* Sentiment Result Card */}
            <div className={`glass-card p-8 text-center border-l-8 ${colorClass} flex flex-col justify-center`}>
              <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">Predicted Sentiment</span>
              <h1 className="text-4xl font-black mt-2 tracking-tight">
                {displayEmoji} {displaySent}
              </h1>
              {result.confidence !== null && result.confidence !== undefined && (
                <p className="text-lg font-bold text-cyan-400 mt-2">Confidence: {result.confidence}%</p>
              )}
              <span className="text-xs text-slate-500 block mt-4">Classifier Model: {result.model_used}</span>
            </div>

            {/* Sentiment Class Probabilities Graph */}
            {result.probabilities && Object.keys(result.probabilities).length > 0 && (
              <div className="glass-card p-6">
                <h3 className="text-md font-bold text-white mb-4">Sentiment Class Probabilities (%)</h3>
                <Plot
                  data={[
                    {
                      x: Object.values(result.probabilities) as any,
                      y: Object.keys(result.probabilities) as any,
                      type: 'bar',
                      orientation: 'h',
                      marker: {
                        color: Object.keys(result.probabilities).map((k: string) => {
                          const l = k.toLowerCase();
                          if (l.includes('pos') || l === '5' || l === '4') return '#22C55E';
                          if (l.includes('neg') || l === '1' || l === '2') return '#EF4444';
                          return '#FACC15';
                        })
                      }
                    }
                  ]}
                  layout={{ ...plotlyLayout, height: 210 }}
                  useResizeHandler
                  className="w-full"
                />
              </div>
            )}
          </div>
        </motion.div>
      )}
    </div>
  );
};
