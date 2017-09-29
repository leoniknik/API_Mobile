import paho.mqtt.client as mqtt
from API_Hardware.models import *
import multiprocessing
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.core import serializers
import json


import random
import time
import calendar

mqtt_listener = None
queue = multiprocessing.Queue()
analyzers = []
debug = False

def get_car_data(request):
    try:
        json_data = json.loads(str(request.body, encoding='utf-8'))
        print(json_data)
        vin = json_data['vin']

        vehicle = Vehicle.objects.get(vin=vin)

        if vehicle is None:
            return JsonResponse({"code": 404})
        else:

            telemetry = LocationTelemetry.objects.filter(vehicle=vehicle).values('id', 'spd', 'latitude', 'longitude')[:5]
            telemetry = list(telemetry)
            return JsonResponse({"code": 200, "data":
                    telemetry
                })
    except Exception as e:
        print(e)
        return JsonResponse({"code": 404})

class MessageParser:
    car_id = 0
    dataset_type_id = 0
    raw_data = []
    raw_data_string = ""

    def __init__(self, raw_data_string):
        self.raw_data_string = raw_data_string
        self.parse_data()

    def parse_data(self):
        raw_array = self.raw_data_string.split('_')
        self.car_id = raw_array[0]
        self.dataset_type_id = int(raw_array[1])
        self.raw_data = raw_array[2:]

        if self.dataset_type_id == 1:
            self.parse_dataset_1()
        elif self.dataset_type_id == 2:
            self.parse_dataset_2()
        elif self.dataset_type_id == 3:
            self.parse_dataset_3()
        elif self.dataset_type_id == 4:
            self.parse_dataset_4()
        print(calendar.timegm(time.gmtime()))

    def parse_dataset_1(self):
        if debug : print("dataset_1")
        #message_date_time = datetime.datetime.utcfromtimestamp(int(self.raw_data[0]))
        #if debug : print(message_date_time)
        error_codes = self.raw_data[1:]
        if debug : print(error_codes)
        vehicle = Vehicle.objects.get(VIN=self.car_id)

        if vehicle is not None:
            for error in error_codes:
                if not error=="":
                    crash_description, _ = CrashDescription.objects.get_or_create(code=error)
                    if crash_description.full_description == "":
                        crash_description.full_description = error
                    if crash_description.short_description == "":
                        crash_description.short_description = error
                    #crash_description.save()

                    crash = Crash.objects.create()
                    crash.actual = True
                    crash.description = crash_description
                    crash.date = calendar.timegm(time.gmtime())
#datetime.datetime.utcnow()#str(datetime.datetime)#message_date_time
                    crash.vehicle = vehicle
                    #crash.save()
                    if debug : print(error)


    def parse_dataset_2(self):
        if debug : print("dataset_2")
        #message_date_time = datetime.datetime.utcfromtimestamp(int(self.raw_data[0]))
        #if debug : print(message_date_time)
        rpm = float(float(self.raw_data[1])/3000.1)*8000
        torque = float(self.raw_data[2])/250.1
        breake = float(self.raw_data[3])/250.1
        if debug : print("rpm "+str(rpm))
        if debug : print("torque " + str(torque))
        if debug : print("breake " + str(breake))

        vehicle = Vehicle.objects.get(VIN=self.car_id)

        if vehicle is not None:
            control_telemetry = ControlTelemetry.objects.create()
            control_telemetry.vehicle = vehicle
            control_telemetry.datetime = calendar.timegm(time.gmtime())
#datetime.datetime.utcnow()#str(datetime.datetime)#datetime.datetime#message_date_time
            control_telemetry.rpm = rpm
            control_telemetry.breake = breake
            control_telemetry.torque = torque
            control_telemetry.save()

            if(breake>0.7 or torque>0.7):
                ControlExcess.objects.create(control_telemetry=control_telemetry).save()

    def parse_dataset_3(self):
        if debug : print("dataset_3")
        #message_date_time = datetime.datetime.utcfromtimestamp(int(self.raw_data[0]))
        #if debug : print(message_date_time)
        spd = float(self.raw_data[1])
        latitude = float(self.raw_data[2])
        longitude = float(self.raw_data[3])
        if debug : print("spd " + str(spd))
        if debug : print("latitude " + str(latitude))
        if debug : print("longetude " + str(longitude))

        vehicle = Vehicle.objects.get(VIN=self.car_id)

        if vehicle is not None:
            telemetry = LocationTelemetry.objects.create()
            telemetry.vehicle = vehicle
            telemetry.datetime = calendar.timegm(time.gmtime())
