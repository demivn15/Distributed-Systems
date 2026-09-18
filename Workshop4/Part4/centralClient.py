import zmq
import time
import sys
import random

# Change SERVER_IP to the actual IP of the machine running centralServer.py
SERVER_IP = "127.23.207.8"
SERVER_PORT = 6000

def run_client(client_id):
    context = zmq.Context()
    sock = context.socket(zmq.REQ)
    sock.connect(f"tcp://{SERVER_IP}:{SERVER_PORT}")
    
    for i in range(3): # Perform 3 access cycles
        time.sleep(random.uniform(2, 5))
        
        # 1. Request access
        print(f"[Client {client_id}] Requesting access to shared resource...")
        sock.send_json({"client_id": client_id, "action": "REQUEST"})
        response = sock.recv_json()
        
        if response.get("status") == "GRANTED":
            print(f"[Client {client_id}] -> ENTERED Critical Section (Using shared resource).")
            time.sleep(2) # Simulate work with the shared resource
            
            # 2. Release resource
            print(f"[Client {client_id}] Leaving Critical Section. Releasing resource...")
            sock.send_json({"client_id": client_id, "action": "RELEASE"})
            _ = sock.recv_json()
            print(f"[Client {client_id}] Resource successfully released.\n")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python centralClient.py <client_id>")
        sys.exit(1)
        
    cid = sys.argv[1]
    run_client(cid)