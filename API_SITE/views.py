from rat.models import User, Vehicle, Crash, CrashDescription, Offer, Service, Review
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.core import serializers
import json


def logon(request):
    try:
        json_data = json.loads(str(request.body, encoding='utf-8'))
        print(json_data)
        login = json_data['login']
        password = json_data['password']
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
        return JsonResponse({"code": 404})


def get_offered_vehicles(request):
    try:
        json_data = json.loads(str(request.body, encoding='utf-8'))
        print(json_data)
        service_id = json_data['service_id']
        #service_id = request.POST["service_id"]
        service = Service.objects.get(id=service_id)
        if service is None:
            return JsonResponse({"code": 404})
        else:
            offers = Offer.objects.all().filter(service=service, status=2)
            body = list()
            for offer in offers:
                raw_vehicle = offer.vehicle
                vehicle = {
                    "id": raw_vehicle.id,
                    "year": raw_vehicle.year,
                    "brand": raw_vehicle.brand,
                    "model": raw_vehicle.model,
                    "vin": raw_vehicle.VIN,
                    "number": raw_vehicle.number
                }
                crashes = Crash.objects.all().filter(vehicle=raw_vehicle)
                count_crashes = crashes.count()
                body.append({"vehicle": vehicle, "count_crashes": count_crashes})
            return JsonResponse({"code": 200, "data": body
        })

    except Exception as e:
        print(e)
        return JsonResponse({"code": 404})


def get_lists_of_vehicles_and_crashes(request):
    try:
        vehicles = Vehicle.objects.all().values('id', 'VIN', 'number', 'brand', 'model', 'year')
        vehicles = list(vehicles)
        for vehicle in vehicles:
            actual_crashes = Crash.objects.filter(vehicle_id=vehicle["id"], actual=True).values('id', 'description__code', 'description__full_description',
                                    'description__short_description', 'date')
            actual_crashes = list(actual_crashes)
            vehicle['actual_crashes'] = actual_crashes

            history_crashes = Crash.objects.filter(vehicle_id=vehicle["id"], actual=False).values('id',
                                                                                                'description__code',
                                                                                                'description__full_description',
                                                                                                'description__short_description',
                                                                                                'date')
            history_crashes = list(history_crashes)
            vehicle['history_crashes'] = history_crashes
        return JsonResponse({"code": 200, "data": vehicles})
    except Exception as e:
        print(e)
        return JsonResponse({"code": 404})


def create_offer(request):
    try:
        json_data = json.loads(str(request.body, encoding='utf-8'))
        print(json_data)
        vehicle_id = json_data['vehicle_id']
        service_id = json_data['service_id']
        price = json_data['price']
        message = json_data['message']
        date = "29.09.2017"
        service = Service.objects.get(pk=service_id)
        vehicle = Vehicle.objects.get(pk=vehicle_id)
        if service is None:
            return JsonResponse({"code": 404})
        if vehicle is None:
            return JsonResponse({"code": 404})
        else:
            offer = Offer.objects.filter(vehicle=vehicle, service=service).first()
            if offer is None or offer.status == 3:
                Offer.objects.create(vehicle=vehicle, service=service, price=price, message=message, date=date, status=0)
                return JsonResponse({"code": 200})
            else:
                return JsonResponse({"code": 500})
    except Exception as e:
        print(e)
        return JsonResponse({"code": 404})


def get_offers(request):
    try:
        json_data = json.loads(str(request.body, encoding='utf-8'))
        print(json_data)
        service_id = json_data['service_id']
        #service_id = request.POST['service_id']
        service = Service.objects.get(pk=service_id)
        if service is None:
            return JsonResponse({"code": 404})
        else:
            offers = Offer.objects.all().filter(service=service).values('id',
                                                                'price',
                                                                'message',
                                                                'status',
                                                                'date',
                                                                'vehicle_id')
            offers = list(offers)

            for offer in offers:
                raw_vehicle = Vehicle.objects.get(pk=offer["vehicle_id"])
                vehicle = {
                    "id": raw_vehicle.id,
                    "year": raw_vehicle.year,
                    "brand": raw_vehicle.brand,
                    "model": raw_vehicle.model,
                    "vin": raw_vehicle.VIN,
                    "number": raw_vehicle.number
                }
                offer["vehicle"] = vehicle

            return JsonResponse({"code": 200, "offers": offers})
    except Exception as e:
        print(e)
        return JsonResponse({"code": 404})


def get_reviews(request):
    try:
        json_data = json.loads(str(request.body, encoding='utf-8'))
        print(json_data)
        service_id = json_data['service_id']
        service = Service.objects.get(pk=service_id)
        if service is None:
            return JsonResponse({"code": 404})
        else:
            reviews = Review.objects.all().filter(service=service).values('id',
                                                                'user__firstname',
                                                                'text',
                                                                'date')
            reviews = list(reviews)
            return JsonResponse({"code": 200, "reviews": reviews})
    except Exception as e:
        print(e)
        return JsonResponse({"code": 404})


def complete_offer(request):
    try:
        json_data = json.loads(str(request.body, encoding='utf-8'))
        print(json_data)
        offer_id = json_data['offer_id']
        offer = Offer.objects.get(pk=offer_id)
        if offer is None:
            return JsonResponse({"code": 404})
        else:
            offer.status = 3
            vehicle = offer.vehicle
            crashes = Crash.objects.filter(vehicle=vehicle)
            for crash in crashes:
                crash.actual = False
                crash.save()
            return JsonResponse({"code": 200})
    except Exception as e:
        print(e)
        return JsonResponse({"code": 404})