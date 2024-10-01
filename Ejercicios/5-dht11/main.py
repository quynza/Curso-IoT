from machine import Pin
import socket
import uselect as select
import DHT11

temp = 0
hum = 0

def web_page():
    f = open('html_dht11.html')
    text = f.read()
    f.close()
    
    html = str(text)
    html = str(html).replace("%temp", str(temp))
    html = str(html).replace("%hum", str(hum))
    return html

# Create a Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind the socket to a IP Address and Port
s.bind(('', 80))
# Accept maximum 5 connections
s.listen(5)

while True:
    # Read Sensor
    temp,hum = DHT11.read_DHT11(23)
    
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
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            
            # Close Socket
            conn.close()
