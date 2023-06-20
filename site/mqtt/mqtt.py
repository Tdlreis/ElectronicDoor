import paho.mqtt.client as mqtt
from django.conf import settings
from hours_app.models import User, Punch, HoursWorked
from django.utils import timezone
import time
import socket
import threading

def on_connect(client, userdata, flags, rc):
    if rc == 0:
         print('Connected successfully')        
         client.publish("server/status", "online", 2, True)
    else:
         print('Bad connection. Code:', rc)

def on_message(client, userdata, msg):
    # # Print MQTT message to the terminal
    # print("Received message from topic: {}".format(msg.topic))
    # print("Payload: {}".format(msg.payload.decode("utf-8")))
    # print("=============================")

    if msg.topic == "server/auth":
        try:
            user = User.objects.get(rfid_num=msg.payload.decode("utf-8"))
            print(user.user_name)
            last_punch = user.punch_set.last()
            
            if not user.authorization:
                client.publish("door/notauth", " ")
            elif not last_punch or not last_punch.is_in:
                client.publish("door/enter", user.user_name)
                punch_in(user.pk)
            else:
                punch_out(user.pk)
                client.publish("door/leave", user.user_name)        
        except User.DoesNotExist:
            print("Não encontrado")
            client.publish("door/notopen", " ")
            pass

def on_disconnect(client, userdata, rc):
    client.loop_stop()
    mqtt_thread = threading.Thread(target=establish_mqtt_connection)
    mqtt_thread.start()

def start_mqtt_handler():
    mqtt_thread = threading.Thread(target=establish_mqtt_connection)
    mqtt_thread.start()

def establish_mqtt_connection():
    # Create MQTT client and connect
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    # Set MQTT broker credentials if required
    if settings.MQTT_USER and settings.MQTT_PASSWORD:
        client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)

    client.will_set("server/status", "offline", 2, True)

    # Connect to the MQTT broker
    while True:
        try:
            client.connect(settings.MQTT_SERVER, settings.MQTT_PORT, 60)
            # Subscribe to topics
            for topic in settings.MQTT_TOPICS:
                client.subscribe(topic, qos=2)

            # Start the MQTT loop in a non-blocking manner
            client.loop_start()
            break
        except socket.error as e:
            # Handle the socket connection error
            print(f"Socket connection error: {e}")
            time.sleep(1)

def punch_in(user_id):
    user = User.objects.get(pk=user_id)
    current_time = timezone.now()
    last_punch = user.punch_set.last()

    if not last_punch or not last_punch.is_in:
        Punch.objects.create(user=user, punch_time=current_time, is_in=True)

def punch_out(user_id):
    user = User.objects.get(pk=user_id)
    current_time = timezone.now()
    last_punch = user.punch_set.last()

    if last_punch and last_punch.is_in:
        Punch.objects.create(user=user, punch_time=current_time, is_in=False)

        # Calculate hours worked and update HoursWorked model
        punches = user.punch_set.all().order_by('punch_time')
        total_hours = 0.0
        in_time = None
        for punch in punches:
            if punch.is_in:
                in_time = punch.punch_time
            else:
                if in_time:
                    out_time = punch.punch_time
                    duration = out_time - in_time
                    total_hours += duration.total_seconds() / 3600
                    in_time = None

        hours_worked, _ = HoursWorked.objects.get_or_create(user=user)
        hours_worked.hours = total_hours
        hours_worked.save()