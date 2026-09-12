import uuid
import socket

entity_id = uuid.uuid5(uuid.NAMESPACE_DNS, "student-a")
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

entity = {
 "id": str(entity_id),
 "address": (ip, 5000)
}

entity["address"] = (ip, 6000)

def main():
    print("Entity ID :", entity_id)
    print("Hostname :", hostname)
    print("Address :", ip)
    print(entity)

if __name__ == "__main__":
    main()
