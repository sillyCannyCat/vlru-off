from api.models import Building, Street
from django.db.models import Count, Q
from unicodedata import numeric

async def get_autocomplete(data:str):
    street_number = data.split(' ')
    if len(street_number) == 1:
        query = Q(street_name__startswith=street_number[0])
        data = await Street.objects().filter(query).values('street_name')\
            .oreder_by('street_name').all()
        return data
    elif len(street_number) == 2:
        posible_numbers = list()
        posible_numbers.append(street_number[-1])
        if street_number[-1] %10 !=0:
            for i in range(1, 10):
                posible_numbers.append(int(f'{i}{posible_numbers[-1]}'))
                posible_numbers.append(int(f'{posible_numbers[-1]}{i}'))
        else:
            for i in range(1, 100):
                posible_numbers.append(int(f'{i}{posible_numbers[-1]}'))
                posible_numbers.append(int(f'{posible_numbers[-1]}{i}'))
        query = Q(street_id__street_name = street_number[0])
        query.add(Q(number__in=posible_numbers), Q.AND)
        data = await Building.objects().filter(query).value('street_name', 'number')\
            .order_by('number')\
            .all()
        return data
