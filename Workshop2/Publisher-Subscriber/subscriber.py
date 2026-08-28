import zmq

DEFAULT_SERVER_NAME = "0.0.0.0"
DEFAULT_SERVER_PORT = 15000
MIN_SERVER_PORT = 0
MAX_SERVER_PORT = 65535

context = zmq.Context()
s = context.socket(zmq.SUB)

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
s.connect(p)

s.setsockopt_string(zmq.SUBSCRIBE, "TIME")

for i in range(5):
    time = s.recv().decode("utf-8")
    print(time)

