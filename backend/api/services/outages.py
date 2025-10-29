from api.models import Blackout, Initiator
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

async def get_outages_stats(request):
    _type_query = Q(end_date__gte=timezone.now())
    _type_query.add(Q(start_date__lte=timezone.now()), Q.AND)
    _type_query.add(Q(type__in=['HW', 'CW', 'EL']), Q.AND)
    _type_data = await Blackout.objects.filter(
        _type_query
    ).values('type').annotate(count=Count('blackout_id')).all()
    org_data = await Blackout.objects.filter(
        _type_query
    ).values('initiator_id', 'initiator_id__initiator_name') \
        .annotate(count=Count('blackout_id'))\
        .order_by('count').all()
    return _type_data, org_data

async def get_outages_stats_today(request):
    today = timezone.now()
    yesterday = today - timedelta(days=1)
    today_query = Q(start_date__lte=today)
    today_query.add(Q(end_date__gte=today), Q.AND)
    today_query.add(Q(end_date__isnull=True), Q.OR)
    today_count =  await Blackout.objects.filter(today_query).count()
    yesterday_query = Q(start_date__lte=yesterday)
    yesterday_query.add(Q(end_date__gte=yesterday), Q.AND)
    yesterday_query.add(Q(end_date__isnull=True), Q.OR)
    yesterday_count = await Blackout.objects.filter(yesterday_query).count()
    planned_query= Q(start_date__lte=today)
    planned_query.add(Q(end_date__gte=today), Q.AND)
    planned_count = await Blackout.objects.filter(planned_query).count()
    return today_count, yesterday_count, planned_count
