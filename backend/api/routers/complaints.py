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
            'count':count,
            'created_at':timezone.now()
        }
    except Exception as e:
        return 500, {'message':'Ошибка сервера при обработке жалоб'}

@router.get('/graph/', response={200: ComplaintGraphOut, 400: ErrorSchema, 500: ErrorSchema})
async def complaints_graph(request, type: str):
    black_type_mapping = {
        'HW': 'hot_water',
        'CW': 'cold_water',
        'EL': 'electricity',
    }

    if type not in ['24h', '60m']:
        return 400, {'message': 'Неправильный type. Должен быть "24h" или "60m"'}

    try:
        raw_data = await get_complaints_graph(type)
        data = []

        for timestamp, values in raw_data.items():
            row = {
                "time": f"{timestamp.hour:02}:{timestamp.minute:02}"
            }
            for black_type, value in values.items():
                row[black_type_mapping[black_type]] = value
            data.append(row)

        return {"data": data}

    except Exception as e:
        return 500, {"message": f"Ошибка сервера при построении графиков: {e}"}
