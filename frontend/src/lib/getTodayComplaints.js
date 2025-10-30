import axios from 'axios'

export async function getTodayComplaints() {
  const response = await axios.get(``)
  return response.data
}
