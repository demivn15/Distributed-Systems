from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import numpy as np 

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

serverName = input("Enter server hostname or IP address: ")
if not serverName:
    serverName = "localhost"
try:
    serverPort = int(input("Enter server port number: "))
except:
    print("Invalid input. Using default port 12000.")
    serverPort = 12000

if serverPort <= 0 or serverPort > 65535:
    serverPort = 12000

# Create server
with SimpleXMLRPCServer((serverName, serverPort),
                         requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    # Register a function under a different name
    def add(matrix1_list, matrix2_list):

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
        return np.dot(matrix1_list, matrix2_list).tolist()

    
    server.register_function(add, 'add')
    server.register_function(subtract, 'subtract')
    server.register_function(multiply, 'multiply')

    # Run the server's main loop
    print(f"Server is listening on {serverName}:{serverPort}...")
    server.serve_forever()

