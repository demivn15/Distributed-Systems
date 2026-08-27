from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

DEFAULT_SERVER_NAME:str = "localhost"
DEFAULT_SERVER_PORT:int = 12000
MIN_SERVER_PORT_NUMBER:int = 0
MAX_SERVER_PORT_NUMBER:int = 62235

class RequestHandler(SimpleXMLRPCRequestHandler): # Restrict to a particular path.
    rpc_paths = ('/RPC2',)

serverName:str = input("Enter server hostname or IP address: ")
if not serverName:
    serverName:str = DEFAULT_SERVER_NAME
try:
    serverPort:int = int(input("Enter server port number: "))
except:
    print(f"Invalid input. Using default port {DEFAULT_SERVER_PORT}.")
    serverPort:int = DEFAULT_SERVER_PORT

if serverPort <= MIN_SERVER_PORT_NUMBER or serverPort > MAX_SERVER_PORT_NUMBER:
    serverPort = DEFAULT_SERVER_PORT

with SimpleXMLRPCServer((serverName, serverPort), requestHandler=RequestHandler) as server: # Create server
    server.register_introspection_functions()
    def add(x, y): # Register a function under a different name
        return x + y

    server.register_function(add, 'add')

    print(f"Server is listening on {serverName}:{serverPort}...") # Run the server's main loop
    server.serve_forever()

