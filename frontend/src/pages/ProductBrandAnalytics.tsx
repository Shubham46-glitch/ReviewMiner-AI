import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import { motion } from 'framer-motion';
import { Building2, Package, Tag, Star } from 'lucide-react';

interface ProductBrandProps {
  onNavigate: (tab: string) => void;
}

export const ProductBrandAnalytics: React.FC<ProductBrandProps> = ({ onNavigate }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const res = await axios.get('/api/dataset/active');
      setData(res.data);
    } catch (err) {
      setData(null);
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

  if (loading) return <div className="p-8 text-center text-slate-400">Loading Product & Brand Analytics...</div>;

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-8 border-purple-500/20">
        <div className="flex items-center gap-3 mb-2">
          <Building2 className="w-6 h-6 text-purple-400" />
          <h2 className="text-2xl font-bold text-white">Product & Brand Intelligence</h2>
        </div>
        <p className="text-slate-400 text-sm">
          Dynamic catalog breakdown and hierarchical brand/product distributions:
        </p>
      </motion.div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="glass-card p-6 border-l-4 border-l-purple-500">
          <div className="flex items-center gap-2 text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">
            <Package className="w-4 h-4 text-purple-400" />
            <span>Active Dataset</span>
          </div>
          <p className="text-xl font-bold text-white truncate">{data?.name || 'Uploaded Data'}</p>
          <span className="text-xs text-purple-400">{data?.row_count?.toLocaleString()} rows</span>
        </div>

        <div className="glass-card p-6 border-l-4 border-l-cyan-500">
          <div className="flex items-center gap-2 text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">
            <Tag className="w-4 h-4 text-cyan-400" />
            <span>Text Column</span>
          </div>
          <p className="text-xl font-bold text-cyan-400 truncate">{data?.mapped?.text_col || 'Detected'}</p>
          <span className="text-xs text-slate-400">Mapped text</span>
        </div>

        <div className="glass-card p-6 border-l-4 border-l-emerald-500">
          <div className="flex items-center gap-2 text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">
            <Star className="w-4 h-4 text-emerald-400" />
            <span>Label Status</span>
          </div>
          <p className="text-xl font-bold text-emerald-400">{data?.has_labels ? 'True Labels' : 'AI VADER'}</p>
          <span className="text-xs text-slate-400">Sentiment source</span>
        </div>

        <div className="glass-card p-6 border-l-4 border-l-amber-500">
          <div className="flex items-center gap-2 text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">
            <Building2 className="w-4 h-4 text-amber-400" />
            <span>Category Column</span>
          </div>
          <p className="text-xl font-bold text-amber-400 truncate">{data?.mapped?.plat_col || 'General'}</p>
          <span className="text-xs text-slate-400">Segment filter</span>
        </div>
      </div>
    </div>
  );
};
