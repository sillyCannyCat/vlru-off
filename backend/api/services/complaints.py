from api.models import Blackout
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

async def get_complaints():
    today = timezone.now()
    comp_query = Q(start_date__isnull=timezone.now())
    comp_query.add(Q(end_date__isnull=True), Q.AND)
    comp_data = Blackout.objects.filter(comp_query)\
        .values('type', 'start_date')\
        .annotate(count=Count('blackout_id')).all()
    return comp_data