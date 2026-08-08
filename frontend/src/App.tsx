import React, { useEffect, useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { Navbar } from './components/Navbar';
import { LandingPage } from './pages/LandingPage';
import { UploadDataset } from './pages/UploadDataset';
import { DataPreprocessing } from './pages/DataPreprocessing';
import { EDA } from './pages/EDA';
import { ProductBrandAnalytics } from './pages/ProductBrandAnalytics';
import { TopicFeatureMining } from './pages/TopicFeatureMining';
import { SentimentDashboard } from './pages/SentimentDashboard';
import { WordCloudAnalytics } from './pages/WordCloudAnalytics';
import { MachineLearning } from './pages/MachineLearning';
import { Prediction } from './pages/Prediction';
import { BusinessIntelligence } from './pages/BusinessIntelligence';
import { DatasetComparison } from './pages/DatasetComparison';
import { ExecutiveReport } from './pages/ExecutiveReport';
import { Settings } from './pages/Settings';
import { Lock, CheckCircle2, AlertCircle, X } from 'lucide-react';
import { DatasetProvider, useDataset } from './context/DatasetContext';

const AppContent: React.FC = () => {
  const { datasetInfo, isUploaded, refreshDataset } = useDataset();
  const [activeTab, setActiveTab] = useState(isUploaded ? 'landing' : 'upload');
  const [toast, setToast] = useState<{ message: string; type: 'info' | 'success' } | null>(null);

  useEffect(() => {
    if (isUploaded && activeTab === 'upload') {
      setActiveTab('landing');
    }
  }, [isUploaded]);

  const showToast = (message: string, type: 'info' | 'success' = 'info') => {
    setToast({ message, type });
    setTimeout(() => {
      setToast(null);
    }, 4500);
  };

  const handleTabChange = (tab: string) => {
    if (!isUploaded && tab !== 'upload') {
      showToast("Upload a dataset to unlock analytics.", "info");
      setActiveTab('upload');
      return;
    }
    setActiveTab(tab);
  };

  const handleUploadSuccess = () => {
    refreshDataset();
    showToast("Dataset uploaded successfully. Analytics generated.", "success");
    setActiveTab('landing');
  };

  const renderContent = () => {
    if (!isUploaded && activeTab !== 'upload') {
      return (
        <div className="p-12 text-center max-w-2xl mx-auto space-y-6">
          <div className="w-16 h-16 rounded-full bg-purple-500/10 border border-purple-500/30 flex items-center justify-center mx-auto text-purple-400">
            <Lock className="w-8 h-8" />
          </div>
          <h2 className="text-3xl font-black text-white">Analytics Locked</h2>
          <p className="text-slate-400 text-base">
            Upload a dataset to unlock analytics. All text mining, EDA, sentiment analysis, and machine learning modules require an active dataset.
          </p>
          <button
            onClick={() => setActiveTab('upload')}
            className="px-8 py-3.5 rounded-xl bg-gradient-to-r from-purple-600 to-cyan-500 hover:from-purple-500 hover:to-cyan-400 text-white font-bold text-sm shadow-lg shadow-purple-500/30 transition-all"
          >
            📂 Go to Upload Dataset
          </button>
        </div>
      );
    }

    switch (activeTab) {
      case 'upload':
        return <UploadDataset onDatasetUpdated={handleUploadSuccess} onNavigate={handleTabChange} />;
      case 'landing':
        return <LandingPage onNavigate={handleTabChange} isUploaded={isUploaded} datasetInfo={datasetInfo} />;
      case 'preprocessing':
        return <DataPreprocessing onNavigate={handleTabChange} />;
      case 'eda':
        return <EDA onNavigate={handleTabChange} />;
      case 'product':
        return <ProductBrandAnalytics onNavigate={handleTabChange} />;
      case 'topic':
        return <TopicFeatureMining onNavigate={handleTabChange} />;
      case 'sentiment':
        return <SentimentDashboard onNavigate={handleTabChange} />;
      case 'wordcloud':
        return <WordCloudAnalytics onNavigate={handleTabChange} />;
      case 'ml':
        return <MachineLearning onNavigate={handleTabChange} />;
      case 'prediction':
        return <Prediction />;
      case 'bi':
        return <BusinessIntelligence onNavigate={handleTabChange} />;
      case 'comparison':
        return <DatasetComparison onNavigate={handleTabChange} />;
      case 'report':
        return <ExecutiveReport onNavigate={handleTabChange} />;
      case 'settings':
        return <Settings />;
      default:
        return <UploadDataset onDatasetUpdated={handleUploadSuccess} onNavigate={handleTabChange} />;
    }
  };

  return (
    <div className="flex min-h-screen bg-[#0B1220] text-slate-100 antialiased font-['Inter',sans-serif] relative">
      {/* Floating Toast Popup */}
      {toast && (
        <div className="fixed top-5 right-5 z-50 flex items-center gap-3 px-5 py-3.5 rounded-2xl shadow-2xl backdrop-blur-xl border border-white/10 transition-all animate-bounce"
          style={{
            background: toast.type === 'success' 
              ? 'linear-gradient(135deg, rgba(16, 185, 129, 0.9), rgba(6, 182, 212, 0.9))' 
              : 'linear-gradient(135deg, rgba(124, 58, 237, 0.9), rgba(236, 72, 153, 0.9))'
          }}
        >
          {toast.type === 'success' ? (
            <CheckCircle2 className="w-5 h-5 text-white flex-shrink-0" />
          ) : (
            <AlertCircle className="w-5 h-5 text-white flex-shrink-0" />
          )}
          <span className="text-sm font-bold text-white tracking-wide">{toast.message}</span>
          <button onClick={() => setToast(null)} className="ml-2 text-white/70 hover:text-white">
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      <Sidebar 
        activeTab={activeTab} 
        setActiveTab={handleTabChange} 
        isUploaded={isUploaded}
        onDisabledClick={() => showToast("Upload a dataset to unlock analytics.", "info")}
      />
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar activeTab={activeTab} datasetInfo={datasetInfo} />
        <main className="flex-1 overflow-y-auto custom-scrollbar">
          {renderContent()}
        </main>
      </div>
    </div>
  );
};

export const App: React.FC = () => (
  <DatasetProvider>
    <AppContent />
  </DatasetProvider>
);

export default App;
