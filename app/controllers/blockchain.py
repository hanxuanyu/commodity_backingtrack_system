from flask import Blueprint, request, jsonify
from common.lib.Helper import ops_render
import json
from common.lib.ChainServerHelper import send_message
from common.models.commodity import Commodity
from common.lib.ComService import ComService
from common.models.user import User

block_chain_page = Blueprint("block_chain_page", __name__)


@block_chain_page.route("/info", methods=["GET"])
def info():
    response = send_message("need_chain", "")
    data_dict = json.loads(response)
    req = request.values
    com_id = req["comid"] if "comid" in req else ""
    current_com = ComService.find_com_by_id(com_id)
    ops_list = []
    content = {"ops_list": [],"current_com":current_com}
    chain_data = data_dict["msg"] if "msg" in data_dict else None

    if chain_data:
        chain_list = chain_data["chain"] if "chain" in chain_data else []
        for block in chain_list:
            if not block["index"] == 1:
                content_list = block["content"]
                for ops in content_list:
                    if int(ops["commodity"]) == int(com_id):
                        ops_list.append(ops)

    for ops in ops_list:
        user = User.query.filter_by(id=ops["operator"]).first()
        data = {
            "operator": user.name,
            "option": ops["option"],
            "time": ops["time"]
        }
        content["ops_list"].append(data)

    return ops_render("/blockchain/info.html",content)
