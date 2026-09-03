M = 5
RING_SIZE = 2 ** M
nodes = [1, 4, 9, 11, 14, 18, 20, 21, 28]

def successor(key):
    for node in nodes:
         if node >= key:
             return node
    return nodes[0]

def finger_table(node):
    table = []
    for i in range(M):
        start = (node + 2**i) % RING_SIZE
        target = successor(start)
        table.append((i + 1, start, target))
    return table

def lookup(starting_node, goal_node):
    print(f"Resolve key {goal_node} starting at node {starting_node}")
    hops = 0
    while True:
        print(current)
        
        imm_succ = successor(current + 1)
        
        # Calculate circular distances
        dist_to_key = (key - current) % RING_SIZE
        dist_to_succ = (imm_succ - current) % RING_SIZE
        
        # If the key falls between the current node and its immediate successor
        if 0 < dist_to_key <= dist_to_succ:
            print(f"-> successor({key}) = {imm_succ}")
            hops += 1
            print(f"Total hops = {hops}")
            break
            
        # Otherwise, search the finger table for the furthest node before the key
        ft = finger_table(current)
        next_node = current
        max_dist = 0
        
        for entry in ft:
            target = entry[2]
            dist_to_target = (target - current) % RING_SIZE
            
            # Check if the target is strictly between current and key
            if 0 < dist_to_target < dist_to_key:
                if dist_to_target > max_dist:
                    max_dist = dist_to_target
                    next_node = target
                    
        # Fallback to immediate successor if no valid finger is found
        if next_node == current:
            next_node = imm_succ
            
        print("-> ", end="")
        current = next_node
        hops += 1

def main():
    print(f"i \t start \t successor")
    print(f"--------------------------")
    for entry in finger_table(1):
        print(f"{entry[0]} \t {entry[1]} \t {entry[2]}")

if __name__ == "__main__":
    main()
