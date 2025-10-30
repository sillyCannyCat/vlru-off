import axios from 'axios'

export async function getComplaintsData(period) {
  const response = await axios.get(``, { params: { type: period } })
  return response.data
}
