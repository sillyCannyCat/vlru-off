from api.models import Blackout
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

async def get_complaints(request):
    today = timezone.now()
    comp_query = Q(start_date__isnull=timezone.now())
    comp_query.add(Q(end_date__isnull=True), Q.AND)
    comp_data = Blackout.objects.filter(comp_query)\
        .values('type', 'start_date')\
        .annotate(count=Count('blackout_id')).all()
    return comp_data

async def get_complaints_graph(_type:str):
    today = timezone.now()
    data = dict()
    if _type == '24h':
        for hour in range(today.date().day):
            now_time = today
            now_time.hour = hour
            now_time.minute = 0
            now_time.second=0
            query = Q(start_date__gte=now_time)
            query.add(Q(end_date__isnull=True), Q.AND)
            query.add(Q(start_date__lt=now_time+ timedelta(days=1)), Q.AND)
            query.add(Q(type__in=['HW', 'CW', 'EL']), Q.AND)
            now_data =  await Blackout.objects.filter(
                    query
                ).values('type').annotate(count=Count('blackout_id')).all()
            data[now_time] = now_data
    elif _type == '60m':
        for hour in range(today.date().day):
            for minute_cof in range(12):
                now_time = today
                now_time.hour = hour
                now_time.minute = 5 * minute_cof
                now_time.second = 0
                query = Q(start_date__gte=now_time)
                query.add(Q(end_date__isnull=True), Q.AND)
                query.add(Q(start_date__lt=now_time + timedelta(days=1)), Q.AND)
                query.add(Q(type__in=['HW', 'CW', 'EL']), Q.AND)
                now_data = await Blackout.objects.filter(
                    query
                ).values('type').annotate(count=Count('blackout_id')).all()
                data[now_time] = now_data
    return data