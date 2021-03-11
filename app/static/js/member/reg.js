;
const member_reg_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".reg_wrap .do-reg").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理，请不要重复点击");
                return;
            }
            var name = $(".reg_wrap input[name=name]").val();
            var type = $(".reg_wrap .active input[name=type]").val();
            var password = $(".reg_wrap input[name=password]").val();
            var password2 = $(".reg_wrap input[name=password2]").val();

            if (name === undefined || name.length < 1) {
                common_ops.alert("请输入正确的用户名");
                return;
            }
            if (type === undefined){
                common_ops.alert("请选择用户类型");
                return;
            }

            if (password === undefined || password.length < 6) {
                common_ops.alert("请输入正确的密码，不可小于6个字符");
                return;
            }

            if (password2 === undefined || password2 !== password) {
                common_ops.alert("两次密码输入不一致");
                return;
            }


            btn_target.addClass("disabled")

            $.ajax({
                url: common_ops.buildUrl("/member/reg"),
                type: "POST",
                data: {
                    name: name,
                    type: type,
                    password: password,
                    password2: password2

                },
                dataType: "json",
                success: function (res) {
                    btn_target.removeClass("disabled")
                    var callback = null;
                    if (res.code === 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/member/login");
                        }
                    }
                    common_ops.alert(res.msg, callback)
                }
            });

        });
    },
};

$(document).ready(function () {
    member_reg_ops.init();

});