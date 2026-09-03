M = 5
RING_SIZE = 2 ** M
nodes = [1, 4, 9, 11, 14, 18, 20, 21, 28]
def successor(key):
 for node in nodes:
 if node >= key:
 return node
 return nodes[0]
for key in [3, 8, 12, 19, 26, 30]:
 print(
 "Key:", key,
 "-> node:", successor(key)
 )
