from django.db import models


class User(models.Model):
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    phone = models.CharField(verbose_name='phone', max_length=11, default="")
    firstname = models.CharField(verbose_name='firstname', max_length=255, default="")
    lastname = models.CharField(verbose_name='lastname', max_length=255, default="")


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


class Service(models.Model):
    login = models.TextField(verbose_name='login', default="")
    password = models.TextField(verbose_name='login', default="")
    name = models.CharField(verbose_name='name', max_length=100, default="")
    description = models.TextField(verbose_name='description', default="")
    address = models.TextField(verbose_name='address', default="")
    phone = models.CharField(verbose_name='phone', max_length=20, default="")
    email = models.TextField(verbose_name='email', default="")
    longitude = models.FloatField(verbose_name='longitude', default=0.0)
    latitude = models.FloatField(verbose_name='latitude', default=0.0)

    @classmethod
    def auth_service(self, login,  password):
        service = Service.objects.get(login=login)
        actual_password = service.password
        if actual_password == password:
            return service


class Review(models.Model):
    service = models.ForeignKey(Service, null=True)
    date = models.TextField(verbose_name='review_date', default="")
    user = models.ForeignKey(User, null=True)
    text = models.TextField(verbose_name='text', default="")


class Offer(models.Model):
    vehicle = models.ForeignKey(Vehicle, null=True)
    service = models.ForeignKey(Service, null=True)
    price = models.IntegerField(verbose_name='price', default=0)
    message = models.TextField(verbose_name='message', default="")
    date = models.TextField(verbose_name='date', default="")
    status = models.IntegerField(verbose_name='status', default=0)