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

        hops += 1

def main():
    print(f"i \t start \t successor")
    print(f"--------------------------")
    for entry in finger_table(1):
        print(f"{entry[0]} \t {entry[1]} \t {entry[2]}")

if __name__ == "__main__":
    main()
