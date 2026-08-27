import xmlrpc.client
import numpy as np 

DEFAULT_SERVER_NAME:str = "localhost"
DEFAULT_SERVER_PORT:int = 12000
MIN_SERVER_PORT_NUMBER:int = 0
MAX_SERVER_PORT_NUMBER:int = 62235

createClientProxy() -> None:
    serverName:str = input("Enter server hostname or IP address: ") # Create a client proxy
    if not serverName:
        serverName:str = DEFAULT_SERVER_NAME
    try:
        serverPort:int = int(input("Enter server port number: "))
    except:
        print(f"Invalid input. Using default port {DEFAULT_SERVER_PORT}.")
        serverPort:int = DEFAULT_SERVER_PORT
    if serverPort <= MIN_SERVER_PORT_NUMBER or serverPort > MAX_SERVER_PORT_NUMBER:
        serverPort = DEFAULT_SERVER_PORT
    return proxy = xmlrpc.client.ServerProxy(f"http://{serverName}:{serverPort}/RPC2")

def main() -> None:
    createClientProxy()
    result = proxy.add(8, 3) # Call the remote method 'add'
    print("8 + 3 =", result)
