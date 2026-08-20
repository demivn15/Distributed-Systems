# Client socket in Python

from socket import *
import threading

SERVER_NAME:str = "localhost"
DEFAULT_PORT:int = 12000
MIN_PORT:int = 0
MAX_PORT:int = 65535


def connectServer() -> tuple:
    serverName = input("Enter server hostname or IP address: ")
    if not serverName:
        serverName = SERVER_NAME
    try:
        serverPort = int(input("Enter server port number: "))
    except:
        print("Invalid input. Using default port", DEFAULT_PORT)
        serverPort = DEFAULT_PORT

    if serverPort <= MIN_PORT or serverPort > MAX_PORT:
        serverPort = DEFAULT_PORT
    return (serverName, serverPort)

def sendMessage(serverName:str, serverPort:int) -> None:
    next:bool = True
    while next:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        try:
            clientSocket.connect((serverName, serverPort))
        except Exception as e:
            print("Connection error:", e)
            repeat = input("Do you want to try again? (Y/N)")
            if repeat.upper() == "N":
                break
            else:
                continue
        sentence = input("Input lowercase sentence:")
        clientSocket.send(sentence.encode())
        modifiedSentence = clientSocket.recv(1024)
        print("From Server:", modifiedSentence.decode())
        other = input("Other message: (Y/N)")
        if other.upper() == "N":
            next = False
        clientSocket.close()

def client() -> None:
    serverInfo  = connectServer()
    sendMessage(serverInfo[0], serverInfo[1])

def main() -> None:
    thread1 = threading.Thread(target = client)
    thread2 = threading.Thread(target = client)

    thread1.start()
    thread1.join()

if __name__ == "__main__":
    main()
