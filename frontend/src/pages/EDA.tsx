import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import { motion } from 'framer-motion';
import { Database, ShieldAlert, Hash, Layers, FileText, Info, BarChart3, CheckCircle2, AlertTriangle } from 'lucide-react';

interface EDAProps {
  onNavigate: (tab: string) => void;
}

export const EDA: React.FC<EDAProps> = ({ onNavigate }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedNumCol, setSelectedNumCol] = useState<string>('');
  const [selectedCatCol, setSelectedCatCol] = useState<string>('');

  useEffect(() => {
    fetchEDAData();
  }, []);

  const fetchEDAData = async () => {
    try {
      setLoading(true);
      const res = await axios.get('/api/analytics/eda');
      const responseData = res.data;
      setData(responseData);

      const numKeys = Object.keys(responseData.numerical_analysis || {});
      if (numKeys.length > 0) setSelectedNumCol(numKeys[0]);

      const catKeys = Object.keys(responseData.categorical_analysis || {});
      if (catKeys.length > 0) setSelectedCatCol(catKeys[0]);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load EDA analytics.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-8 text-center text-slate-400">Profiling dataset & building dynamic EDA analytics...</div>;
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

  const basePlotlyLayout: any = {
    font: { family: 'Inter, sans-serif', color: '#FFFFFF' },
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
  };

  const overview = data.overview || {};
  const schemaTable = data.schema_table || [];
  const dataQuality = data.data_quality || {};
  const numAnalysis = data.numerical_analysis || {};
  const catAnalysis = data.categorical_analysis || {};
  const textAnalysis = data.text_analysis || {};

  const numKeys = Object.keys(numAnalysis);
  const catKeys = Object.keys(catAnalysis);

  const selectedNumStats = selectedNumCol ? numAnalysis[selectedNumCol] : null;
  const selectedCatStats = selectedCatCol ? catAnalysis[selectedCatCol] : null;

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* SECTION A — Dataset Overview */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <Database className="w-5 h-5 text-purple-400" />
          SECTION A — Dataset Overview
        </h2>

        {/* 7 Overview KPI Cards */}
        <div className="grid grid-cols-2 md:grid-cols-7 gap-4">
          <div className="glass-card p-4 border-l-4 border-l-purple-500">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Total Records</span>
            <p className="text-xl font-black text-white">{overview.total_records?.toLocaleString()}</p>
            <span className="text-[10px] text-purple-400">Rows</span>
          </div>

          <div className="glass-card p-4 border-l-4 border-l-cyan-500">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Total Columns</span>
            <p className="text-xl font-black text-white">{overview.total_columns}</p>
            <span className="text-[10px] text-cyan-400">Fields</span>
          </div>

          <div className="glass-card p-4 border-l-4 border-l-emerald-500">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Text Cols</span>
            <p className="text-xl font-black text-white">{overview.text_columns_count}</p>
            <span className="text-[10px] text-emerald-400">NLP Text</span>
          </div>

          <div className="glass-card p-4 border-l-4 border-l-amber-500">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Numeric Cols</span>
            <p className="text-xl font-black text-white">{overview.numeric_columns_count}</p>
            <span className="text-[10px] text-amber-400">Numbers</span>
          </div>

          <div className="glass-card p-4 border-l-4 border-l-indigo-500">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Categorical</span>
            <p className="text-xl font-black text-white">{overview.categorical_columns_count}</p>
            <span className="text-[10px] text-indigo-400">Factors</span>
          </div>

          <div className="glass-card p-4 border-l-4 border-l-pink-500">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Date Cols</span>
            <p className="text-xl font-black text-white">{overview.date_columns_count}</p>
            <span className="text-[10px] text-pink-400">Timestamps</span>
          </div>

          <div className="glass-card p-4 border-l-4 border-l-teal-500">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Dataset Size</span>
            <p className="text-xl font-black text-white">{overview.dataset_size}</p>
            <span className="text-[10px] text-teal-400">Memory</span>
          </div>
        </div>

        {/* Schema Table */}
        <div className="glass-card p-6 overflow-x-auto">
          <h3 className="text-lg font-bold text-white mb-3">Interactive Dataset Schema Table</h3>
          <table className="w-full text-left text-xs text-slate-300 border-collapse">
            <thead>
              <tr className="border-b border-white/10 text-purple-400 uppercase font-bold">
                <th className="p-3">Column Name</th>
                <th className="p-3">Data Type</th>
                <th className="p-3">Detected Semantic Type</th>
                <th className="p-3">Non-Null Count</th>
                <th className="p-3">Null Count</th>
                <th className="p-3">Missing %</th>
                <th className="p-3">Unique Values</th>
                <th className="p-3">Duplicate Count</th>
              </tr>
            </thead>
            <tbody>
              {schemaTable.map((row: any, idx: number) => (
                <tr key={idx} className="border-b border-white/5 hover:bg-slate-800/40">
                  <td className="p-3 font-semibold text-white">{row.column}</td>
                  <td className="p-3 text-cyan-400 font-mono">{row.type}</td>
                  <td className="p-3 text-purple-300 font-bold">{row.semantic_type}</td>
                  <td className="p-3">{row.non_null?.toLocaleString()}</td>
                  <td className="p-3 text-red-400">{row.null_count?.toLocaleString()}</td>
                  <td className="p-3 text-emerald-400">{row.missing_pct}%</td>
                  <td className="p-3 text-amber-400">{row.unique_values?.toLocaleString()}</td>
                  <td className="p-3 text-slate-400">{row.duplicate_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* SECTION B — Data Quality */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <ShieldAlert className="w-5 h-5 text-amber-400" />
          SECTION B — Data Quality Analytics
        </h2>

        {/* Zero-Missing State vs Warnings */}
        {!dataQuality.has_missing_values ? (
          <div className="p-5 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 flex items-center gap-3">
            <CheckCircle2 className="w-6 h-6 text-emerald-400 flex-shrink-0" />
            <div>
              <h4 className="font-bold text-sm text-emerald-200">Excellent — No Missing Values Detected</h4>
              <p className="text-xs text-emerald-400/80 mt-0.5">All columns in your dataset are 100% complete across all records.</p>
            </div>
          </div>
        ) : (
          dataQuality.warnings?.length > 0 && (
            <div className="space-y-2">
              {dataQuality.warnings.map((w: string, idx: number) => (
                <div key={idx} className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-amber-400 flex-shrink-0" />
                  <span>{w}</span>
                </div>
              ))}
            </div>
          )
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Missing Values Bar Chart */}
          <div className="glass-card p-6">
            <h3 className="text-base font-bold text-white mb-2">Missing Values per Column</h3>
            <Plot
              data={[
                {
                  x: dataQuality.missing_by_column?.map((item: any) => item.column),
                  y: dataQuality.missing_by_column?.map((item: any) => item.missing_count),
                  type: 'bar',
                  marker: { color: '#EF4444' }
                }
              ]}
              layout={{
                ...basePlotlyLayout,
                margin: { l: 40, r: 20, t: 20, b: 50 },
                xaxis: { title: { text: 'Column Name', font: { size: 11, color: '#94A3B8' } } },
                yaxis: { title: { text: 'Missing Record Count', font: { size: 11, color: '#94A3B8' } } },
                height: 300
              }}
              useResizeHandler
              className="w-full"
            />
          </div>

          {/* Column Completeness Chart */}
          <div className="glass-card p-6">
            <h3 className="text-base font-bold text-white mb-2">Column Completeness Score (%)</h3>
            <Plot
              data={[
                {
                  x: dataQuality.missing_by_column?.map((item: any) => item.column),
                  y: dataQuality.missing_by_column?.map((item: any) => item.completeness),
                  type: 'bar',
                  marker: { color: '#22C55E' }
                }
              ]}
              layout={{
                ...basePlotlyLayout,
                margin: { l: 40, r: 20, t: 20, b: 50 },
                xaxis: { title: { text: 'Column Name', font: { size: 11, color: '#94A3B8' } } },
                yaxis: { title: { text: 'Completeness (%)', font: { size: 11, color: '#94A3B8' } } },
                height: 300
              }}
              useResizeHandler
              className="w-full"
            />
          </div>
        </div>
      </div>

      {/* SECTION C — Numerical Analysis */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <Hash className="w-5 h-5 text-cyan-400" />
          SECTION C — Numerical Column Analysis
        </h2>

        {numKeys.length > 0 ? (
          <div className="glass-card p-6 space-y-6">
            <div className="flex items-center justify-between">
              <label className="text-sm font-bold text-slate-300">Select Numeric Column to Analyze:</label>
              <select
                value={selectedNumCol}
                onChange={(e) => setSelectedNumCol(e.target.value)}
                className="px-4 py-2 rounded-xl bg-slate-900 border border-white/10 text-white font-semibold text-xs focus:outline-none focus:border-cyan-400"
              >
                {numKeys.map((k) => (
                  <option key={k} value={k}>{k}</option>
                ))}
              </select>
            </div>

            {selectedNumStats && (
              <div className="space-y-6">
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                  <div className="p-3.5 rounded-xl bg-slate-900/60 border border-white/5">
                    <span className="text-slate-400 text-xs block">Mean</span>
                    <span className="text-lg font-bold text-cyan-400">{selectedNumStats.mean}</span>
                  </div>
                  <div className="p-3.5 rounded-xl bg-slate-900/60 border border-white/5">
                    <span className="text-slate-400 text-xs block">Median</span>
                    <span className="text-lg font-bold text-purple-400">{selectedNumStats.median}</span>
                  </div>
                  <div className="p-3.5 rounded-xl bg-slate-900/60 border border-white/5">
                    <span className="text-slate-400 text-xs block">Std Dev</span>
                    <span className="text-lg font-bold text-amber-400">{selectedNumStats.std}</span>
                  </div>
                  <div className="p-3.5 rounded-xl bg-slate-900/60 border border-white/5">
                    <span className="text-slate-400 text-xs block">Min / Max</span>
                    <span className="text-lg font-bold text-slate-200">{selectedNumStats.min} / {selectedNumStats.max}</span>
                  </div>
                  <div className="p-3.5 rounded-xl bg-slate-900/60 border border-white/5">
                    <span className="text-slate-400 text-xs block">Outliers Flagged</span>
                    <span className="text-lg font-bold text-red-400">{selectedNumStats.outlier_count}</span>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <Plot
                    data={[{ x: selectedNumStats.values, type: 'histogram', marker: { color: '#06B6D4' } }]}
                    layout={{
                      ...basePlotlyLayout,
                      title: `${selectedNumCol} Frequency Histogram`,
                      margin: { l: 40, r: 20, t: 35, b: 45 },
                      xaxis: { title: { text: selectedNumCol, font: { size: 11, color: '#94A3B8' } } },
                      yaxis: { title: { text: 'Frequency', font: { size: 11, color: '#94A3B8' } } },
                      height: 280
                    }}
                    useResizeHandler
                    className="w-full"
                  />

                  <Plot
                    data={[{ y: selectedNumStats.values, type: 'box', marker: { color: '#7C3AED' } }]}
                    layout={{
                      ...basePlotlyLayout,
                      title: `${selectedNumCol} Box Plot`,
                      margin: { l: 40, r: 20, t: 35, b: 45 },
                      yaxis: { title: { text: selectedNumCol, font: { size: 11, color: '#94A3B8' } } },
                      height: 280
                    }}
                    useResizeHandler
                    className="w-full"
                  />
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="glass-card p-6 text-center text-slate-400">
            ℹ️ Numerical analysis unavailable for this dataset. This section requires numeric columns.
          </div>
        )}
      </div>

      {/* SECTION D — Categorical Analysis */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <Layers className="w-5 h-5 text-emerald-400" />
          SECTION D — Categorical Column Analysis
        </h2>

        {catKeys.length > 0 ? (
          <div className="glass-card p-6 space-y-6">
            <div className="flex items-center justify-between">
              <label className="text-sm font-bold text-slate-300">Select Categorical Column to Analyze:</label>
              <select
                value={selectedCatCol}
                onChange={(e) => setSelectedCatCol(e.target.value)}
                className="px-4 py-2 rounded-xl bg-slate-900 border border-white/10 text-white font-semibold text-xs focus:outline-none focus:border-emerald-400"
              >
                {catKeys.map((k) => (
                  <option key={k} value={k}>{k}</option>
                ))}
              </select>
            </div>

            {selectedCatStats && (
              <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
                  <div className="p-3.5 rounded-xl bg-slate-900/60 border border-white/5">
                    <span className="text-slate-400 block">Total Cardinality</span>
                    <span className="text-lg font-bold text-emerald-400">{selectedCatStats.cardinality} Unique Values</span>
                  </div>
                  <div className="p-3.5 rounded-xl bg-slate-900/60 border border-white/5">
                    <span className="text-slate-400 block">Most Frequent Category</span>
                    <span className="text-lg font-bold text-cyan-400">{selectedCatStats.most_frequent_value}</span>
                  </div>
                  <div className="p-3.5 rounded-xl bg-slate-900/60 border border-white/5">
                    <span className="text-slate-400 block">Top Category Frequency</span>
                    <span className="text-lg font-bold text-purple-400">{selectedCatStats.most_frequent_count} Records</span>
                  </div>
                </div>

                <Plot
                  data={[
                    {
                      x: selectedCatStats.frequencies?.map((f: any) => f.count),
                      y: selectedCatStats.frequencies?.map((f: any) => f.category),
                      type: 'bar',
                      orientation: 'h',
                      marker: { color: '#22C55E' }
                    }
                  ]}
                  layout={{
                    ...basePlotlyLayout,
                    title: `Top Category Frequencies for '${selectedCatCol}'`,
                    margin: { l: 120, r: 20, t: 35, b: 45 },
                    xaxis: { title: { text: 'Frequency Count', font: { size: 11, color: '#94A3B8' } } },
                    yaxis: { title: { text: selectedCatCol, font: { size: 11, color: '#94A3B8' } }, autorange: 'reversed', automargin: true },
                    height: 320
                  }}
                  useResizeHandler
                  className="w-full"
                />
              </div>
            )}
          </div>
        ) : (
          <div className="glass-card p-6 text-center text-slate-400">
            ℹ️ Categorical analysis unavailable for this dataset.
          </div>
        )}
      </div>

    </div>
  );
};
