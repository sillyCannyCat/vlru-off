from ninja import Router
from api.schemas.address import AddressAutocompleteOut, AddressOut
from api.schemas.errors import ErrorSchema
from api.services.address import get_autocomplete, get_address_outages
from django.utils import timezone

router = Router(tags=['address'])


@router.get('/autocomplete/', response={200: AddressAutocompleteOut, 500: ErrorSchema})
async def autocomplete(request, query: str):
    try:
        data = await get_autocomplete(query)
        to_return = []

        if data['type'] == 'street':
            if not data['street']:
                return {'data': []}
            for item in data['street']:
                to_return.append({
                    'type': 'street',
                    'address': item['street_name']
                })

        else:
            if not data['address']:
                return {'data': []}
            for item in data['address']:
                to_return.append({
                    'type': 'address',
                    'address': f"{item['street_id__street_name']} {item['number']}"
                })

        return {'data': to_return}

    except Exception as e:
        return 500, {'message': f'Ошибка в автокомплите: {e}'}



@router.get('/', response={200: AddressOut, 500: ErrorSchema})
async def address(request, query: str):
    try:
        data = await get_address_outages(query)

        if not data or not data.get('flag'):
            return {
                'date': str(timezone.now().date()),
                'full_address': query,
                'outages_flag': False,
                'type': [],
                'outages_ending': [{'time': '', 'date': ''}]
            }

        _types = []
        outages_data = []

        for item in data['records']:
            end_date = item.get('blackout_id__end_date')
            end_time_str = (
                f"{end_date.hour:02}:{end_date.minute:02}"
                if end_date else ""
            )

            if item['blackout_id__type'] not in _types:
                _types.append(item['blackout_id__type'])

            outages_data.append({'time': end_time_str})

        return {
            'date': str(timezone.now().date()),
            'full_address': query,
            'outages_flag': True,
            'type': _types,
            'outages_ending': outages_data
        }

    except Exception as e:
        return 500, {'message': f'Ошибка в получении данных по адресу: {e}'}

