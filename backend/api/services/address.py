from api.models import Building, Street, BlackoutBuilding
from django.db.models import Count, Q

async def get_autocomplete(data:str):
    street_number = data.split(' ')
    if len(street_number) == 1:
        query = Q(street_name__contains=street_number[0])
        data = await Street.objects().filter(query).values('street_name')\
            .oreder_by('street_name').all()
        return data
    else:
        posible_numbers = list()
        posible_numbers.append(int(street_number[-1]))
        if street_number[-1] %10 !=0:
            for i in range(1, 10):
                posible_numbers.append(int(f'{i}{posible_numbers[-1]}'))
                posible_numbers.append(int(f'{posible_numbers[-1]}{i}'))
        else:
            for i in range(1, 100):
                posible_numbers.append(int(f'{i}{posible_numbers[-1]}'))
                posible_numbers.append(int(f'{posible_numbers[-1]}{i}'))
        query = Q(street_id__street_name__contains = street_number[0])
        query.add(Q(number__in=posible_numbers), Q.AND)
        data = await Building.objects().filter(query).value('street_name', 'number')\
            .order_by('street_name', 'number')\
            .all()
        return data


async def get_address_outages(address:str):
    raw_street_first, raw_street_second, number = address.split()
    street_name = raw_street_first + raw_street_second
    query = Q(building_id__street_id__street_name=street_name)
    query.add(Q(building_id__number=number), Q.AND)
    count_data = await BlackoutBuilding.objects().filter(query)\
        .values('building_id').\
        annotate(count=Count('blackout_id')).all()[0]
    data = dict()
    if count_data['count'] == 0:
        data['flag'] = False
    elif count_data['count'] > 0:
        data['flag'] = True
        query = Q(building_id=count_data['building_id'])
        outages_data = await BlackoutBuilding.objects().filter(query)\
            .values('blackout_id__type', 'blackout_id__end_date').all()
        data['data'] = outages_data
    return data