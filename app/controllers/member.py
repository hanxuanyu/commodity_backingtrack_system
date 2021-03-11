from flask import Blueprint, render_template, request, jsonify, make_response, redirect
from common.lib.Helper import ops_renderJSON, ops_renderErrJSON, ops_render
from common.lib.DataHelper import get_current_time
from common.lib.UrlManager import UrlManager
from common.models.user import User
from common.lib.UserService import UserService
from application import db, app

member_page = Blueprint("member_page", __name__)


@member_page.route("/reg", methods=["GET", "POST"])
def reg():
    if request.method == "GET":
        return ops_render("member/reg.html")
    elif request.method == "POST":
        req = request.values
        name = req["name"] if "name" in req else ""
        type = req["type"] if "type" in req else ""
        password = req["password"] if "password" in req else ""
        password2 = req["password2"] if "password2" in req else ""

        if name is None or len(name) < 1:
            return ops_renderErrJSON(msg="请输入正确的用户名")
        if type is None or len(type) < 1:
            return ops_renderErrJSON(msg="请选择正确的类型")

        if password is None or len(password) < 6:
            return ops_renderErrJSON(msg="请输入正确的密码")

        if password2 != password2:
            return ops_renderErrJSON(msg="两次密码不一致")

        user_info = User.query.filter_by(name=name).first()
        if user_info:
            return ops_renderErrJSON(msg="用户名已被注册，请更换用户名重新注册")

        model_user = User()
        model_user.name = name
        model_user.type = type
        model_user.password = UserService.gene_pwd(password)
        model_user.regist_time = get_current_time()
        db.session.add(model_user)
        db.session.commit()
        return ops_renderJSON(msg="注册成功~")


@member_page.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return ops_render("member/login.html")
    elif request.method == "POST":
        req = request.values
        name = req["name"] if "name" in req else ""
        password = req["password"] if "password" in req else ""

        if name is None or len(name) < 1:
            return ops_renderErrJSON(msg="请输入正确的用户名")
        if password is None or len(password) < 6:
            return ops_renderErrJSON(msg="请输入正确的密码")

        user_info = User.query.filter_by(name=name).first()
        if not user_info:
            return ops_renderErrJSON(msg="请输入正确的登录用户名和密码(user not found)")

        if user_info.password != UserService.gene_pwd(password):
            return ops_renderErrJSON(msg="请输入正确的登录用户名和密码(error password)")

        response = make_response(ops_renderJSON(msg="登录成功~"))
        response.set_cookie(app.config["AUTH_COOKIE_NAME"],
                            "%s#%s" % (UserService.gene_auth_code(user_info), user_info.id), 60 * 60 * 24)
        return response


@member_page.route("/logout")
def logout():
    response = make_response(redirect(UrlManager.build_url("/member/login")))
    response.delete_cookie(app.config["AUTH_COOKIE_NAME"])
    return response