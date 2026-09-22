import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
  headers: { 'Content-Type': 'application/json' },
  timeout: 30000,
});

export async function analyzeText(text) {
  const response = await api.post('/analyze', { text });
  return response.data;
}

export async function simplifyText(text) {
  const response = await api.post('/simplify', { text });
  return response.data;
}

export default api;
