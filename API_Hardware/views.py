import paho.mqtt.client as mqtt
from API_Hardware.models import *
import multiprocessing
mqtt_listener = None


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

    def parse_dataset_1(self):
        print("dataset_1")
        message_date_time = datetime.datetime.utcfromtimestamp(int(self.raw_data[0]))
        print(message_date_time)
        error_codes = self.raw_data[1:]
        print(error_codes)
        vehicle = Vehicle.objects.get(VIN=self.car_id)

        if vehicle is not None:
            for error in error_codes:
                crash_description, _ = CrashDescription.objects.get_or_create(code=error)
                if crash_description.full_description == "":
                    crash_description.full_description = error
                if crash_description.short_description == "":
                        crash_description.short_description = error
                crash_description.save()

                crash = Crash.objects.create()
                crash.actual = True
                crash.description = crash_description
                crash.date = message_date_time
                crash.vehicle = vehicle
                crash.save()
                print(error)

    def parse_dataset_2(self):
        print("dataset_2")
        message_date_time = datetime.datetime.utcfromtimestamp(int(self.raw_data[0]))
        print(message_date_time)
        rpm = float(int(self.raw_data[1])/3000.1)*8000
        torque = int(self.raw_data[2])/250.1
        breake = int(self.raw_data[3])/250.1
        print("rpm "+str(rpm))
        print("torque " + str(torque))
        print("breake " + str(breake))

        vehicle = Vehicle.objects.get(VIN=self.car_id)

        if vehicle is not None:
            control_telemetry = ControlTelemetry.objects.create()
            control_telemetry.vehicle = vehicle
            control_telemetry.datetime = message_date_time
            control_telemetry.rpm = rpm
            control_telemetry.breake = breake
            control_telemetry.torque = torque
            control_telemetry.save()

    def parse_dataset_3(self):
        print("dataset_3")
        message_date_time = datetime.datetime.utcfromtimestamp(int(self.raw_data[0]))
        print(message_date_time)
        spd = float(self.raw_data[2])
        latitude = float(self.raw_data[3])
        longitude = float(self.raw_data[4])
        print("spd " + str(spd))
        print("latitude " + str(latitude))
        print("longetude " + str(longitude))

        vehicle = Vehicle.objects.get(VIN=self.car_id)

        if vehicle is not None:
            telemetry = LocationTelemetry.objects.create()
            telemetry.vehicle = vehicle
            telemetry.datetime = message_date_time
            telemetry.spd = spd
            telemetry.latitude = latitude
            telemetry.longitude = longitude
            telemetry.save()

    def parse_dataset_4(self):
        print("dataset_4")
        fuel = int(int(self.raw_data[1]) / 255.0)
        print("fuel " + str(fuel))
#        #accX = float(self.raw_data[2])
#        #accY = float(self.raw_data[3])
#        #accZ = float(self.raw_data[4])


def on_connect(rc):
    print("rc: " + str(rc))


def on_message(msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    try:
        MessageParser(msg.payload.decode("utf-8"))
    except Exception:
        print('shitty message')


def on_publish(mid):
    print("mid: " + str(mid))


def on_subscribe(mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(string):
    print(string)


def setup_listener():
    mqttc = mqtt.Client()
    # Assign event callbacks
    mqttc.on_message = on_message
    # mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    # Connect
    mqttc.connect("broker.hivemq.com", 1883, 60)
    mqttc.subscribe("mts_hardware_get_info_chanel", qos=0)
    # Continue the network loop
    mqttc.loop_forever()


def lauch_listener():
    listner = multiprocessing.Process(target=setup_listener, args=())
    listner.start()
    # while(True):
    #    print("_")
    #    time.sleep(3)

print('prepare to lauch')
if mqtt_listener is None:
    setup_listener()  #lauch_listener()
