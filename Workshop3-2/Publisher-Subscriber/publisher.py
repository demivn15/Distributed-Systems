import zmq
import time
import ldap

DEFAULT_SERVER_NAME = "0.0.0.0"
DEFAULT_SERVER_PORT = 15000
MIN_SERVER_PORT = 0
MAX_SERVER_PORT = 65535
LDAP_SERVER = "ldap://localhost"

def registerServiceInLDAP(serviceNameInput: str, ipInput: str, portInput: int) -> None:
    serviceName: str = serviceNameInput
    ip: str = ipInput
    port: int = portInput
    
    dn: str = f"cn={serviceName},ou=People,dc=alejandroydemian,dc=com"
    uri: str = f"tcp://{ip}:{port}"
    
    adminDN: str = "cn=admin,dc=alejandroydemian,dc=com"
    adminPassword: str = "password123"
    
    try:
        conn = ldap.initialize(LDAP_SERVER)
        conn.simple_bind_s(adminDN, adminPassword)
        
        attrs = [
            ('objectClass', [b'inetOrgPerson']),
            ('cn', [serviceName.encode('utf-8')]),
            ('sn', [serviceName.encode('utf-8')]),
            ('description', [uri.encode('utf-8')])
        ]
        
        try:
            conn.add_s(dn, attrs)
            print(f"Service '{serviceName}' registered successfully in LDAP at {dn}")
        except ldap.ALREADY_EXISTS:
            conn.modify_s(dn, [(ldap.MOD_REPLACE, 'description', [uri.encode('utf-8')])])
            print(f"Service '{serviceName}' updated successfully in LDAP at {dn}")
            
        conn.unbind_s()
    except Exception as error:
        print(f"LDAP Registration Error: {error}")

def main() -> None:
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

    topic = input("Ingresa el servicio a publicar (ej. FITNESS, NUTRITION): ").strip().upper()
    if not topic:
        topic = "GENERAL"

    registerServiceInLDAP(topic, serverName if serverName != "0.0.0.0" else "localhost", serverPort)

    print(f"Publicador iniciado en {p} ofreciendo el servicio '{topic}'...")

    cont = 0
    while True:
        time.sleep(3)
        cont += 1
        
        if topic == "FITNESS":
            mensaje = f"{topic} - Entrenamiento #{cont}: Recordatorio de rutina de 2 horas."
        elif topic == "NUTRITION":
            mensaje = f"{topic} - Comida #{cont}: Menestra de lentejas con atún y plátano verde."
        else:
            mensaje = f"{topic} - Mensaje genérico #{cont}"
            
        s.send(mensaje.encode("utf-8"))

if __name__ == "__main__":
    main()
