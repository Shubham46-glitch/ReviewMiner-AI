import React, { useEffect, useState } from 'react';
import axios from 'axios';
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
import { Settings } from './pages/Settings';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState('landing');
  const [datasetInfo, setDatasetInfo] = useState<any>(null);

  useEffect(() => {
    fetchActiveDatasetInfo();
  }, []);

  const fetchActiveDatasetInfo = async () => {
    try {
      const res = await axios.get('/api/dataset/active');
      setDatasetInfo(res.data);
    } catch (err) {
      setDatasetInfo(null);
    }
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'landing':
        return <LandingPage onNavigate={setActiveTab} />;
      case 'upload':
        return <UploadDataset onDatasetUpdated={fetchActiveDatasetInfo} onNavigate={setActiveTab} />;
      case 'preprocessing':
        return <DataPreprocessing onNavigate={setActiveTab} />;
      case 'eda':
        return <EDA onNavigate={setActiveTab} />;
      case 'product':
        return <ProductBrandAnalytics onNavigate={setActiveTab} />;
      case 'topic':
        return <TopicFeatureMining onNavigate={setActiveTab} />;
      case 'sentiment':
        return <SentimentDashboard onNavigate={setActiveTab} />;
      case 'wordcloud':
        return <WordCloudAnalytics onNavigate={setActiveTab} />;
      case 'ml':
        return <MachineLearning onNavigate={setActiveTab} />;
      case 'prediction':
        return <Prediction />;
      case 'bi':
        return <BusinessIntelligence onNavigate={setActiveTab} />;
      case 'comparison':
        return <DatasetComparison onNavigate={setActiveTab} />;
      case 'settings':
        return <Settings />;
      default:
        return <LandingPage onNavigate={setActiveTab} />;
    }
  };

  return (
    <div className="flex min-h-screen bg-[#0B1220] text-slate-100 antialiased font-['Inter',sans-serif]">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar activeTab={activeTab} datasetInfo={datasetInfo} />
        <main className="flex-1 overflow-y-auto custom-scrollbar">
          {renderContent()}
        </main>
      </div>
    </div>
  );
};

export default App;
