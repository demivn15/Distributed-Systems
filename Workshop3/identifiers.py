import uuid
import socket
entity_id = uuid.uuid5(uuid.NAMESPACE_DNS, "student-a")
entity = {
 "id": str(entity_id),
 "address": (ip, 5000)
}
print(entity)
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
print("Entity ID :", entity_id)
print("Hostname :", hostname)
print("Address :", ip)
