import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


import api.models as models
import sqlite3
import random
from datetime import datetime

conn = sqlite3.connect(r'../../Road_to_Final/databases/farpost.db')
cur = conn.cursor()

cur.execute('''SELECT DISTINCT initiator_name FROM blackouts LIMIT 10''')

initiator_data = cur.fetchall()
print(initiator_data)
print(len(initiator_data))

for initiator in initiator_data:
    print(initiator[0])
    models.Initiator.objects.create(initiator_name=initiator[0])

cur.execute('''SELECT DISTINCT source FROM blackouts LIMIT 10''')

source_data = cur.fetchall()
for source in source_data:
    print(source[0])
    models.Source.objects.create(source_name=source[0])

cur.execute('''SELECT
    description,
    type
FROM blackouts
LIMIT 1000''')

for data in cur.fetchall():
    _type_converter ={
        'electricity':'EL',
        'cold_water':'CW',
        'hot_water':'HW',
        'heat':'HT'
    }
    _id = random.choices(range(1, 11))
    models.Blackout.objects.create(
        start_date=datetime(2025, month=10, day=27),
        end_date=datetime(2025, month=11, day=3),
        description=data[0],
        type=_type_converter[data[-1]],
        initiator_id=models.Initiator.objects.get(initiator_id=_id[0]),
        source_id=models.Source.objects.get(source_id=_id[0])
    )
print('Good')

models.Street.objects.all().delete()
models.District.objects.all().delete()
models.FolkDistrict.objects.all().delete()
models.BuildingType.objects.all().delete()
models.City.objects.all().delete()
models.Building.objects.all().delete()

cur.execute('''SELECT
    name
FROM streets
LIMIT 10''')
street_data = cur.fetchall()

cur.execute('''SELECT
    name
FROM districts
LIMIT 10''')
districts_data = cur.fetchall()

cur.execute('''SELECT
    name
FROM folk_districts
LIMIT 10''')
folk_districts_data = cur.fetchall()

cur.execute('''SELECT
    DISTINCT type
FROM buildings
WHERE type IS NOT NULL
LIMIT 10''')
_type_data = cur.fetchall()
print(_type_data)
models.City.objects.create(city_name='Владивосток')

for street, district, folk_district, _type in\
    zip(street_data, districts_data, folk_districts_data, _type_data):
    models.Street.objects.create(street_name=street[0])
    models.District.objects.create(district_name=district[0])
    models.FolkDistrict.objects.create(folk_district_name = folk_district[0])
    models.BuildingType.objects.create(building_type_name=_type[0])

cur.execute('''SELECT
    s.name,
    b.coordinates,
    b.number
FROM buildings as b
LEFT JOIN streets as s ON b.street_id = s.id
WHERE  b.coordinates IS NOT NULL AND s.name="1-й Байкальский пер." OR  s.name="1-й Вокзальный пер." OR
    s.name="1-й Воровского пер."OR    s.name="1-й Зареченский пер."OR
    s.name="1-й Линейный пер." AND b.number IS NOT NULL
LIMIT 1000''')

build_data = cur.fetchall()
for i in range(len(build_data)):
    _id = random.choices(range(1, 6))
    if build_data[i][1] == None:
        continue
    models.Building.objects.create(
        street_id=models.Street.objects.get(street_name=build_data[i][0]),
        number=build_data[i][-1],
        district_id=models.District.objects.get(district_id=_id[0]),
        folk_district_id=models.FolkDistrict.objects.get(folk_district_id=_id[0]),
        is_current=True,
        building_type_id=models.BuildingType.objects.get(building_type_id=_id[0]),
        city_id=models.City.objects.get(city_id=1),
        coordinates=build_data[i][1]
    )
print("GG")

for i in range(100):
    models.Blackout.objects.create(
        start_date=datetime(2025, month=10, day=27),
        end_date=None,
        type='EL',
        initiator_id=None,
        source_id=None
    )

blackout_ids = models.Blackout.objects.all().values('blackout_id')
building_ids = models.Building.objects.all().values('building_id')


for blackout in blackout_ids:
    house = random.choices(range(1, 70))[0]
    models.BlackoutBuilding.objects.create(
        blackout_id=models.Blackout.objects.get(blackout_id=blackout['blackout_id']),
        building_id=models.Building.objects.get(building_id=building_ids[house]['building_id'])
    )
