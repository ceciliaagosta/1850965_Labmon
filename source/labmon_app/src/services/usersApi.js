import axios from 'axios'
import { useAuthStore } from "../stores/authStore";

const usersApi = axios.create({
  // baseURL: '/api/users', 
  baseURL: "http://localhost:5001/users",
  timeout: 10000
})

usersApi.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}` 
    }
    return config
  },
  (error) => Promise.reject(error)
)

export async function _register(credentials) {
  const res = await usersApi.post(`/register`, credentials)
  return res
}

export async function _login(credentials) {
  const res = await usersApi.post(`/login`, credentials)
  return res
}

export async function _tokenExpired() {
  const authStore = useAuthStore()
  authStore.logout()
  return
}

// admin routes
export async function _fetchAllUsers() {
  const res = await usersApi.get(``)
  return res
}

export async function _manualRegister(credentials) {
    const res = await usersApi.post(``, credentials)
    return res
}
// ---

export async function _fetchUser(userId) {
  const res = await usersApi.get(`/${userId}`)
  return res
}

export async function _updateUser(userId, userData) {
    const res = await usersApi.put(`/${userId}`, userData)
    return res
}

export async function _deleteUser(userId) {
    const res = await usersApi.delete(`/${userId}`)
    return res
}
export { usersApi }