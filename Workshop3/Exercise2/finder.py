import socket

<<<<<<< HEAD
ENTITY_ID = "Demian-Student"
=======
ENTITY_ID = "Demian"
>>>>>>> 2785ff4fad33e0bbacb981a41a6026fa2df400b0
PORT = 50000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.settimeout(3)
<<<<<<< HEAD
sock.sendto( ENTITY_ID.encode(), ("172.23.255.255", PORT))
=======
sock.sendto( ENTITY_ID.encode(), ("255.255.255.255", PORT))
>>>>>>> 2785ff4fad33e0bbacb981a41a6026fa2df400b0

def main():
    try:
        data, addr = sock.recvfrom(1024)
        print("Entity found:", data.decode())
    except socket.timeout:
        print("Entity not found")

if __name__ == "__main__":
    main()
