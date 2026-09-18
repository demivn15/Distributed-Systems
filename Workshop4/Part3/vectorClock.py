import multiprocessing
import threading
import time
import random
import json
import zmq

# Configuration for the distributed system
NUM_NODES = 3

# Mapping of node IDs to (IP, Port) using ZMQ TCP transport
NODE_CONFIG = {
    0: ("127.0.0.1", 5551),
    1: ("127.0.0.1", 5552),
    2: ("127.0.0.1", 5553),
}

def peer_listener(node_id, port, vector_clock, lock):
    """Background thread using a ZMQ REP socket to listen for incoming messages."""
    context = zmq.Context.instance()
    sock = context.socket(zmq.REP)
    sock.bind(f"tcp://*:{port}")
    
    print(f"[Node {node_id}] ZMQ REP Listener started on port {port}")
    
    while True:
        try:
            # Receive message frame payload
            message_bytes = sock.recv()
            message = json.loads(message_bytes.decode('utf-8'))
            
            sender_id = message['sender_id']
            remote_vc = message['vector_clock']
            payload = message['payload']
            
            with lock:
                # Vector Clock Update Rule on Receive:
                # 1. V_i[k] = max(V_i[k], V_msg[k]) for all k
                for i in range(len(vector_clock)):
                    vector_clock[i] = max(vector_clock[i], remote_vc[i])
                
                # 2. Increment its own component
                vector_clock[node_id] += 1
                
                print(f"\n[Node {node_id}] RECEIVED message from Node {sender_id}: '{payload}'")
                print(f"[Node {node_id}] Updated Vector Clock -> {vector_clock}\n")
            
            # Send acknowledgment reply back to maintain REQ-REP protocol contract
            sock.send(b"ACK")
            
        except Exception as e:
            print(f"[Node {node_id}] Error in listener: {e}")
            break

def peer_process(node_id, peers_config):
    """Main process for each distributed node."""
    vector_clock = [0] * NUM_NODES
    lock = threading.Lock()
    
    my_ip, my_port = peers_config[node_id]
    
    # Start background listener thread
    listener_thread = threading.Thread(
        target=peer_listener, 
        args=(node_id, my_port, vector_clock, lock), 
        daemon=True
    )
    listener_thread.start()
    
    # ZMQ Context and REQ socket for sending messages to peers
    context = zmq.Context()
    sock = context.socket(zmq.REQ)
    
    # Allow time for listeners to bind successfully
    time.sleep(1)
    
    cycle = 0
    while cycle < 5:  # Simulation cycles
        time.sleep(random.uniform(2, 4))
        
        with lock:
            action = random.choice(['internal', 'send'])
            
            if action == 'internal':
                # Rule for internal event: increment own vector clock component
                vector_clock[node_id] += 1
                print(f"[Node {node_id}] INTERNAL EVENT. Vector Clock -> {vector_clock}")
            else:
                # Pick a random peer to send a message to
                other_nodes = [nid for nid in peers_config.keys() if nid != node_id]
                target_id = random.choice(other_nodes)
                target_ip, target_port = peers_config[target_id]
                
                # Rule for sending a message: increment own component before dispatching
                vector_clock[node_id] += 1
                
                message = {
                    'sender_id': node_id,
                    'vector_clock': list(vector_clock),
                    'payload': f"Hello via ZMQ from Node {node_id} (Cycle {cycle})"
                }
                
                try:
                    # Connect dynamically to the target node's REQ-REP endpoint
                    target_endpoint = f"tcp://{target_ip}:{target_port}"
                    sock.connect(target_endpoint)
                    
                    sock.send(json.dumps(message).encode('utf-8'))
                    _ = sock.recv()  # Block until ACK is received
                    
                    print(f"[Node {node_id}] SENT message to Node {target_id}. Vector Clock -> {vector_clock}")
                    
                    # Disconnect so we can safely reconnect to other peers in future iterations
                    sock.disconnect(target_endpoint)
                except Exception as e:
                    print(f"[Node {node_id}] Failed to send message via ZMQ: {e}")
                    
        cycle += 1

if __name__ == '__main__':
    print("Starting Vector Clock Distributed System Simulation with ZeroMQ...")
    processes = []
    
    # Spawn a multiprocessing process for each node
    for node_id in NODE_CONFIG.keys():
        p = multiprocessing.Process(target=peer_process, args=(node_id, NODE_CONFIG))
        processes.append(p)
        p.start()
        
    try:
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        print("\nStopping all nodes...")
        for p in processes:
            p.terminate()