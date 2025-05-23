from machine import Pin, Timer
import socket
import uselect as select

# Configuración de pines para los segmentos (a-g, punto decimal)
segments = [Pin(i, Pin.OUT) for i in [15,16,17,18,19,21,22]]
# Configuración de pines para los dígitos (catodos/anodos)
digits = [Pin(i, Pin.OUT) for i in [13,12,14,27]]

j = 0

# Tabla de segmentos para números y letras
segment_map = {
    ' ': 0,
    '0': 63,
    '1': 6,
    '2': 91,
    '3': 79,
    '4': 102,
    '5': 109,
    '6': 125,
    '7': 7,
    '8': 127,
    '9': 103,
    'A': 119,
    'B': 124,
    'C': 57,
    'D': 94,
    'E': 121,
    'F': 113,
    'G': 111,
    'H': 118,
    'I': 25,
    'J': 30,
    'K': 122,
    'L': 56,
    'M': 55,
    'N': 84,
    'O': 63,
    'P': 115,
    'Q': 103,
    'R': 80,
    'S': 109,
    'T': 120,
    'U': 28,
    'V': 62,
    'W': 29,
    'X': 112,
    'Y': 110,
    'Z': 73,
}

params = {
    'd1': " ",
    'd2': " ",
    'd3': " ",
    'd4': " "
}

def decode_segments(value):
    # Generar un array de tamaño 7 representando cada segmento
    return [(value >> i) & 1 for i in range(0, 7, 1)]

def display_digit(digit, value):
    # Desactivar todos los dígitos
    for i, pin in enumerate(digits):
        pin.init(pin.IN)
        pin.value(0)
    
    # Desactivar todos los segmentos
    for i, pin in enumerate(segments):
        pin.init(pin.IN)
        pin.value(0)
    
    # Activar el dígito correspondiente
    digits[digit].init(Pin.OUT)
    digits[digit].value(1)

    # Activar segmentos según el valor decodificado
    segment_values = decode_segments(segment_map[value])
    for i, pin in enumerate(segments):
        if segment_values[i]:
            pin.init(Pin.OUT)
            pin.value(0)  # Activo (cátodo común)

# Callback function for the timer
def update_diplay(timer):
    global j
    if j<3:
        j = j + 1
    else:
        j = 0
    display_digit(j, params.get("d"+str(j+1), " "))

# Create a periodic timer
blink_timer = Timer(1)
blink_timer.init(mode=Timer.PERIODIC, period=5, callback=update_diplay)  # Timer repeats 10ms

def web_page(param):
    f = open('html_7_segment.html')
    text = f.read()
    f.close()
    
    html = str(text)
    html = str(html).replace("%d1", str(params.get("d1", " ")))
    html = str(html).replace("%d2", str(params.get("d2", " ")))
    html = str(html).replace("%d3", str(params.get("d3", " ")))
    html = str(html).replace("%d4", str(params.get("d4", " ")))
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
    # Check incoming client each 0.5 seg
    r, w, err = select.select((s,), (), (), 1)
    if r:
        for readable in r:
            # When a client connects, the connection is accepted
            conn, addr = s.accept()
            
            # Get the received request of the client
            request = conn.recv(1024)
            request = request.decode()

            if 'POST' in request:
                body = request.split('\r\n\r\n')[1]
                params = {"d"+str(i+1): param for i,param in enumerate(body.split('&'))}
                print(f"d1: {params.get("d1", " ")}, d2: {params.get("d2", " ")}, d3: {params.get("d3", " ")}, d4: {params.get("d4", " ")}")

            if 'GET' in request:
                # Generate the HTML text of Web Site
                response = web_page(params)
                # Send the responde to client following HTML protocols
                conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                conn.sendall(response)

            conn.close()
