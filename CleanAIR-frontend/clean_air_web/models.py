from django.db import models

# Django models implicitly have a pk id - so it is not missing!

class CarbonDioxideData(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    sensor = models.CharField(max_length=20, blank=True, null=True)
    co2 = models.FloatField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'carbon_dioxide_data'


class InfraredData(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    sensor = models.CharField(max_length=20, blank=True, null=True)
    state = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'infrared_data'


class PhotoElectricData(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    sensor = models.CharField(max_length=20, blank=True, null=True)
    state = models.TextField(blank=True, null=True)  # This field type is a guess.
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'photo_electric_data'


class TrafficLightData(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    sensor = models.CharField(max_length=20, blank=True, null=True)
    state = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'traffic_light_data'


class WindowStateData(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    sensor = models.CharField(max_length=20, blank=True, null=True)
    state = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'window_state_data'

class Limit(models.Model):
    name = models.CharField(primary_key=True, max_length=20)
    limit = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'limit'
