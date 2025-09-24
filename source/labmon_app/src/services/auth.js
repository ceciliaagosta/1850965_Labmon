import { useAuthStore } from "../stores/authStore";
import { api } from "./api";

export async function _register(credentials) {
  const res = await api.post(`/register`, credentials)
  return res
}

export async function _login(credentials) {
  const res = await api.post(`/login`, credentials)
  return res
}

export async function _tokenExpired() {
  const authStore = useAuthStore()
  authStore.logout()
  return
}