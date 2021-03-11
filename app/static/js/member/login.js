;
var member_login_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".login_wrap .do-login").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在登录,不要着急哦");
            }

            var name = $(".login_wrap input[name=name]").val();
            var password = $(".login_wrap input[name=password]").val();

            if(name === undefined || name.length < 1){
                common_ops.alert("请输入用户名");
                return;
            }

            if(password === undefined || password.length < 6){
                common_ops.alert("正确的密码");
            }

            btn_target.addClass("disabled");
            $.ajax({
                url: common_ops.buildUrl("/member/login"),
                type: "POST",
                data: {
                    name: name,
                    password: password,
                },
                dataType: "json",
                success: function (res) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code === 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/");
                        };
                    }
                    common_ops.alert(res.msg, callback)
                }
            });
        });
    }

};

$(document).ready(function () {
    member_login_ops.init()
});