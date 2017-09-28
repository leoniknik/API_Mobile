from rat.models import *


class ControlTelemetry(models.Model):
    vehicle = models.ForeignKey(Vehicle, null=True)
    datetime = models.BigIntegerField(verbose_name='datetime', default=0)#datetime = models.DateTimeField(verbose_name='datetime', null=True)
    torque = models.FloatField(verbose_name='torque', default=0)
    breake = models.FloatField(verbose_name='breake', default=0)
    rpm = models.FloatField(verbose_name='rpm', default=0)


class LocationTelemetry(models.Model):
    vehicle = models.ForeignKey(Vehicle, null=True)
    datetime = models.BigIntegerField(verbose_name='datetime', default=0)#datetime = models.DateTimeField(verbose_name='datetime', null=True)
    spd = models.FloatField(verbose_name='spd', default=0)
    latitude = models.FloatField(verbose_name='latitude', default=0)
    longitude = models.FloatField(verbose_name='longitude', default=0)

class SpeedTask(models.Model):
    loc_telemetry = models.ForeignKey(LocationTelemetry, null=True)

class Telemetry(models.Model):
    vehicle = models.ForeignKey(Vehicle, null=True)
    datetime = models.BigIntegerField(verbose_name='datetime',default=0)#models.DateTimeField(verbose_name='datetime', null=True)
    fuel = models.FloatField(verbose_name='fuel', default=0)
    acc_x = models.FloatField(verbose_name='acc_x', default=0)
    acc_y = models.FloatField(verbose_name='acc_y', default=0)
    acc_z = models.FloatField(verbose_name='acc_z', default=0)

class SpeedExcess(models.Model):
    loc_telemetry = models.ForeignKey(LocationTelemetry,null=True)
    limit = models.IntegerField(verbose_name='limit', default=0)