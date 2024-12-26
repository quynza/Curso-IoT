from machine import Pin, PWM
import socket
import uselect as select
import time

r = 0
g = 0
b = 0
# Configuración de pines PWM para el LED RGB
red = PWM(Pin(14), freq=5000)
green = PWM(Pin(12), freq=5000)
blue = PWM(Pin(13), freq=5000)

# Función para ajustar el brillo de cada canal RGB
def set_color(r, g, b):
    red.duty_u16(int(r * 65535 / 255))
    green.duty_u16(int(g * 65535 / 255))
    blue.duty_u16(int(b * 65535 / 255))

def web_page():
    f = open('html_rgb_control.html')
    text = f.read()
    f.close()
    
    html = str(text)
    html = str(html).replace("%r", str(r))
    html = str(html).replace("%g", str(g))
    html = str(html).replace("%b", str(b))
    html = str(html).replace("%color", 'rgb('+str(r)+','+str(g)+','+str(b)+')')
    return html

# Create a Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind the socket to a IP Address and Port
s.bind(('', 80))
# Accept maximum 5 connections
s.listen(5)
# Tiempo mínimo entre mensajes (en segundos)
last_request_time = time.ticks_ms()

while True:
    # Check incoming client each 0.5 seg
    r, w, err = select.select((s,), (), (), 0.5)
    if r:
        for readable in r:
            # When a client connects, the connection is accepted
            conn, addr = s.accept()
            
            # Get the received request of the client
            request = conn.recv(1024)
            request = request.decode()
            
            # Extraer datos del formulario si es POST
            if 'POST' in request:
                # Obtener tiempo actual
                current_time = time.ticks_ms()
                # Ignorar solicitudes si no ha pasado el intervalo mínimo
                if time.ticks_diff(current_time, last_request_time) < 200:
                    conn.close()
                    continue
                else:
                    # Actualizar el tiempo de la última solicitud procesada
                    last_request_time = current_time
                    body = request.split('\r\n\r\n')[1]
                    params = {param.split('=')[0]: int(param.split('=')[1]) for param in body.split('&')}
                    r = params.get('red', 0)
                    g = params.get('green', 0)
                    b = params.get('blue', 0)
                    set_color(r, g, b)
            
            # Generate the HTML text of Web Site
            response = web_page()
            # Send the responde to client following HTML protocols
            conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            conn.sendall(response)
            
            # Close Socket
            conn.close()
