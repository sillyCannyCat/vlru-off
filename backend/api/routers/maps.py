from ninja import Router
from typing import List
from api.models import Blackout, BlackoutsBuilding, Building, Street
from api.schemas.maps import AddressSuggestion, BlackoutOut
from api.schemas.errors import ErrorSchema
from django.db.models import Prefetch
from aiocache import cached
from aiocache.serializers import JsonSerializer
import re
import httpx
import os
from typing import Optional, Tuple

router = Router(tags=['maps'])

@cached(ttl=300, serializer=JsonSerializer())
async def cached_street_search(query: str):
    streets = await Street.objects.filter(
        street_name__istartswith=query
    ).values('street_name').distinct()[:10].all()
    return [s['street_name'] async for s in streets]


@cached(ttl=300, serializer=JsonSerializer())
async def cached_house_search(street_part: str, number_part: str):
    if not number_part:
        return []

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

async def geocode_address(address: str) -> Optional[Tuple[float, float]]:
    api_key = os.environ.get('YANDEX_API_KEY')
    if not api_key:
        raise ValueError('YANDEX_API_KEY не найден в .env')

    url = 'https://geocode-maps.yandex.ru/1.x/'
    params = {
        'apikey': api_key,
        'geocode': address,
        'format': 'json',
        'results': 1,
        'lang': 'ru_RU'
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

        geo_objects = data['response']['GeoObjectCollection']['featureMember']
        if not geo_objects:
            return None

        pos = geo_objects[0]['GeoObject']['Point']['pos']
        lon, lat = map(float, pos.split())
        return lat, lon

    except httpx.HTTPStatusError as e:
        print(f"Ошибка HTTP: {e.response.status_code} — {e.response.text}")
        return None
    except Exception as e:
        print(f"Ошибка геокодирования: {e}")
        return None

@router.get('/address/autocomplete/', response={200: List[AddressSuggestion], 400: ErrorSchema})
async def address_autocomplete(request, query: str = ''):
    if not query or not query.strip():
        return 400, {'message': 'Параметр query обязателен'}

    query = query.strip()
    parts = query.split()

    number_pattern = re.compile(r'\d+')
    has_number = any(number_pattern.search(part) for part in parts)

    if not has_number:
        street_names = await cached_street_search(query)
        return [{"type": "street", "name": name} for name in street_names]
    else:
        number_part_raw = next(
            (p for p in reversed(parts) if number_pattern.search(p)),
            ''
        )
        cleaned_number = re.sub(r'[^0-9АБаб]', '', number_part_raw)

        street_part = ' '.join([
            p for p in parts
            if p != number_part_raw and not number_pattern.search(p)
        ])

        return await cached_house_search(street_part, cleaned_number)

@router.get('/blackouts/', response={200: List[BlackoutOut], 404: ErrorSchema})
async def get_blackouts(request):
    blackouts = await Blackout.objects.filter(end_date__isnull=True) \
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
            'end_date': blackout.end_date,
            'description': blackout.description,
            'type': blackout.type,
            'initiator_name': blackout.initiator_id.initiator_name if blackout.initiator_id else None,
            'source_name': blackout.source_id.source_name if blackout.source_id else None,
            'buildings': buildings
        })

    return results