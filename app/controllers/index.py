from flask import Blueprint, g
from common.models.user import User
from common.models.commodity import Commodity
from common.lib.Helper import ops_render

index_page = Blueprint("index_page", __name__)


@index_page.route("/")
def index():
    content = {}
    user = g.current_user
    com_list = []
    if user.type == "经销商":
        com_list = Commodity.query.filter(Commodity.status.in_(["出售中", "待发货", "已发货", "运输中", "已入库", "已分发"])).filter_by(
            seller=user.id)
    if user.type == "运输商":
        com_list_base = []
        com_list_custom = []
        com_list_base += Commodity.query.filter(Commodity.status.in_(["已发货"]))
        com_list_custom += Commodity.query.filter(Commodity.status.in_(["运输中", "已入库"])).filter_by(trans=user.id)
        com_list = com_list_custom + com_list_base
    if user.type == "仓库管理员":
        com_list_base = []
        com_list_custom = []
        com_list_base += Commodity.query.filter(Commodity.status.in_(["运输中"]))
        com_list_custom += Commodity.query.filter(Commodity.status.in_(["已入库", "已分发"])).filter_by(warehouse=user.id)
        com_list = com_list_custom + com_list_base
    if user.type == "超市管理员":
        com_list_selling = []
        com_list_buyed = []

        com_list_buyed += Commodity.query.filter(Commodity.status.in_(["待发货", "已发货", "运输中", "已入库", "已分发","已销售"])).filter_by(buyer=user.id)
        com_list_selling += Commodity.query.filter(Commodity.status.in_(["出售中"]))
        com_list = com_list_buyed + com_list_selling
    content["com_list"] = com_list
    return ops_render("index.html", content)
