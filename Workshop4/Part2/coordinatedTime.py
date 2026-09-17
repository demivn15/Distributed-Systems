import multiprocessing
import socket
import threading
import time
import random

# Configuración de los puertos para simular nodos en la misma máquina
PORTS = [5001, 5002, 5003]
HOST = '127.0.0.1'

def peer_listener(port, shared_time):
    """Hilo en segundo plano que escucha peticiones de tiempo de otros nodos."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, port))
    
    while True:
        data, addr = sock.recvfrom(1024)
        if data.decode() == "REQ_TIME":
            # Cuando otro nodo pide el tiempo, enviamos el reloj lógico actual
            sock.sendto(str(shared_time['clock']).encode(), addr)

def peer_process(peer_id, port, other_ports):
    """Proceso principal de cada nodo."""
    # Inicializamos el reloj del nodo (simulado con el tiempo real de inicio)
    shared_time = {'clock': time.time()}

    # Iniciamos el servidor UDP del nodo en un hilo para no bloquear el proceso principal
    listener = threading.Thread(target=peer_listener, args=(port, shared_time), daemon=True)
    listener.start()

    # Socket para enviar peticiones a los otros nodos
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.5) # Evita quedarse esperando eternamente si un nodo no responde

    k_cycles = 3 # Aplicar deriva y sincronizar cada 3 ciclos
    ciclos_actuales = 0

    while True:
        time.sleep(1) # Simula el paso del tiempo físico
        shared_time['clock'] += 1
        ciclos_actuales += 1

        if ciclos_actuales >= k_cycles:
            # 1. Agregar deriva aleatoria al reloj (simulando imperfecciones de hardware)
            drift = random.uniform(-0.5, 0.5)
            shared_time['clock'] += drift
            print(f"[Nodo {peer_id}] Deriva de {drift:+.3f}s aplicada. Tiempo local: {shared_time['clock']:.3f}")

            # 2. Solicitar tiempo a los demás nodos (Peers)
            collected_times = [shared_time['clock']] # Incluye su propio tiempo
            
            for p in other_ports:
                try:
                    sock.sendto(b"REQ_TIME", (HOST, p))
                    data, _ = sock.recvfrom(1024)
                    collected_times.append(float(data.decode()))
                except socket.timeout:
                    continue # Si falla, continúa con los nodos disponibles

            # 3. Calcular el promedio y ajustar el reloj local
            if len(collected_times) > 1:
                promedio = sum(collected_times) / len(collected_times)
                ajuste = promedio - shared_time['clock']
                shared_time['clock'] = promedio
                
                print(f"[Nodo {peer_id}] Sincronizando con {len(collected_times)-1} pares.")
                print(f"[Nodo {peer_id}] Nuevo tiempo promedio: {promedio:.3f} (Ajuste: {ajuste:+.3f}s)\n")
            
            ciclos_actuales = 0 # Reiniciar contador de ciclos

if __name__ == '__main__':
    procesos = []
    
    # Crear y lanzar un proceso independiente por cada puerto/nodo
    for i, port in enumerate(PORTS):
        other_ports = [p for p in PORTS if p != port]
        p = multiprocessing.Process(target=peer_process, args=(i+1, port, other_ports))
        procesos.append(p)
        p.start()

    try:
        # Mantener el programa principal en ejecución
        for p in procesos:
            p.join()
    except KeyboardInterrupt:
        print("\nDeteniendo todos los procesos...")
        for p in procesos:
            p.terminate()
