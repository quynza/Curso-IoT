from machine import Pin
import network

p2 = Pin(2,Pin.OUT)

def do_connect(ssid,pwd):
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        p2.off()
        print('connecting to network...')
        wlan.connect(ssid, pwd)
        while not wlan.isconnected():
            pass
        p2.on()

do_connect("XXX","YYY")