from api.models import BlackoutBuilding
from django.db.models import Count, Q
from django.utils import timezone


async def get_address(request):
    today = timezone.now()
    query = Q(blackout_id__isnull =False)
    query.add(Q(blackout_id__start_date__lte=today), Q.AND)
    query.add(Q(blackout_id__end_date__lte=today), Q.AND)
    data = await BlackoutBuilding.objects().filter(query)\
        .values('blackout_id__type', 'blackout_id__description', 'building_id__street_id__street_name',
                'building_id__name', 'building_id__coordinates').all()
    return data