# Client in Python

import logging
import random
from socket import *
import string
import threading

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s - %(levelname)s - %(message)s"
)

DEFAULT_NUMBER_OF_CLIENTS:int = 3
DEFAULT_SERVER_NAME:str = "172.23.197.112"
DEFAULT_PORT_NUMBER:int = 12000
MIN_PORT_NUMBER:int = 0
MAX_PORT_NUMBER:int = 65535
BYTES_DATA_CHUNK:int = 1024

def serverIdentification() -> tuple:
    serverName:str = input("Enter server hostname or IP address: ")
    if not serverName:
        serverName = DEFAULT_SERVER_NAME
        logging.info(f"No IP address specified. Using default address: {DEFAULT_SERVER_NAME}")
    serverPort:str = input("Enter server port number: ")
    if not serverPort:
        serverPort = DEFAULT_PORT_NUMBER
        logging.info(f"No port number specified. Using default port number: {DEFAULT_PORT_NUMBER}")
    try:
        serverPort_int:int = int(serverPort)
    except:
        serverPort_int = DEFAULT_PORT_NUMBER
        logging.info(f"Invalid port number. Using default port number: {DEFAULT_PORT_NUMBER}")
    if serverPort_int <= MIN_PORT_NUMBER or serverPort_int > MAX_PORT_NUMBER:
        serverPort_int = DEFAULT_PORT_NUMBER
    logging.info(f"Preparing to connect to the server...")
    return (serverName, serverPort_int)

def clientInitialization(clientID:int, serverName:str, serverPort:int) -> None:
    numberOfMessages = random.randint(1, 3)
    clientSocket:socket = socket(AF_INET, SOCK_STREAM)
    try:
        clientSocket.connect((serverName, serverPort))
    except Exception as exception:
        logging.error(f"Client {clientID} failed: {exception}")
        break # Break the loop if connection fails.
    for message in range(numberOfMessages):
        randomText = "".join(random.choices(string.ascii_lowercase, k = 8))
        sentence:str = f"Client {clientID}, message {message + 1}: {randomText}"
        logging.info(f"Client {clientID} successfully connected to the server.")
        clientSocket.send(sentence.encode())
        modifiedSentence:bytes = clientSocket.recv(BYTES_DATA_CHUNK)
        print(f"[Client {clientID}] Message from server:", modifiedSentence.decode())
        clientSocket.close()

def main() -> None:
    numberOfClients:str = input("Enter the number of clients: ")
    if not numberOfClients:
        numberOfClients_int = DEFAULT_NUMBER_OF_CLIENTS
        logging.info(f"No number of clients specified. Using {DEFAULT_NUMBER_OF_CLIENTS} clients.")
    else:
        numberOfClients_int = int(numberOfClients)
    serverName, serverPort = serverIdentification()
    threads:list = []
    for _id in range(numberOfClients_int):
        thread:threading.Thread = threading.Thread(target = clientInitialization, args = (_id + 1, serverName, serverPort))
        threads.append(thread)
        thread.start()

if __name__ == "__main__":
    main()
