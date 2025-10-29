import axios from 'axios'

const gameApi = axios.create({
  baseURL: '/api/game', 
  // baseURL: "http://localhost:5004/game",
  timeout: 10000
})

gameApi.interceptors.request.use(
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
export async function _fetchAllEncounters() {
  const res = await gameApi.get(`/encounters`)
  return res
}
// ---

export async function _generateEncounter() {
  const res = await gameApi.post(`/encounters`)
  return res
}

export async function _fetchEncounter(encounterId) {
  const res = await gameApi.get(`/encounters/${encounterId}`)
  return res
}

export async function _quitEncounter(encounterId) {
  const res = await gameApi.delete(`/encounters/${encounterId}`)
  return res
}

export async function _catchEncounter(encounterId) {
  const res = await gameApi.post(`/encounters/${encounterId}/catch`)
  return res
}

export async function _startTimer() {
  const res = await gameApi.post('/timer')
}

export async function _getCollection() {
  const res = await gameApi.get('/collection')
  return res
}

export async function _shard(monsterId) {
  const res = await gameApi.put('/collection/shard', {
    monster_id: monsterId
  })
  return res
}

export async function _getInventory() {
  const res = await gameApi.get('/inventory')
  return res
}
