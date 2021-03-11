import zmq, json, threading


def send_message(cmd, msg):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://{}:{}".format("127.0.0.1", "5003"))
    socket.send(bytes(json.dumps(build_msg(cmd, msg)), encoding="utf-8"))
    response = socket.recv()
    print("response: %s" % response)
    return response



def build_msg(cmd, msg):
    data = {
        "cmd": cmd,
        "msg": msg
    }
    return data
