import { api } from "./api";

// admin routes
export async function _fetchAllMonsters() {
  const res = await api.get(`/monsters`)
  return res
}

export async function _createMonster(monsterData) {
    const res = await api.post(`/monsters`, monsterData)
    return res
}

export async function _updateMonster(monsterId, monsterData) {
    const res = await api.put(`/monsters/${monsterId}`, monsterData)
    return res
}

export async function _deleteMonster(monsterId) {
    const res = await api.delete(`/monsters/${monsterId}`)
    return res
}

// ---

export async function _fetchMonster(monsterId) {
  const res = await api.get(`/monsters/${monsterId}`)
  return res
}