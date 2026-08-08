import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles, ArrowRight, Zap, Shield, BarChart2, Cpu, FileText } from 'lucide-react';

interface LandingPageProps {
  onNavigate: (tab: string) => void;
  isUploaded?: boolean;
  datasetInfo?: any;
}

export const LandingPage: React.FC<LandingPageProps> = ({ onNavigate, isUploaded = false, datasetInfo }) => {
  return (
    <div className="p-8 space-y-12 max-w-7xl mx-auto">
      {/* Hero Section */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="glass-card p-10 md:p-14 text-center relative overflow-hidden border border-purple-500/20"
      >
        <div className="absolute -top-24 -left-24 w-72 h-72 bg-purple-600/20 rounded-full blur-3xl pointer-events-none"></div>
        <div className="absolute -bottom-24 -right-24 w-72 h-72 bg-cyan-600/20 rounded-full blur-3xl pointer-events-none"></div>

        {isUploaded ? (
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-emerald-500/15 border border-emerald-500/40 text-emerald-300 text-xs font-bold mb-6">
            <Sparkles className="w-4 h-4 text-emerald-400" />
            <span>📁 Active Dataset: {datasetInfo?.name || 'Uploaded Dataset'} ({datasetInfo?.row_count?.toLocaleString() || '2,304'} records)</span>
          </div>
        ) : (
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-purple-500/10 border border-purple-500/30 text-purple-300 text-xs font-semibold mb-6">
            <Sparkles className="w-4 h-4 text-cyan-400" />
            <span>Production-Ready Text Analytics Engine</span>
          </div>
        )}

        <h1 className="text-4xl md:text-6xl font-black tracking-tight text-white mb-6 leading-tight">
          Transform Unstructured Text into <br />
          <span className="animated-gradient-text">Actionable Intelligence</span>
        </h1>

        <p className="text-slate-300 text-lg max-w-3xl mx-auto mb-8 font-normal leading-relaxed">
          ReviewMiner AI is an enterprise-grade NLP and Machine Learning platform. Perform automated schema detection, interactive EDA, sentiment distribution, supervised ML classification, and executive PDF reporting.
        </p>

        <div className="flex flex-wrap justify-center gap-4">
          {isUploaded ? (
            <>
              <button
                onClick={() => onNavigate('eda')}
                className="flex items-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-purple-600 to-cyan-500 hover:from-purple-500 hover:to-cyan-400 text-white font-bold text-base shadow-lg shadow-purple-500/30 transition-all duration-200 transform hover:-translate-y-0.5"
              >
                <span>📊 Explore EDA Analytics</span>
                <ArrowRight className="w-5 h-5" />
              </button>

              <button
                onClick={() => onNavigate('sentiment')}
                className="flex items-center gap-2 px-6 py-4 rounded-xl bg-slate-800/80 hover:bg-slate-700/80 border border-white/10 text-cyan-400 font-bold text-base transition-all duration-200"
              >
                <span>😊 View Sentiment Analysis</span>
              </button>

              <button
                onClick={() => onNavigate('upload')}
                className="flex items-center gap-2 px-6 py-4 rounded-xl bg-slate-900/60 hover:bg-slate-800/60 border border-white/10 text-slate-300 font-semibold text-sm transition-all duration-200"
              >
                <span>📤 Change Dataset</span>
              </button>
            </>
          ) : (
            <>
              <button
                onClick={() => onNavigate('upload')}
                className="flex items-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-purple-600 to-cyan-500 hover:from-purple-500 hover:to-cyan-400 text-white font-bold text-base shadow-lg shadow-purple-500/30 transition-all duration-200 transform hover:-translate-y-0.5"
              >
                <span>Upload Dataset Now</span>
                <ArrowRight className="w-5 h-5" />
              </button>
            </>
          )}
        </div>
      </motion.div>

      {/* Feature Highlights Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[
          {
            icon: Zap,
            title: "Dynamic Schema Detection",
            desc: "Upload CSV, TXT, or Excel files. ReviewMiner AI automatically detects review text and sentiment columns using heuristic algorithms without hardcoded schemas.",
            color: "from-purple-500 to-indigo-600"
          },
          {
            icon: Cpu,
            title: "Supervised ML Pipeline",
            desc: "TF-IDF feature extraction combined with Multinomial Naive Bayes models to evaluate accuracy, precision, recall, F1 scores, and confusion matrix heatmaps.",
            color: "from-cyan-500 to-blue-600"
          },
          {
            icon: BarChart2,
            title: "Executive PDF Export",
            desc: "Automated business intelligence summarizing customer satisfaction %, top complaints, positive feature drivers, and downloadable PDF reports.",
            color: "from-emerald-500 to-teal-600"
          }
        ].map((feat, idx) => {
          const Icon = feat.icon;
          return (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 * idx }}
              className="glass-card p-6 flex flex-col justify-between hover:border-purple-500/40"
            >
              <div>
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${feat.color} flex items-center justify-center text-white mb-4 shadow-md`}>
                  <Icon className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-bold text-white mb-2">{feat.title}</h3>
                <p className="text-slate-400 text-sm leading-relaxed">{feat.desc}</p>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Workflow Step-by-Step */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="glass-card p-8"
      >
        <h2 className="text-2xl font-bold text-white mb-8 text-center">
          End-to-End Execution Pipeline
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {[
            { step: "01", name: "Data Ingestion", desc: "Drag & drop CSV/TXT dataset with auto column detection." },
            { step: "02", name: "Text Cleaning", desc: "Lowercasing, punctuation, stopwords & lemmatization." },
            { step: "03", name: "ML Classification", desc: "Train Naive Bayes models with evaluation metrics." },
            { step: "04", name: "BI Reporting", desc: "Generate strategic insights & export executive PDF." }
          ].map((item, idx) => (
            <div key={idx} className="relative p-5 rounded-xl bg-slate-900/60 border border-white/5 flex flex-col items-center text-center">
              <span className="text-3xl font-black text-purple-500/40 mb-2">{item.step}</span>
              <h4 className="text-base font-bold text-white mb-1">{item.name}</h4>
              <p className="text-xs text-slate-400">{item.desc}</p>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};
