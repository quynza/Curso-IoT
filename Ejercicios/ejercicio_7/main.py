from machine import Pin
import socket
import uselect as select
import time

sensor_ir = Pin(23, Pin.IN)  # Pin para el sensor infrarrojo
actual_value = 0
last_value = 0
detections = [] # Historial de detecciones

def web_page():
    background_color = "red" if actual_value else "white"
    alarm_status = "Movimiento detectado" if actual_value else "No se detecta movimiento"
    detection_list = "".join([f"<li>{d}</li>" for d in detections])
    
    f = open('html_IR.html')
    text = f.read()
    f.close()
    
    html = str(text)
    html = str(html).replace("%bg_color", str(background_color))
    html = str(html).replace("%status", str(alarm_status))
    html = str(html).replace("%detect_list", str(detection_list))
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
    if time.ticks_diff(time2, time1) >= 2000000:
        time1 = time.ticks_us()
        try:
            last_value = actual_value
            # Detectar movimiento
            actual_value = not sensor_ir.value()
            if actual_value and not last_value:
                now = time.localtime()
                current_time = "{}-{}-{} {}:{}:{}".format(now[0], now[1], now[2], now[3], now[4], now[5])
                detections.append(f"Movimiento detectado a las {current_time}")
                if len(detections) > 10:  # Limitar a las últimas 10 detecciones
                    detections.pop(0)
            
            
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
