from api.models import Building, Street, BlackoutBuilding
from django.db.models import Count, Q
from asgiref.sync import sync_to_async

@sync_to_async
def get_autocomplete(data: str):
    data = data.strip()
    to_return = {}

    parts = data.split()
    last_part = parts[-1] if parts else ""
    is_house_number = any(ch.isdigit() for ch in last_part) and len(last_part) <= 6

    if is_house_number:
        to_return['type'] = 'address'
        street_name = ' '.join(parts[:-1])
        number = last_part

        query = Q(street_id__street_name__icontains=street_name)
        query.add(Q(number__istartswith=number), Q.AND)

        qs = Building.objects.filter(query).order_by('street_id__street_name', 'number')[:10]
        to_return['address'] = list(qs.values('street_id__street_name', 'number'))
        return to_return
    else:
        to_return['type'] = 'street'
        query = Q(street_name__icontains=data)
        qs = Street.objects.filter(query).order_by('street_name')[:10]
        to_return['street'] = list(qs.values('street_name'))
        return to_return

async def get_address_outages(address: str):
    parts = address.split()

    if len(parts) < 2:
        return {'flag': False}

    if len(parts) == 2:
        street_name = parts[0]
        number = parts[1]
    else:
        street_name = ' '.join(parts[:-1])
        number = parts[-1]

    query = Q(building_id__street_id__street_name=street_name)
    query.add(Q(building_id__number=number), Q.AND)

    count_qs = await sync_to_async(list)(
        BlackoutBuilding.objects
        .filter(query)
        .values('building_id')
        .annotate(count=Count('blackout_id'))
    )

    if not count_qs:
        return {'flag': False}

    count_data = count_qs[0]
    data = {}

    if count_data['count'] == 0:
        data['flag'] = False
    else:
        data['flag'] = True
        query = Q(building_id=count_data['building_id'])

        outages_data = await sync_to_async(list)(
            BlackoutBuilding.objects
            .filter(query)
            .values('blackout_id__type', 'blackout_id__end_date')
        )
        data['data'] = outages_data

    return data
