from api.models import Blackout, Initiator
from django.db.models import Count, Q
from django.utils import timezone

async def get_outages_stats(request):
    type_mapping = {
        'HW': 'hot_water',
        'CW': 'cold_water',
        'EL': 'electricity'
    }
    _type_query = Q(end_date__gte=timezone.now())
    _type_query.add(Q(start_date_lte=timezone.now()), Q.AND)
    _type_query.add(Q(type__in=['HW', 'CW', 'EL']), Q.AND)
    _type_data = await Blackout.objects.filter(
        _type_query
    ).values('type').annotate(count=Count('blackout_id')).all()
    # _types_result = dict()
    # async for item in _type_stats:
    #     _types_result[item['type']] = {"value": item['count']}
    org_data = await Blackout.objects.filter(
        _type_query
    ).values('initiator_id', 'initiator_id__initiator_name') \
        .annotate(count=Count('blackout_id'))\
        .order_by('count').all()
    return _type_data, org_data