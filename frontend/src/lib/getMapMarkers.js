import api from './apiAxios.js'

export async function getMapMarkers() {
  const response = await api.get(`/maps/`)
  return response.data
}
