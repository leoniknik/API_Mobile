"""API_Mobile URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from API_SITE.views import logon, get_offered_vehicles, get_lists_of_vehicles_and_crashes, create_offer, get_offers, get_reviews, user_by_vehicle
from API_Hardware.views import get_car_data

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^service_logon$', logon),
    url(r'^get_offered_vehicles$', get_offered_vehicles),
    url(r'^get_lists_of_vehicles_and_crashes$', get_lists_of_vehicles_and_crashes),
    url(r'^create_offer$', create_offer),
    url(r'^get_offers$', get_offers),
    url(r'^get_reviews$', get_reviews),
    url(r'^user_by_vehicle$', user_by_vehicle),
    url(r'^get_location$', get_car_data),

]
