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
    proxy = xmlrpc.client.ServerProxy(f"http://{serverName}:{serverPort}/RPC2")

<<<<<<< HEAD
matrix1 = np.array([[1, 2], [3, 4]])
matrix2 = np.array([[5, 6], [7, 8]])

matrix1_list = matrix1.tolist()
matrix2_list = matrix2.tolist()


#Call the remote method 'add, substract, multiply' matrix
suma_matrix= proxy.add(matrix1_list, matrix2_list)
resta_matrix= proxy.subtract(matrix1_list, matrix2_list)
multiplicacion_matrix= proxy.multiply(matrix1_list, matrix2_list)

print("Matrix 1:")
print(matrix1)
print("Matrix 2:")
print(matrix2)
print("Suma de matrices:")
print(np.array(suma_matrix))
print("Resta de matrices:")
print(np.array(resta_matrix))
print("Multiplicacion de matrices:")
print(np.array(multiplicacion_matrix))


=======
result = proxy.add(8, 3) # Call the remote method 'add'
print("8 + 3 =", result)

def main() -> None:
    createClientProxy()
>>>>>>> d25d9742854c2a7028c55a5f3fa6807a38870ba9
