import zmq, time, pickle, sys

context = zmq.Context()

r = context.socket(zmq.PULL)
me = str(sys.argv[1]) if len(sys.argv) > 1 else "Unknown Worker"


serverName = "localhost"
#Change to the Broker's OUTPUT port 
serverPort = 13001

if serverPort <= 0 or serverPort > 65535:
    serverPort = 13001

p = "tcp://" + serverName + ":" + str(serverPort)
r.connect(p)

print(f"Worker {me} connected to Broker at {p}...")

count = 0
try:
    while True:
        work = pickle.loads(r.recv())
        count += 1

        print(f"Worker {me} | received work: {work} | Total processed: {count}")

        time.sleep(work[0] * 0.1)
except KeyboardInterrupt:
    print(f"\nWorker {me} processed a total of {count} tasks. Exiting...")