# Client socket in Python

from socket import *
import threading
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

DEFAULT_NUMBER_CLIENTS:int = 3
DEFAULT_SERVER_NAME:str = "172.23.202.123"
DEFAULT_PORT_NUMBER:int = 12000
MIN_PORT_NUMBER:int = 0
MAX_PORT_NUMBER:int = 65535
DATA_CHUNK:int = 1024

def serverIdentification() -> tuple:
    serverName = input("Enter server hostname or IP address: ")
    if not serverName:
        serverName = DEFAULT_SERVER_NAME
    try:
        serverPort = int(input("Enter server port number: "))
    except:
        logging.info(f"Invalid input. Using default port {DEFAULT_PORT_NUMBER}")
        serverPort = DEFAULT_PORT_NUMBER
    if serverPort <= MIN_PORT_NUMBER or serverPort > MAX_PORT_NUMBER:
        serverPort = DEFAULT_PORT_NUMBER
    return (serverName, serverPort)

def client(clientID:int, serverName:str, serverPort:int ) -> None:
    next:bool = True
    while next:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        try:
            clientSocket.connect((serverName, serverPort))
        except Exception as exception:
            logging.info(exception)
            repeat = input("Do you want to try again? (Y/N)")
            if repeat.upper() == "N":
                break
            else:
                continue
        sentence = input(f"Enter a lowercase sentence for client {clientID}:")
        clientSocket.send(sentence.encode())
        modifiedSentence = clientSocket.recv(DATA_CHUNK)
        print("Message from server:", modifiedSentence.decode())
        other = input("Other message: (Y/N)")
        if other.upper() == "N":
            next = False
        clientSocket.close()

def main() -> None:
    clientsNumber:int = input("Enter the number of clients: ")
    if not clientsNumber:
        clientsNumber = DEFAULT_NUMBER_CLIENTS
    threads:list = []
    for _id in range(clientsNumber):
        serverName, serverPort = serverIdentification()
        thread = threading.Thread(
                target = client,
                args=(_id + 1, serverName, serverPort)
                )
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
