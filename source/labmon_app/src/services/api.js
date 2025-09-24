import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5001', 
  timeout: 10000
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}` 
    }
    return config
  },
  (error) => Promise.reject(error)
)

export { api }