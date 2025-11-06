import os
from urllib.request import build_opener

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


import api.models as models
import sqlite3
import random
from datetime import timedelta
from api.routers.maps import  coordinate_converter
from tqdm import tqdm
from django.utils import timezone

conn = sqlite3.connect(r'../../Road_to_Final/databases/farpost.db')
cur = conn.cursor()

_types = ['HT', 'HW', 'CW','EL']

cur.execute('''SELECT
name
FROM cities''')
city_data = cur.fetchall()
for city in city_data:
    models.City.objects.create(city_name=city[0])
print("City done")

cur.execute('''SELECT
s.name,
c.name
FROM streets AS s
LEFT JOIN cities AS c ON c.id=s.city_id''')
street_data = cur.fetchall()
for street in street_data:
    models.Street.objects.create(street_name=street[0],
                                 street_city_id=models.City.objects.get(city_name=street[-1]))

print('Street done')

cur.execute('''SELECT
name
FROM districts''')
district_data = cur.fetchall()
for district in district_data:
    models.District.objects.create(district_name=district[0])
print('District done')

cur.execute('''SELECT
DISTINCT name
FROM folk_districts''')
folk_district_data= cur.fetchall()
for folk_district in folk_district_data:
    models.FolkDistrict.objects.create(folk_district_name=folk_district[0])
print('Folk District done')

_type_converter ={
    'нежилое': 'нежилое',
    'жилое многоквартирное': 'жилое',
    'общественное' : 'общественное',
    'строящееся':'строящееся',
    'частный дом': 'частный дом',
    'производственное':'производственное',
    'Нежилое строение':'нежилое',
    'Нежилое':'нежилое',
    'Жилое сельское':'жилое',
    'Жилое сельское строение': 'жилое',
    'Жилое строение': 'жилое',
    'разрушенное': 'нежилое',
    'Жилое':'жилое',
    'дача': 'частный дом',
    'строение':'нежилое',
    'Разрушенное': 'нежилое',
    'гаражи':'нежилое',
    'планируемое':'планируемое',
    'Строящееся':'строящееся',
    'Строение жилое':'жилое',
    'Строящееся строение':'строящееся',
    'Производственное строение':'производственное',
    'Производственное':'производственное',
    'СНТ':'жилое',
    'Строение жилое сельское':'жилое',
    'Строение нежилое':'нежилое',
    'Строение строящееся':'строящееся',
    'Строение производственное':'производственное',
    'Постройка без адреса':'нежилое'
}
cur.execute('''SELECT
DISTINCT  type
FROM buildings
WHERE type IS NOT NULL''')
_type_data = cur.fetchall()

for _type in _type_data:
    if models.BuildingType.objects.filter(building_type_name=_type_converter[_type[0]]).exists() == False:
        models.BuildingType.objects.create(building_type_name=_type_converter[_type[0]])
print('Type done')

cur.execute('''SELECT
DISTINCT initiator_name
FROM blackouts
WHERE initiator_name IS NOT NULL''')

initiator_data = cur.fetchall()
for initiator in initiator_data:
    models.Initiator.objects.create(initiator_name=initiator[0])
print('Initiator done')

cur.execute('''SELECT
DISTINCT source
FROM blackouts
WHERE source IS NOT NULL''')
source_data = cur.fetchall()
for source in source_data:
    models.Source.objects.create(source_name=source[0])
print('Source done')

cur.execute('''SELECT
    s.name,
    b.number,
    d.name,
    f.name,
    b.type,
    c.name,
    b.coordinates
    FROM
    buildings AS b
LEFT JOIN streets AS s ON
    b.street_id = s.id AND b.street_id IS NOT NULL
LEFT JOIN  districts AS d ON
    b.district_id = d.id AND b.district_id IS NOT NULL
LEFT JOIN cities AS c ON
    b.city_id = c.id AND b.city_id IS NOT NULL
LEFT JOIN folk_districts AS f ON
    b.folk_district_id = f.id AND b.folk_district_id IS NOT NULL
WHERE b.is_fake=0 AND
    s.name IS NOT NULL AND
    b.number IS NOT NULL AND
    d.name IS NOT NULL AND
    f.name IS NOT NULL AND
    b.type IS NOT NULL AND
    c.name IS NOT NULL AND
    b.coordinates IS NOT NULL
''')
build_data = cur.fetchall()
models.Building.objects.all().delete()
for build in tqdm(build_data):
    new_cords = coordinate_converter(build[6])
    models.Building.objects.create(
        street_id = models.Street.objects.get(street_name = build[0],\
                                              street_city_id = models.City.objects.get(city_name=build[5])),
        number = build[1],
        district_id = models.District.objects.get(district_name=build[2]),
        folk_district_id = models.FolkDistrict.objects.get(folk_district_name=build[3]),
        is_current=True,
        building_type_id = models.BuildingType.objects.get(building_type_name=_type_converter[build[4]]),
        city_id = models.City.objects.get(city_name=build[5]),
        coordinates = f'{new_cords[0]}, {new_cords[-1]}'
    )
print('Build done')
def add_data_to_models():
    for black_type in tqdm(['HT', 'HW', 'CW', 'EL']):
        start_days = random.randrange(1, 365, 1)
        end_days = random.randrange(1, 365, 1)
        initiator_type = random.choice([0, 1])
        if initiator_type == 1:
            blackout = models.Blackout.objects.create(
                start_date=timezone.now() + timedelta(hours=10) - timedelta(days=start_days),
                end_date=timezone.now()+ timedelta(hours=10) + timedelta(days=end_days),
                type=black_type,
                initiator_id=None,
                source_id=None,
                description=None
            )
        else:
            blackout = models.Blackout.objects.create(
                start_date=timezone.now() + timedelta(hours=10) - timedelta(days=start_days),
                end_date=timezone.now() + timedelta(hours=10) + timedelta(days=end_days),
                type=black_type,
                initiator_id=models.Initiator.objects.all().order_by('?'),
                source_id=models.Source.objects.all().order_by('?'),
                description=None
            )
        count = random.choice(range(100, 1000, 1))
        for build in models.Building.objects.all().order_by('?')[:count]:
            models.BlackoutBuilding.objects.create(
                blackout_id = blackout,
                building_id = build
            )