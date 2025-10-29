from django.db import models
from django_ulidfield import ULIDField

class Initiator(models.Model):
    initiator_id = models.IntegerField(primary_key=True)
    initiator_name = models.CharField(max_length=256)

class Source(models.Model):
    source_id = models.IntegerField(primary_key=True)
    source_name = models.CharField(max_length=256)

class Blackout(models.Model):
    TYPE_CHOICES = {
        'HT': 'Heat',
        'HW': 'Hot water',
        'CW': 'Cold water',
        'EL': 'Electricity'
    }
    blackout_id = ULIDField(primary_key=True)
    start_date = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField(default=None)
    description = models.CharField(max_length=256, null=True, default=None)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    initiator_id = models.ForeignKey(Initiator, on_delete=models.SET_NULL, null=True)
    source_id = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True)

class Street(models.Model):
    street_id = models.IntegerField(primary_key=True)
    street_name = models.CharField(max_length=128)

class District(models.Model):
    district_id = models.IntegerField(primary_key=True)
    district_name = models.CharField(max_length=64)

class FolkDistrict(models.Model):
    folk_district_id = models.IntegerField(primary_key=True)
    folk_district_name = models.CharField(max_length=128)

class BuildingType(models.Model):
    building_type_id = models.IntegerField(primary_key=True)
    building_type_name = models.CharField(max_length=128)

class City(models.Model):
    city_id = models.IntegerField(primary_key=True)
    city_name = models.CharField(max_length=128)

class Building(models.Model):
    building_id = ULIDField(primary_key=True)
    street_id = models.ForeignKey(Street, on_delete=models.SET_NULL, null=True)
    number = models.IntegerField()
    district_id = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    folk_district_id = models.ForeignKey(FolkDistrict, on_delete=models.SET_NULL, null=True)
    is_current = models.BinaryField()
    building_type_id = models.ForeignKey(BuildingType, on_delete=models.SET_NULL, null=True)
    city_id = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    coordinates = models.CharField(max_length = 128)

class BlackoutBuilding(models.Model):
    blackout_id = models.ForeignKey(Blackout, on_delete=models.CASCADE)
    building_id = models.ForeignKey(Building, on_delete=models.CASCADE)
