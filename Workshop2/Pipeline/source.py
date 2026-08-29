import zmq
import time
import pickle
import random

context = zmq.Context()

s = context.socket(zmq.PUSH)

serverPort = 13000

p = "tcp://localhost:" + str(serverPort)
s.connect(p)

print(f"Source connected to Broker at {p}")
print("Sending a burst of 10 tasks...\n")

for i in range(10):
    workload = random.randint(1, 100)
    work = (workload, i)

    print("Sending:", work)
    s.send(pickle.dumps(work))
    time.sleep(0.1)

print("All taks sent. Waiting for workers to finish...\n")
