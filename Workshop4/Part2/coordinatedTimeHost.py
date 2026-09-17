import multiprocessing
import socket
import threading
import time
import random

# Configuración de Demian
MY_BIND_IP = "0.0.0.0" # Permite escuchar peticiones locales y desde tu PC
PORTS = [5001, 5002]

# Tu configuración (Nodo externo)
HOST_EXTERNAL = "172.23.207.8"
PORT_EXTERNAL = 5003

def peer_listener(port, shared_time):
    """Hilo en segundo plano que escucha peticiones de tiempo de otros nodos."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((MY_BIND_IP, port))
    
    while True:
        data, addr = sock.recvfrom(1024)
        if data.decode() == "REQ_TIME":
            # Cuando otro nodo pide el tiempo, enviamos el reloj lógico actual
            sock.sendto(str(shared_time['clock']).encode(), addr)

def peer_process(peer_id, port, other_ports):
    """Proceso principal de cada nodo."""
    shared_time = {'clock': time.time()}

    listener = threading.Thread(target=peer_listener, args=(port, shared_time), daemon=True)
    listener.start()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.5)

    k_cycles = 3 
    ciclos_actuales = 0

    while True:
        time.sleep(1) 
        shared_time['clock'] += 1
        ciclos_actuales += 1

        if ciclos_actuales >= k_cycles:
            drift = random.uniform(-0.5, 0.5)
            shared_time['clock'] += drift
            print(f"[Nodo {peer_id}] Deriva de {drift:+.3f}s aplicada. Tiempo local: {shared_time['clock']:.3f}")

            collected_times = [shared_time['clock']] 
            
            for ip, p in other_ports:
                try:
                    sock.sendto(b"REQ_TIME", (ip, p))
                    data, _ = sock.recvfrom(1024)
                    collected_times.append(float(data.decode()))
                except socket.timeout:
                    continue 

            if len(collected_times) > 1:
                promedio = sum(collected_times) / len(collected_times)
                ajuste = promedio - shared_time['clock']
                shared_time['clock'] = promedio
                
                print(f"[Nodo {peer_id}] Sincronizando con {len(collected_times)-1} pares.")
                print(f"[Nodo {peer_id}] Nuevo tiempo promedio: {promedio:.3f} (Ajuste: {ajuste:+.3f}s)\n")
            
            ciclos_actuales = 0 

if __name__ == '__main__':
    procesos = []
    
    # Demian levanta sus dos procesos locales
    for i, port in enumerate(PORTS):
        other_local_port = [p for p in PORTS if p != port][0]
        # Destinos: su otro nodo local y tu nodo en Windows
        other_nodes = [
            ('127.0.0.1', other_local_port),
            (HOST_EXTERNAL, PORT_EXTERNAL)
        ]
        
        p = multiprocessing.Process(target=peer_process, args=(i+1, port, other_nodes))
        procesos.append(p)
        p.start()

    try:
        # Mantiene el programa corriendo y une los procesos correctamente
        for p in procesos:
            p.join()
    except KeyboardInterrupt:
        print("\nDeteniendo todos los procesos...")
        for p in procesos:
            p.terminate()