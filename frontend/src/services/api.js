import axios from 'axios';

const API_BASE_URL = 'https://izob8k3keg.execute-api.us-east-1.amazonaws.com/prod';

export const fetchDashboardSummary = async () => {
  const response = await axios.get(`${API_BASE_URL}/dashboard/summary`);
  return response.data;
};

export const fetchCategoryBreakdown = async () => {
  const response = await axios.get(`${API_BASE_URL}/dashboard/categories`);
  return response.data;
};

export const fetchMetric = async (metricType) => {
  const response = await axios.get(`${API_BASE_URL}/metrics/${metricType}`);
  return response.data;
};
