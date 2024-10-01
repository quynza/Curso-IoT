from machine import Pin

p2 = Pin(2,Pin.OUT)

def do_connect(ssid,pwd):
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    wlan.active(True)
    if not wlan.isconnected():
        p2.off()
        print('Conectando a red WiFi...')
        wlan.connect(ssid, pwd)
        while not wlan.isconnected():
            pass
        p2.on()
        print('Conexión exitosa!')
        config = wlan.ifconfig()
        print("IP address: " + config[0] + ", subnet mask: "+ config[1] + ", gateway: " + config[2] + ", DNS server: " + config[3])

do_connect("Quynza","Majo2011")