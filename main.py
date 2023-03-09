import sys
from Adafruit_IO import MQTTClient
import time
import random
from simple_ai import *
from uart import *

# set up information
AIO_FEED_IDs = ["nutnhan1", "nutnhan2"]
AIO_USERNAME = "huy_tran"
AIO_KEY = "aio_qyRp58d3H6xf0Kr1tOV1nPNJAvT1"

# define four functions of gateway
def connected(client):
    print("Ket noi thanh cong ...")
    for topic in AIO_FEED_IDs:
            client.subscribe(topic)
def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")
def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)
def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload + " , feed id:" + feed_id)
    if(feed_id == "nutnhan1"):      #nhutnhan1 = light
        if payload == "0":
            writeData(0)
        else:
            writeData(1)
    if(feed_id == "nutnhan2"):
        if payload == "0":
            writeData(3)
        else:
            writeData(4)

#init a gateway object
client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
counter = 10
counter_ai = 5

#infinite loop
while True:
    # counter = counter - 1
    # if counter <= 0:
    #     counter = 10
    #     #TODO
    #     print("Random data is publishing...")
    #     temp = random.randint(10, 20)
    #     client.publish("cambien1", temp)
    #     humi = random.randint(50, 70)
    #     client.publish("cambien2", humi)
    #     light = random.randint(100, 500)
    #     client.publish("cambien3", light)

    #image detector
    counter_ai = counter_ai - 1
    if counter_ai <= 0:
        counter_ai = 5
        ai_result = image_detector()
        print("AI_output: ", ai_result)
        client.publish("ai", ai_result)

    #read data from sensor (simulation)
    readSerial(client)
    time.sleep(1)