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
        print(starting_node, end="")
        imm_succ = successor(starting_node + 1)
        dist_to_goal_node = (goal_node - starting_node) % RING_SIZE
        dist_to_succ = (imm_succ - starting_node) % RING_SIZE
        if 0 < dist_to_goal_node <= dist_to_succ:
            print(f" -> successor({goal_node}) = {imm_succ}")
            hops += 1
            print(f"Total hops = {hops}")
            break
        ft = finger_table(starting_node)
        next_node = starting_node
        max_dist = 0
        for entry in ft:
            target = entry[2]
            dist_to_target = (target - starting_node) % RING_SIZE
            if 0 < dist_to_target < dist_to_goal_node:
                if dist_to_target > max_dist:
                    max_dist = dist_to_target
                    next_node = target
        if next_node == starting_node:
            next_node = imm_succ
        print(" -> ", end="")
        starting_node = next_node
        hops += 1

def main():
    lookup(1, 26)
    print()
    lookup(28, 12)

if __name__ == "__main__":
    main()
