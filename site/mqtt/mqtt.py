import paho.mqtt.client as mqtt
from django.conf import settings
from door_user.models import User, PunchCard, Rfid
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
            print(msg.payload.decode("utf-8"))
            rfid = Rfid.objects.get(rfid_uid=msg.payload.decode("utf-8"))
            user = rfid.user

            last_punch = user.punchcard_set.last()
            
            if not user.authorization:
                client.publish("door/notauth", " ")
            elif not rfid.authorization:
                client.publish("door/notauth", " ")
            elif not last_punch or not last_punch.out:
                client.publish("door/enter", user.user_name)
                punch_in(user.pk)
            else:
                punch_out(user.pk)
                client.publish("door/leave", user.user_name)        
        except Rfid.DoesNotExist:
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
    last_punch = user.punchcard_set.last()

    if not last_punch or not last_punch.out:
        PunchCard.objects.create(user=user, punch_in_time=current_time, out=True)

def punch_out(user_id):
    user = User.objects.get(pk=user_id)
    current_time = timezone.now()
    last_punch = user.punchcard_set.last()

    if last_punch and last_punch.out:
        last_punch.out = False
        last_punch.punch_out_time = current_time
        last_punch.save()