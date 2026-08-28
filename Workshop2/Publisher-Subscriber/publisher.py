import zmq, time

DEFAULT_SERVER_NAME = "0.0.0.0"
DEFAULT_SERVER_PORT = 15000
MIN_SERVER_PORT = 0
MAX_SERVER_PORT = 65535

context = zmq.Context()
s = context.socket(zmq.PUB)

<<<<<<< HEAD
serverName = input("Enter server hostname or IP address [default: localhost]: ") or "localhost"
try:
    serverPort = int(input("Enter server port number [default: 15000]: ") or 15000)
except ValueError:
    serverPort = 15000

p = f"tcp://{serverName}:{serverPort}"
=======
serverName = input("Enter server hostname or IP address: ")
if not serverName:
    serverName = DEFAULT_SERVER_NAME
try:
    serverPort = int(input("Enter server port number: "))
except:
    print(f"Invalid input. Using default port {DEFAULT_SERVER_PORT}.")
    serverPort = DEFAULT_SERVER_PORT

if serverPort <= MIN_SERVER_PORT or serverPort > MAX_SERVER_PORT:
    serverPort = DEFAULT_SERVER_PORT

p = "tcp://" + serverName + ":" + str(serverPort)
>>>>>>> d5368acef01f719061c1845f0f2afcc16b53edb2
s.bind(p)

# Solicitamos el servicio (Topic) que este publicador va a ofrecer
topic = input("Ingresa el servicio a publicar (ej. FITNESS, NUTRITION): ").upper()
if not topic:
    topic = "GENERAL"

print(f"Publicador iniciado en {p} ofreciendo el servicio '{topic}'...")

cont = 0
while True:
    time.sleep(3) # Pausa de 3 segundos
    cont += 1
<<<<<<< HEAD
    
    # Generamos un mensaje distinto dependiendo del servicio elegido
    if topic == "FITNESS":
        mensaje = f"{topic} - Entrenamiento #{cont}: Recordatorio de rutina de 2 horas."
    elif topic == "NUTRITION":
        mensaje = f"{topic} - Comida #{cont}: Menestra de lentejas con atún y plátano verde."
    else:
        mensaje = f"{topic} - Mensaje genérico #{cont}"
        
    s.send(mensaje.encode("utf-8"))
=======
    s.send(("TIME " + time.asctime() + " - Message #" + str(cont)).encode("utf-8"))
>>>>>>> d5368acef01f719061c1845f0f2afcc16b53edb2
