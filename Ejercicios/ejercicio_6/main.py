from machine import Pin
import socket
import uselect as select
import dht
import time

sensor = dht.DHT11(Pin(23))
temp = 0
humi = 0

def web_page():
    f = open('html_dht11.html')
    text = f.read()
    f.close()
    
    html = str(text)
    html = str(html).replace("%temp", str(temp))
    html = str(html).replace("%hum", str(humi))
    return html

# Create a Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind the socket to a IP Address and Port
s.bind(('', 80))
# Accept maximum 5 connections
s.listen(5)

time1 = time.ticks_us()
while True:
    time2 = time.ticks_us()
    if time.ticks_diff(time2, time1) >= 5000000:
        time1 = time.ticks_us()
        try:
            # Measure temperature and humidity
            sensor.measure()

            # Get temperature and humidity values
            temp = sensor.temperature()
            humi = sensor.humidity()
            
        except Exception as e:
            print("Error: ", e)
    
    # Check incoming client each 0.5 seg
    r, w, err = select.select((s,), (), (), 0.5)
    if r:
        for readable in r:
            # When a client connects, the connection is accepted
            conn, addr = s.accept()
            print('Got a connection from %s' % str(addr))
            
            # Get the received request of the client
            request = conn.recv(1024)
            request = str(request)
            print('Content = %s' % request)
                
            # Generate the HTML text of Web Site
            response = web_page()
            
            # Send the responde to client following HTML protocols
            conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            conn.sendall(response)
            
            # Close Socket
            conn.close()
