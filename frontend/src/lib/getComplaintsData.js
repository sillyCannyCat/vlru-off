import api from './apiAxios.js'

export async function getComplaintsData(period) {
  const response = await api.get(`/complaints/graph/`, { params: { type: period } })
  return response.data
}
