from socket import *
import time
import threading # Importamos el módulo de hilos

def handle_client(connectionSocket, addr):
    print(f"From Client: {addr}")
    try:
        sentence = connectionSocket.recv(1024).decode()
        print(f"I received from {addr}: {sentence}")
        
        capitalizedSentence = sentence.upper()
        time.sleep(3) # Simulamos un procesamiento pesado
        
        connectionSocket.send(capitalizedSentence.encode())
    except Exception as e:
        print("Error with client", addr, ":", e)
    finally:
        connectionSocket.close()

# Configuración inicial (igual que antes)
try:
    serverPort = int(input("Enter server port number: "))
except:
    print("Invalid input. Using default port 12000.")
    serverPort = 12000

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(5) # Aumentamos el backlog a 5 para soportar conexiones en cola
print("The multithreaded server is ready to receive")

while True:
    try:
        connectionSocket, addr = serverSocket.accept()
        
        # En lugar de procesarlo aquí, creamos un hilo para este cliente
        client_thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
        client_thread.start()
        print(f"Active connections: {threading.active_count() - 1}")
        
    except KeyboardInterrupt:
        print("\nServer is shutting down.")
        break
