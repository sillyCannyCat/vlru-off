from ninja import Router
from typing import List, Dict
from api.models import Blackout, BlackoutsBuilding, Building, Street, Initiator
from api.schemas.maps import AddressSuggestion, TodayStatsOut, BlackoutOut, OutagesStatsOut, ComplaintSummaryOut, ComplaintGraphItem, ComplaintGraphOut
from api.schemas.errors import ErrorSchema
from django.db.models import Prefetch, Q, Count
from django.utils import timezone
from datetime import timedelta, datetime as dt
from aiocache import cached
from aiocache.serializers import JsonSerializer
from api.models import Complaint
import pytz

router = Router(tags=['maps'])

@cached(ttl=300, serializer=JsonSerializer())
async def cached_street_search(query: str):
    streets = await Street.objects.filter(
        street_name__istartswith=query
    ).values('street_name').distinct()[:10].all()
    return [s['street_name'] async for s in streets]


@cached(ttl=300, serializer=JsonSerializer())
async def cached_house_search(street_part: str, number_part: str):
    streets = await Street.objects.filter(street_name__icontains=street_part).all()
    if not streets:
        return []

    street_ids = [s.street_id async for s in streets]
    buildings = await Building.objects.filter(
        street_id__in=street_ids,
        number__icontains=number_part
    ).select_related('street_id')[:10].all()

    results = []
    async for b in buildings:
        full_addr = f"{b.street_id.street_name} ул. {b.number}"
        results.append({
            "type": "house",
            "street": b.street_id.street_name,
            "full_address": full_addr
        })
    return results

@router.get('/address/autocomplete/', response={200: List[AddressSuggestion], 400: ErrorSchema})
async def address_autocomplete(request, query: str = ''):
    if not query or not query.strip():
        return 400, {'message': 'Параметр query обязателен'}

    query = query.strip()
    parts = query.split()
    has_number = any(
        part.replace('А', '').replace('Б', '').replace('а', '').replace('б', '').isdigit()
        for part in parts
    )

    if not has_number:
        street_names = await cached_street_search(query)
        return [{"type": "street", "name": name} for name in street_names]
    else:
        number_part = next(
            (p for p in reversed(parts) if p.replace('А', '').replace('Б', '').replace('а', '').replace('б', '').isdigit()),
            ''
        )
        street_part = ' '.join([
            p for p in parts
            if p != number_part and not p.replace('А', '').replace('Б', '').replace('а', '').replace('б', '').isdigit()
        ])

        houses = await cached_house_search(street_part, number_part.replace('А', '').replace('Б', '').replace('а', '').replace('б', ''))
        return houses

@router.get('/outages/stats/today/', response={200: TodayStatsOut})
async def today_stats(request):
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)

    today_count = await Blackout.objects.filter(
        start_date__date=today,
        end_data__isnull=True
    ).acount()

    yesterday_count = await Blackout.objects.filter(
        start_date__date=yesterday,
        end_data__isnull=True
    ).acount()

    planned_count = await Blackout.objects.filter(
        start_date__date=today,
        description__icontains="плановое"
    ).acount()

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

@router.get('/blackouts/', response={200: List[BlackoutOut], 404: ErrorSchema})
async def get_blackouts(request):
    blackouts = await Blackout.objects.filter(end_data__isnull=True) \
        .select_related('initiator_id', 'source_id') \
        .prefetch_related(
            Prefetch(
                'blackoutsbuilding_set',
                queryset=BlackoutsBuilding.objects.select_related('building_id'),
                to_attr='buildings_links'
            )
        ).all()

    if not blackouts:
        return 404, {'message': 'Нет активных отключений'}

    results = []
    async for blackout in blackouts:
        buildings = []
        async for link in blackout.buildings_links:
            building = link.building_id
            street_name = building.street_id.street_name if building.street_id else None
            district_name = building.district_id.district_name if building.district_id else None
            folk_district_name = building.folk_district_id.folk_district_name if building.folk_district_id else None
            lat, lon = building.get_coordinates()
            buildings.append({
                'building_id': str(building.building_id),
                'street_name': street_name,
                'number': building.number,
                'district_name': district_name,
                'folk_district_name': folk_district_name,
                'latitude': lat,
                'longitude': lon
            })
        results.append({
            'blackout_id': str(blackout.blackout_id),
            'start_date': blackout.start_date,
            'end_date': blackout.end_data,
            'description': blackout.description,
            'type': blackout.type,
            'initiator_name': blackout.initiator_id.initiator_name if blackout.initiator_id else None,
            'source_name': blackout.source_id.source_name if blackout.source_id else None,
            'buildings': buildings
        })
    return results

