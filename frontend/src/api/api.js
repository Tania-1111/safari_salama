import axios from 'axios';

const API_URL = 'http://localhost:5197/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});


// Add a request interceptor to attach the auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth endpoints
export const login = async (credentials) => {
  const response = await api.post('/auth/login', credentials);
  return response.data;
};

export const register = async (userData) => {
  const response = await api.post('/auth/register', userData);
  return response.data;
};

// Guardian endpoints
export const getStudents = async () => {
  const response = await api.get('/guardian/students');
  return response.data;
};

export const getTrips = async () => {
  const response = await api.get('/guardian/trips');
  return response.data;
};

// Admin endpoints
export const getAllGuardians = async () => {
  const response = await api.get('/admin/guardians');
  return response.data;
};

export const getAllStudents = async () => {
  const response = await api.get('/admin/students');
  return response.data;
};

export const getAllBuses = async () => {
  const response = await api.get('/admin/buses');
  return response.data;
};
