from flask import Blueprint, jsonify, request, g
from common.models.commodity import Commodity
from common.lib.DataHelper import get_current_time
from application import db
from common.models.user import User
from common.models.operation import Operation
from common.lib.ComService import ComService

from common.lib.Helper import ops_renderJSON, ops_renderErrJSON, ops_render

com_page = Blueprint("com_page", __name__)


@com_page.route("/add", methods=["POST"])
def add():
    req = request.values
    name = req["name"] if "name" in req else ""
    origin = req["origin"] if "origin" in req else ""

    if name is None or len(name) < 1:
        return ops_renderErrJSON(msg="请输入正确的商品名")
    if origin is None or len(origin) < 1:
        return ops_renderErrJSON(msg="请输入正确的产地")

    model_com = Commodity()

    model_com.name = name
    model_com.origin = origin
    model_com.status = "出售中"
    model_com.seller = g.current_user.id
    db.session.add(model_com)
    db.session.commit()

    com_info = Commodity.query.order_by(Commodity.id.desc()).filter_by(name=name).first()
    ComService.do_ops(g.current_user.id, com_info.id, "上架")
    return ops_renderJSON(msg="上架成功")


@com_page.route("/del", methods=["POST"])
def del_com():
    req = request.values
    com_id = req["id"] if "id" in req else ""
    com = ComService.find_com_by_id(com_id)
    if g.current_user.type not in ["经销商"] and com.seller != g.current_user.id:
        return ops_renderErrJSON("您无权执行此操作")
    if com is None:
        return ops_renderErrJSON(msg="该商品不存在")
    if com.status not in ["出售中"]:
        return ops_renderErrJSON(msg="只能下架销售中的商品")

    ComService.delete_com(com_id)
    ComService.do_ops(g.current_user.id, com_id, "下架")
    return ops_renderJSON(msg="下架成功")


@com_page.route("/buy", methods=["POST"])
def buy_com():
    req = request.values
    com_id = req["id"] if "id" in req else ""
    com = ComService.find_com_by_id(com_id)
    if g.current_user.type not in ["超市管理员"]:
        return ops_renderErrJSON("您无权执行此操作")
    if com is None:
        return ops_renderErrJSON(msg="该商品不存在")
    if com.status not in ["出售中"]:
        return ops_renderErrJSON(msg="商品已被购买")

    com.status = "待发货"
    com.buyer = g.current_user.id
    db.session.commit()
    ComService.do_ops(g.current_user.id, com_id, "下单")
    return ops_renderJSON(msg="下单成功")


@com_page.route("/send", methods=["POST"])
def send_com():
    req = request.values
    com_id = req["id"] if "id" in req else ""
    com = ComService.find_com_by_id(com_id)
    if g.current_user.type not in ["经销商"] and com.seller != g.current_user.id:
        return ops_renderErrJSON("您无权执行此操作")
    if com is None:
        return ops_renderErrJSON(msg="该商品不存在")
    if com.status not in ["待发货"]:
        return ops_renderErrJSON(msg="只能发货已下单的商品")
    com.status = "已发货"
    db.session.commit()
    ComService.do_ops(g.current_user.id, com_id, "发货")
    return ops_renderJSON(msg="发货成功")


@com_page.route("/trans", methods=["POST"])
def trans_com():
    req = request.values
    com_id = req["id"] if "id" in req else ""
    com = ComService.find_com_by_id(com_id)
    if g.current_user.type not in ["运输商"]:
        return ops_renderErrJSON("您无权执行此操作")
    if com is None:
        return ops_renderErrJSON(msg="该商品不存在")
    if com.status not in ["已发货"]:
        return ops_renderErrJSON(msg="只能运输已发货的商品")
    com.status = "运输中"
    com.trans = g.current_user.id
    db.session.commit()
    ComService.do_ops(g.current_user.id, com_id, "运输")
    return ops_renderJSON(msg="运输成功")


@com_page.route("/warehouse", methods=["POST"])
def warehouse_com():
    req = request.values
    com_id = req["id"] if "id" in req else ""
    com = ComService.find_com_by_id(com_id)
    if g.current_user.type not in ["仓库管理员"]:
        return ops_renderErrJSON("您无权执行此操作")
    if com is None:
        return ops_renderErrJSON(msg="该商品不存在")
    if com.status not in ["运输中"]:
        return ops_renderErrJSON(msg="只能入库运输中的商品")
    com.status = "已入库"
    com.warehouse = g.current_user.id
    db.session.commit()
    ComService.do_ops(g.current_user.id, com_id, "入库")
    return ops_renderJSON(msg="入库成功")


@com_page.route("/distribution", methods=["POST"])
def distribution_com():
    req = request.values
    com_id = req["id"] if "id" in req else ""
    com = ComService.find_com_by_id(com_id)
    if g.current_user.type not in ["仓库管理员"]  and com.warehouse != g.current_user.id:
        return ops_renderErrJSON("您无权执行此操作")
    if com is None:
        return ops_renderErrJSON(msg="该商品不存在")
    if com.status not in ["已入库"]:
        return ops_renderErrJSON(msg="只能分发已入库的商品")
    com.status = "已分发"
    com.warehouse = g.current_user.id
    db.session.commit()
    ComService.do_ops(g.current_user.id, com_id, "分发")
    return ops_renderJSON(msg="分发成功")


@com_page.route("/sale", methods=["POST"])
def sale_com():
    req = request.values
    com_id = req["id"] if "id" in req else ""
    com = ComService.find_com_by_id(com_id)
    if g.current_user.type not in ["超市管理员"] and com.buyer != g.current_user.id:
        return ops_renderErrJSON("您无权执行此操作")
    if com is None:
        return ops_renderErrJSON(msg="该商品不存在")
    if com.status not in ["已分发"]:
        return ops_renderErrJSON(msg="只能销售已分发的商品")
    com.status = "已销售"
    db.session.commit()
    ComService.do_ops(g.current_user.id, com_id, "销售")
    return ops_renderJSON(msg="销售成功")
