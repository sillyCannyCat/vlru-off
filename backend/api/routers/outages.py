from ninja import Router
from api.models import Blackout, Initiator
from api.schemas.outages import OutagesStatsOut
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

router = Router(tags=['outages'])


@router.get('/', response={200: OutagesStatsOut})
async def outages_stats(request):
    
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