from ninja import Router
from api.schemas.address import AddressAutocompleteOut, AddressOut
from api.schemas.errors import ErrorSchema
from api.services.address import get_autocomplete, get_address_outages
from django.utils import timezone

router = Router(tags=['address'])


@router.get('/autocomplete', response={200: AddressAutocompleteOut, 500: ErrorSchema})
async def autocomplete(request, query: str):
    try:
        data = get_autocomplete(query)
        to_return = list()
        if data['type'] =='street':
            if data['street'] == 0:
                return to_return
            for item in data['street']:
                to_return.append({
                    'type': data['type'],
                    'name': item['street_name']
                })
        else:
            if data['address'] == 0:
                return to_return
            for item in data['address']:
                to_return.append({
                    'type': data['type'],
                    'name': item['street_name'] + item['number']
                })
        return to_return
    except Exception:
        return 500, {'message': 'Ошибка в автокомплите'}


@router.get('/', response={200: AddressOut, 500: ErrorSchema})
async def address(request, query: str):
    try:
        data = await get_address_outages(query)
        if data['flag'] == False:
            return {
                'date': str(timezone.now().date()),
                'full_address': query,
                'outages_flag': False,
                'type': list(),
                'outages_ending': [{'time': '',
                                    'date': ''}]
            }
        else:
            _types = list()
            outages_data = list()
            async for item in data:
                if item['blackout_id__type'] not in _types:
                    _types.append(item['blackout_id__type'])
                outages_data.append({
                    'time': f'{str(item['blackout_id__end_date'].hour).ljust(2, '0')}:'
                            f'{str(item['blackout_id__end_date'].minute).ljust(2, '0')}'
                })
            return {
                'date': str(timezone.now().date()),
                'full_address': query,
                'outages_flag': True,
                'type': _types,
                'outages_ending': outages_data
            }
    except Exception:
        return 500, {'message': 'Ошибка в получение данных по адрессу'}