@router.get('/outages/stats/', response={200: OutagesStatsOut})
async def outages_stats(request):
    type_mapping = {
        'HW': 'hot_water',
        'CW': 'cold_water',
        'EL': 'electricity',
        'HT': 'heating'
    }

    type_stats = await Blackout.objects.filter(
        end_data__isnull=True
    ).values('type').annotate(count=Count('blackout_id')).all()

    types_result = {}
    async for item in type_stats:
        key = type_mapping.get(item['type'], item['type'].lower())
        types_result[key] = {"value": item['count']}

    for name in type_mapping.values():
        types_result.setdefault(name, {"value": 0})

    REQUIRED_ORGS = [
        "МУВП ВПЭС",
        'КГУП "Приморский водоканал"',
        "Управляющие компании"
    ]

    org_objects = await Initiator.objects.filter(
        initiator_name__in=REQUIRED_ORGS
    ).all()

    org_name_to_id = {}
    async for org in org_objects:
        org_name_to_id[org.initiator_name] = org.initiator_id

    org_stats = await Blackout.objects.filter(
        end_data__isnull=True,
        initiator_id__in=org_name_to_id.values()
    ).values('initiator_id').annotate(count=Count('blackout_id')).all()

    org_count_map = {}
    async for item in org_stats:
        org_count_map[item['initiator_id']] = item['count']

    organizations = []
    for name in REQUIRED_ORGS:
        org_id = org_name_to_id.get(name)
        count = org_count_map.get(org_id, 0)
        organizations.append({
            "id": org_id or 0,
            "name": name,
            "value": count
        })

    return {
        "types": types_result,
        "organizations": organizations
    }

@router.get('/complaints/', response={200: ComplaintSummaryOut})
async def complaints_summary(request):
    """Сводка по жалобам за последние 24 часа"""
    now = timezone.now()
    start = now - timedelta(hours=24)

    complaints = await Complaint.objects.filter(
        created_at__gte=start
    ).all()

    count = await Complaint.objects.filter(created_at__gte=start).acount()

    type_counts = {"HW": 0, "CW": 0, "EL": 0}
    async for c in complaints:
        type_counts[c.type] += 1

    parts = []
    if type_counts["HW"] > 5:
        parts.append("горячей воды")
    if type_counts["CW"] > 5:
        parts.append("холодной воды")
    if type_counts["EL"] > 5:
        parts.append("света")

    if parts:
        summary = f"Жители сообщают о множественных отключениях {', '.join(parts[:-1]) + ' и ' + parts[-1] if len(parts) > 1 else parts[0]}"
    else:
        summary = "Жалоб за последние 24 часа не поступало"

    local_tz = pytz.timezone('Asia/Vladivostok')
    local_now = now.astimezone(local_tz)

    return {
        "report_date": now.strftime("%Y-%m-%d"),
        "summary": summary,
        "complaint_count": count,
        "created_at": local_now.isoformat()
    }

@router.get('/complaints/graph/', response={200: ComplaintGraphOut})
async def complaints_graph(request, type: str = "24h"):
    now = timezone.now()
    local_tz = pytz.timezone('Asia/Vladivostok')
    now_local = now.astimezone(local_tz)

    if type == "60m":
        start = now - timedelta(minutes=60)
        interval = timedelta(minutes=10)
        format_str = "%H:%M"
        hours = [start + i * interval for i in range(7)]
    else:
        start = now - timedelta(hours=24)
        interval = timedelta(hours=1)
        format_str = "%H:00"
        hours = [start + i * interval for i in range(25)]

    data = []
    for h in hours:
        data.append({
            "time": h.astimezone(local_tz).strftime(format_str),
            "cold_water": 0,
            "hot_water": 0,
            "electricity": 0
        })

    complaints = await Complaint.objects.filter(
        created_at__gte=start
    ).all()

    type_map = {"CW": "cold_water", "HW": "hot_water", "EL": "electricity"}

    async for c in complaints:
        c_local = c.created_at.astimezone(local_tz)
        for i, h in enumerate(hours):
            if i == len(hours) - 1 or c_local < hours[i + 1]:
                key = type_map.get(c.type, None)
                if key:
                    data[i][key] += 1
                break

    return {"data": data}