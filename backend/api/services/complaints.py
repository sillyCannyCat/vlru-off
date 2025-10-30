from api.models import Blackout
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from asgiref.sync import sync_to_async


@sync_to_async
def get_complaints(request):
    comp_query = Q(start_date__gte=timezone.now() - timedelta(days=1))
    comp_query.add(Q(end_date__isnull=True), Q.AND)
    comp_data = Blackout.objects.filter(comp_query) \
        .values('type', 'start_date') \
        .annotate(count=Count('blackout_id')).all()
    return comp_data


@sync_to_async
def get_complaints_graph(_type: str):
    today = timezone.now() + timedelta(hours=10)
    data = dict()
    if _type == '24h':
        for hour in range(today.hour):
            now_time = today
            now_time = now_time.replace(hour=hour)
            now_time = now_time.replace(minute=0)
            now_time = now_time.replace(second=0)
            query = Q(start_date__gte=now_time)
            query.add(Q(end_date__isnull=True), Q.AND)
            query.add(Q(start_date__lt=now_time + timedelta(days=1)), Q.AND)
            query.add(Q(type__in=['HW', 'CW', 'EL']), Q.AND)
            now_data = Blackout.objects.filter(
                query
            ).values('type').annotate(count=Count('blackout_id'))\
                .values_list('type', 'count')
            # print(now_data.values_list()[0])
            if len(now_data) >0:
                data[now_time] = now_data[0]
    elif _type == '60m':
        for hour in range(today.hour):
            for minute_cof in range(12):
                now_time = today
                now_time = now_time.replace(hour=hour)
                now_time = now_time.replace(minute=5*minute_cof)
                now_time = now_time.replace(second=0)
                query = Q(start_date__gte=now_time)
                query.add(Q(end_date__isnull=True), Q.AND)
                query.add(Q(start_date__lt=now_time + timedelta(days=1)), Q.AND)
                query.add(Q(type__in=['HW', 'CW', 'EL']), Q.AND)
                now_data = Blackout.objects.filter(
                    query
                ).values('type').annotate(count=Count('blackout_id')) \
                    .values_list('type', 'count')
                if len(now_data) > 0:
                    data[now_time] = now_data[0]
    return data
