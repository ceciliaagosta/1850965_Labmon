import { api } from "./api";

// admin routes
export async function _fetchAllUsers() {
  const res = await api.get(`/users`)
  return res
}

export async function _manualRegister(credentials) {
    const res = await api.post(`/users`, credentials)
    return res
}

// ---

// fixare in be: torna sempre lo user che effettua la chiamata invece di userId
export async function _fetchUser(userId) {
  const res = await api.get(`/users/${userId}`)
  return res
}

export async function _updateUser(userId, userData) {
    const res = await api.put(`/users/${userId}`, userData)
    return res
}

export async function _deleteUser(userId) {
    const res = await api.delete(`/users/${userId}`)
    return res
}