import axios from 'axios'

export async function getTodayStats() {
  const response = await axios.get(``)
  return { types: response.data.types, orgs: response.data.organizations }
}
