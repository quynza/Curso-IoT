from umqtt.simple import MQTTClient
import random
import time
from machine import Pin

Bttn_Stop = Pin(12, Pin.IN)
Bttn_Start = Pin(13, Pin.IN)
Bttn_Em_Stop = Pin(14, Pin.IN)
do = False
Em_Stop = False
CLIENT_NAME = "umqtt_client"
SERVER_ADDR = "192.168.1.10"
mqtt_client = MQTTClient(CLIENT_NAME, SERVER_ADDR, keepalive=60)
mqtt_client.connect()

time1 = time.ticks_us()
time3 = time.ticks_us()
while not Em_Stop:
    time2 = time.ticks_us()
    if time.ticks_diff(time2, time1) >= 1000000:
        time1 = time.ticks_us()
        if do:
            try:
                mqtt_client.publish("sensor1",str(random.randint(0,10)))
                mqtt_client.publish("sensor2",str(random.randint(0,10)))
                mqtt_client.publish("sensor3",str(random.randint(0,10)))
                mqtt_client.publish("sensor4",str(random.randint(0,10)))
            except Exception as e:
                print("Error: ", e)
    
    time4 = time.ticks_us()
    if time.ticks_diff(time4, time3) >= 100000:
        time3 = time.ticks_us()
        Em_Stop = Bttn_Em_Stop.value()
        if Bttn_Start.value():
            do = True
        if Bttn_Stop.value():
            do = False
            
