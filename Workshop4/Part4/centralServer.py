import zmq
import time

SERVER_PORT = 6000

def run_central_server():
    context = zmq.Context()
    sock = context.socket(zmq.REP)
    sock.bind(f"tcp://*:{SERVER_PORT}")
    
    print(f"[Central Server] Running on port {SERVER_PORT}...")
    current_holder = None

    while True:
        try:
            message = sock.recv_json()
            client_id = message['client_id']
            action = message['action']
            
            if action == 'REQUEST':
                print(f"[Server] Client {client_id} requested access to the shared resource.")
                # ZMQ REP-REQ naturally queues incoming requests while servicing the current holder
                sock.send_json({"status": "GRANTED"})
                current_holder = client_id
                print(f"[Server] Access GRANTED to Client {client_id}.")
                
            elif action == 'RELEASE':
                print(f"[Server] Client {client_id} released the shared resource.")
                sock.send_json({"status": "ACK"})
                current_holder = None
                
        except Exception as e:
            print(f"[Server] Error: {e}")
            break

if __name__ == '__main__':
    run_central_server()