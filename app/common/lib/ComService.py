from flask import g
import threading
from application import db
from common.lib.DataHelper import get_current_time
from common.models.user import User
from common.models.operation import Operation
from common.models.commodity import Commodity
from common.lib.ChainServerHelper import send_message


class ComService(object):
    @staticmethod
    def do_ops(userid, comid, ops):
        model_ops = Operation()
        model_ops.user_id = userid
        model_ops.type = ops
        model_ops.commodity_id = comid
        model_ops.date = get_current_time()
        db.session.add(model_ops)
        db.session.commit()
        data = (
            {
                "operator": userid,
                "option": ops,
                "commodity": comid,
                "time": get_current_time()
            }
        )

        threading.Thread(target=send_message, args=("new_ops", data)).start()

    @staticmethod
    def find_com_by_id(comid):
        model_com = Commodity.query.filter_by(id=comid).first()
        return model_com

    @staticmethod
    def delete_com(comid):
        model_com = Commodity.query.filter_by(id=comid).first()
        db.session.delete(model_com)
        db.session.commit()
