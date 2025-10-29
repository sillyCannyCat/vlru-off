from ninja import Router
from api.models import Blackout, Initiator
from api.schemas.outages import OutagesStatsOut,TodayStatsOut
from api.schemas.errors import ErrorSchema
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from api.services.outagers import get_outages_stats

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
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        today_count = await Blackout.objects.filter(start_date__date=today, end_date__isnull=True).acount()
        yesterday_count = await Blackout.objects.filter(start_date__date=yesterday, end_date__isnull=True).acount()
        planned_count = await Blackout.objects.filter(start_date__date=today, description__icontains="плановое").acount()

        difference = today_count - yesterday_count
        difference_percent = round(abs(difference / yesterday_count * 100), 2) if yesterday_count > 0 else 0
        trend = "up" if difference > 0 else "down" if difference < 0 else "same"

        return {
            "date": today.strftime("%Y-%m-%d"),
            "today_count": today_count,
            "yesterday_count": yesterday_count,
            "planned_count": planned_count,
            "difference": difference,
            "difference_percent": int(difference_percent),
            "trend": trend
        }

    except Exception as e:
        return 500, {"message": "Ошибка при получении статистики на сегодня"}