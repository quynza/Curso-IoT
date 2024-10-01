import network

wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)                   # activate the interface
listWifi = wlan.scan()              # scan for access points

for item in listWifi:
    ssid = item[0].decode('utf-8')
    channel = str(item[2])
    rssi = str(item[3])
    security = str(item[4])
    hidden =  str(bool(item[5]))
    
    print("SSID: "+ ssid + ", Canal: "+ channel + ", RSSI: "+ rssi + ", Securidad: "+ security + ", Oculto: "+ hidden)
