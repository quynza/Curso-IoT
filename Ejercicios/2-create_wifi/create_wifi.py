from machine import Pin
import network

p2 = Pin(2, Pin.OUT)

ap = network.WLAN(network.AP_IF) # create access-point interface
ap.active(True)         # Desactivate the interface
ap.config(essid='ESP32', channel = 11, authmode = 3, password = 'quynza123')
ap.config(max_clients=10) # set how many clients can connect to the network

def printClients():
    clients = ap.status('stations')

    if len(clients) > 0:
        p2.on()
    else:
        p2.off()

while True:
    printClients()
