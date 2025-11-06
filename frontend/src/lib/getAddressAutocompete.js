import api from './apiAxios.js'

export async function getAddressAutocomplete(queryAddress) {
  const response = await api.get(`/address/autocomplete/`, {
    params: { query: queryAddress },
  })
  return response.data
}
