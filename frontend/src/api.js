import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const authAPI = {
  register: (email, password) => api.post('/api/v1/auth/register', { email, password }),
  login: (email, password) => api.post('/api/v1/auth/login', { email, password }),
}

export const grievancesAPI = {
  create: (data) => api.post('/api/v1/grievances/', data).then(res => res.data),
  list: () => api.get('/api/v1/grievances/').then(res => res.data),
  get: (id) => api.get(`/api/v1/grievances/${id}`).then(res => res.data),
  update: (id, data) => api.patch(`/api/v1/grievances/${id}`, data).then(res => res.data),
}

export const filesAPI = {
  upload: (file, userId) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/api/v1/files/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  download: (fileId) => api.get(`/api/v1/files/${fileId}`),
  delete: (fileId) => api.delete(`/api/v1/files/${fileId}`),
}

export default api
