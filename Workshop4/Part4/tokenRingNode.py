import zmq
import time
import sys
import json

def run_node(node_id, bind_port, next_node_ip, next_node_port, has_initial_token=False):
    context = zmq.Context()
    
    # REP socket to receive the token from the previous node
    rep_sock = context.socket(zmq.REP)
    rep_sock.bind(f"tcp://*:{bind_port}")
    
    # REQ socket to pass the token to the next node
    req_sock = context.socket(zmq.REQ)
    req_sock.connect(f"tcp://{next_node_ip}:{next_node_port}")
    
    print(f"[Node {node_id}] Listening for token on port {bind_port}...")
    print(f"[Node {node_id}] Will pass token to {next_node_ip}:{next_node_port}")

    # If this node starts with the token, trigger the first cycle
    holding_token = has_initial_token
    
    if holding_token:
        print(f"[Node {node_id}] ---> STARTING with the Token!")
        use_shared_resource(node_id)
        pass_token(node_id, req_sock)
        holding_token = False

    while True:
        try:
            # Wait to receive token message from predecessor
            message_bytes = rep_sock.recv()
            message = json.loads(message_bytes.decode('utf-8'))
            
            print(f"\n[Node {node_id}] Received token from Node {message['sender_id']}.")
            
            # Acknowledge receipt to predecessor
            rep_sock.send_json({"status": "TOKEN_RECEIVED_ACK"})
            
            # Use the shared resource
            use_shared_resource(node_id)
            
            # Pass the token to the next node in the ring
            time.sleep(1)
            pass_token(node_id, req_sock)
            
        except Exception as e:
            print(f"[Node {node_id}] Error in token ring loop: {e}")
            break

def use_shared_resource(node_id):
    print(f"[Node {node_id}] *** ENTERED Critical Section (Using Shared Resource) ***")
    time.sleep(3) # Simulate critical section work
    print(f"[Node {node_id}] *** EXITED Critical Section ***")

def pass_token(node_id, req_sock):
    print(f"[Node {node_id}] Passing token to next node...")
    message = {"sender_id": node_id, "payload": "TOKEN"}
    req_sock.send_json(message)
    _ = req_sock.recv_json() # Wait for acknowledgment from successor
    print(f"[Node {node_id}] Token successfully transferred.")

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Usage: python tokenRingNode.py <node_id> <bind_port> <next_ip> <next_port> [has_token (True/False)]")
        sys.exit(1)
        
    n_id = sys.argv[1]
    b_port = int(sys.argv[2])
    n_ip = sys.argv[3]
    n_port = int(sys.argv[4])
    initial_token = len(sys.argv) > 5 and sys.argv[5].lower() == 'true'
    
    run_node(n_id, b_port, n_ip, n_port, initial_token)