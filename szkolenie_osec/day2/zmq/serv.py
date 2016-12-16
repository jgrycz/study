import random
import time
import zmq


ctx = zmq.Context()
pub_server = ctx.socket(zmq.PUB)
pub_server.bind("tcp://*:5555")

# pub_server = ctx.socket(zmq.PUB)
# pub_server.bind("tcp://*:5555")

usrs = ['Stefan', 'Kazik', 'Gienek']

count = 0
while True:
    msg = "Achtung {}!".format(count)
    print("Sending:\n\t", msg)
    pub_server.send_string(msg)
    name = random.choice(usrs)
    pub_server.send_string(name+' jak tam?')
    time.sleep(1)
    count += 1
