from ninja import Router
from api.models import Blackout, Initiator
from api.schemas.outages import OutagesStatsOut,TodayStatsOut
from api.schemas.errors import ErrorSchema
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from api.services.outagers import get_outages_stats,get_outages_stats_today

router = Router(tags=['outages'])

@router.get('/stats/', response={200: OutagesStatsOut, 500: ErrorSchema})
async def outages_stats(request):
    try:
        _type_mapping = {
            'HW': 'hot_water',
            'CW': 'cold_water',
            'EL': 'electricity'
        }
        _type_data, org_data = get_outages_stats(request)
        _type_result = dict()
        async for item in _type_data:
            _type_result[_type_mapping[item[0]]] = {'value' : item['count']}
        for _key in _type_mapping.keys():
            _type_result.setdefault(_key, {'value':0})
        org_result = list()
        async for item in org_data:
            org_result.append({
                'id' : org_data['initiator_id'],
                'name' : org_data['initiator_id__initiator_name'],
                'value' : org_data['count']
            })
        return {
            'types' : _type_result,
            'organizations' : org_data
        }
    except Exception as e:
        return 500, {"message": "Ошибка при получении статистики отключений"}

@router.get('/stats/today/', response={200: TodayStatsOut, 500: ErrorSchema})
async def today_stats(request):
    try:
        today_count, yesterday_count, planned_count = get_outages_stats_today(request)
        percent = round(yesterday_count/(today_count/100))
        return{
            'date' : timezone.now().date(),
            'today_count' : today_count,
            'yesterday_count':yesterday_count,
            'difference':today_count-yesterday_count,
            'percent':100-percent,
            'trend' : 'up'if today_count> yesterday_count else\
                'down' if today_count< yesterday_count else 'same'
        }
    except Exception as e:
        return 500, {"message": "Ошибка при получении статистики на сегодня"}