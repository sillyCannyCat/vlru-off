from api.models import Building, Street, BlackoutBuilding
from django.db.models import Count, Q

from backend.faker import street


async def get_autocomplete(data: str):
    to_analyze = data.split()
    to_return = dict()
    if len(to_analyze) <= 2:
        to_return['type'] = 'street'
        query = Q(street_name__startswith=data)
        data = Street.objects().filter(query).order_by('street_name')
        to_return['street'] = data
    else:
        to_return['type'] = 'address'
        query = Q(street_id__street_name=to_analyze[0] +' '+ to_analyze[1])
        query.add(Q(number=to_analyze[-1]), Q.AND)
        data = Building.objects().filter(query).order_by('street_id__street_name','number')
        to_return['address'] = data
    return to_return

async def get_address_outages(address: str):
    raw_street_first, raw_street_second, number = address.split()
    street_name = raw_street_first + raw_street_second
    query = Q(building_id__street_id__street_name=street_name)
    query.add(Q(building_id__number=number), Q.AND)
    count_data = await BlackoutBuilding.objects().filter(query) \
        .values('building_id'). \
        annotate(count=Count('blackout_id')).all()[0]
    data = dict()
    if count_data['count'] == 0:
        data['flag'] = False
    elif count_data['count'] > 0:
        data['flag'] = True
        query = Q(building_id=count_data['building_id'])
        outages_data = await BlackoutBuilding.objects().filter(query) \
            .values('blackout_id__type', 'blackout_id__end_date').all()
        data['data'] = outages_data
    return data
