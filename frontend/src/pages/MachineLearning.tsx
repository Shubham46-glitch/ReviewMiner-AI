import React, { useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import { motion } from 'framer-motion';
import { Cpu, Award, CheckCircle2, AlertCircle, Play, Layers, Zap, Search, AlertTriangle, Sparkles } from 'lucide-react';

interface MLProps {
  onNavigate: (tab: string) => void;
}

export const MachineLearning: React.FC<MLProps> = ({ onNavigate }) => {
  const [loading, setLoading] = useState(false);
  const [mlResult, setMlResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  // Playground state
  const [inputText, setInputText] = useState("The battery life is amazing and display screen is super crisp!");
  const [predicting, setPredicting] = useState(false);
  const [predictionRes, setPredictionRes] = useState<any>(null);
  const [predictionError, setPredictionError] = useState<string | null>(null);

  // Explorer filter state
  const [explorerFilter, setExplorerFilter] = useState<'ALL' | 'CORRECT' | 'MISCLASSIFIED'>('ALL');

  const handleTrain = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await axios.post('/api/ml/train');
      setMlResult(res.data.results);
      setPredictionRes(null);
      setPredictionError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to train ML model.');
    } finally {
      setLoading(false);
    }
  };

  const handlePredict = async () => {
    if (!inputText || !inputText.trim()) {
      setPredictionError("Please enter a review to classify.");
      return;
    }
    setPredicting(true);
    setPredictionError(null);
    setPredictionRes(null);
    try {
      const formData = new FormData();
      formData.append('text', inputText);
      const res = await axios.post('/api/ml/predict', formData);
      if (res.data.status === 'error') {
        setPredictionError(res.data.detail);
      } else {
        setPredictionRes(res.data);
      }
    } catch (err: any) {
      setPredictionError(err.response?.data?.detail || 'Prediction failed.');
    } finally {
      setPredicting(false);
    }
  };

  const plotlyLayout: any = {
    font: { family: 'Inter, sans-serif', color: '#FFFFFF' },
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    margin: { l: 55, r: 25, t: 40, b: 50 },
    xaxis: { gridcolor: 'rgba(255,255,255,0.05)' },
    yaxis: { gridcolor: 'rgba(255,255,255,0.05)' },
  };

  const tInfo = mlResult?.target_info || {};
  const metrics = mlResult?.metrics || {};
  const modelsComp = mlResult?.models_comparison || {};
  const cvInfo = mlResult?.cross_validation || {};
  const testPreds = mlResult?.test_predictions || [];
  const misclassifications = mlResult?.misclassifications || [];

  const filteredTestPreds = testPreds.filter((item: any) => {
    if (explorerFilter === 'CORRECT') return item.correct === true;
    if (explorerFilter === 'MISCLASSIFIED') return item.correct === false;
    return true;
  });

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* ML Pipeline Banner */}
      <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-8 border-purple-500/20">
        <div className="flex items-center gap-3 mb-2">
          <Cpu className="w-6 h-6 text-purple-400" />
          <h2 className="text-2xl font-bold text-white">Supervised Machine Learning Pipeline</h2>
        </div>
        <p className="text-slate-400 text-sm mb-6">
          Train and evaluate 3 classifiers (Multinomial Naive Bayes, Logistic Regression, Linear SVM) dynamically on your active dataset.
        </p>

        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex flex-wrap items-center gap-3 text-xs font-semibold text-slate-300">
            <span className="px-3 py-1.5 rounded-lg bg-purple-500/20 border border-purple-500/30 text-purple-300">TF-IDF Features</span>
            <span>→</span>
            <span className="px-3 py-1.5 rounded-lg bg-cyan-500/20 border border-cyan-500/30 text-cyan-300">80/20 Stratified Split</span>
            <span>→</span>
            <span className="px-3 py-1.5 rounded-lg bg-emerald-500/20 border border-emerald-500/30 text-emerald-300">3-Model Evaluation</span>
          </div>

          <button
            onClick={handleTrain}
            disabled={loading}
            className="flex items-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-purple-600 to-cyan-500 hover:from-purple-500 hover:to-cyan-400 text-white font-bold text-sm shadow-lg shadow-purple-500/30 transition-all disabled:opacity-50"
          >
            <Play className="w-4 h-4 fill-white" />
            <span>{loading ? 'Training Models...' : 'Train ML Models Now'}</span>
          </button>
        </div>

        {error && (
          <div className="mt-4 p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-sm flex items-center gap-3">
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}
      </motion.div>

      {mlResult && (
        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="space-y-8">
          
          {/* Target Detection Banner */}
          <div className="glass-card p-6 border-l-4 border-l-cyan-500 space-y-4">
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <Layers className="w-5 h-5 text-cyan-400" />
              Target Label Detection & Dataset Information
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="p-3 rounded-lg bg-white/5 border border-white/10">
                <div className="text-[11px] text-slate-400 font-bold uppercase">Target Column</div>
                <div className="text-lg font-bold text-white">{tInfo.target_column}</div>
              </div>
              <div className="p-3 rounded-lg bg-white/5 border border-white/10">
                <div className="text-[11px] text-slate-400 font-bold uppercase">Target Classes</div>
                <div className="text-lg font-bold text-purple-400">{tInfo.num_classes} Unique Classes</div>
              </div>
              <div className="p-3 rounded-lg bg-white/5 border border-white/10">
                <div className="text-[11px] text-slate-400 font-bold uppercase">Actual Labels</div>
                <div className="text-sm font-bold text-emerald-400">{(tInfo.labels || []).join(', ')}</div>
              </div>
              <div className="p-3 rounded-lg bg-white/5 border border-white/10">
                <div className="text-[11px] text-slate-400 font-bold uppercase">Train / Test Split</div>
                <div className="text-sm font-bold text-cyan-400">{tInfo.train_samples} / {tInfo.test_samples} Samples</div>
              </div>
            </div>
          </div>

          {/* Model Comparison Table */}
          <div className="glass-card p-6 space-y-4">
            <h3 className="text-xl font-bold text-white flex items-center gap-2">
              <Award className="w-5 h-5 text-amber-400" />
              Algorithm Model Comparison Matrix
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm text-slate-300">
                <thead className="bg-white/5 text-xs text-purple-400 uppercase">
                  <tr>
                    <th className="p-3">Model Algorithm</th>
                    <th className="p-3">Accuracy</th>
                    <th className="p-3">Precision</th>
                    <th className="p-3">Recall</th>
                    <th className="p-3">F1-Score</th>
                    <th className="p-3">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  {Object.entries(modelsComp).map(([mName, mVal]: [string, any]) => (
                    <tr key={mName} className={`hover:bg-white/5 ${mName === mlResult.best_model_name ? 'bg-purple-950/20' : ''}`}>
                      <td className="p-3 font-bold text-white">{mName}</td>
                      <td className="p-3 text-cyan-400">{(mVal.accuracy * 100).toFixed(2)}%</td>
                      <td className="p-3 text-emerald-400">{(mVal.precision * 100).toFixed(2)}%</td>
                      <td className="p-3 text-amber-400">{(mVal.recall * 100).toFixed(2)}%</td>
                      <td className="p-3 text-purple-400 font-bold">{(mVal.f1_score * 100).toFixed(2)}%</td>
                      <td className="p-3">
                        {mName === mlResult.best_model_name ? (
                          <span className="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-400 font-bold text-xs">
                            🏆 Best Model
                          </span>
                        ) : (
                          <span className="text-slate-500 text-xs">Evaluated</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* ML Best Model Evaluation Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="glass-card p-6 border-l-4 border-l-purple-500">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Accuracy Score</span>
              <p className="text-3xl font-black text-white mt-1">{(metrics.accuracy * 100).toFixed(1)}%</p>
              <span className="text-xs text-purple-400">Winning model correctness</span>
            </div>

            <div className="glass-card p-6 border-l-4 border-l-cyan-500">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Precision Score</span>
              <p className="text-3xl font-black text-white mt-1">{(metrics.precision * 100).toFixed(1)}%</p>
              <span className="text-xs text-cyan-400">Positive predictive value</span>
            </div>

            <div className="glass-card p-6 border-l-4 border-l-emerald-500">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Recall Score</span>
              <p className="text-3xl font-black text-white mt-1">{(metrics.recall * 100).toFixed(1)}%</p>
              <span className="text-xs text-emerald-400">Sensitivity rate</span>
            </div>

            <div className="glass-card p-6 border-l-4 border-l-amber-500">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">F1 Score</span>
              <p className="text-3xl font-black text-white mt-1">{(metrics.f1_score * 100).toFixed(1)}%</p>
              <span className="text-xs text-amber-400">Harmonic mean score</span>
            </div>
          </div>

          {/* Confusion Matrix & Classification Report */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="glass-card p-6">
              <h3 className="text-xl font-bold text-white mb-4">Confusion Matrix Heatmap ({mlResult.best_model_name})</h3>
              <Plot
                data={[
                  {
                    z: mlResult.confusion_matrix.matrix,
                    x: mlResult.confusion_matrix.labels,
                    y: mlResult.confusion_matrix.labels,
                    type: 'heatmap',
                    colorscale: 'Purples'
                  } as any
                ]}
                layout={{
                  ...plotlyLayout,
                  title: { text: `Confusion Matrix (${mlResult.best_model_name})`, font: { color: '#FFFFFF', size: 14 } },
                  xaxis: { title: { text: 'Predicted Label', font: { color: '#94A3B8', size: 12 } } },
                  yaxis: { title: { text: 'Actual Ground Truth Label', font: { color: '#94A3B8', size: 12 } }, autorange: 'reversed' },
                  height: 350
                }}
                useResizeHandler
                className="w-full"
              />
            </div>

            {/* Classification Report */}
            <div className="glass-card p-6 overflow-x-auto">
              <h3 className="text-xl font-bold text-white mb-4">Classification Metrics Report</h3>
              <table className="w-full text-left text-sm text-slate-300 border-collapse">
                <thead>
                  <tr className="border-b border-white/10 text-xs font-bold text-purple-400 uppercase">
                    <th className="p-3">Class Label</th>
                    <th className="p-3">Precision</th>
                    <th className="p-3">Recall</th>
                    <th className="p-3">F1-Score</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(mlResult.classification_report).map(([cls, scores]: [string, any]) => {
                    if (typeof scores !== 'object') return null;
                    return (
                      <tr key={cls} className="border-b border-white/5 hover:bg-slate-800/40">
                        <td className="p-3 font-semibold text-white">{cls}</td>
                        <td className="p-3 text-cyan-400">{scores.precision?.toFixed(4)}</td>
                        <td className="p-3 text-emerald-400">{scores.recall?.toFixed(4)}</td>
                        <td className="p-3 text-purple-400">{scores['f1-score']?.toFixed(4)}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>

          {/* Cross Validation & Feature Insights */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="glass-card p-6 space-y-3">
              <h3 className="text-lg font-bold text-white flex items-center gap-2">
                <Zap className="w-5 h-5 text-emerald-400" />
                5-Fold Stratified Cross-Validation
              </h3>
              {cvInfo.has_cv ? (
                <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
                  <div className="text-xl font-black text-emerald-400">Mean CV Accuracy: {cvInfo.mean_accuracy}%</div>
                  <div className="text-xs text-slate-400 mt-1">Standard Deviation: ±{cvInfo.std_accuracy}% across 5 stratified folds.</div>
                </div>
              ) : (
                <div className="p-4 rounded-xl bg-slate-900/50 border border-white/5 text-xs text-slate-400">
                  5-Fold Cross Validation unavailable: Requires at least 5 samples per target class.
                </div>
              )}
            </div>

            {/* Interactive Prediction Playground */}
            <div className="glass-card p-6 space-y-4">
              <h3 className="text-lg font-bold text-white flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-purple-400" />
                Real-Time Prediction Playground
              </h3>
              <textarea
                value={inputText}
                onChange={(e) => {
                  setInputText(e.target.value);
                  setPredictionRes(null);
                  setPredictionError(null);
                }}
                rows={2}
                className="w-full p-3 rounded-xl bg-slate-900/80 border border-white/10 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-purple-500"
                placeholder="Enter review text..."
              />
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <button
                  onClick={handlePredict}
                  disabled={predicting}
                  className="px-6 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs shadow-md transition-all disabled:opacity-50"
                >
                  {predicting ? 'Analyzing Review...' : 'Predict Sentiment'}
                </button>

                {predictionError && (
                  <div className="text-xs text-red-400 font-semibold flex items-center gap-1">
                    <AlertCircle className="w-4 h-4 flex-shrink-0" />
                    <span>{predictionError}</span>
                  </div>
                )}

                {predictionRes && (
                  <div className="text-xs text-right space-y-0.5">
                    <div>
                      <span className="text-slate-400">Predicted Class: </span>
                      <span className="font-bold text-emerald-400 text-sm">{predictionRes.predicted_class}</span>
                      {predictionRes.confidence !== null && predictionRes.confidence !== undefined && (
                        <span className="text-purple-300 font-semibold ml-2">({predictionRes.confidence}%)</span>
                      )}
                    </div>
                    <div className="text-[11px] text-slate-500">{predictionRes.model_used}</div>
                  </div>
                )}
              </div>

              {predictionRes && predictionRes.class_probabilities && Object.keys(predictionRes.class_probabilities).length > 0 && (
                <div className="mt-4 pt-4 border-t border-white/5 space-y-2">
                  <div className="text-xs font-bold text-slate-400 uppercase">Class Probabilities</div>
                  <div className="space-y-2">
                    {Object.entries(predictionRes.class_probabilities).map(([cls, prob]: [string, any]) => (
                      <div key={cls} className="space-y-1">
                        <div className="flex justify-between text-xs">
                          <span className="text-slate-300 font-semibold">{cls}</span>
                          <span className="text-purple-400 font-bold">{prob}%</span>
                        </div>
                        <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                          <div
                            className="bg-gradient-to-r from-purple-500 to-cyan-400 h-2 rounded-full transition-all duration-500"
                            style={{ width: `${Math.min(100, Math.max(0, prob))}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Test Prediction Explorer & Misclassifications */}
          <div className="glass-card p-6 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-xl font-bold text-white flex items-center gap-2">
                <Search className="w-5 h-5 text-cyan-400" />
                Test Predictions & Failure Audit ({filteredTestPreds.length})
              </h3>
              <div className="flex gap-2">
                <button
                  onClick={() => setExplorerFilter('ALL')}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold ${explorerFilter === 'ALL' ? 'bg-purple-600 text-white' : 'bg-white/5 text-slate-400'}`}
                >
                  All ({testPreds.length})
                </button>
                <button
                  onClick={() => setExplorerFilter('CORRECT')}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold ${explorerFilter === 'CORRECT' ? 'bg-emerald-600 text-white' : 'bg-white/5 text-slate-400'}`}
                >
                  Correct ({testPreds.filter((i: any) => i.correct).length})
                </button>
                <button
                  onClick={() => setExplorerFilter('MISCLASSIFIED')}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold ${explorerFilter === 'MISCLASSIFIED' ? 'bg-red-600 text-white' : 'bg-white/5 text-slate-400'}`}
                >
                  Misclassified ({misclassifications.length})
                </button>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-300">
                <thead className="bg-white/5 text-slate-400 uppercase">
                  <tr>
                    <th className="p-3">#</th>
                    <th className="p-3">Review Text</th>
                    <th className="p-3">Actual Label</th>
                    <th className="p-3">Predicted Label</th>
                    <th className="p-3">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  {filteredTestPreds.slice(0, 30).map((item: any) => (
                    <tr key={item.index} className="hover:bg-white/5">
                      <td className="p-3 font-mono text-slate-500">{item.index}</td>
                      <td className="p-3 font-mono text-slate-200">{item.review}</td>
                      <td className="p-3 font-bold">{item.actual}</td>
                      <td className="p-3 font-bold text-purple-400">{item.predicted}</td>
                      <td className="p-3">
                        {item.correct ? (
                          <span className="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 font-bold text-[10px]">
                            Correct
                          </span>
                        ) : (
                          <span className="px-2 py-0.5 rounded-full bg-red-500/20 text-red-400 font-bold text-[10px]">
                            Misclassified
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

        </motion.div>
      )}
    </div>
  );
};
