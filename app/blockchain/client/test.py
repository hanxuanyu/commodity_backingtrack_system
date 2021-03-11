# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
import json

app = Flask(__name__)


@app.route("/test", methods=["POST"])  # 注意点一：methods=["POST"] 而不是 methods="POST"，必须卸载列表里面，不写methods默认是get请求方式。
def get_method_args():
    req = request.values

    return "收到信息:%s" % (req)


if __name__ == '__main__':
    app_port = 5000
    app.run(host="0.0.0.0", port=app_port, debug=True)
