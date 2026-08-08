import React from 'react';
import { 
  Upload,
  Home, 
  BarChart3, 
  Sparkles, 
  Smile, 
  Cpu, 
  TrendingUp, 
  Layers, 
  Settings,
  Lock,
  Wrench,
  Cloud,
  FileText
} from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  isUploaded?: boolean;
  onDisabledClick?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ 
  activeTab, 
  setActiveTab, 
  isUploaded = false,
  onDisabledClick 
}) => {
  const menuItems = [
    { id: 'upload', label: 'Upload Dataset', icon: Upload, isFirst: true },
    { id: 'landing', label: 'Dashboard', icon: Home },
    { id: 'eda', label: 'EDA Analytics', icon: BarChart3 },
    { id: 'topic', label: 'Topic & Aspect Mining', icon: Sparkles },
    { id: 'sentiment', label: 'Sentiment Analysis', icon: Smile },
    { id: 'ml', label: 'Machine Learning', icon: Cpu },
    { id: 'prediction', label: 'Prediction', icon: Sparkles },
    { id: 'bi', label: 'Business Intelligence', icon: TrendingUp },
    { id: 'comparison', label: 'AI Insights', icon: Layers },
    { id: 'report', label: 'Executive Report', icon: FileText },
    { id: 'settings', label: 'Platform Settings', icon: Settings },
  ];

  return (
    <aside className="w-64 bg-[#0B1220]/90 backdrop-blur-xl border-r border-purple-500/15 flex flex-col h-screen sticky top-0 z-50 select-none">
      {/* Brand Header */}
      <div className="p-5 border-b border-white/5 flex flex-col items-center justify-center text-center">
        <h1 className="text-2xl font-black animated-gradient-text tracking-tight">
          ReviewMiner AI
        </h1>
        <p className="text-xs font-semibold text-cyan-400 tracking-wider uppercase mt-1">
          Text Analytics Platform
        </p>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto custom-scrollbar">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          const isLocked = !isUploaded && item.id !== 'upload';

          return (
            <button
              key={item.id}
              onClick={() => {
                if (isLocked) {
                  if (onDisabledClick) onDisabledClick();
                } else {
                  setActiveTab(item.id);
                }
              }}
              className={`w-full flex items-center justify-between px-4 py-3 rounded-xl font-medium text-sm transition-all duration-200 ${
                isActive
                  ? 'bg-gradient-to-r from-purple-600 to-cyan-500 text-white font-bold shadow-lg shadow-purple-500/30 border border-cyan-400/50'
                  : isLocked
                  ? 'opacity-45 text-slate-500 hover:text-slate-400 hover:bg-slate-900/50 cursor-not-allowed border border-transparent'
                  : 'text-slate-400 hover:text-white hover:bg-purple-600/20 hover:border-purple-500/30 border border-transparent'
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon className={`w-4 h-4 ${isActive ? 'text-white' : isLocked ? 'text-slate-600' : 'text-purple-400'}`} />
                <span>{item.label}</span>
              </div>
              {isLocked && <Lock className="w-3.5 h-3.5 text-slate-500" />}
            </button>
          );
        })}
      </nav>

      {/* Footer System Status */}
      <div className="p-4 border-t border-white/5 bg-slate-900/40">
        <div className="flex items-center justify-between text-xs text-slate-400">
          <span>Engine Status</span>
          <span className="flex items-center gap-1.5 text-emerald-400 font-semibold">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            {isUploaded ? 'Dataset Active' : 'Upload Required'}
          </span>
        </div>
      </div>
    </aside>
  );
};
