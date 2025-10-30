import api from './apiAxios.js'

export async function getAddressData(queryAddress) {
  const response = await api.get(`/address/`, {
    params: { query: queryAddress },
  })
  return response.data
}
