import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

interface DatasetContextType {
  datasetInfo: any;
  isUploaded: boolean;
  loading: boolean;
  refreshDataset: () => Promise<void>;
}

const DatasetContext = createContext<DatasetContextType>({
  datasetInfo: null,
  isUploaded: false,
  loading: true,
  refreshDataset: async () => {},
});

export const DatasetProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [datasetInfo, setDatasetInfo] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const refreshDataset = async () => {
    try {
      const res = await axios.get('/api/dataset/active');
      if (res.data && (res.data.active === true || (res.data.row_count && res.data.row_count > 0))) {
        setDatasetInfo(res.data);
      } else {
        setDatasetInfo(null);
      }
    } catch (err) {
      setDatasetInfo(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshDataset();
  }, []);

  const isUploaded = Boolean(
    datasetInfo && (datasetInfo.active === true || (datasetInfo.row_count && datasetInfo.row_count > 0))
  );

  return (
    <DatasetContext.Provider value={{ datasetInfo, isUploaded, loading, refreshDataset }}>
      {children}
    </DatasetContext.Provider>
  );
};

export const useDataset = () => useContext(DatasetContext);
