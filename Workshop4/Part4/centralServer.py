import zmq
import time

# Bind to all interfaces so external network clients can connect
SERVER_IP = "0.0.0.0"
SERVER_PORT = 6000

def run_central_server():
    context = zmq.Context()
    sock = context.socket(zmq.REP)
    sock.bind(f"tcp://{SERVER_IP}:{SERVER_PORT}")
    
    print(f"[Central Server] Running and listening on port {SERVER_PORT}...")

    while True:
        try:
            # Receive request from any connected client
            message = sock.recv_json()
            client_id = message['client_id']
            action = message['action']
            
            if action == 'REQUEST':
                print(f"[Server] Client {client_id} requested access to the shared resource.")
                # Respond granting access (ZMQ REP-REQ ensures fair queueing)
                sock.send_json({"status": "GRANTED"})
                print(f"[Server] Access GRANTED to Client {client_id}.")
                
            elif action == 'RELEASE':
                print(f"[Server] Client {client_id} released the shared resource.")
                sock.send_json({"status": "ACK"})
                
        except Exception as e:
            print(f"[Server] Error: {e}")
            break

if __name__ == '__main__':
    run_central_server()