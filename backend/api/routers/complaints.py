from idna import valid_label_length
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
            'HT': 'heat',
            'HW': 'hot_water',
            'CW': 'cold_water',
            'EL': 'electricity'
        }
        complaints_data = await get_complaints(request)
        count = [
            ['heat', 0],
            ['hot_water', 0],
            ['cold_water', 0],
            ['electricity', 0]
        ]
        _type_to_ind ={
            'heat': 0,
            'hot_water': 1,
            'cold_water': 2,
            'electricity': 3
        }
        all_count = 0
        async for item in complaints_data:
            count[_type_to_ind[_type_vals[item['type']]]][-1] += item['count']
            all_count += item['count']
        count.sort(key=lambda x:x[-1], reverse=True)
        _types = list()
        for item in filter(lambda x: x[-1] >0, count[:2]):
            print(item[0])
            _types.append(item[0])
        return {
            'report_date' : str(timezone.now().date()),
            'summary':_types,
            'count':all_count,
            'created_at': str(timezone.now())
        }
    except Exception as e:
        return 500, {'message': f'Ошибка сервера при обработке жалоб: {e}'}

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
            print(values[0])
            for _type in black_type_mapping:
                row.setdefault(black_type_mapping[_type], 0)
            row[black_type_mapping[values[0]]] = values[-1]
            data.append(row)
        print(data)
        return {"data": data}

    except Exception as e:
        return 500, {"message": f"Ошибка сервера при построении графиков: {e}"}
