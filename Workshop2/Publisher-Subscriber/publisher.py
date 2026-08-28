import zmq, time

DEFAULT_SERVER_NAME = "0.0.0.0"
DEFAULT_SERVER_PORT = 15000
MIN_SERVER_PORT = 0
MAX_SERVER_PORT = 65535

context = zmq.Context()
s = context.socket(zmq.PUB)

serverName = input("Enter server hostname or IP address: ")
if not serverName:
    serverName = DEFAULT_SERVER_NAME
try:
    serverPort = int(input("Enter server port number: "))
except:
    print(f"Invalid input. Using default port {DEFAULT_SERVER_PORT}.")
    serverPort = DEFAULT_SERVER_PORT

if serverPort <= MIN_SERVER_PORT or serverPort > MAX_SERVER_PORT:
    serverPort = DEFAULT_SERVER_PORT

p = "tcp://" + serverName + ":" + str(serverPort)
s.bind(p)

cont = 0
while True:
    time.sleep(5)
    cont += 1
    s.send(("TIME " + time.asctime() + " - Message #" + str(cont)).encode("utf-8"))
