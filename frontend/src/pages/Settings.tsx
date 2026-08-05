import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Settings as SettingsIcon, RefreshCw, Cpu, CheckCircle2 } from 'lucide-react';

export const Settings: React.FC = () => {
  const [health, setHealth] = useState<any>(null);
  const [loadingHealth, setLoadingHealth] = useState(true);

  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      setLoadingHealth(true);
      const res = await axios.get('/api/health');
      setHealth(res.data);
    } catch (err) {
      setHealth({ status: "offline", service: "FastAPI Engine Offline" });
    } finally {
      setLoadingHealth(false);
    }
  };

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-8 border-purple-500/20">
        <div className="flex items-center gap-3 mb-2">
          <SettingsIcon className="w-6 h-6 text-purple-400" />
          <h2 className="text-2xl font-bold text-white">Platform Settings & System Monitor</h2>
        </div>
        <p className="text-slate-400 text-sm">
          System health monitoring, model retrain triggers, and application controls:
        </p>
      </motion.div>

      {/* Health Monitor */}
      <div className="glass-card p-8">
        <h3 className="text-xl font-bold text-white mb-6">Backend Engine Health</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-5 rounded-xl bg-slate-900/60 border border-white/10">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-1">API Engine Status</span>
            <span className="text-lg font-bold text-emerald-400 flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
              {health?.status === 'online' ? 'FastAPI Engine Online' : 'Connecting...'}
            </span>
          </div>

          <div className="p-5 rounded-xl bg-slate-900/60 border border-white/10">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-1">NLP Subsystem</span>
            <span className="text-lg font-bold text-cyan-400">NLTK + Scikit-Learn</span>
          </div>

          <div className="p-5 rounded-xl bg-slate-900/60 border border-white/10">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-1">Engine Version</span>
            <span className="text-lg font-bold text-purple-400">v2.0.0 Enterprise</span>
          </div>
        </div>

        <div className="mt-6">
          <button
            onClick={checkHealth}
            disabled={loadingHealth}
            className="flex items-center gap-2 px-6 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm font-semibold transition-all"
          >
            <RefreshCw className={`w-4 h-4 ${loadingHealth ? 'animate-spin' : ''}`} />
            <span>Check Engine Health</span>
          </button>
        </div>
      </div>
    </div>
  );
};
