import axios from 'axios';

const baseURL = import.meta.env.VITE_API_URL || import.meta.env.VITE_API_BASE_URL || '/api';

const axiosClient = axios.create({
  baseURL: baseURL.endsWith('/api') ? baseURL : `${baseURL}/api`.replace(/\/\//g, '/').replace(':/', '://'),
  headers: {
    'Content-Type': 'application/json',
  },
});

axiosClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('dayflow_access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

axiosClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Clear token if unauthorized and not already on login
      if (!window.location.pathname.includes('/login')) {
        localStorage.removeItem('dayflow_access_token');
        localStorage.removeItem('dayflow_role');
        localStorage.removeItem('dayflow_employee_id');
        localStorage.removeItem('dayflow_user');
        window.location.href = '/login';
      }
    }

    let errorMsg = 'An unexpected error occurred';
    if (error.response?.data?.detail) {
      const detail = error.response.data.detail;
      if (typeof detail === 'string') {
        errorMsg = detail;
      } else if (Array.isArray(detail)) {
        errorMsg = detail.map((d) => d.msg || (typeof d === 'string' ? d : JSON.stringify(d))).join(', ');
      } else if (typeof detail === 'object') {
        errorMsg = JSON.stringify(detail);
      }
    } else if (error.message) {
      errorMsg = error.message;
    }

    return Promise.reject(errorMsg);
  }
);

export default axiosClient;
