# Client socket in Python

import logging
from socket import *
import threading

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s - %(levelname)s - %(message)s"
)

DEFAULT_NUMBER_OF_CLIENTS:int = 3
DEFAULT_SERVER_NAME:str = "172.23.202.123"
DEFAULT_PORT_NUMBER:int = 12000
MIN_PORT_NUMBER:int = 0
MAX_PORT_NUMBER:int = 65535
BYTES_DATA_CHUNK:int = 1024

def serverIdentification(clientID:int) -> tuple:
    serverName:str = input("Enter server hostname or IP address: ")
    if not serverName:
        serverName = DEFAULT_SERVER_NAME
        logging.info(f"No IP address specified. Using default address: {DEFAULT_SERVER_NAME}")
    serverPort:str = input("Enter server port number: ")
    if not serverPort:
        serverPort = DEFAULT_PORT_NUMBER
        logging.info(f"No port number specified. Using default port number: {DEFAULT_PORT_NUMBER}")
    if serverPort <= MIN_PORT_NUMBER or serverPort > MAX_PORT_NUMBER:
        serverPort = DEFAULT_PORT_NUMBER
    logging.info(f"Client {clientID} trying to connect to the server...")
    return (serverName, serverPort)

def clientInitialization(clientID:int, serverName:str, serverPort:int) -> None:
    next:bool = True
    while next:
        clientSocket:socket.socket = socket(AF_INET, SOCK_STREAM)
        try:
            clientSocket.connect((serverName, serverPort))
        except Exception as exception:
            logging.info(exception)
            repeat:str = input("Do you want to try again? (Y/N)")
            if repeat.upper() == "N":
                break
            else:
                continue
        logging.info(f"Client {clientID} successfully connected to the server.")
        sentence:str = input(f"Enter a lowercase sentence for client {clientID}:")
        clientSocket.send(sentence.encode())
        modifiedSentence:str = clientSocket.recv(BYTES_DATA_CHUNK)
        print("Message from server:", modifiedSentence.decode())
        other:str = input("Other message: (Y/N)")
        if other.upper() == "N":
            next = False
        clientSocket.close()

def main() -> None:
    numberOfClients:str = input("Enter the number of clients: ")
    if not numberOfClients:
        numberOfClients = DEFAULT_NUMBER_OF_CLIENTS
        logging.info(f"No number of clients specified. Using {DEFAULT_NUMBER_OF_CLIENTS} clients.")
    threads:list = []
    for _id in range(int(numberOfClients)):
        serverName, serverPort = serverIdentification(_id + 1)
        thread:threading.Thread = threading.Thread(target = clientInitialization, args = (_id + 1, serverName, serverPort))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
