from flask import jsonify,g,render_template


def ops_render(template,context = {}):
    if "current_user" in g:
        context["current_user"] = g.current_user
    return render_template(template,**context)

def ops_renderJSON(code=200, msg="操作成功", data=None):
    if data is None:
        data = {}
    resp = {"code": code, "msg": msg, "data": data}
    return jsonify(resp)


def ops_renderErrJSON(msg="出错啦", data=None):
    if data is None:
        data = {}
    return jsonify(code=-1, msg=msg, data=data)
