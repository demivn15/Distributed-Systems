import socket

ENTITY_ID = "Demian-Student"
PORT = 50000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.settimeout(3)
sock.sendto( ENTITY_ID.encode(), ("172.23.255.255", PORT))

def main():
    try:
        data, addr = sock.recvfrom(1024)
        print("Entity found:", data.decode())
    except socket.timeout:
        print("Entity not found")

if __name__ == "__main__":
    main()
