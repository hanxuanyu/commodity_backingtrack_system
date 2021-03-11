from application import app
from flask import request, g, make_response, redirect
from common.models.user import User
from common.lib.UserService import UserService
from common.lib.Helper import ops_render
from common.lib.UrlManager import UrlManager


@app.before_request
def before_request():
    # 当用户未登录时，在列表中的请求将被重定向到登录界面
    filter_list = [
        "/",
        "/commodity/add",
        "/commodity/del",
        "/commodity/buy",
        "/commodity/send",
        "/commodity/trans",
        "/commodity/warehouse",
        "/commodity/distribution",
        "/commodity/sale"
    ]
    app.logger.info("--------before_request:%s--------" % (request.path))

    user_info = check_login()
    g.current_user = None
    app.logger.info("user_info:%s" % user_info)
    if user_info:
        g.current_user = user_info
        app.logger.info("current_user:%s" % g.current_user)
    if g.current_user is None:
        # 用户未登录
        app.logger.info("current_user is null,进行重定向")
        if request.path in filter_list:
            # 拦截普通请求
            response = make_response(redirect(UrlManager.build_url("/member/login")))
            response.delete_cookie(app.config["AUTH_COOKIE_NAME"])
            return response

    return


@app.after_request
def after_request(response):
    app.logger.info("--------after_request--------")
    return response


'''
判断用户是否登录
'''


def check_login():
    cookies = request.cookies
    cookie_name = app.config["AUTH_COOKIE_NAME"]
    auth_cookie = cookies[cookie_name] if cookie_name in cookies else None
    if auth_cookie is None:
        return False
    auth_info = auth_cookie.split("#")
    if len(auth_info) != 2:
        return False
    try:
        user_info = User.query.filter_by(id=auth_info[1]).first()
    except Exception:
        return False

    if user_info is None:
        return False

    if auth_info[0] != UserService.gene_auth_code(user_info):
        return False

    return user_info
