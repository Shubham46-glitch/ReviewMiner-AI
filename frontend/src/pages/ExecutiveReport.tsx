import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Download, FileText, CheckCircle, Award, Lightbulb, ShieldAlert, Sparkles } from 'lucide-react';

interface ExecutiveReportProps {
  onNavigate?: (tab: string) => void;
}

export const ExecutiveReport: React.FC<ExecutiveReportProps> = ({ onNavigate }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    fetchBI();
  }, []);

  const fetchBI = async () => {
    try {
      const res = await axios.get('/api/analytics/business-intelligence');
      setData(res.data);
    } catch (err) {
      console.error("Failed to load BI report data:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = async () => {
    setDownloading(true);
    try {
      const response = await axios.get('/api/analytics/export-pdf', {
        responseType: 'blob'
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'Executive_BI_Report.pdf');
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error("PDF export failed:", err);
    } finally {
      setDownloading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[500px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-cyan-500" />
      </div>
    );
  }

  const kpis = data?.kpi_summary || {};
  const actionPlan = data?.action_plan || [];
  const strongest = data?.strongest_business_areas || [];
  const problems = data?.priority_problems || [];

  return (
    <div className="p-8 space-y-8 max-w-6xl mx-auto text-slate-100">
      
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 glass-card p-6 border-purple-500/20">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-purple-500/20 border border-purple-500/30 flex items-center justify-center text-purple-300">
            <FileText className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-3xl font-black text-white tracking-tight">
              Executive PDF Report & Management Brief
            </h1>
            <p className="text-slate-400 text-sm mt-0.5">
              Downloadable C-suite executive briefing document with KPIs, strategic findings, risk matrix, and action plan.
            </p>
          </div>
        </div>

        <button
          onClick={handleDownloadPDF}
          disabled={downloading}
          className="inline-flex items-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-purple-600 to-cyan-500 hover:from-purple-500 hover:to-cyan-400 text-white font-bold text-sm shadow-xl shadow-purple-500/30 transition-all shrink-0"
        >
          <Download className="w-5 h-5" />
          <span>{downloading ? 'Generating PDF...' : 'Download Executive PDF Report'}</span>
        </button>
      </div>

      {/* Report Document Preview Container */}
      <div className="glass-card p-8 space-y-8 border-white/10 bg-slate-900/80">
        
        {/* Document Header */}
        <div className="border-b border-white/10 pb-6 flex items-center justify-between">
          <div>
            <div className="text-xs font-bold text-cyan-400 uppercase tracking-widest">ReviewMiner AI • Official Briefing</div>
            <h2 className="text-2xl font-black text-white mt-1">Executive Business Intelligence Report</h2>
          </div>
          <span className="text-xs font-semibold px-3 py-1.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
            Status: Ready for Executive Review
          </span>
        </div>

        {/* 1. Executive Summary Synthesis */}
        <div className="space-y-3">
          <h3 className="text-sm font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-2">
            <Lightbulb className="w-4 h-4" /> 1. Executive Summary
          </h3>
          <p className="text-slate-200 text-base leading-relaxed p-5 rounded-xl bg-slate-950/60 border border-white/5 font-medium">
            {data?.executive_summary}
          </p>
        </div>

        {/* 2. Executive KPI Overview */}
        <div className="space-y-3">
          <h3 className="text-sm font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-2">
            <Award className="w-4 h-4" /> 2. Executive KPI Scorecard
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="p-4 rounded-xl bg-slate-950/60 border border-white/5">
              <span className="text-xs text-slate-400 uppercase font-semibold">Satisfaction Index</span>
              <div className="text-2xl font-black text-white mt-1">{kpis.satisfaction_index ?? 0}%</div>
            </div>
            <div className="p-4 rounded-xl bg-slate-950/60 border border-white/5">
              <span className="text-xs text-slate-400 uppercase font-semibold">Positive Feedback %</span>
              <div className="text-2xl font-black text-cyan-400 mt-1">{kpis.positive_pct ?? 0}%</div>
            </div>
            <div className="p-4 rounded-xl bg-slate-950/60 border border-white/5">
              <span className="text-xs text-slate-400 uppercase font-semibold">Dissatisfaction Rate</span>
              <div className="text-2xl font-black text-red-400 mt-1">{kpis.dissatisfaction_rate ?? 0}%</div>
            </div>
            <div className="p-4 rounded-xl bg-slate-950/60 border border-white/5">
              <span className="text-xs text-slate-400 uppercase font-semibold">Dominant Sentiment</span>
              <div className="text-2xl font-black text-purple-300 mt-1">{kpis.dominant_sentiment ?? 'N/A'}</div>
            </div>
          </div>
        </div>

        {/* 3. Primary Strengths & Risk Priorities */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-3">
            <h3 className="text-sm font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-2">
              <CheckCircle className="w-4 h-4" /> Strongest Brand Pillars
            </h3>
            <div className="space-y-2">
              {strongest.map((area: any, idx: number) => (
                <div key={idx} className="p-3.5 rounded-xl bg-emerald-500/5 border border-emerald-500/20 text-xs">
                  <div className="font-bold text-emerald-400 text-sm mb-1">{area.focus_area}</div>
                  <div className="text-slate-300">{area.evidence}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-3">
            <h3 className="text-sm font-bold text-red-400 uppercase tracking-wider flex items-center gap-2">
              <ShieldAlert className="w-4 h-4" /> Operational Friction Priorities
            </h3>
            <div className="space-y-2">
              {problems.map((prob: any, idx: number) => (
                <div key={idx} className="p-3.5 rounded-xl bg-red-500/5 border border-red-500/20 text-xs">
                  <div className="font-bold text-red-400 text-sm mb-1">{prob.priority} • {prob.issue}</div>
                  <div className="text-slate-300">{prob.evidence}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* 4. Ranked Executive Action Directives */}
        <div className="space-y-3">
          <h3 className="text-sm font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-2">
            <Sparkles className="w-4 h-4" /> 4. Actionable Executive Directives
          </h3>
          <div className="space-y-3">
            {actionPlan.map((act: any, idx: number) => (
              <div key={idx} className="p-4 rounded-xl bg-slate-950/60 border border-white/5 flex items-start gap-4">
                <span className="w-7 h-7 rounded-full bg-cyan-500/20 text-cyan-300 font-bold text-xs flex items-center justify-center shrink-0 mt-0.5 border border-cyan-500/30">
                  #{act.rank || idx + 1}
                </span>
                <div className="flex-1 text-xs">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-bold text-white text-sm">{act.domain}</span>
                    <span className="font-bold text-red-400 text-[10px] uppercase">IMPACT: {act.impact}</span>
                  </div>
                  <div className="text-slate-400 mb-1">Evidence: {act.evidence}</div>
                  <div className="text-emerald-400 font-bold text-xs">Directive: {act.action}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Bottom Download Footer */}
        <div className="pt-6 border-t border-white/10 flex flex-col md:flex-row items-center justify-between gap-4">
          <span className="text-xs text-slate-400">Export as formal PDF document for board presentations and operational planning.</span>
          <button
            onClick={handleDownloadPDF}
            disabled={downloading}
            className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-purple-600 to-cyan-500 hover:from-purple-500 hover:to-cyan-400 text-white font-bold text-sm shadow-lg transition-all"
          >
            <Download className="w-4 h-4" />
            <span>{downloading ? 'Generating PDF...' : 'Download Executive PDF Report'}</span>
          </button>
        </div>

      </div>

    </div>
  );
};
