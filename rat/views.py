from django.shortcuts import render
from rat.models import User, Vehicle, Crash, CrashDescription, Offer, Service, Review
import json
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.core import serializers

def user_login(request):
    try:
        json_data = json.loads(str(request.body, encoding='utf-8'))
        print(json_data)
        email = json_data['email']
        user = User.objects.filter(email=email).first()
        if user is None:
            return JsonResponse({"code": 403})
        else:
            return JsonResponse({"code": 200, "data": {
                }})
    except Exception as e:
        print(e)
        return JsonResponse({"code": 403})