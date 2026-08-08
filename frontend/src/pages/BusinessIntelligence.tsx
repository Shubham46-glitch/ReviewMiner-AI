import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import { motion } from 'framer-motion';
import { Download, ThumbsUp, AlertTriangle, ShieldAlert, CheckCircle, ArrowRight, Zap, Target, TrendingUp } from 'lucide-react';

interface BusinessIntelligenceProps {
  onNavigate?: (tab: string) => void;
}

export const BusinessIntelligence: React.FC<BusinessIntelligenceProps> = ({ onNavigate }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);
  const [selectedDomain, setSelectedDomain] = useState<string | null>(null);

  useEffect(() => {
    fetchBI();
  }, []);

  const fetchBI = async () => {
    try {
      const res = await axios.get('/api/analytics/business-intelligence');
      setData(res.data);
    } catch (err) {
      console.error("Failed to load Business Intelligence data:", err);
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
  const viz = data?.visualizations || {};
  const posDrivers = viz.positive_drivers || [];
  const negDrivers = viz.negative_drivers || [];
  const strengthVsPain = viz.strength_vs_pain || [];
  const riskBubbles = viz.risk_bubbles || [];
  const oppRanking = viz.opportunity_ranking || [];
  const actionPlan = data?.action_plan || [];

  const plotlyBaseLayout: any = {
    font: { family: 'Inter, sans-serif', color: '#94A3B8' },
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    margin: { l: 150, r: 40, t: 30, b: 40 },
    xaxis: { gridcolor: 'rgba(255,255,255,0.05)', color: '#94A3B8' },
    yaxis: { gridcolor: 'rgba(255,255,255,0.05)', color: '#94A3B8' },
  };

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto text-slate-100">
      
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 glass-card p-6 border-cyan-500/20">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-black text-white tracking-tight">
              Executive Analytics & Strategic BI Dashboard
            </h1>
            {selectedDomain && (
              <button
                onClick={() => setSelectedDomain(null)}
                className="text-xs px-3 py-1 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 hover:bg-cyan-500/30 transition-colors"
              >
                Clear Filter: <strong>{selectedDomain}</strong> ✕
              </button>
            )}
          </div>
          <p className="text-slate-400 text-sm mt-1">
            Data-driven strategic decision support matrix, risk profiling, and actionable executive directives.
          </p>
        </div>

        <button
          onClick={handleDownloadPDF}
          disabled={downloading}
          className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-purple-600 to-cyan-500 hover:from-purple-500 hover:to-cyan-400 text-white font-bold text-sm shadow-lg shadow-purple-500/20 transition-all shrink-0"
        >
          <Download className="w-4 h-4" />
          <span>{downloading ? 'Generating PDF...' : 'Export Executive PDF Report'}</span>
        </button>
      </div>

      {/* 1. EXECUTIVE KPI HEADER */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        
        {/* KPI 1: Top Positive Driver */}
        <motion.div
          initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.05 }}
          onClick={() => setSelectedDomain(kpis.top_positive_driver)}
          className={`glass-card p-5 border-l-4 border-l-cyan-500 cursor-pointer transition-all ${selectedDomain === kpis.top_positive_driver ? 'ring-2 ring-cyan-500 bg-cyan-500/10' : 'hover:border-cyan-400'}`}
        >
          <div className="flex items-center justify-between text-slate-400 text-xs font-bold uppercase tracking-wider mb-1">
            <span>Top Positive Driver</span>
            <ThumbsUp className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-xl font-bold text-white truncate">{kpis.top_positive_driver || 'Product Quality'}</div>
          <div className="text-2xl font-black text-cyan-400 mt-1">{kpis.top_positive_pct || 0}%</div>
          <div className="text-[10px] text-slate-500 mt-1">Primary customer satisfaction share</div>
        </motion.div>

        {/* KPI 2: Top Customer Pain Point */}
        <motion.div
          initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
          onClick={() => setSelectedDomain(kpis.top_negative_driver)}
          className={`glass-card p-5 border-l-4 border-l-red-500 cursor-pointer transition-all ${selectedDomain === kpis.top_negative_driver ? 'ring-2 ring-red-500 bg-red-500/10' : 'hover:border-red-400'}`}
        >
          <div className="flex items-center justify-between text-slate-400 text-xs font-bold uppercase tracking-wider mb-1">
            <span>Top Customer Pain Point</span>
            <AlertTriangle className="w-4 h-4 text-red-400" />
          </div>
          <div className="text-xl font-bold text-white truncate">{kpis.top_negative_driver || 'Product Quality'}</div>
          <div className="text-2xl font-black text-red-400 mt-1">{kpis.top_negative_pct || 0}%</div>
          <div className="text-[10px] text-slate-500 mt-1">Largest negative complaint share</div>
        </motion.div>

        {/* KPI 3: Quality Complaints */}
        <motion.div
          initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }}
          onClick={() => setSelectedDomain('Product Quality & Build')}
          className={`glass-card p-5 border-l-4 border-l-amber-500 cursor-pointer transition-all ${selectedDomain === 'Product Quality & Build' ? 'ring-2 ring-amber-500 bg-amber-500/10' : 'hover:border-amber-400'}`}
        >
          <div className="text-slate-400 text-xs font-bold uppercase tracking-wider mb-1">Quality Complaints</div>
          <div className="text-3xl font-black text-white">{kpis.quality_complaints || 0}</div>
          <div className="text-xs text-amber-400 font-semibold mt-1">reviews flagged</div>
          <div className="text-[10px] text-slate-500 mt-0.5">Build & durability issues</div>
        </motion.div>

        {/* KPI 4: Delivery Complaints */}
        <motion.div
          initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
          onClick={() => setSelectedDomain('Delivery & Logistics')}
          className={`glass-card p-5 border-l-4 border-l-purple-500 cursor-pointer transition-all ${selectedDomain === 'Delivery & Logistics' ? 'ring-2 ring-purple-500 bg-purple-500/10' : 'hover:border-purple-400'}`}
        >
          <div className="text-slate-400 text-xs font-bold uppercase tracking-wider mb-1">Delivery Complaints</div>
          <div className="text-3xl font-black text-white">{kpis.delivery_complaints || 0}</div>
          <div className="text-xs text-purple-400 font-semibold mt-1">reviews flagged</div>
          <div className="text-[10px] text-slate-500 mt-0.5">Shipping & delay friction</div>
        </motion.div>

        {/* KPI 5: Performance Complaints */}
        <motion.div
          initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.25 }}
          onClick={() => setSelectedDomain('Performance & Battery')}
          className={`glass-card p-5 border-l-4 border-l-blue-500 cursor-pointer transition-all ${selectedDomain === 'Performance & Battery' ? 'ring-2 ring-blue-500 bg-blue-500/10' : 'hover:border-blue-400'}`}
        >
          <div className="text-slate-400 text-xs font-bold uppercase tracking-wider mb-1">Performance Complaints</div>
          <div className="text-3xl font-black text-white">{kpis.performance_complaints || 0}</div>
          <div className="text-xs text-blue-400 font-semibold mt-1">reviews flagged</div>
          <div className="text-[10px] text-slate-500 mt-0.5">Battery & thermal issues</div>
        </motion.div>

      </div>

      {/* MIDDLE SECTION — POSITIVE & NEGATIVE DRIVERS HORIZONTAL BAR CHARTS */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        {/* 2. CUSTOMER STRENGTHS — HORIZONTAL BAR CHART */}
        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-6">
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <ThumbsUp className="w-5 h-5 text-cyan-400" /> Positive Review Drivers (%)
            </h2>
            <span className="text-xs text-slate-400">Sorted Descending</span>
          </div>
          {posDrivers.length > 0 ? (
            <Plot
              data={[
                {
                  x: posDrivers.map((d: any) => d.percentage).reverse(),
                  y: posDrivers.map((d: any) => d.domain).reverse(),
                  type: 'bar',
                  orientation: 'h',
                  text: posDrivers.map((d: any) => `${d.percentage}%`).reverse(),
                  textposition: 'inside',
                  marker: {
                    color: posDrivers.map((d: any) => {
                      if (selectedDomain && d.domain === selectedDomain) return '#38BDF8';
                      return d.domain.includes('Quality') ? '#06B6D4' : '#1E293B';
                    }).reverse(),
                    line: {
                      color: posDrivers.map((d: any) => d.domain.includes('Quality') ? '#38BDF8' : '#475569').reverse(),
                      width: 1.5
                    }
                  }
                } as any
              ]}
              layout={{
                ...plotlyBaseLayout,
                height: 250,
                xaxis: { title: { text: 'Positive Share (%)' }, range: [0, Math.max(...posDrivers.map((d: any) => d.percentage), 50) + 5] }
              } as any}
              onClick={(e: any) => {
                if (e.points && e.points[0]) {
                  setSelectedDomain(e.points[0].y);
                }
              }}
              useResizeHandler
              className="w-full cursor-pointer"
            />
          ) : (
            <div className="h-48 flex items-center justify-center text-slate-500 text-sm">No positive drivers data available</div>
          )}
        </motion.div>

        {/* 3. CUSTOMER PAIN POINTS — HORIZONTAL BAR CHART */}
        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-6">
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-red-400" /> Negative Complaint Drivers (%)
            </h2>
            <span className="text-xs text-slate-400">Share & Review Count</span>
          </div>
          {negDrivers.length > 0 ? (
            <Plot
              data={[
                {
                  x: negDrivers.map((d: any) => d.percentage).reverse(),
                  y: negDrivers.map((d: any) => d.domain).reverse(),
                  type: 'bar',
                  orientation: 'h',
                  text: negDrivers.map((d: any) => `${d.percentage}% (${d.count} rev)`).reverse(),
                  textposition: 'inside',
                  marker: {
                    color: negDrivers.map((d: any) => {
                      if (selectedDomain && d.domain === selectedDomain) return '#F87171';
                      return d.domain.includes('Quality') ? '#EF4444' : '#F97316';
                    }).reverse(),
                    line: {
                      color: '#F87171',
                      width: 1.5
                    }
                  }
                } as any
              ]}
              layout={{
                ...plotlyBaseLayout,
                height: 250,
                xaxis: { title: { text: 'Complaint Share (%)' }, range: [0, Math.max(...negDrivers.map((d: any) => d.percentage), 50) + 5] }
              } as any}
              onClick={(e: any) => {
                if (e.points && e.points[0]) {
                  setSelectedDomain(e.points[0].y);
                }
              }}
              useResizeHandler
              className="w-full cursor-pointer"
            />
          ) : (
            <div className="h-48 flex items-center justify-center text-slate-500 text-sm">No negative drivers data available</div>
          )}
        </motion.div>

      </div>

      {/* CENTRAL STRATEGIC SECTION — STRENGTH VS PAIN MATRIX & PRIORITY RISK MATRIX */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        {/* 4. CENTRAL FEATURE — STRENGTH VS PAIN MATRIX (2-AXIS QUADRANT CHART) */}
        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-6 border-cyan-500/30">
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Target className="w-5 h-5 text-cyan-400" /> Strength vs Pain Matrix (2-Axis Quadrant)
            </h2>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 font-bold border border-cyan-500/40">
              Strategic Matrix
            </span>
          </div>

          <Plot
            data={strengthVsPain.map((pt: any) => ({
              x: [pt.strength],
              y: [pt.pain],
              mode: 'markers+text',
              name: pt.domain,
              text: [pt.domain],
              textposition: 'top center',
              textfont: { color: '#FFFFFF', size: 11 },
              marker: {
                size: selectedDomain === pt.domain ? 24 : 18,
                color: pt.quadrant === 'Fix & Protect' ? '#EF4444' : pt.quadrant === 'Leverage & Promote' ? '#22C55E' : '#F59E0B',
                line: { color: '#FFFFFF', width: 2 }
              }
            })) as any}
            layout={{
              font: { family: 'Inter, sans-serif', color: '#94A3B8' },
              paper_bgcolor: 'rgba(0,0,0,0)',
              plot_bgcolor: 'rgba(0,0,0,0)',
              margin: { l: 60, r: 40, t: 30, b: 50 },
              height: 310,
              showlegend: false,
              xaxis: { title: { text: 'Customer Strength (%) →' }, range: [0, 55], gridcolor: 'rgba(255,255,255,0.05)' },
              yaxis: { title: { text: 'Customer Pain / Dissatisfaction (%) ↑' }, range: [0, 50], gridcolor: 'rgba(255,255,255,0.05)' },
              shapes: [
                { type: 'line', x0: 20, y0: 0, x1: 20, y1: 50, line: { color: 'rgba(255,255,255,0.15)', dash: 'dash' } },
                { type: 'line', x0: 0, y0: 15, x1: 55, y1: 15, line: { color: 'rgba(255,255,255,0.15)', dash: 'dash' } }
              ],
              annotations: [
                { x: 37, y: 38, text: '🔴 FIX & PROTECT', showarrow: false, font: { color: '#EF4444', size: 12 } },
                { x: 37, y: 7, text: '🟢 LEVERAGE & PROMOTE', showarrow: false, font: { color: '#22C55E', size: 12 } },
                { x: 8, y: 38, text: '🟠 MITIGATE FRICTION', showarrow: false, font: { color: '#F59E0B', size: 12 } },
                { x: 8, y: 7, text: '⚪ MONITOR', showarrow: false, font: { color: '#94A3B8', size: 12 } }
              ]
            } as any}
            onClick={(e: any) => {
              if (e.points && e.points[0]) {
                setSelectedDomain(e.points[0].data.name);
              }
            }}
            useResizeHandler
            className="w-full cursor-pointer"
          />

          {/* Central Callout Box */}
          <div className="mt-3 p-3.5 rounded-xl bg-slate-900/90 border border-cyan-500/30 flex items-center gap-3">
            <Zap className="w-5 h-5 text-cyan-400 shrink-0" />
            <p className="text-xs text-slate-200 font-semibold leading-relaxed">
              <strong>Core Executive Insight:</strong> Product Quality & Build is simultaneously the brand's <u>biggest competitive strength</u> (41.6%) — and its <u>primary source of dissatisfaction</u> (41.3% / 95 complaints).
            </p>
          </div>
        </motion.div>

        {/* 5. PRIORITY RISK MATRIX (BUBBLE / SCATTER CHART) */}
        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-6 border-red-500/30">
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <ShieldAlert className="w-5 h-5 text-red-400" /> Operational Risk & Frequency Matrix
            </h2>
            <span className="text-xs text-slate-400">Bubble Size = Review Complaints</span>
          </div>

          <Plot
            data={riskBubbles.map((b: any) => ({
              x: [b.frequency],
              y: [b.impact],
              mode: 'markers+text',
              name: b.domain,
              text: [b.domain],
              textposition: 'top center',
              textfont: { color: '#FFFFFF', size: 11 },
              marker: {
                size: Math.max(16, Math.min(48, b.reviews / 2.5)),
                color: b.priority.includes('High') ? '#EF4444' : b.priority.includes('Medium') ? '#F97316' : '#22C55E',
                opacity: selectedDomain && b.domain !== selectedDomain ? 0.4 : 0.85,
                line: { color: '#FFFFFF', width: 1.5 }
              }
            })) as any}
            layout={{
              font: { family: 'Inter, sans-serif', color: '#94A3B8' },
              paper_bgcolor: 'rgba(0,0,0,0)',
              plot_bgcolor: 'rgba(0,0,0,0)',
              margin: { l: 60, r: 40, t: 30, b: 50 },
              height: 310,
              showlegend: false,
              xaxis: { title: { text: 'Complaint Frequency (%) →' }, range: [0, 50], gridcolor: 'rgba(255,255,255,0.05)' },
              yaxis: { title: { text: 'Business Dissatisfaction Impact ↑' }, range: [0, 12], gridcolor: 'rgba(255,255,255,0.05)' }
            } as any}
            onClick={(e: any) => {
              if (e.points && e.points[0]) {
                setSelectedDomain(e.points[0].data.name);
              }
            }}
            useResizeHandler
            className="w-full cursor-pointer"
          />

          <div className="mt-3 p-3.5 rounded-xl bg-slate-900/90 border border-white/10 flex items-center justify-between text-xs text-slate-400">
            <span>🔴 High Priority (&gt;15% complaints)</span>
            <span>🟠 Medium Priority (5-15%)</span>
            <span>🟢 Low Priority (&lt;5%)</span>
          </div>
        </motion.div>

      </div>

      {/* BOTTOM SECTION — BUSINESS OPPORTUNITY RANKING & AI ACTION PLAN */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        {/* 6. BUSINESS GROWTH OPPORTUNITIES — OPPORTUNITY RANKING VISUAL */}
        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-6">
          <h2 className="text-lg font-bold text-white flex items-center gap-2 mb-4">
            <TrendingUp className="w-5 h-5 text-purple-400" /> Business Opportunity Ranking
          </h2>
          
          <div className="space-y-4">
            {oppRanking.length > 0 ? (
              oppRanking.map((item: any) => (
                <div
                  key={item.rank}
                  onClick={() => setSelectedDomain(item.domain)}
                  className={`p-4 rounded-xl bg-slate-900/80 border transition-all cursor-pointer ${selectedDomain === item.domain ? 'border-purple-500 ring-1 ring-purple-500 bg-purple-500/10' : 'border-white/10 hover:border-purple-500/50'}`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <div className="flex items-center gap-2">
                      <span className="w-6 h-6 rounded-full bg-purple-500/20 text-purple-300 font-black text-xs flex items-center justify-center border border-purple-500/30">
                        #{item.rank}
                      </span>
                      <h3 className="font-bold text-white text-sm">{item.domain}</h3>
                    </div>
                    <span className="text-xs font-extrabold px-2.5 py-0.5 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30">
                      {item.impact} IMPACT
                    </span>
                  </div>

                  <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden my-2">
                    <div
                      className="bg-gradient-to-r from-purple-600 to-cyan-400 h-full rounded-full transition-all"
                      style={{ width: `${item.opportunity_score}%` }}
                    />
                  </div>

                  <div className="flex items-center justify-between text-xs text-slate-400 mt-1">
                    <span>Complaint Share: <strong className="text-red-400">{item.complaint_pct}%</strong> ({item.count} reviews)</span>
                    <span>Opportunity Score: <strong className="text-purple-300">{item.opportunity_score} / 100</strong></span>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-slate-500 text-sm">No opportunity rankings calculated.</div>
            )}
          </div>
        </motion.div>

        {/* 7. STRATEGIC AI ACTION PLAN — COMPACT DIRECTIVES TABLE */}
        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-6">
          <h2 className="text-lg font-bold text-white flex items-center gap-2 mb-4">
            <CheckCircle className="w-5 h-5 text-emerald-400" /> Ranked AI Executive Action Plan
          </h2>

          <div className="space-y-3">
            {actionPlan.length > 0 ? (
              actionPlan.map((act: any) => (
                <div
                  key={act.rank}
                  onClick={() => setSelectedDomain(act.domain)}
                  className={`p-4 rounded-xl bg-slate-900/80 border border-l-4 transition-all cursor-pointer ${act.impact === 'VERY HIGH' ? 'border-l-red-500' : 'border-l-amber-500'} ${selectedDomain === act.domain ? 'border-cyan-500 ring-1 ring-cyan-500 bg-cyan-500/10' : 'border-white/10 hover:border-cyan-500/50'}`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <div className="flex items-center gap-2">
                      <span className="font-black text-xs text-slate-400">#{act.rank}</span>
                      <span className="font-bold text-white text-sm">{act.domain}</span>
                    </div>
                    <span className={`text-[10px] font-extrabold px-2 py-0.5 rounded-full ${act.impact === 'VERY HIGH' ? 'bg-red-500/20 text-red-400 border border-red-500/30' : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'}`}>
                      IMPACT: {act.impact}
                    </span>
                  </div>

                  <div className="text-xs text-cyan-400 font-semibold mb-1">
                    🔍 Evidence: <span className="text-slate-300">{act.evidence}</span>
                  </div>

                  <div className="text-xs font-bold text-emerald-400 flex items-center gap-1.5 mt-2">
                    <ArrowRight className="w-3.5 h-3.5 shrink-0" />
                    <span>Directive: {act.action}</span>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-slate-500 text-sm">No action plan items generated.</div>
            )}
          </div>
        </motion.div>

      </div>

    </div>
  );
};
