from ninja import Router
from api.schemas.address import AddressAutocompleteOut
from api.schemas.errors import ErrorSchema
from api.services.address import get_autocomplete

router = Router(tags=['address'])

@router.get('/autocomplete', response={200: AddressAutocompleteOut, 500: ErrorSchema})
async def autocomplete(request):
    query = request.get()['query']
    if 0>=len(query.split) > 2 :
        return {'data':list()}
    try:
        data = await get_autocomplete(query)
        to_return = list()
        if len(query.split) == 1:
            for item in data:
                to_return.append({'type':'address',
                                  'full_address':item['street']})
        elif len(query.split) == 2:
            for item in data:
                to_return.append({'type':'address',
                                  'full_address':f'{item['street']} {item['number']}'})
        return {
            'data':to_return
        }
    except Exception:
        return 500, {'message': 'Ошибка в автокомплите'}