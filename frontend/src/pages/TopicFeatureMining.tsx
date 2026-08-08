import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import { motion } from 'framer-motion';
import { Search, Compass, Tag, Info, FileText, Cloud, Layers, AlertTriangle, ThumbsUp, ThumbsDown, BarChart3 } from 'lucide-react';

interface TopicFeatureProps {
  onNavigate: (tab: string) => void;
}

export const TopicFeatureMining: React.FC<TopicFeatureProps> = ({ onNavigate }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchNLPData();
  }, []);

  const fetchNLPData = async () => {
    try {
      setLoading(true);
      const res = await axios.get('/api/analytics/topics');
      setData(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load Topic & Aspect Mining analytics.');
    } finally {
      setLoading(false);
    }
  };

  const plotlyLayout: any = {
    font: { family: 'Inter, sans-serif', color: '#FFFFFF' },
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
  };

  if (loading) return <div className="p-8 text-center text-slate-400">Extracting N-Grams, LDA Topics & Aspect Radar Features...</div>;
  if (error || !data) {
    return (
      <div className="p-8 max-w-xl mx-auto text-center">
        <div className="glass-card p-8">
          <p className="text-red-400 font-semibold mb-4">{error || 'No active dataset loaded.'}</p>
          <button onClick={() => onNavigate('upload')} className="px-6 py-3 rounded-xl bg-purple-600 text-white font-bold text-sm">
            Upload Dataset
          </button>
        </div>
      </div>
    );
  }

  const topics = data.topics || [];
  const aspects = data.aspects || [];
  const complaints = data.complaints || [];
  const topUnigrams = data.top_unigrams || [];
  const topBigrams = data.top_bigrams || [];
  const topTrigrams = data.top_trigrams || [];
  const textStats = data.text_statistics || {};
  const positivePhrases = data.positive_phrases || [];
  const negativePhrases = data.negative_phrases || [];

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* Header Banner */}
      <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-8 border-purple-500/20">
        <div className="flex items-center gap-3 mb-2">
          <Search className="w-6 h-6 text-purple-400" />
          <h2 className="text-2xl font-bold text-white">Topic Discovery, N-Grams & Aspect Feature Mining</h2>
        </div>
        <p className="text-slate-400 text-sm">
          Comprehensive NLP suite: N-gram keyphrase frequency, word cloud, LDA topic modeling, aspect sentiment radar, and praise/complaint phrase mining.
        </p>
      </motion.div>

      {/* 1. TEXT STATISTICS */}
      <div className="space-y-4">
        <h3 className="text-xl font-bold text-white flex items-center gap-2">
          <FileText className="w-5 h-5 text-cyan-400" />
          Section A — Text Statistics & Length Distribution
        </h3>
        
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div className="glass-card p-4 border-l-4 border-l-purple-500">
            <span className="text-[10px] font-bold text-slate-400 uppercase block mb-1">Total Documents</span>
            <p className="text-xl font-black text-white">{textStats.total_documents?.toLocaleString()}</p>
            <span className="text-[10px] text-purple-400">Records</span>
          </div>

          <div className="glass-card p-4 border-l-4 border-l-cyan-500">
            <span className="text-[10px] font-bold text-slate-400 uppercase block mb-1">Avg Words / Doc</span>
            <p className="text-xl font-black text-white">{textStats.avg_words_per_doc}</p>
            <span className="text-[10px] text-cyan-400">Words</span>
          </div>

          <div className="glass-card p-4 border-l-4 border-l-emerald-500">
            <span className="text-[10px] font-bold text-slate-400 uppercase block mb-1">Avg Chars / Doc</span>
            <p className="text-xl font-black text-white">{textStats.avg_chars_per_doc}</p>
            <span className="text-[10px] text-emerald-400">Characters</span>
          </div>

          <div className="glass-card p-4 border-l-4 border-l-amber-500">
            <span className="text-[10px] font-bold text-slate-400 uppercase block mb-1">Min Text Length</span>
            <p className="text-xl font-black text-white">{textStats.min_words}</p>
            <span className="text-[10px] text-amber-400">Words</span>
          </div>

          <div className="glass-card p-4 border-l-4 border-l-pink-500">
            <span className="text-[10px] font-bold text-slate-400 uppercase block mb-1">Max Text Length</span>
            <p className="text-xl font-black text-white">{textStats.max_words}</p>
            <span className="text-[10px] text-pink-400">Words</span>
          </div>
        </div>

        {/* Character Length Distribution Histogram */}
        {textStats.lengths_distribution && (
          <div className="glass-card p-6">
            <h4 className="text-base font-bold text-white mb-2">Review Character Length Distribution</h4>
            <Plot
              data={[
                {
                  x: textStats.lengths_distribution,
                  type: 'histogram',
                  marker: { color: '#7C3AED' },
                  name: 'Review Length'
                }
              ]}
              layout={{
                ...plotlyLayout,
                margin: { l: 65, r: 25, t: 25, b: 60 },
                xaxis: { title: { text: 'Character Count per Review (Chars)', font: { size: 12, color: '#94A3B8' } }, gridcolor: 'rgba(255,255,255,0.05)' },
                yaxis: { title: { text: 'Number of Reviews (Frequency)', font: { size: 12, color: '#94A3B8' } }, gridcolor: 'rgba(255,255,255,0.05)' },
                height: 280
              }}
              useResizeHandler
              className="w-full"
            />
          </div>
        )}
      </div>

      {/* 2. WORD CLOUD VISUALIZATION */}
      <div className="space-y-4">
        <h3 className="text-xl font-bold text-white flex items-center gap-2">
          <Cloud className="w-5 h-5 text-purple-400" />
          Section B — Word Cloud & High Frequency Corpus Keywords
        </h3>
        
        <div className="glass-card p-6 flex flex-col items-center">
          {data.wordcloud_base64 ? (
            <img src={data.wordcloud_base64} alt="Dataset Word Cloud" className="rounded-xl border border-white/10 max-h-[380px] object-contain w-full" />
          ) : (
            <p className="text-slate-400 text-sm">Insufficient text for word cloud generation.</p>
          )}
        </div>
      </div>

      {/* 3. N-GRAM ANALYSIS (UNIGRAMS, BIGRAMS, TRIGRAMS) */}
      <div className="space-y-4">
        <h3 className="text-xl font-bold text-white flex items-center gap-2">
          <BarChart3 className="w-5 h-5 text-emerald-400" />
          Section C — N-Gram Keyphrase Frequency Analysis (Unigrams, Bigrams & Trigrams)
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Top 15 Unigrams */}
          <div className="glass-card p-6">
            <h4 className="text-lg font-bold text-white mb-1">Top 15 Single Words (Unigrams)</h4>
            <p className="text-xs text-slate-400 mb-4">Most frequent individual words</p>
            <Plot
              data={[
                {
                  x: topUnigrams.map((item: any) => item.frequency),
                  y: topUnigrams.map((item: any) => item.word),
                  type: 'bar',
                  orientation: 'h',
                  marker: { color: '#06B6D4' }
                }
              ]}
              layout={{
                ...plotlyLayout,
                margin: { l: 110, r: 20, t: 20, b: 50 },
                xaxis: { title: { text: 'Frequency (Occurrences)', font: { size: 11, color: '#94A3B8' } }, gridcolor: 'rgba(255,255,255,0.05)' },
                yaxis: { title: { text: 'Unigram Word', font: { size: 11, color: '#94A3B8' } }, gridcolor: 'rgba(255,255,255,0.05)', autorange: 'reversed', automargin: true },
                height: 380
              }}
              useResizeHandler
              className="w-full"
            />
          </div>

          {/* Top 15 Bigrams */}
          <div className="glass-card p-6">
            <h4 className="text-lg font-bold text-white mb-1">Top 15 Bigrams (2-word phrases)</h4>
            <p className="text-xs text-slate-400 mb-4">Most frequent 2-word combinations</p>
            <Plot
              data={[
                {
                  x: topBigrams.map((item: any) => item.frequency),
                  y: topBigrams.map((item: any) => item.word),
                  type: 'bar',
                  orientation: 'h',
                  marker: { color: '#7C3AED' }
                }
              ]}
              layout={{
                ...plotlyLayout,
                margin: { l: 130, r: 20, t: 20, b: 50 },
                xaxis: { title: { text: 'Frequency (Occurrences)', font: { size: 11, color: '#94A3B8' } }, gridcolor: 'rgba(255,255,255,0.05)' },
                yaxis: { title: { text: 'Bigram Phrase', font: { size: 11, color: '#94A3B8' } }, gridcolor: 'rgba(255,255,255,0.05)', autorange: 'reversed', automargin: true },
                height: 380
              }}
              useResizeHandler
              className="w-full"
            />
          </div>

          {/* Top 15 Trigrams */}
          <div className="glass-card p-6">
            <h4 className="text-lg font-bold text-white mb-1">Top 15 Trigrams (3-word phrases)</h4>
            <p className="text-xs text-slate-400 mb-4">Most frequent 3-word combinations</p>
            <Plot
              data={[
                {
                  x: topTrigrams.map((item: any) => item.frequency),
                  y: topTrigrams.map((item: any) => item.word),
                  type: 'bar',
                  orientation: 'h',
                  marker: { color: '#22C55E' }
                }
              ]}
              layout={{
                ...plotlyLayout,
                margin: { l: 140, r: 20, t: 20, b: 50 },
                xaxis: { title: { text: 'Frequency (Occurrences)', font: { size: 11, color: '#94A3B8' } }, gridcolor: 'rgba(255,255,255,0.05)' },
                yaxis: { title: { text: 'Trigram Phrase', font: { size: 11, color: '#94A3B8' } }, gridcolor: 'rgba(255,255,255,0.05)', autorange: 'reversed', automargin: true },
                height: 380
              }}
              useResizeHandler
              className="w-full"
            />
          </div>
        </div>
      </div>

      {/* 4. LDA TOPIC DISCOVERY */}
      <div className="space-y-4">
        <h3 className="text-xl font-bold text-white flex items-center gap-2">
          <Compass className="w-5 h-5 text-cyan-400" />
          Section D — LDA Topic Modeling & Feature Clusters
        </h3>

        <div className="glass-card p-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {topics.map((t: any, idx: number) => (
              <div key={idx} className="p-5 rounded-xl bg-slate-900/60 border border-white/10 space-y-2">
                <span className="text-xs font-bold text-purple-400 uppercase tracking-wider">{t.topic_id}</span>
                <p className="text-base font-bold text-white">{t.keywords}</p>
                <div className="flex flex-wrap gap-1.5 mt-2">
                  {t.top_words?.map((w: string, i: number) => (
                    <span key={i} className="px-2.5 py-1 rounded-md bg-purple-500/10 border border-purple-500/20 text-purple-300 text-xs font-medium">
                      #{w}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 5. ASPECT MINING & ASPECT X SENTIMENT */}
      <div className="space-y-4">
        <h3 className="text-xl font-bold text-white flex items-center gap-2">
          <Layers className="w-5 h-5 text-amber-400" />
          Section E — Aspect Mining & Aspect × Sentiment Breakdown
        </h3>

        {aspects.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="glass-card p-6">
              <h4 className="text-lg font-bold text-white mb-2">Aspect Feature Positivity Radar (%)</h4>
              <p className="text-xs text-slate-400 mb-4">Aspect satisfaction percentage across polar feature vectors</p>
              <Plot
                data={[
                  {
                    r: aspects.map((a: any) => a.positive_score),
                    theta: aspects.map((a: any) => a.aspect),
                    type: 'scatterpolar',
                    fill: 'toself',
                    marker: { color: '#06B6D4' }
                  }
                ]}
                layout={{
                  ...plotlyLayout,
                  polar: { radialaxis: { visible: true, range: [0, 100] } },
                  margin: { l: 40, r: 40, t: 30, b: 40 },
                  height: 340
                }}
                useResizeHandler
                className="w-full"
              />
            </div>

            <div className="glass-card p-6">
              <h4 className="text-lg font-bold text-white mb-2">Aspect Sentiment Stacked Breakdown</h4>
              <p className="text-xs text-slate-400 mb-4">Positive, Neutral and Negative review counts per aspect</p>
              <Plot
                data={[
                  {
                    x: aspects.map((a: any) => a.aspect),
                    y: aspects.map((a: any) => a.positive_count),
                    name: 'Positive',
                    type: 'bar',
                    marker: { color: '#22C55E' }
                  },
                  {
                    x: aspects.map((a: any) => a.aspect),
                    y: aspects.map((a: any) => a.neutral_count),
                    name: 'Neutral',
                    type: 'bar',
                    marker: { color: '#FACC15' }
                  },
                  {
                    x: aspects.map((a: any) => a.aspect),
                    y: aspects.map((a: any) => a.negative_count),
                    name: 'Negative',
                    type: 'bar',
                    marker: { color: '#EF4444' }
                  }
                ]}
                layout={{
                  ...plotlyLayout,
                  barmode: 'stack',
                  margin: { l: 40, r: 20, t: 20, b: 60 },
                  xaxis: { title: { text: 'Aspect', font: { size: 11, color: '#94A3B8' } }, gridcolor: 'rgba(255,255,255,0.05)' },
                  yaxis: { title: { text: 'Review Count', font: { size: 11, color: '#94A3B8' } }, gridcolor: 'rgba(255,255,255,0.05)' },
                  height: 340
                }}
                useResizeHandler
                className="w-full"
              />
            </div>
          </div>
        ) : (
          <div className="glass-card p-6 text-center text-slate-400">
            No aspect features extracted for current dataset.
          </div>
        )}
      </div>

      {/* 6. COMPLAINT & PRAISE PHRASE MINING */}
      <div className="space-y-4">
        <h3 className="text-xl font-bold text-white flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-red-400" />
          Section F — Complaint, Praise & Sentiment Phrase Mining
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Praise & Positive Phrases */}
          <div className="glass-card p-6">
            <h4 className="text-lg font-bold text-emerald-400 flex items-center gap-2 mb-1">
              <ThumbsUp className="w-5 h-5" />
              Praise & Positive Keyphrase Mining
            </h4>
            <p className="text-xs text-slate-400 mb-4">Top keyphrases extracted from positive customer feedback</p>
            
            <div className="space-y-2">
              {positivePhrases.slice(0, 10).map((item: any, idx: number) => (
                <div key={idx} className="flex items-center justify-between p-2.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-xs">
                  <span className="font-semibold text-emerald-200">#{idx + 1} {item.word}</span>
                  <span className="font-bold text-emerald-400">{item.frequency} occurrences</span>
                </div>
              ))}
            </div>
          </div>

          {/* Complaints & Friction Themes */}
          <div className="glass-card p-6">
            <h4 className="text-lg font-bold text-red-400 flex items-center gap-2 mb-1">
              <ThumbsDown className="w-5 h-5" />
              Complaint & Friction Theme Mining
            </h4>
            <p className="text-xs text-slate-400 mb-4">Top customer complaint categories and pain points</p>

            {complaints.length > 0 ? (
              <Plot
                data={[
                  {
                    x: complaints.map((c: any) => c.count),
                    y: complaints.map((c: any) => c.category),
                    type: 'bar',
                    orientation: 'h',
                    marker: { color: '#EF4444' }
                  }
                ]}
                layout={{
                  ...plotlyLayout,
                  margin: { l: 140, r: 20, t: 20, b: 50 },
                  xaxis: { title: { text: 'Complaint Count', font: { size: 11, color: '#94A3B8' } }, gridcolor: 'rgba(255,255,255,0.05)' },
                  yaxis: { title: { text: 'Complaint Category', font: { size: 11, color: '#94A3B8' } }, gridcolor: 'rgba(255,255,255,0.05)', autorange: 'reversed', automargin: true },
                  height: 320
                }}
                useResizeHandler
                className="w-full"
              />
            ) : (
              <div className="space-y-2">
                {negativePhrases.slice(0, 10).map((item: any, idx: number) => (
                  <div key={idx} className="flex items-center justify-between p-2.5 rounded-lg bg-red-500/10 border border-red-500/20 text-xs">
                    <span className="font-semibold text-red-200">#{idx + 1} {item.word}</span>
                    <span className="font-bold text-red-400">{item.frequency} occurrences</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