#datetime.datetime.utcnow()#str(datetime.datetime)#datetime.datetime#message_date_time
            telemetry.spd = spd
            telemetry.latitude = latitude
            telemetry.longitude = longitude
            telemetry.save()

            #analys(telemetry)

            queue.put(telemetry.id)

    def parse_dataset_4(self):
        if debug : print("dataset_4")
        #message_date_time = datetime.utcfromtimestamp(int(self.raw_data[0]))
        #if debug : print(message_date_time)
        fuel = float(float(self.raw_data[1]) / 255.0)
        if debug : print("fuel " + str(fuel))
        acc_x = float(self.raw_data[2])
        acc_y = float(self.raw_data[3])
        acc_z = float(self.raw_data[4])
        if debug : print('acc_x ' + str(acc_x))
        if debug : print('acc_y ' + str(acc_y))
        if debug : print('acc_z ' + str(acc_z))

        vehicle = Vehicle.objects.get(VIN=self.car_id)

        if vehicle is not None:
            telemetry = Telemetry.objects.create()
            telemetry.vehicle = vehicle
            telemetry.datetime = calendar.timegm(time.gmtime())
#datetime.datetime.utcnow()#str(datetime.datetime)#datetime.datetime#message_date_time
            telemetry.fuel = fuel
            telemetry.acc_x = acc_x
            telemetry.acc_y = acc_y
            telemetry.acc_z = acc_z
            telemetry.save()

            if(acc_x>8 or acc_y>8or acc_z>8):
                AccelerationExcess.objects.create(telemetry=telemetry).save()




def on_connect(rc):
    if debug : print("rc: " + str(rc))


def on_message(q,e,msg):
    if debug : print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    try:
        print(msg.payload.decode("utf-8"))
        MessageParser(msg.payload.decode("utf-8"))
    except Exception as e:
        print(e)


def on_subscribe(q,w,mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))
def on_disconnect(client, userdata, rc):
    print("disconnected with rtn code [%d]"% (rc) )

def setup_listener():
    mqttc = mqtt.Client()
    # Assign event callbacks
    mqttc.on_message = on_message
    mqttc.on_disconnect =  on_disconnect
    mqttc.on_subscribe = on_subscribe
    # Connect
    mqttc.connect("broker.hivemq.com", 1883, 60)
    mqttc.subscribe("mts_hardware_get_info_chanel", qos=1)
    # Continue the network loop
    mqttc.loop_forever()


def analyzer(id):
    while(True):
        if(not queue.empty()):
            if debug : print('analyzer '+ str(id) + 'start analyze')
            id = queue.get()
            task = LocationTelemetry.objects.get(id=id)
            analys(task)
        else:
            print('analyzer '+ str(id) + 'is waiting')
        time.sleep(1)


def analys(telemetry):
    try:
        # make request to api
        limits = [5, 10, 20, 30, 40, 60, 70, 80, 90, 100, 110]
        limits = [60, 70, 80, 90, 100, 110]
        random.seed()
        limit = limits[random.randrange(0, len(limits) - 1)]
        if (telemetry.spd > limit):
            speed_excess = SpeedExcess.objects.create()
            speed_excess.loc_telemetry = telemetry
            speed_excess.limit = limit
            speed_excess.save()
            print('speedExceed')
    except Exception as ex:
        print(ex)

def lauch_analyzers(count):
    for i in range(0,count):
        process = multiprocessing.Process(target=analyzer, args=(i,))
        process.start()
        analyzers.append(process)

listner = multiprocessing.Process(target=setup_listener, args=())
def lauch_listener():
    listner = multiprocessing.Process(target=setup_listener, args=())
    listner.start()
    # while(True):
    #    if debug : print("_")
    #    time.sleep(3)



if debug : print('prepare to lauch')
col=0
if mqtt_listener is None:
    #setup_listener()
    lauch_listener()
    #listner = multiprocessing.Process(target=setup_listener, args=())
    #listner.start()
#while True:

   #print(listner.is_alive())
    #time.sleep(0.5)

if len(analyzers) == 0:
    lauch_analyzers(1)
