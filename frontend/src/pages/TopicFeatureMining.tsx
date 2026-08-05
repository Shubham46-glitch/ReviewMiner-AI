import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import { motion } from 'framer-motion';
import { Search, Compass, ShieldCheck } from 'lucide-react';

interface TopicFeatureProps {
  onNavigate: (tab: string) => void;
}

export const TopicFeatureMining: React.FC<TopicFeatureProps> = ({ onNavigate }) => {
  const [topics, setTopics] = useState<any[]>([]);
  const [aspects, setAspects] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchNLPData();
  }, []);

  const fetchNLPData = async () => {
    try {
      setLoading(true);
      const [topRes, aspRes] = await Promise.all([
        axios.get('/api/analytics/topics'),
        axios.get('/api/analytics/aspects')
      ]);
      setTopics(topRes.data.topics || []);
      setAspects(aspRes.data.aspects || []);
    } catch (err) {
      setTopics([]);
      setAspects([]);
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

  if (loading) return <div className="p-8 text-center text-slate-400">Extracting LDA Topics & Aspect Radar Features...</div>;

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* Header Banner */}
      <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-8 border-purple-500/20">
        <div className="flex items-center gap-3 mb-2">
          <Search className="w-6 h-6 text-purple-400" />
          <h2 className="text-2xl font-bold text-white">LDA Topic Modeling & Aspect Feature Radar Analytics</h2>
        </div>
        <p className="text-slate-400 text-sm">
          Unsupervised topic clustering combined with aspect-based customer feature sentiment extraction:
        </p>
      </motion.div>

      {/* LDA Topic Modeling Cards */}
      <div className="glass-card p-8">
        <div className="flex items-center gap-2 mb-6">
          <Compass className="w-5 h-5 text-cyan-400" />
          <h3 className="text-xl font-bold text-white">Latent Dirichlet Allocation (LDA) Topic Clusters</h3>
        </div>

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

      {/* Aspect Feature Radar Chart */}
      {aspects.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="glass-card p-6">
            <h3 className="text-xl font-bold text-white mb-4">Aspect Feature Satisfaction Radar (%)</h3>
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
                height: 360
              }}
              useResizeHandler
              className="w-full"
            />
          </div>

          <div className="glass-card p-6">
            <h3 className="text-xl font-bold text-white mb-4">Feature Mention Frequency</h3>
            <Plot
              data={[
                {
                  x: aspects.map((a: any) => a.mentions),
                  y: aspects.map((a: any) => a.aspect),
                  type: 'bar',
                  orientation: 'h',
                  marker: { color: '#7C3AED' }
                }
              ]}
              layout={{ ...plotlyLayout, yaxis: { autorange: 'reversed' }, height: 360 }}
              useResizeHandler
              className="w-full"
            />
          </div>
        </div>
      )}
    </div>
  );
};
