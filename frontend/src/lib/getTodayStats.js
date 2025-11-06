import api from './apiAxios.js'

export async function getTodayStats() {
  const response = await api.get(`/outages/stats/`)
  return { types: response.data.types, orgs: response.data.organizations }
}
