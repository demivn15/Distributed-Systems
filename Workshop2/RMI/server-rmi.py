from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import numpy as np 

DEFAULT_SERVER_NAME:str = "localhost"
DEFAULT_SERVER_PORT:int = 12000
MIN_SERVER_PORT_NUMBER:int = 0
MAX_SERVER_PORT_NUMBER:int = 62235

class RequestHandler(SimpleXMLRPCRequestHandler): # Restrict to a particular path.
    rpc_paths = ('/RPC2',)

def serverIdentification() -> tuple:
    serverName = DEFAULT_SERVER_NAME

    try:
        serverPort:int = int(input("Enter server port number: "))
    except:
        print(f"Invalid input. Using default port {DEFAULT_SERVER_PORT}.")
        serverPort:int = DEFAULT_SERVER_PORT
    if serverPort <= MIN_SERVER_PORT_NUMBER or serverPort > MAX_SERVER_PORT_NUMBER:
        serverPort = DEFAULT_SERVER_PORT
    return serverName, serverPort

def serverCreation(serverName:str, serverPort:int):
    with SimpleXMLRPCServer((serverName, serverPort), requestHandler=RequestHandler) as server: # Create server
        server.register_introspection_functions()

        def add(matrix1_list, matrix2_list): # Register a function under a different name
            np_matrix1 = np.array(matrix1_list)
            np_matrix2 = np.array(matrix2_list)
            return np.add(np_matrix1, np_matrix2).tolist()

        def subtract(matrix1_list, matrix2_list):
            np_matrix1 = np.array(matrix1_list)
            np_matrix2 = np.array(matrix2_list)
            return np.subtract(np_matrix1, np_matrix2).tolist()
        
        def multiply(matrix1_list, matrix2_list):
            np_matrix1 = np.array(matrix1_list)
            np_matrix2 = np.array(matrix2_list)
            if np_matrix1.shape[1] != np_matrix2.shape[0]:
                raise ValueError("Number of columns in the first matrix must be equal to the number of rows in the second matrix for multiplication.")
            return np.dot(np_matrix1, np_matrix2).tolist()

        server.register_function(add, 'add')
        server.register_function(subtract, 'subtract')
        server.register_function(multiply, 'multiply')

        print(f"Server is listening on {serverName}:{serverPort}...") # Run the server's main loop
        server.serve_forever()

def main() -> None:
    serverName:str, serverPort:int = serverIdentification()
    serverCreation(serverName, serverPort)

if __name__ == "__main__":
    main()
