import zmq

DEFAULT_SERVER_NAME = "0.0.0.0"
DEFAULT_SERVER_PORT = 15000
MIN_SERVER_PORT = 0
MAX_SERVER_PORT = 65535

context = zmq.Context()
s = context.socket(zmq.SUB)

<<<<<<< HEAD
serverName = input("Enter server hostname or IP address [default: localhost]: ") or "localhost"

# 1. Nos conectamos a múltiples publicadores (Múltiples llamadas a connect)
# Asumiremos que abriste un publicador en el 15000 y otro en el 15001
puertos_a_conectar = [15000, 15001]

for port in puertos_a_conectar:
    p = f"tcp://{serverName}:{port}"
    print(f"Conectando al publicador en {p}...")
    s.connect(p)

# 2. Nos suscribimos a múltiples servicios (Múltiples llamadas a setsockopt_string)
temas = ["FITNESS", "NUTRITION"]

for tema in temas:
    print(f"Suscribiéndose al servicio: {tema}")
    s.setsockopt_string(zmq.SUBSCRIBE, tema)

print("\nEsperando mensajes de los publicadores (Presiona Ctrl+C para salir)...")

try:
    # 3. Escuchamos de forma continua
    while True:
        mensaje_recibido = s.recv().decode("utf-8")
        print(f"Recibido: {mensaje_recibido}")
except KeyboardInterrupt:
    print("\nSuscriptor desconectado.")
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
s.connect(p)

s.setsockopt_string(zmq.SUBSCRIBE, "TIME")

for i in range(5):
    time = s.recv().decode("utf-8")
    print(time)
>>>>>>> d5368acef01f719061c1845f0f2afcc16b53edb2

