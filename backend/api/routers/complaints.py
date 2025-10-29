from ninja import Router
from api.schemas.complaints import ComplaintSummaryOut, ComplaintGraphOut, ComplaintGraphItem
from api.schemas.errors import ErrorSchema
from api.services.complaints import get_complaints, get_complaints_graph
from django.utils import timezone


router = Router(tags=['complaints'])


@router.get('/', response={200: ComplaintSummaryOut, 500: ErrorSchema})
async def complaints_summary(request):
    try:
        _type_vals = {
            'HT': 'Heat',
            'HW': 'Hot water',
            'CW': 'Cold water',
            'EL': 'Electricity'
        }
        complaints_data = await get_complaints(request)
        count = 0
        _types = list()
        for item in complaints_data:
            _types.append(_type_vals[item[0]])
            count += item[-1]
        return {
            'report_date' : timezone.now().date,
            'summary':_types,
            'complaint_count':count,
            'created_at':timezone.now()
        }
    except Exception as e:
        return 500, {'message':'Ошибка сервера при обработке жалоб'}

@router.get('/graph/', response={{200: ComplaintGraphOut, 400: ErrorSchema, 500: ErrorSchema}})
async def complaints_graph(request):
    _type = request.get()['type']
    black_type_mapping = {
        'HW': 'hot_water',
        'CW': 'cold_water',
        'EL': 'electricity'
    }
    if _type not in ['24h', '60m']:
        return 400, {'message':'Неправильный type\n'
                               'Должен быть или "24h" или "60m"'}
    try:
        raw_data = await get_complaints_graph(_type)
        data = list()
        for timestamp in raw_data.keys():
            to_data = dict()
            to_data['time'] = (f'{str(timestamp.hour).ljust(2, '0')}:'
                               f'{str(timestamp.minute).ljust(2, '0')}')
            for black_type in raw_data[timestamp]:
                to_data[black_type_mapping[raw_data[timestamp]]] = raw_data[timestamp][black_type]
            data.append(to_data)
        return {'data':data}
    except Exception:
        return 500, {'message':'Ошибка сервера при построение граиков'}