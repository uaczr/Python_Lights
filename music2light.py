import time
import paho.mqtt.client as mqtt
from threading import Thread

class LightControl:
    states = ["Starting", "Config", "Running", "Stopping"]

    def __init__(self):
        self.current_state = "Starting"

    def loop(self):
        error = "None"
        if(self.current_state == "Starting"):
            error = self.start()
        if(self.current_state == "Config"):
            error = self.config()
        if(self.current_state == "Running"):
            error = self.run()
        if(self.current_state == "Stopping"):
            error = self.stop()

        return error;

    def start(self):
        print("start")

    def config(self):
        print("config")

    def run(self):
        print("run")

    def stop(self):
        print("stop")



class MqttCommunicator:
    online = False


    # Konstruktor
    def __init__(self, subscription_topics):
        self.MqttClient = mqtt.Client()
        self.MqttClient.on_connect = self.on_connect
        self.MqttClient.on_message = self.on_message
        self.subscription_topics = subscription_topics

    #Aufgerufen, wenn Client verbunden ist.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.MqttClient.publish("current_time", {}.format(int(time.time()*1000)))
        self.MqttClient.publish("hello/id", "0")
        self.MqttClient.publish("beat/predicted_time", {}.format(int(time.time()*1000+500)))
        self.MqttClient.publish("beat/period", "500")
        self.MqttClient.subscribe("devices/#")
        self.online = True

    # Aufgerufen wenn eine Nachricht empfangen wurde
    def on_message(self, client, userdata, msg):
        if(msg.topic == "hello/mac"):
            self.on_hello_mac()
        if(msg.topic == "hello/device"):
            self.on_hello_device()
        if("knopfbox" in msg.topic):
            print(msg.topic)

    # Diese Methode verbindet den Protokollwrapper mit dem MQTT-Broker
    def connect(self, host, port=1883, keepalive=60):
        self.MqttClient.connect(host=host,port=port,keepalive=keepalive)
        thread1 = Thread(target=self.loop_Mqtt)
        thread2 = Thread(target=self.loop_SystemVars)
        thread1.start()
        thread2.start()
        thread1.join()

    # Loop des MQTT Clients
    def loop_Mqtt(self):
        self.MqttClient.loop_forever()


    def loop_SystemVars(self):
        while(True):
            self.MqttClient.publish("current_time", {}.format(int(time.time()*1000)))
            time.sleep(5)



    # Publish Topic and Payload
    def publish(self, topic, payload):
        self.MqttClient.publish(topic, payload=payload)

    # Subscribe topic
    def subscribe(self, topic):
        self.MqttClient.subscribe(topic)


def music2light_worker():
    """Code Hier"""
    print("123")
import time
if __name__ == "__main__":
    lightControl = LightControl()

    while(True):
        lightControl.loop()
        time.sleep(0.1)