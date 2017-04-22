#! /bin/bash
import time
import paho.mqtt.client as mqtt
from threading import Thread

class MqttClient:
    online = False
    times = []
    # Konstruktor
    def __init__(self):
        self.MqttClient = mqtt.Client()
        self.MqttClient.on_connect = self.on_connect
        self.MqttClient.on_message = self.on_message

    #Aufgerufen, wenn Client verbunden ist.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.MqttClient.subscribe("ll/current_time")
        current_time = time.time()
        self.online = True

    # Aufgerufen wenn eine Nachricht empfangen wurde
    def on_message(self, client, userdata, msg):
        self.times.append(time.time() - float(msg.payload))
        #print len(self.times)

    # Diese Methode verbindet den Protokollwrapper mit dem MQTT-Broker
    def connect(self, host, port=1883, keepalive=60):
        self.MqttClient.connect(host=host,port=port,keepalive=keepalive)
        self.MqttClient.loop_forever()

    def publish(self, topic, payload):
        self.MqttClient.publish(topic, payload=payload)





def mqtt_subscription_worker(host, client):
    client.connect(host)

def mqtt_publish_worker(client):
    while(client.online == False):
        time.sleep(1)

    for i in range(0, 100):
        client.publish("ll/current_time", "{:.9f}".format(time.time()))
        time.sleep(0.1)

    number = 0
    sum = 0
    for i in client.times:
        number += 1
        sum += i

    print  "{}".format(number) + " " + "{:.9f}".format(sum/number)

if __name__ == "__main__":
    client = MqttClient()
    subscribe_loop = Thread(target=mqtt_subscription_worker, args=("192.168.178.36",client))
    subscribe_loop.start()
    publish_loop = Thread(target=mqtt_publish_worker, args=(client, ))
    publish_loop.start()

    subscribe_loop.join()

