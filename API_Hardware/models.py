from django.db import models

class Vehicle(models.Model):
    VIN = models.CharField(verbose_name='vin', max_length=17, default="")
    number = models.CharField(verbose_name='number', max_length=9, default="")
    brand = models.CharField(verbose_name='brand', max_length=255, default="")
    model = models.CharField(verbose_name='model', max_length=255, default="")
    year = models.CharField(verbose_name='year', max_length=4, default="")
    user = models.ForeignKey(User, null=True)
    is_auction = models.BooleanField(verbose_name='is_auction', default=False, db_index=True)


class CrashDescription(models.Model):
    code = models.CharField(verbose_name='code', max_length=24, default="", unique=True)
    full_description = models.TextField(verbose_name='full_description', default="")
    short_description = models.TextField(verbose_name='full_description', default="")


class Crash(models.Model):
    vehicle = models.ForeignKey(Vehicle, null=True)
    actual = models.BooleanField(verbose_name='actual', default=True, db_index=True)
    description = models.ForeignKey(CrashDescription, null=True)
    date = models.TextField(verbose_name='crash_date', null=True)
