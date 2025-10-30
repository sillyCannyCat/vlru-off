import api from './apiAxios.js'

export async function getTodayComplaints() {
  const response = await api.get(`/complaints/`)
  return response.data
}
