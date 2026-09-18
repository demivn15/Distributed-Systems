import zmq
import time
import sys
import random

# Replace with the actual local IP address of your Linux server
SERVER_IP = "172.23.207.8"
SERVER_PORT = 6000

def run_client(client_id):
    context = zmq.Context()
    sock = context.socket(zmq.REQ)
    
    target_endpoint = f"tcp://{SERVER_IP}:{SERVER_PORT}"
    print(f"[Client {client_id}] Connecting to server at {target_endpoint}...")
    sock.connect(target_endpoint)
    
    # Give ZeroMQ a brief moment to finish the asynchronous TCP connection handshake
    time.sleep(1)
    
    while True: # Continuous loop until interrupted
        time.sleep(random.uniform(2, 4))
        
        try:
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
                
        except Exception as e:
            print(f"[Client {client_id}] Communication error: {e}")
            break

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python centralClientZmq.py <client_id>")
        sys.exit(1)
        
    cid = sys.argv[1]
    
    try:
        run_client(cid)
    except KeyboardInterrupt:
        print(f"\n[Client {cid}] Interrupted by user (Ctrl+C). Shutting down gracefully...")
        sys.exit(0)