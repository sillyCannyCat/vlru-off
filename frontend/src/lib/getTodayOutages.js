import api from './apiAxios.js'

export async function getTodayOutages() {
  const response = await api.get(`/outages/stats/today/`)
  return response.data
}
