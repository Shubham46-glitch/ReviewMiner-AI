import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import { motion } from 'framer-motion';
import { 
  Smile, Frown, Meh, Percent, TrendingUp, BarChart3, 
  Sparkles, Award, ShieldAlert, Star, Filter, Search, 
  Layers, Zap, CheckCircle2, AlertTriangle
} from 'lucide-react';

interface SentimentProps {
  onNavigate: (tab: string) => void;
}

export const SentimentDashboard: React.FC<SentimentProps> = ({ onNavigate }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Review Explorer State
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedSentimentFilter, setSelectedSentimentFilter] = useState('ALL');

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

  if (loading) return <div className="p-8 text-center text-slate-400">Loading Comprehensive Sentiment Analytics...</div>;
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
    margin: { l: 55, r: 25, t: 40, b: 50 },
    xaxis: { gridcolor: 'rgba(255,255,255,0.05)' },
    yaxis: { gridcolor: 'rgba(255,255,255,0.05)' },
  };

  const ov = data.overview || {};
  const scoreDist = data.score_distribution || {};
  const ratingAnalysis = data.rating_analysis || {};
  const catDims = data.categorical_dimensions || {};
  const trendAnalysis = data.trend_analysis || {};
  const heatmapData = data.sentiment_heatmap || {};
  const confidenceData = data.model_confidence || {};
  const negIntel = data.negative_intelligence || {};
  const posIntel = data.positive_intelligence || {};
  const compMetrics = data.sentiment_comparison || [];
  const reviewExp = data.review_explorer || {};

  // Filter Explorer Reviews
  const filteredReviews = (reviewExp.reviews || []).filter((r: any) => {
    const matchesSentiment = selectedSentimentFilter === 'ALL' || r.sentiment.toUpperCase() === selectedSentimentFilter.toUpperCase();
    const matchesSearch = !searchQuery.trim() || r.text.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesSentiment && matchesSearch;
  });

  return (
    <div className="p-8 space-y-10 max-w-7xl mx-auto">
      
      {/* SECTION A — SENTIMENT OVERVIEW */}
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-white flex items-center gap-2">
              <Sparkles className="w-6 h-6 text-purple-400" />
              Section A — Sentiment Overview & KPI Metrics
            </h2>
            <p className="text-sm text-slate-400 mt-1">
              High-level sentiment breakdown, net polarity, and dominant customer tone.
            </p>
          </div>
        </div>

        {/* 8 Metric Cards Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="glass-card p-5 border-l-4 border-l-purple-500">
            <div className="flex items-center gap-2 text-slate-400 text-xs font-bold uppercase tracking-wider mb-1">
              <Percent className="w-4 h-4 text-purple-400" />
              <span>Total Evaluated</span>
            </div>
            <p className="text-2xl font-black text-white">{ov.total_reviews?.toLocaleString()}</p>
            <span className="text-xs text-purple-400">Review entries</span>
          </div>

          <div className="glass-card p-5 border-l-4 border-l-emerald-500">
            <div className="flex items-center gap-2 text-slate-400 text-xs font-bold uppercase tracking-wider mb-1">
              <Smile className="w-4 h-4 text-emerald-400" />
              <span>Positive Share</span>
            </div>
            <p className="text-2xl font-black text-white">{ov.positive_pct}%</p>
            <span className="text-xs text-emerald-400">{ov.positive_count?.toLocaleString()} positive</span>
          </div>

          <div className="glass-card p-5 border-l-4 border-l-amber-500">
            <div className="flex items-center gap-2 text-slate-400 text-xs font-bold uppercase tracking-wider mb-1">
              <Meh className="w-4 h-4 text-amber-400" />
              <span>Neutral Share</span>
            </div>
            <p className="text-2xl font-black text-white">{ov.neutral_pct}%</p>
            <span className="text-xs text-amber-400">{ov.neutral_count?.toLocaleString()} neutral</span>
          </div>

          <div className="glass-card p-5 border-l-4 border-l-red-500">
            <div className="flex items-center gap-2 text-slate-400 text-xs font-bold uppercase tracking-wider mb-1">
              <Frown className="w-4 h-4 text-red-400" />
              <span>Negative Share</span>
            </div>
            <p className="text-2xl font-black text-white">{ov.negative_pct}%</p>
            <span className="text-xs text-red-400">{ov.negative_count?.toLocaleString()} negative</span>
          </div>

          <div className="glass-card p-5 border-l-4 border-l-cyan-500">
            <div className="flex items-center gap-2 text-slate-400 text-xs font-bold uppercase tracking-wider mb-1">
              <TrendingUp className="w-4 h-4 text-cyan-400" />
              <span>Avg Polarity Score</span>
            </div>
            <p className="text-2xl font-black text-white">{ov.avg_sentiment_score > 0 ? `+${ov.avg_sentiment_score}` : ov.avg_sentiment_score}</p>
            <span className="text-xs text-cyan-400">Scale -1.0 to +1.0</span>
          </div>

          <div className="glass-card p-5 border-l-4 border-l-indigo-500">
            <div className="flex items-center gap-2 text-slate-400 text-xs font-bold uppercase tracking-wider mb-1">
              <Zap className="w-4 h-4 text-indigo-400" />
              <span>Model Confidence</span>
            </div>
            <p className="text-2xl font-black text-white">{ov.avg_confidence_pct}%</p>
            <span className="text-xs text-indigo-400">Prediction certainty</span>
          </div>

          <div className="glass-card p-5 border-l-4 border-l-blue-500">
            <div className="flex items-center gap-2 text-slate-400 text-xs font-bold uppercase tracking-wider mb-1">
              <Award className="w-4 h-4 text-blue-400" />
              <span>Dominant Tone</span>
            </div>
            <p className="text-2xl font-black text-white">{ov.dominant_sentiment}</p>
            <span className="text-xs text-blue-400">Primary sentiment</span>
          </div>

          <div className="glass-card p-5 border-l-4 border-l-teal-500">
            <div className="flex items-center gap-2 text-slate-400 text-xs font-bold uppercase tracking-wider mb-1">
              <Layers className="w-4 h-4 text-teal-400" />
              <span>Net Sentiment Score</span>
            </div>
            <p className="text-2xl font-black text-white">{ov.net_sentiment_score_pct > 0 ? `+${ov.net_sentiment_score_pct}%` : `${ov.net_sentiment_score_pct}%`}</p>
            <span className="text-xs text-teal-400">Pos % minus Neg %</span>
          </div>
        </div>

        {/* Section A Visuals */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="glass-card p-6">
            <h3 className="text-lg font-bold text-white mb-2">Customer Sentiment Share</h3>
            <Plot
              data={[
                {
                  labels: ['Positive', 'Neutral', 'Negative'],
                  values: [ov.positive_count, ov.neutral_count, ov.negative_count],
                  type: 'pie',
                  hole: 0.45,
                  marker: { colors: ['#22C55E', '#FACC15', '#EF4444'] }
                }
              ]}
              layout={{ ...plotlyLayout, height: 320 }}
              useResizeHandler
              className="w-full"
            />
          </div>

          {/* Dynamic Insight Card */}
          <div className="glass-card p-6 flex flex-col justify-between border border-purple-500/20 bg-gradient-to-br from-slate-900/90 to-purple-950/20">
            <div>
              <div className="flex items-center gap-2 text-purple-400 font-bold mb-3">
                <Sparkles className="w-5 h-5" />
                <h3 className="text-lg text-white">Overall Sentiment Insight</h3>
              </div>
              <p className="text-slate-300 text-base leading-relaxed mb-6">
                {ov.insight_summary}
              </p>
            </div>
            <div className="p-4 rounded-xl bg-white/5 border border-white/10 space-y-1">
              <div className="text-xs text-slate-400">Evaluation Context:</div>
              <div className="text-sm font-semibold text-white">
                Evaluated {ov.total_reviews?.toLocaleString()} records with {ov.avg_confidence_pct}% AI confidence.
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* SECTION B — SENTIMENT SCORE DISTRIBUTION */}
      <div className="glass-card p-6 space-y-4">
        <h3 className="text-xl font-bold text-white flex items-center gap-2">
          <BarChart3 className="w-5 h-5 text-emerald-400" />
          Section B — Sentiment Score Polarity Distribution
        </h3>
        <p className="text-xs text-slate-400">Distribution of polarity scores (-1.0 Negative, 0.0 Neutral, +1.0 Positive)</p>
        <Plot
          data={[
            {
              x: scoreDist.scores || [],
              type: 'histogram',
              nbinsx: 30,
              marker: { color: '#06B6D4' }
            } as any
          ]}
          layout={{
            ...plotlyLayout,
            title: { text: 'Sentiment Score Polarity Distribution', font: { color: '#FFFFFF', size: 15 } },
            height: 300,
            xaxis: { title: { text: 'Sentiment Polarity Score (-1.0 to +1.0)', font: { color: '#94A3B8', size: 12 } } },
            yaxis: { title: { text: 'Number of Reviews', font: { color: '#94A3B8', size: 12 } } }
          }}
          useResizeHandler
          className="w-full"
        />
      </div>

      {/* SECTION C — SENTIMENT VS RATING ALIGNMENT */}
      <div className="glass-card p-6 space-y-4">
        <h3 className="text-xl font-bold text-white flex items-center gap-2">
          <Star className="w-5 h-5 text-amber-400" />
          Section C — Sentiment vs Rating Alignment
        </h3>
        {ratingAnalysis.has_rating ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="text-sm font-bold text-slate-300 mb-2">Rating Level Sentiment Breakdown</h4>
              <Plot
                data={[
                  {
                    x: (ratingAnalysis.stacked_bar || []).map((item: any) => `Rating ${item.rating}`),
                    y: (ratingAnalysis.stacked_bar || []).map((item: any) => item.positive),
                    name: 'Positive',
                    type: 'bar',
                    marker: { color: '#22C55E' }
                  },
                  {
                    x: (ratingAnalysis.stacked_bar || []).map((item: any) => `Rating ${item.rating}`),
                    y: (ratingAnalysis.stacked_bar || []).map((item: any) => item.neutral),
                    name: 'Neutral',
                    type: 'bar',
                    marker: { color: '#FACC15' }
                  },
                  {
                    x: (ratingAnalysis.stacked_bar || []).map((item: any) => `Rating ${item.rating}`),
                    y: (ratingAnalysis.stacked_bar || []).map((item: any) => item.negative),
                    name: 'Negative',
                    type: 'bar',
                    marker: { color: '#EF4444' }
                  }
                ]}
                layout={{
                  ...plotlyLayout,
                  title: { text: 'Rating Level Sentiment Breakdown', font: { color: '#FFFFFF', size: 14 } },
                  xaxis: { title: { text: 'Rating', font: { color: '#94A3B8', size: 12 } } },
                  yaxis: { title: { text: 'Number of Reviews', font: { color: '#94A3B8', size: 12 } } },
                  legend: { title: { text: 'Sentiment', font: { color: '#94A3B8', size: 12 } } },
                  barmode: 'stack',
                  height: 300
                }}
                useResizeHandler
                className="w-full"
              />
            </div>
            <div>
              <h4 className="text-sm font-bold text-slate-300 mb-2">Average Polarity Score by Rating</h4>
              <Plot
                data={[
                  {
                    x: (ratingAnalysis.avg_sentiment_by_rating || []).map((item: any) => `Rating ${item.rating}`),
                    y: (ratingAnalysis.avg_sentiment_by_rating || []).map((item: any) => item.avg_score),
                    type: 'scatter',
                    mode: 'lines+markers',
                    line: { color: '#06B6D4', width: 3 },
                    marker: { size: 8 }
                  }
                ]}
                layout={{
                  ...plotlyLayout,
                  title: { text: 'Average Polarity Score by User Rating', font: { color: '#FFFFFF', size: 14 } },
                  xaxis: { title: { text: 'Rating', font: { color: '#94A3B8', size: 12 } } },
                  yaxis: { title: { text: 'Average Sentiment Score', font: { color: '#94A3B8', size: 12 } } },
                  height: 300
                }}
                useResizeHandler
                className="w-full"
              />
            </div>
          </div>
        ) : (
          <div className="p-4 rounded-xl bg-slate-900/50 border border-white/5 space-y-1">
            <h4 className="text-md font-bold text-slate-200">⭐ Rating Analysis Unavailable</h4>
            <p className="text-xs text-slate-400">Rating analysis unavailable: This analysis requires a numeric Rating/Stars column in the uploaded dataset.</p>
          </div>
        )}
      </div>

      {/* SECTION D — CATEGORICAL SENTIMENT BREAKDOWN */}
      {Object.keys(catDims).length > 0 && (
        <div className="glass-card p-6 space-y-6">
          <h3 className="text-xl font-bold text-white flex items-center gap-2">
            <Layers className="w-5 h-5 text-indigo-400" />
            Section D — Categorical Sentiment Breakdown
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {Object.entries(catDims).map(([dimName, items]: [string, any]) => (
              <div key={dimName} className="p-4 rounded-xl bg-white/5 border border-white/10 space-y-3">
                <h4 className="text-md font-bold text-purple-300">Top 10 {dimName} Breakdown</h4>
                <Plot
                  data={[
                    {
                      x: items.map((i: any) => i.name),
                      y: items.map((i: any) => i.positive),
                      name: 'Positive',
                      type: 'bar',
                      marker: { color: '#22C55E' }
                    },
                    {
                      x: items.map((i: any) => i.name),
                      y: items.map((i: any) => i.neutral),
                      name: 'Neutral',
                      type: 'bar',
                      marker: { color: '#FACC15' }
                    },
                    {
                      x: items.map((i: any) => i.name),
                      y: items.map((i: any) => i.negative),
                      name: 'Negative',
                      type: 'bar',
                      marker: { color: '#EF4444' }
                    }
                  ]}
                  layout={{
                    ...plotlyLayout,
                    title: { text: `Top 10 ${dimName} Sentiment Breakdown`, font: { color: '#FFFFFF', size: 14 } },
                    xaxis: { title: { text: dimName, font: { color: '#94A3B8', size: 12 } } },
                    yaxis: { title: { text: 'Number of Reviews', font: { color: '#94A3B8', size: 12 } } },
                    legend: { title: { text: 'Sentiment', font: { color: '#94A3B8', size: 12 } } },
                    barmode: 'group',
                    height: 280
                  }}
                  useResizeHandler
                  className="w-full"
                />
              </div>
            ))}
          </div>
        </div>
      )}

      {/* SECTION E — SENTIMENT TRENDS OVER TIME */}
      <div className="glass-card p-6 space-y-4">
        {trendAnalysis.has_date && (trendAnalysis.time_series || []).length > 0 ? (
          <>
            <h3 className="text-xl font-bold text-white flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-cyan-400" />
              Section E — Sentiment Trends Over Time
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="text-sm font-bold text-slate-300 mb-2">Average Sentiment Score Trend Over Time</h4>
                <Plot
                  data={[
                    {
                      x: (trendAnalysis.time_series || []).map((t: any) => t.date),
                      y: (trendAnalysis.time_series || []).map((t: any) => t.avg_score),
                      type: 'scatter',
                      mode: 'lines+markers',
                      line: { color: '#3B82F6', width: 3 }
                    }
                  ]}
                  layout={{
                    ...plotlyLayout,
                    title: { text: 'Average Sentiment Score Trend Over Time', font: { color: '#FFFFFF', size: 14 } },
                    xaxis: { title: { text: 'Date', font: { color: '#94A3B8', size: 12 } } },
                    yaxis: { title: { text: 'Average Sentiment Score', font: { color: '#94A3B8', size: 12 } } },
                    height: 300
                  }}
                  useResizeHandler
                  className="w-full"
                />
              </div>
              <div>
                <h4 className="text-sm font-bold text-slate-300 mb-2">Sentiment Review Volume Trend Over Time</h4>
                <Plot
                  data={[
                    {
                      x: (trendAnalysis.time_series || []).map((t: any) => t.date),
                      y: (trendAnalysis.time_series || []).map((t: any) => t.positive),
                      name: 'Positive',
                      type: 'scatter',
                      mode: 'lines',
                      line: { color: '#22C55E', width: 2 }
                    },
                    {
                      x: (trendAnalysis.time_series || []).map((t: any) => t.date),
                      y: (trendAnalysis.time_series || []).map((t: any) => t.neutral),
                      name: 'Neutral',
                      type: 'scatter',
                      mode: 'lines',
                      line: { color: '#FACC15', width: 2 }
                    },
                    {
                      x: (trendAnalysis.time_series || []).map((t: any) => t.date),
                      y: (trendAnalysis.time_series || []).map((t: any) => t.negative),
                      name: 'Negative',
                      type: 'scatter',
                      mode: 'lines',
                      line: { color: '#EF4444', width: 2 }
                    }
                  ]}
                  layout={{
                    ...plotlyLayout,
                    title: { text: 'Sentiment Review Volume Trend Over Time', font: { color: '#FFFFFF', size: 14 } },
                    xaxis: { title: { text: 'Date', font: { color: '#94A3B8', size: 12 } } },
                    yaxis: { title: { text: 'Number of Reviews', font: { color: '#94A3B8', size: 12 } } },
                    legend: { title: { text: 'Sentiment', font: { color: '#94A3B8', size: 12 } } },
                    height: 300
                  }}
                  useResizeHandler
                  className="w-full"
                />
              </div>
            </div>
          </>
        ) : (
          <div className="p-4 rounded-xl bg-slate-900/50 border border-white/5 space-y-1">
            <h4 className="text-md font-bold text-slate-200">⏳ Trend Analysis Unavailable</h4>
            <p className="text-xs text-slate-400">No valid date/time column was detected in this dataset.</p>
            <p className="text-[11px] text-slate-500">Upload a dataset containing a review date or timestamp to enable temporal sentiment analysis.</p>
          </div>
        )}
      </div>

      {/* SECTION F — SENTIMENT HEATMAP MATRIX */}
      <div className="glass-card p-6 space-y-4">
        {heatmapData.has_heatmap && (heatmapData.rows || []).length > 0 ? (
          <>
            <h3 className="text-xl font-bold text-white flex items-center gap-2">
              <Layers className="w-5 h-5 text-purple-400" />
              Section F — {heatmapData.dimension} × Sentiment Heatmap
            </h3>
            <p className="text-xs text-slate-400">
              Cross-tabulation matrix mapping review counts across top 10 {heatmapData.dimension} entries.
            </p>
            <Plot
              data={[
                {
                  z: (heatmapData.rows || []).map((r: any) => [r.positive, r.neutral, r.negative]),
                  x: ['Positive', 'Neutral', 'Negative'],
                  y: (heatmapData.rows || []).map((r: any) => r.row),
                  type: 'heatmap',
                  colorscale: 'Viridis',
                  text: (heatmapData.rows || []).map((r: any) => [
                    `${heatmapData.dimension}: ${r.row}<br>Sentiment: Positive<br>Review Count: ${r.positive} (${r.pos_pct}%)`,
                    `${heatmapData.dimension}: ${r.row}<br>Sentiment: Neutral<br>Review Count: ${r.neutral} (${r.neu_pct}%)`,
                    `${heatmapData.dimension}: ${r.row}<br>Sentiment: Negative<br>Review Count: ${r.negative} (${r.neg_pct}%)`
                  ]),
                  hoverinfo: 'text',
                  colorbar: { title: { text: 'Review Count', font: { color: '#94A3B8', size: 12 } }, tickfont: { color: '#94A3B8' } }
                } as any
              ]}
              layout={{
                ...plotlyLayout,
                title: { text: `${heatmapData.dimension} × Sentiment Heatmap`, font: { color: '#FFFFFF', size: 16 } },
                xaxis: { title: { text: 'Sentiment', font: { color: '#94A3B8', size: 13 } } },
                yaxis: { title: { text: heatmapData.dimension, font: { color: '#94A3B8', size: 13 } }, automargin: true, autorange: 'reversed' },
                height: 380
              }}
              useResizeHandler
              className="w-full"
            />
          </>
        ) : (
          <div className="text-center py-4 space-y-1">
            <h3 className="text-md font-bold text-white">Section F — Heatmap Matrix</h3>
            <p className="text-slate-400 text-xs">Heatmap unavailable — no suitable categorical column found in this dataset.</p>
          </div>
        )}
      </div>

      {/* SECTION G — MODEL CONFIDENCE & UNCERTAIN PREDICTIONS */}
      <div className="glass-card p-6 space-y-6">
        <h3 className="text-xl font-bold text-white flex items-center gap-2">
          <Zap className="w-5 h-5 text-amber-400" />
          Section G — Model Certainty & Prediction Audit
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 rounded-xl bg-white/5 border border-white/10">
            <div className="text-xs text-slate-400 uppercase font-bold">Avg Certainty</div>
            <div className="text-2xl font-black text-white">{confidenceData.avg_confidence}%</div>
          </div>
          <div className="p-4 rounded-xl bg-white/5 border border-white/10">
            <div className="text-xs text-emerald-400 uppercase font-bold">High Certainty (≥80%)</div>
            <div className="text-2xl font-black text-white">{confidenceData.high_confidence_count?.toLocaleString()}</div>
          </div>
          <div className="p-4 rounded-xl bg-white/5 border border-white/10">
            <div className="text-xs text-red-400 uppercase font-bold">Low Certainty (&lt;65%)</div>
            <div className="text-2xl font-black text-white">{confidenceData.low_confidence_count?.toLocaleString()}</div>
          </div>
        </div>

        <div>
          <h4 className="text-sm font-bold text-slate-300 mb-3 flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-amber-400" />
            Lowest Confidence Predictions (Requires Audit)
          </h4>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-white/5 text-slate-400 uppercase">
                <tr>
                  <th className="p-3">Review Text</th>
                  <th className="p-3">Predicted Sentiment</th>
                  <th className="p-3">Confidence</th>
                  <th className="p-3">Score</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {(confidenceData.uncertain_reviews || []).map((u: any, idx: number) => (
                  <tr key={idx} className="hover:bg-white/5">
                    <td className="p-3 font-mono text-slate-200">{u.review}</td>
                    <td className="p-3 font-bold">{u.predicted_sentiment}</td>
                    <td className="p-3 text-amber-400 font-bold">{u.confidence_pct}%</td>
                    <td className="p-3 font-bold">{u.score}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* SECTION H & I — NEGATIVE & POSITIVE INTELLIGENCE */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Section H */}
        <div className="glass-card p-6 space-y-4 border-t-4 border-t-red-500">
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-red-400" />
            Section H — Negative Sentiment Intelligence
          </h3>
          <p className="text-xs text-slate-400">Highest friction negative reviews sorted by lowest sentiment score</p>
          <div className="space-y-3">
            {(negIntel.top_negative_reviews || []).slice(0, 5).map((r: any, idx: number) => (
              <div key={idx} className="p-3 rounded-lg bg-red-950/20 border border-red-500/20 text-xs text-slate-300 space-y-1">
                <p className="italic">"{r.review}"</p>
                <div className="flex justify-between text-[11px] text-red-400 font-bold">
                  <span>Category: {r.category}</span>
                  <span>Score: {r.score}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Section I */}
        <div className="glass-card p-6 space-y-4 border-t-4 border-t-emerald-500">
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5 text-emerald-400" />
            Section I — Positive Sentiment Intelligence
          </h3>
          <p className="text-xs text-slate-400">Highest praise positive reviews sorted by highest sentiment score</p>
          <div className="space-y-3">
            {(posIntel.top_positive_reviews || []).slice(0, 5).map((r: any, idx: number) => (
              <div key={idx} className="p-3 rounded-lg bg-emerald-950/20 border border-emerald-500/20 text-xs text-slate-300 space-y-1">
                <p className="italic">"{r.review}"</p>
                <div className="flex justify-between text-[11px] text-emerald-400 font-bold">
                  <span>Category: {r.category}</span>
                  <span>Score: +{r.score}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* SECTION J — SENTIMENT COMPARISON */}
      <div className="glass-card p-6 space-y-4">
        <h3 className="text-xl font-bold text-white flex items-center gap-2">
          <Layers className="w-5 h-5 text-purple-400" />
          Section J — Sentiment Class Comparison Panel
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-white/5 text-slate-400 uppercase">
              <tr>
                <th className="p-3">Sentiment Class</th>
                <th className="p-3">Review Volume</th>
                <th className="p-3">Share (%)</th>
                <th className="p-3">Avg Polarity Score</th>
                <th className="p-3">Avg Rating</th>
                <th className="p-3">Avg Length (Chars)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {compMetrics.map((cm: any, idx: number) => (
                <tr key={idx} className="hover:bg-white/5">
                  <td className="p-3 font-bold">{cm.sentiment}</td>
                  <td className="p-3">{cm.count?.toLocaleString()}</td>
                  <td className="p-3 font-bold">{cm.percentage}%</td>
                  <td className="p-3">{cm.avg_score}</td>
                  <td className="p-3">{cm.avg_rating || 'N/A'}</td>
                  <td className="p-3">{cm.avg_chars}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* SECTION K — INDIVIDUAL REVIEW EXPLORER */}
      <div className="glass-card p-6 space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <h3 className="text-xl font-bold text-white flex items-center gap-2">
            <Search className="w-5 h-5 text-purple-400" />
            Section K — Individual Review Explorer
          </h3>
          <div className="flex flex-wrap items-center gap-3">
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
              <input
                type="text"
                placeholder="Search reviews..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-9 pr-4 py-2 rounded-xl bg-slate-900/80 border border-white/10 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-purple-500"
              />
            </div>
            <select
              value={selectedSentimentFilter}
              onChange={(e) => setSelectedSentimentFilter(e.target.value)}
              className="px-3 py-2 rounded-xl bg-slate-900/80 border border-white/10 text-xs text-white focus:outline-none focus:border-purple-500"
            >
              <option value="ALL">All Sentiments</option>
              <option value="POSITIVE">Positive Only</option>
              <option value="NEUTRAL">Neutral Only</option>
              <option value="NEGATIVE">Negative Only</option>
            </select>
          </div>
        </div>

        <div className="text-xs text-slate-400">
          Showing <span className="font-bold text-white">{filteredReviews.length}</span> matching reviews
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-white/5 text-slate-400 uppercase">
              <tr>
                <th className="p-3">#</th>
                <th className="p-3">Review Text</th>
                <th className="p-3">Sentiment</th>
                <th className="p-3">Score</th>
                <th className="p-3">Confidence</th>
                <th className="p-3">Rating</th>
                <th className="p-3">Category</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {filteredReviews.slice(0, 50).map((r: any) => (
                <tr key={r.id} className="hover:bg-white/5">
                  <td className="p-3 text-slate-500 font-mono">{r.id}</td>
                  <td className="p-3 max-w-md font-mono text-slate-200">{r.text}</td>
                  <td className="p-3">
                    <span className={`px-2 py-1 rounded-full text-[10px] font-bold ${
                      r.sentiment === 'Positive' ? 'bg-emerald-500/20 text-emerald-400' :
                      r.sentiment === 'Negative' ? 'bg-red-500/20 text-red-400' : 'bg-amber-500/20 text-amber-400'
                    }`}>
                      {r.sentiment}
                    </span>
                  </td>
                  <td className="p-3 font-bold">{r.score > 0 ? `+${r.score}` : r.score}</td>
                  <td className="p-3">{r.confidence}%</td>
                  <td className="p-3">{r.rating}</td>
                  <td className="p-3">{r.category}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
};
