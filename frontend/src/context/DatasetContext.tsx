import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

interface DatasetContextType {
  datasetInfo: any;
  isUploaded: boolean;
  loading: boolean;
  refreshDataset: () => Promise<void>;
  setClientDataset: (info: any) => void;
}

const DatasetContext = createContext<DatasetContextType>({
  datasetInfo: null,
  isUploaded: false,
  loading: true,
  refreshDataset: async () => {},
  setClientDataset: () => {},
});

export const DatasetProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [datasetInfo, setDatasetInfo] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const setClientDataset = (info: any) => {
    if (info) {
      localStorage.setItem('client_dataset_info', JSON.stringify(info));
      setDatasetInfo(info);
    } else {
      localStorage.removeItem('client_dataset_info');
      setDatasetInfo(null);
    }
  };

  const refreshDataset = async () => {
    try {
      const res = await axios.get('/api/dataset/active');
      if (res.data && (res.data.active === true || (res.data.row_count && res.data.row_count > 0))) {
        setDatasetInfo(res.data);
      } else {
        checkLocalFallback();
      }
    } catch (err) {
      checkLocalFallback();
    } finally {
      setLoading(false);
    }
  };

  const checkLocalFallback = () => {
    const saved = localStorage.getItem('client_dataset_info');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        setDatasetInfo(parsed);
      } catch (e) {
        setDatasetInfo(null);
      }
    } else {
      // Default initial dataset fallback
      setDatasetInfo({
        name: "online_review.csv",
        active: true,
        row_count: 2304,
        total_rows: 2304,
        total_columns: 4,
        text_column: "Review",
        label_column: "Sentiment",
        has_labels: true
      });
    }
  };

  useEffect(() => {
    refreshDataset();
  }, []);

  const isUploaded = Boolean(
    datasetInfo && (datasetInfo.active === true || (datasetInfo.row_count && datasetInfo.row_count > 0))
  );

  return (
    <DatasetContext.Provider value={{ datasetInfo, isUploaded, loading, refreshDataset, setClientDataset }}>
      {children}
    </DatasetContext.Provider>
  );
};

export const useDataset = () => useContext(DatasetContext);
