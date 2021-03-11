import zmq
import threading
import json
import os
from blockchain import BlockChain

_basepath = os.path.abspath(os.path.dirname(__file__))
conf = json.load(open(os.path.abspath(os.path.dirname(__file__)) + "\\config.json"))

lock = threading.Lock()


def build_msg(cmd, msg):
    data = {
        "cmd": cmd,
        "msg": msg
    }
    return data


class ZmqClient:
    def __init__(self):
        self.server = conf["server"]
        self.calc_port = conf["calc_port"]
        self.add_port = conf["add_port"]
        self.signal_port = conf["signal_port"]
        self.blockchain = BlockChain()

    def check_blockchain(self, length):
        if length == len(self.blockchain.chain)+1:
            return True
        else:
            return False

    def add_block_topic(self):
        context = zmq.Context()
        subscriber = context.socket(zmq.SUB)
        subscriber.connect("tcp://{}:{}".format(self.server, self.add_port))
        subscriber.setsockopt(zmq.SUBSCRIBE, b"add_task")
        while True:
            # Read envelope with address
            [topic, contents] = subscriber.recv_multipart()
            print("[%s] %s" % (topic, contents))
            if topic == b"add_task":
                contents_dict = json.loads(contents)
                data = contents_dict["data"]
                with lock:
                    if self.check_blockchain(contents_dict["index"]):
                        self.blockchain.new_block(data, contents_dict["proof"])
                    else:
                        self.send_message(build_msg("need_chain", ""))

    def calc_newblock_topic(self):
        context = zmq.Context()
        subscriber = context.socket(zmq.SUB)
        subscriber.connect("tcp://{}:{}".format(self.server, self.calc_port))
        subscriber.setsockopt(zmq.SUBSCRIBE, b"calc_task")
        while True:
            # Read envelope with address
            [topic, contents] = subscriber.recv_multipart()
            print("[%s] %s" % (topic, contents))
            if topic == b"calc_task":
                data = json.loads(contents)
                with lock:
                    new_proof = self.blockchain.proof_of_work(data)
                    msg = build_msg("new_proof", new_proof)
                    self.send_message(msg)

    def send_message(self, data):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://{}:{}".format(self.server, self.signal_port))
        socket.send(bytes(json.dumps(data), encoding="utf-8"))
        response = socket.recv()
        print("response: %s" % response)
        response_dict = json.loads(response)

        if response_dict["cmd"] == "new_chain":
            print("替换本地区块成功")
            self.blockchain.chain = response_dict["msg"]["chain"]
            self.blockchain.update_file()


if __name__ == '__main__':
    client = ZmqClient()
    # instead of s.sub_newblock(),we use thread fun,avoid locking
    calc_thread = threading.Thread(target=client.calc_newblock_topic, name="calc_thread")
    calc_thread.start()

    add_thread = threading.Thread(target=client.add_block_topic(), name="add_thread")
    add_thread.start()
