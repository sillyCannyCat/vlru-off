from ninja import Router
from api.schemas.outages import OutagesStatsOut, TodayStatsOut
from api.schemas.errors import ErrorSchema
from django.utils import timezone
from api.services.outages import get_outages_stats, get_outages_stats_today

router = Router(tags=['outages'])


@router.get('/stats/', response={200: OutagesStatsOut, 500: ErrorSchema})
async def outages_stats(request):
    try:
        _type_mapping = {
            'HW': 'hot_water',
            'CW': 'cold_water',
            'EL': 'electricity'
        }

        _type_data, org_data = await get_outages_stats(request)

        _type_result = {}
        for item in _type_data:
            _type_result[_type_mapping[item['type']]] = {'value': item['count']}

        for key in _type_mapping.values():
            _type_result.setdefault(key, {'value': 0})

        org_result = [
            {
                'id': item['initiator_id'],
                'name': item['initiator_id__initiator_name'],
                'value': item['count']
            }
            for item in org_data
        ]

        return {
            'types': _type_result,
            'organizations': org_result
        }

    except Exception as e:
        return 500, {'message': f'Ошибка при получении статистики отключений: {e}'}


@router.get('/stats/today/', response={200: TodayStatsOut, 500: ErrorSchema})
async def today_stats(request):
    try:
        today_count, yesterday_count, planned_count = await get_outages_stats_today(request)
        percent = round(yesterday_count / (today_count / 100))
        return {
            'date': str(timezone.now().date()),
            'today_count': today_count,
            'yesterday_count': yesterday_count,
            'difference': today_count - yesterday_count,
            'difference_percentage': 100 - percent,
            'trend': 'up' if today_count > yesterday_count else \
                'down' if today_count < yesterday_count else 'same',
            'planned_count': planned_count
        }
    except Exception as e:
        return 500, {"message": "Ошибка при получении статистики на сегодня"}
