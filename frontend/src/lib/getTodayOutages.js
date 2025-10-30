import axios from 'axios'

export async function getTodayOutages() {
  const response = await axios.get(``)
  return response.data
}
