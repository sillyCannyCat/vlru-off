from os.path import split

from ninja import Router
from api.schemas.maps import MapAddressOut
from api.schemas.errors import ErrorSchema
from api.services.maps import get_address

router = Router(tags=['maps'])

def coordinate_converter(cords: str):
    data = cords.split(', ')
    to_return = list()
    to_return.append(float(data[0][9:]))
    to_return.append(float(data[-1][7:-3]))
    return to_return


@router.get('/', response={200: MapAddressOut, 500: ErrorSchema})
async def map_address(request):
    _type_vals = {
        'HT': 'Heat',
        'HW': 'Hot water',
        'CW': 'Cold water',
        'EL': 'Electricity'
    }
    data = await get_address(request)
    to_return = list()
    async for item in  data:
        to_return.append({
            'type': _type_vals[item['blackout_id__type']],
            'description': item['blackout_id__description'],
            'address': item['building_id__street_id__street_name'] + item['building_id__number'],
            'coordinates': coordinate_converter(item['building_id__coordinates'])
        })
    return{
        'data':to_return
    }