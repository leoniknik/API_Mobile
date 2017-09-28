from django.db import models
from rat.models import *
import datetime

class ControlTelemetry(models.Model):
    vehicle = models.ForeignKey(Vehicle,null=True)
    datetime = models.DateTimeField(verbose_name='datetime',null=True)
    torque = models.FloatField(verbose_name='torque', default=0)
    breake = models.FloatField(verbose_name='breake', default=0)
    rpm = models.FloatField(verbose_name='rpm', default=0)


class LocationTelemetry(models.Model):
    vehicle = models.ForeignKey(Vehicle, null=True)
    datetime = models.DateTimeField(verbose_name='datetime', null=True)
    spd = models.FloatField(verbose_name='spd', default=0)
    latitude = models.FloatField(verbose_name='latitude', default=0)
    longitude = models.FloatField(verbose_name='longitude', default=0)

class Telemetry(models.Model):
    vehicle = models.ForeignKey(Vehicle, null=True)
    datetime = models.DateTimeField(verbose_name='datetime', null=True)
    fuel = models.FloatField(verbose_name='fuel', default=0)
    acc_x = models.FloatField(verbose_name='acc_x', default=0)
    acc_y = models.FloatField(verbose_name='acc_y', default=0)
    acc_z = models.FloatField(verbose_name='acc_z', default=0)

#class CrashDescription(models.Model):
#    code = models.CharField(verbose_name='code', max_length=24, default="", unique=True)
#    full_description = models.TextField(verbose_name='full_description', default="")
#    short_description = models.TextField(verbose_name='full_description', default="")#
##
#
#class Crash(models.Model):
#    vehicle = models.ForeignKey(Vehicle, null=True)
#    actual = models.BooleanField(verbose_name='actual', default=True, db_index=True)
#    description = models.ForeignKey(CrashDescription, null=True)
#    date = models.TextField(verbose_name='crash_date', null=True)
