#include <stdio.h>

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
