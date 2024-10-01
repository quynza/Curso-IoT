from machine import Pin
import socket

p2 = Pin(2,Pin.OUT)

def web_page():
    if p2.value() == 1:
        gpio_state="ON"
    else:
        gpio_state="OFF"
    
    f = open('html_led.html')
    text = f.read()
    f.close()
    
    html = str(text)
    html = str(html).replace("%s", gpio_state)
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
    # When a client connects, the connection is accepted
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    
    # Get the received request of the client
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)
    
    # Find commands of client to turn ON/OFF the led
    led_on = request.find('/?led=on')
    led_off = request.find('/?led=off')
    if led_on == 6:
        print('LED ON')
        p2.value(1)
    if led_off == 6:
        print('LED OFF')
        p2.value(0)
        
    # Generate the HTML text of Web Site
    response = web_page()
    
    # Send the responde to client following HTML protocols
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    
    # Close Socket
    conn.close()
