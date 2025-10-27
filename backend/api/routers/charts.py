from ninja import Router
from typing import List
from api.models import Blackout
from api.schemas.charts import StatsByType, StatsByDistrict, TimelineStats, ChartFilterIn
from api.schemas.errors import ErrorSchema
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from models import BlackoutsBuilding

router = Router(tags=['charts'])

@router.get('/stats/by_type', response={200: List[StatsByType], 400: ErrorSchema})
def stats_by_type(request, filters: ChartFilterIn = None):
    query = Q()
    if filters and filters.start_date:
        query &= Q(start_date__gte=filters.start_date)
    if filters and filters.end_date:
        query &= Q(start_date__lte=filters.end_date)
    stats = Blackout.objects.filter(query).values('type').annotate(count=Count('blackout_id'))
    return [{'type': item['type'], 'count': item['count']} for item in stats]

@router.get('/stats/by_district', response={200: List[StatsByDistrict], 400: ErrorSchema})
def stats_by_district(request, filters: ChartFilterIn = None):
    query = Q()
    if filters and filters.start_date:
        query &= Q(blackout__start_date__gte=filters.start_date)
    if filters and filters.end_date:
        query &= Q(blackout__start_date__lte=filters.end_date)
    if filters and filters.type:
        query &= Q(blackout__type=filters.type)
    stats = BlackoutsBuilding.objects.filter(query).values('building_id__district_id__district_name').annotate(count=Count('blackout_id'))
    return [{'district_name': item['building_id__district_id__district_name'], 'count': item['count']} for item in stats if item['building_id__district_id__district_name']]

@router.get('/stats/timeline', response={200: List[TimelineStats], 400: ErrorSchema})
def timeline_stats(request, filters: ChartFilterIn = None):
    query = Q()
    if filters and filters.start_date:
        query &= Q(start_date__gte=filters.start_date)
    if filters and filters.end_date:
        query &= Q(start_date__lte=filters.end_date)
    if filters and filters.type:
        query &= Q(type=filters.type)
    stats = Blackout.objects.filter(query).annotate(date=TruncDate('start_date')).values('date').annotate(count=Count('blackout_id')).order_by('date')
    return [{'date': item['date'], 'count': item['count']} for item in stats]