import axios from 'axios'

const monstersApi = axios.create({
  // baseURL: '/api/monsters', 
  baseURL: "http://localhost:5002/monsters",
  timeout: 10000
})

monstersApi.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}` 
    }
    return config
  },
  (error) => Promise.reject(error)
)

// admin routes
export async function _fetchAllMonsters() {
  const res = await monstersApi.get(``)
  return res
}

export async function _createMonster(monsterData) {
    const res = await monstersApi.post(``, monsterData)
    return res
}

export async function _updateMonster(monsterId, monsterData) {
    const res = await monstersApi.put(`/${monsterId}`, monsterData)
    return res
}

export async function _deleteMonster(monsterId) {
    const res = await monstersApi.delete(`/${monsterId}`)
    return res
}

// ---

export async function _fetchMonster(monsterId) {
  const res = await monstersApi.get(`/${monsterId}`)
  return res
}
export { monstersApi }