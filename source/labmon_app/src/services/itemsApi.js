import axios from 'axios'

const itemsApi = axios.create({
  baseURL: '/api/items', 
//   baseURL: "http://localhost:5003/items",
  timeout: 10000
})

itemsApi.interceptors.request.use(
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
export async function _fetchAllItems() {
  const res = await itemsApi.get(``)
  return res
}

export async function _createItem(itemData) {
    const res = await itemsApi.post(``, itemData)
    return res
}

export async function _updateItem(itemId, itemData) {
    const res = await itemsApi.put(`/${itemId}`, itemData)
    return res
}

export async function _deleteItem(itemId) {
    const res = await itemsApi.delete(`/${itemId}`)
    return res
}

// ---

export async function _fetchItem(itemId) {
  const res = await itemsApi.get(`/${itemId}`)
  return res
}