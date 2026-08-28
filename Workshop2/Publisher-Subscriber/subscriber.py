import zmq

context = zmq.Context()
s = context.socket(zmq.SUB)

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

