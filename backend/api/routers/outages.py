from ninja import Router
from api.models import Blackout, Initiator
from api.schemas.outages import OutagesStatsOut,TodayStatsOut
from api.schemas.errors import ErrorSchema
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

router = Router(tags=['outages'])

@router.get('/', response={200: OutagesStatsOut, 500: ErrorSchema})
async def outages_stats(request):
    try:
        type_mapping = {
            'HW': 'hot_water',
            'CW': 'cold_water',
            'EL': 'electricity'
        }

        type_stats = await Blackout.objects.filter(
            end_data__isnull=True,
            type__in=type_mapping.keys()
        ).values('type').annotate(count=Count('blackout_id')).all()

        types_result = {}
        async for item in type_stats:
            key = type_mapping.get(item['type'], item['type'].lower())
            types_result[key] = {"value": item['count']}
        for name in type_mapping.values():
            types_result.setdefault(name, {"value": 0})

        org_stats = await Blackout.objects.filter(
            end_data__isnull=True,
            initiator_id__isnull=False
        ).values('initiator_id', 'initiator_id__initiator_name') \
         .annotate(count=Count('blackout_id')) \
         .order_by('-count')[:5].all()

        organizations = []
        async for item in org_stats:
            organizations.append({
                "id": item['initiator_id'],
                "name": item['initiator_id__initiator_name'] or f"Организация {item['initiator_id']}",
                "value": item['count']
            })

        return {
            "types": types_result,
            "organizations": organizations
        }

    except Exception as e:
        return 500, {"message": "Ошибка при получении статистики отключений"}

@router.get('/today/', response={200: TodayStatsOut, 500: ErrorSchema})
async def today_stats(request):
    try:
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        today_count = await Blackout.objects.filter(start_date__date=today, end_data__isnull=True).acount()
        yesterday_count = await Blackout.objects.filter(start_date__date=yesterday, end_data__isnull=True).acount()
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