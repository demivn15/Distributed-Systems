import zmq, time

context = zmq.Context()
s = context.socket(zmq.PUB)

serverName = input("Enter server hostname or IP address [default: localhost]: ") or "localhost"
try:
    serverPort = int(input("Enter server port number [default: 15000]: ") or 15000)
except ValueError:
    serverPort = 15000

p = f"tcp://{serverName}:{serverPort}"
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
    
    # Generamos un mensaje distinto dependiendo del servicio elegido
    if topic == "FITNESS":
        mensaje = f"{topic} - Entrenamiento #{cont}: Recordatorio de rutina de 2 horas."
    elif topic == "NUTRITION":
        mensaje = f"{topic} - Comida #{cont}: Menestra de lentejas con atún y plátano verde."
    else:
        mensaje = f"{topic} - Mensaje genérico #{cont}"
        
    s.send(mensaje.encode("utf-8"))