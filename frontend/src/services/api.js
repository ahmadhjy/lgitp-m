import axios from 'axios';

export const MainUrl = 'http://localhost:8000';

const api = axios.create({
  baseURL: MainUrl,
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
