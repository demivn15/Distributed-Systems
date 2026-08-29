import zmq

context = zmq.Context()

# Frontend (Entrada): Recibe las tareas de múltiples Sources
frontend = context.socket(zmq.PULL)
frontend.bind("tcp://*:13000")

# Backend (Salida): Empuja las tareas hacia múltiples Workers
backend = context.socket(zmq.PUSH)
backend.bind("tcp://*:13001")

print("Broker iniciado.")
print("Escuchando Sources en el puerto 13000...")
print("Distribuyendo a Workers en el puerto 13001...")

try:
    # El bucle infinito que pasa los mensajes de un lado a otro
    while True:
        # 1. Recibe el mensaje serializado (pickle) del Source
        mensaje = frontend.recv()
        
        # 2. Lo reenvía inmediatamente al Worker que esté libre
        backend.send(mensaje)
        
except KeyboardInterrupt:
    print("\nBroker detenido.")