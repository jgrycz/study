import zmq


ctx = zmq.Context()
socket = ctx.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
socket.setsockopt_string(zmq.SUBSCRIBE, "Achtung")
socket.setsockopt_string(zmq.SUBSCRIBE, "Stefan")

while True:
    print(socket.recv_string())
