# Server in Python

from socket import *
import time
import threading

def handle_client(connectionSocket, addr):
    while True:
        print(f"From Client: {addr}")
        try:
            sentence = connectionSocket.recv(1024).decode()
            print(f"I received from {addr}: {sentence}")
            capitalizedSentence = sentence.upper()
            time.sleep(3)
            connectionSocket.send(capitalizedSentence.encode())
        except Exception as e:
            print("Error with client", addr, ":", e)
        finally:
            connectionSocket.close()
            break

try:
    serverPort = int(input("Enter server port number: "))
except:
    print("Invalid input. Using default port 12000.")
    serverPort = 12000

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(5)
print("The multithreaded server is ready to receive")

while True:
    try:
        connectionSocket, addr = serverSocket.accept()
        client_thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
        client_thread.start()
        print(f"Active connections: {threading.active_count() - 1}")
    except KeyboardInterrupt:
        print("\nServer is shutting down.")
        break
