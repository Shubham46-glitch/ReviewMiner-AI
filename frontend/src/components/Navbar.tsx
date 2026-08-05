import React from 'react';
import { Database, FileSpreadsheet, Sparkles } from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  datasetInfo: any;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, datasetInfo }) => {
  const getTitle = () => {
    switch (activeTab) {
      case 'landing': return 'Overview & Architecture';
      case 'upload': return 'Dataset Upload & Schema Detection';
      case 'preprocessing': return 'Text Cleaning & Tokenization';
      case 'eda': return 'Exploratory Data Analysis';
      case 'sentiment': return 'Sentiment Distribution Dashboard';
      case 'wordcloud': return 'Word Cloud & Term Analytics';
      case 'ml': return 'Machine Learning Classification';
      case 'prediction': return 'Live Sentiment Predictor';
      case 'bi': return 'Business Intelligence & Executive PDF Report';
      case 'comparison': return 'Multi-Dataset Comparison Engine';
      case 'settings': return 'Platform Settings & System Health';
      default: return 'ReviewMiner AI';
    }
  };

  return (
    <header className="h-16 border-b border-white/5 bg-[#0B1220]/80 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-40">
      <div className="flex items-center gap-3">
        <h2 className="text-lg font-bold text-white tracking-wide">
          {getTitle()}
        </h2>
      </div>

      <div className="flex items-center gap-4">
        {datasetInfo && datasetInfo.active ? (
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-semibold">
            <FileSpreadsheet className="w-3.5 h-3.5" />
            <span className="max-w-[180px] truncate">{datasetInfo.name}</span>
            <span className="px-1.5 py-0.5 rounded bg-cyan-500/20 text-[10px]">
              {datasetInfo.row_count?.toLocaleString()} rows
            </span>
          </div>
        ) : (
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-purple-500/10 border border-purple-500/30 text-purple-400 text-xs font-semibold">
            <Database className="w-3.5 h-3.5" />
            <span>No Active Dataset</span>
          </div>
        )}

        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-800/60 border border-white/10 text-slate-300 text-xs font-medium">
          <Sparkles className="w-3.5 h-3.5 text-purple-400" />
          <span>v2.0 Enterprise</span>
        </div>
      </div>
    </header>
  );
};
