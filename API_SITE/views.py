from rat.models import User, Vehicle, Crash, CrashDescription, Offer, Service, Review
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.core import serializers


def logon(request):
    try:
        login = request.POST['login']
        password = request.POST['password']
        service = Service.auth_service(login=login, password=password)
        if service is None:
            return JsonResponse({"code": 404})
        else:
            return JsonResponse({"code": 200, "data": {
                "id": service.id,
                "service_name": service.name,
                "description": {
                    "longitude": service.longitude,
                    "latitude": service.latitude,
                    "phone": service.phone,
                    "address": service.address,
                    "email": service.email,
                    "content": service.description,
                }}})

    except Exception as e:
        print(e)
        return JsonResponse({"code": 403})
