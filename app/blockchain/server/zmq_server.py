import datetime
import random

import zmq
import threading
import json
import os
import time
import blockchain as chain

_basepath = os.path.abspath(os.path.dirname(__file__))
conf = json.load(open(os.path.abspath(os.path.dirname(__file__)) + "\\config.json"))

lock = threading.Lock()


def build_msg(cmd, msg):
    data = {
        "cmd": cmd,
        "msg": msg
    }
    return data


class ZmqServer(object):
    def __init__(self):
        self.server = conf["server"]
        self.calc_port = conf["calc_port"]
        self.add_port = conf["add_port"]
        self.signal_port = conf["signal_port"]
        self.client_num = conf["client_num"]
        self.chain = chain.BlockChain()
        print("服务器初始化的链id:%s" % id(self.chain))
        self.ops_list = []
        self.uncalc_ops = []
        self.proof_list = []

    def add_ops(self, option):
        with lock:
            self.ops_list.append(option)

    def publish_calc_task(self):
        while True:

            self.uncalc_ops = list(self.ops_list)
            print("未计算的缓存操作列表：%s"%self.uncalc_ops)
            print("待计算的操作列表：%s"%self.ops_list)
            if len(self.uncalc_ops) > 0:
                thread = threading.Thread(target=self.publish_topic,
                                          args=("calc_task", self.uncalc_ops, self.calc_port),
                                          name="calc_task")
                thread.start()
            time.sleep(15)

    def publish_add_task(self, proof):

        pub_data = {
            "data": list(self.uncalc_ops),
            "proof": proof,
            "index": len(self.chain.chain) + 1
        }
        print("即将发布新块:%s" % pub_data)
        self.ops_list.clear()
        self.chain.new_block(pub_data["data"], pub_data["proof"])
        thread = threading.Thread(target=self.publish_topic, args=("add_task", pub_data, self.add_port),
                                  name="add_task")
        thread.start()

    def check_proofs(self, proof):

        with lock:
            self.proof_list.append(proof)
            temp = list(self.proof_list)
            print("收到的证明列表：%s" % temp)
            if len(temp) == self.client_num:
                max_proof = max(temp, key=temp.count)
                print("占大多数的证明：%s" % max_proof)
                self.publish_add_task(proof)
                self.proof_list.clear()

    def publish_topic(self, topic, topic_data, port):
        context = zmq.Context()
        publisher = context.socket(zmq.PUB)
        try:
            publisher.bind("tcp://{}:{}".format(self.server, port))
            print("publish_topic：bind:[%s]:%s" % (self.server, port))
        except zmq.ZMQError as e:
            print("publish_topic：bindfailed:[%s]:%s" % (e, port))

        data_string = json.dumps(topic_data, sort_keys=True)
        print("publish_topic：send:[%s]:%s" % (topic, data_string))
        i = 0
        while True:
            publisher.send_multipart([bytes(topic, "utf-8"), bytes(data_string, 'utf-8')])
            time.sleep(2)
            i += 1
            if i == 2:
                print("publish_topic：finished")
                break

        publisher.close()
        context.term()

    def listen_msg(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://{}:{}".format(self.server, self.signal_port))

        while True:
            message = socket.recv()
            message_dict = json.loads(message)
            print("Received: %s" % json.dumps(message_dict))

            if message_dict["cmd"] == "new_proof":
                self.check_proofs(message_dict["msg"])
                response_string = json.dumps(build_msg("accept_proof", ""))
                socket.send(bytes(response_string, encoding="utf-8"))
            elif message_dict["cmd"] == "need_chain":
                data_dict = build_msg("new_chain", self.chain.full_chain())
                data_string = json.dumps(data_dict)
                socket.send(bytes(data_string, encoding="utf-8"))
            elif message_dict["cmd"] == "new_ops":
                self.add_ops(message_dict["msg"])
                response_string = json.dumps(build_msg("accept_ops", ""))
                socket.send(bytes(response_string, encoding="utf-8"))


    def add_fake_data(self):
        while True:
            data = (
                {
                    "id": random.randint(0, 9),
                    "operator": "operator",
                    "option": "option",
                    "commodity": "commodity",
                    "time": get_current_time()
                }
            )
            self.add_ops(data)
            time.sleep(9)


def get_current_time(frm="%Y-%m-%d %H:%M:%S"):
    dt = datetime.datetime.now()
    return dt.strftime(frm)


if __name__ == '__main__':
    server = ZmqServer()

    # add_fake_thread = threading.Thread(target=server.add_fake_data, name="客户端消息监听")
    # add_fake_thread.start()

    publish_calc_task_thread = threading.Thread(target=server.publish_calc_task, name="客户端消息监听")
    publish_calc_task_thread.start()
    listen_thread = threading.Thread(target=server.listen_msg, name="客户端消息监听")
    listen_thread.start()
