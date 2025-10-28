from ninja import Router
from typing import List
from api.models import Blackout, BlackoutsBuilding, Building, Street, District, FolkDistrict, Initiator, Source
from api.schemas.maps import BlackoutOut, AddressIn
from api.schemas.errors import ErrorSchema
from django.db.models import Prefetch
import requests
import os
from typing import Optional

router = Router(tags=['maps'])

def get_coordinates_from_address(address: str) -> tuple[Optional[float], Optional[float]]:
    api_key = os.environ.get('YANDEX_API_KEY')
    if not api_key:
        raise ValueError('YANDEX_API_KEY не указан в .env')

    url = 'https://geocode-maps.yandex.ru/1.x/'
    params = {
        'apikey': api_key,
        'geocode': address,
        'format': 'json'
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        point = data['response']['GeoObjectCollection']['featureMember']
        if not point:
            return None, None
        pos = point[0]['GeoObject']['Point']['pos']
        lon, lat = map(float, pos.split())
        return lat, lon
    except Exception as e:
        return None, None

@router.get('/blackouts/', response={200: List[BlackoutOut], 404: ErrorSchema})
def get_blackouts(request):
    blackouts = Blackout.objects.filter(end_data__isnull=True).select_related(
        'initiator_id', 'source_id'
    ).prefetch_related(
        Prefetch(
            'blackoutsbuilding_set',
            queryset=BlackoutsBuilding.objects.select_related('building_id'),
            to_attr='buildings_links'
        )
    )
    if not blackouts.exists():
        return 404, {'message': 'Нет активных отключений'}

    results = []
    for blackout in blackouts:
        buildings = []
        for link in blackout.buildings_links:
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

@router.post('/blackouts/by_address/', response={200: List[BlackoutOut], 400: ErrorSchema, 404: ErrorSchema})
def get_blackouts_by_address(request, data: AddressIn):
    address = data.address.strip()
    if not address:
        return 400, {'message': 'Адрес не указан'}

    lat, lon = get_coordinates_from_address(address)
    if lat is None or lon is None:
        return 404, {'message': 'Не удалось определить координаты по указанному адресу'}

    buildings = Building.objects.filter(
        street_id__street_name__iexact=address.split(',')[1].strip() if ',' in address else address,
        number__in=[int(n) for n in address.split() if n.isdigit()]
    )

    if not buildings.exists():
        return 404, {'message': 'Здание с указанным адресом не найдено'}

    target_building = None
    for building in buildings:
        b_lat, b_lon = building.get_coordinates()
        if abs(b_lat - lat) < 0.001 and abs(b_lon - lon) < 0.001:
            target_building = building
            break

    if not target_building:
        return 404, {'message': 'Здание с указанным адресом не соответствует координатам'}

    blackouts = Blackout.objects.filter(
        end_data__isnull=True,
        blackoutsbuilding__building_id=target_building
    ).select_related(
        'initiator_id', 'source_id'
    ).prefetch_related(
        Prefetch(
            'blackoutsbuilding_set',
            queryset=BlackoutsBuilding.objects.select_related('building_id'),
            to_attr='buildings_links'
        )
    )

    if not blackouts.exists():
        return 404, {'message': 'Активных отключений для указанного адреса нет'}

    results = []
    for blackout in blackouts:
        buildings = []
        for link in blackout.buildings_links:
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