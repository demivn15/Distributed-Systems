import xmlrpc.client
import numpy as np 
# Create a client proxy
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

proxy = xmlrpc.client.ServerProxy(f"http://{serverName}:{serverPort}/RPC2")

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


