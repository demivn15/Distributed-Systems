import zmq
import ldap

LDAP_SERVER = "ldap://localhost"

def queryServiceFromLDAP(serviceNameInput: str) -> str:
    serviceName: str = serviceNameInput
    baseDN: str = "ou=People,dc=alejandroydemian,dc=com"
    searchFilter: str = f"(cn={serviceName})"
    
    try:
        conn = ldap.initialize(LDAP_SERVER)
        conn.simple_bind_s("cn=admin,dc=alejandroydemian,dc=com", "password123") # Replace with your actual password if different
        
        result = conn.search_s(baseDN, ldap.SCOPE_SUBTREE, searchFilter, ['description'])
        conn.unbind_s()
        
        if result:
            dn, attrs = result[0]
            if 'description' in attrs:
                uri = attrs['description'][0].decode('utf-8')
                return uri
    except Exception as error:
        print(f"LDAP Query Error: {error}")
    
    return ""

def main() -> None:
    context = zmq.Context()
    s = context.socket(zmq.SUB)

    temas_input = input("Ingresa los servicios a buscar y suscribirse (separados por coma, ej. FITNESS,NUTRITION): ").strip()
    if not temas_input:
        temas = ["FITNESS", "NUTRITION"]
    else:
        temas = [t.strip().upper() for t in temas_input.split(",")]

    for tema in temas:
        print(f"\nConsultando LDAP para el servicio: {tema}")
        uri = queryServiceFromLDAP(tema)
        if uri:
            print(f"Servicio '{tema}' encontrado en LDAP: {uri}")
            print(f"Conectando al publicador en {uri}...")
            s.connect(uri)
            s.setsockopt_string(zmq.SUBSCRIBE, tema)
        else:
            print(f"Servicio '{tema}' no encontrado en LDAP.")

    print("\nEsperando mensajes de los publicadores (Presiona Ctrl+C para salir)...")

    try:
        while True:
            mensaje_recibido = s.recv().decode("utf-8")
            print(f"Recibido: {mensaje_recibido}")
    except KeyboardInterrupt:
        print("\nSuscriptor desconectado.")

if __name__ == "__main__":
    main()
