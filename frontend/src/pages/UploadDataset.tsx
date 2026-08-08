import React, { useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Upload, FileCheck, AlertCircle, ArrowRight, CheckCircle2 } from 'lucide-react';

interface UploadDatasetProps {
  onDatasetUpdated: () => void;
  onNavigate: (tab: string) => void;
}

export const UploadDataset: React.FC<UploadDatasetProps> = ({ onDatasetUpdated, onNavigate }) => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  // Column mapping states
  const [selectedTextCol, setSelectedTextCol] = useState('');
  const [selectedLabelCol, setSelectedLabelCol] = useState('');
  const [selectedPlatCol, setSelectedPlatCol] = useState('');
  const [mapSuccess, setMapSuccess] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setMapSuccess(false);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post('/api/dataset/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setUploadResult(res.data);
      setSelectedTextCol(res.data.detected.text_col || res.data.columns[0]);
      setSelectedLabelCol(res.data.detected.label_col || 'none');
      setSelectedPlatCol(res.data.detected.platform_col || 'none');
      onDatasetUpdated();
    } catch (err: any) {
      const msg = err.response?.data?.detail || err.message || 'Failed to upload dataset. Ensure backend server is running.';
      console.error('Upload Error:', err);
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleMapColumns = async () => {
    if (!uploadResult || !selectedTextCol) return;
    setLoading(true);

    const formData = new FormData();
    formData.append('dataset_id', uploadResult.dataset_id);
    formData.append('text_col', selectedTextCol);
    formData.append('label_col', selectedLabelCol === 'none' ? '' : selectedLabelCol);
    formData.append('plat_col', selectedPlatCol === 'none' ? '' : selectedPlatCol);

    try {
      await axios.post('/api/dataset/map', formData);
      setMapSuccess(true);
      onDatasetUpdated();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to map columns.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* Upload Header Card */}
      <motion.div 
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-8 border-purple-500/20"
      >
        <h2 className="text-2xl font-bold text-white mb-2">Upload Custom Review Dataset</h2>
        <p className="text-slate-400 text-sm">
          Select or drag and drop your CSV, TXT, or Excel dataset. ReviewMiner AI will automatically parse schema attributes and run NLP analytics.
        </p>

        {/* Dropzone Box */}
        <div className="mt-6 border-2 border-dashed border-purple-500/30 hover:border-purple-500/60 rounded-2xl p-8 text-center bg-slate-900/40 transition-colors">
          <Upload className="w-12 h-12 text-purple-400 mx-auto mb-4 animate-bounce" />
          <input
            type="file"
            accept=".csv, .txt, .xlsx, .xls, .tsv"
            onChange={handleFileChange}
            className="hidden"
            id="dataset-upload-input"
          />
          <label
            htmlFor="dataset-upload-input"
            className="cursor-pointer inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-semibold text-sm transition-all"
          >
            <span>Choose File</span>
          </label>
          <p className="text-xs text-slate-400 mt-3">
            Supported Formats: CSV, TXT, TSV, XLSX (Up to 200MB)
          </p>

          {file && (
            <div className="mt-4 inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-800 border border-white/10 text-cyan-400 text-sm font-semibold">
              <FileCheck className="w-4 h-4" />
              <span>{file.name} ({(file.size / 1024).toFixed(1)} KB)</span>
            </div>
          )}
        </div>

        {file && (
          <div className="mt-6 text-right">
            <button
              onClick={handleUpload}
              disabled={loading}
              className="px-8 py-3 rounded-xl bg-gradient-to-r from-purple-600 to-cyan-500 hover:from-purple-500 hover:to-cyan-400 text-white font-bold text-sm shadow-lg shadow-purple-500/30 transition-all disabled:opacity-50"
            >
              {loading ? 'Processing Dataset...' : '🚀 Analyze Dataset Schema'}
            </button>
          </div>
        )}

        {error && (
          <div className="mt-4 p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-sm flex items-center gap-3">
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}
      </motion.div>

      {/* Dataset Summary & Column Mapping */}
      {uploadResult && (
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Summary Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="glass-card p-6 border-l-4 border-l-purple-500">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Total Rows</span>
              <p className="text-3xl font-black text-white mt-1">{uploadResult.row_count.toLocaleString()}</p>
              <span className="text-xs text-purple-400">Processed text records</span>
            </div>
            <div className="glass-card p-6 border-l-4 border-l-cyan-500">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Total Columns</span>
              <p className="text-3xl font-black text-white mt-1">{uploadResult.col_count}</p>
              <span className="text-xs text-cyan-400">Dataset attributes</span>
            </div>
            <div className="glass-card p-6 border-l-4 border-l-emerald-500">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Detected Text Column</span>
              <p className="text-xl font-bold text-emerald-400 mt-1 truncate">{uploadResult.detected.text_col || 'N/A'}</p>
              <span className="text-xs text-slate-400">Auto-schema matched</span>
            </div>
          </div>

          {/* Column Mapping Controls */}
          <div className="glass-card p-8">
            <h3 className="text-xl font-bold text-white mb-4">Confirm Column Mapping</h3>
            <p className="text-sm text-slate-400 mb-6">
              Review and adjust the mapped text, sentiment, and platform/category columns:
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">
                  Review Text Column *
                </label>
                <select
                  value={selectedTextCol}
                  onChange={(e) => setSelectedTextCol(e.target.value)}
                  className="w-full bg-slate-900 border border-white/10 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-purple-500"
                >
                  {uploadResult.columns.map((c: string) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">
                  Sentiment Label Column
                </label>
                <select
                  value={selectedLabelCol}
                  onChange={(e) => setSelectedLabelCol(e.target.value)}
                  className="w-full bg-slate-900 border border-white/10 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-purple-500"
                >
                  <option value="none">[Auto-Generate AI VADER Sentiments]</option>
                  {uploadResult.columns.map((c: string) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">
                  Platform / Category Column
                </label>
                <select
                  value={selectedPlatCol}
                  onChange={(e) => setSelectedPlatCol(e.target.value)}
                  className="w-full bg-slate-900 border border-white/10 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-purple-500"
                >
                  <option value="none">[None / Default Category]</option>
                  {uploadResult.columns.map((c: string) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="mt-8 flex items-center justify-between">
              {mapSuccess ? (
                <div className="flex items-center gap-2 text-emerald-400 text-sm font-semibold">
                  <CheckCircle2 className="w-5 h-5" />
                  <span>Columns mapped & NLP pipeline re-executed successfully!</span>
                </div>
              ) : <div></div>}

              <button
                onClick={handleMapColumns}
                disabled={loading}
                className="px-6 py-3 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-sm transition-all"
              >
                {loading ? 'Applying Mapping...' : 'Confirm Column Mapping'}
              </button>
            </div>
          </div>

          {/* Raw Data Preview Table */}
          <div className="glass-card p-8 overflow-x-auto">
            <h3 className="text-xl font-bold text-white mb-4">Raw Data Preview</h3>
            <table className="w-full text-left text-sm text-slate-300 border-collapse">
              <thead>
                <tr className="border-b border-white/10 text-xs font-bold text-purple-400 uppercase">
                  {uploadResult.columns.map((c: string) => (
                    <th key={c} className="p-3">{c}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {uploadResult.preview.map((row: any, i: number) => (
                  <tr key={i} className="border-b border-white/5 hover:bg-slate-800/40">
                    {uploadResult.columns.map((c: string) => (
                      <td key={c} className="p-3 max-w-xs truncate">{String(row[c] || '')}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>

            <div className="mt-8 text-right">
              <button
                onClick={() => onNavigate('eda')}
                className="inline-flex items-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-purple-600 to-cyan-500 text-white font-bold text-sm shadow-lg shadow-purple-500/30"
              >
                <span>Proceed to Exploratory Data Analysis (EDA)</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
};
