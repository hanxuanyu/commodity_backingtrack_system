;
var commodiy_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        // 添加按钮
        $(".commodiy_add .add").click(function () {
            var name = $(".commodiy_add input[name=name]").val();
            var origin = $(".commodiy_add input[name=origin]").val();
            if (name === undefined || name.length < 1) {
                common_ops.alert("请输入商品名")
                return
            }

            if (origin === undefined || origin.length < 1) {
                common_ops.alert("请输入商品产地")
                return;
            }


            $.ajax({
                url: common_ops.buildUrl("/commodity/add"),
                type: "POST",
                data: {
                    name: name,
                    origin: origin,
                },
                dataType: "json",
                success: function (res) {
                    var callback = null;
                    if (res.code === 200) {
                        $('#addModal').modal('hide')
                        callback = function () {
                            window.location.reload()
                        }
                    }
                    common_ops.alert(res.msg, callback)
                }
            });

        });
        // 刷新按钮
        $("#refresh_com").click(function () {
            window.location.reload()
        });
        //下架按钮
        $(".com_ops_del").click(function () {
            var btn_ops = $(this);
            var com_id = btn_ops.parent().attr("id");
            common_ops.alert("您确定要下架该商品吗?", function () {
                $.ajax({
                    url: common_ops.buildUrl("/commodity/del"),
                    type: "POST",
                    data: {
                        id: com_id.substring(7)
                    },
                    dataType: "json",
                    success: function (res) {
                        var callback = null;
                        callback = function () {
                            window.location.reload()
                        }
                        if (res.code === 200) {
                            window.location.reload()
                        } else {
                            common_ops.alert(res.msg, callback);
                        }
                    }
                });
            });
        });

        //下单按钮
        $(".com_ops_buy").click(function () {
            var btn_ops = $(this);
            var com_id = btn_ops.parent().attr("id");
            common_ops.alert("您确定要购买该商品吗?", function () {
                $.ajax({
                    url: common_ops.buildUrl("/commodity/buy"),
                    type: "POST",
                    data: {
                        id: com_id.substring(7)
                    },
                    dataType: "json",
                    success: function (res) {
                        var callback = null;
                        callback = function () {
                            window.location.reload()
                        }
                        if (res.code === 200) {
                            window.location.reload()
                        } else {
                            common_ops.alert(res.msg, callback);
                        }

                    }
                });
            });
        });
        //发货按钮
        $(".com_ops_send").click(function () {
            var btn_ops = $(this);
            var com_id = btn_ops.parent().attr("id");
            common_ops.alert("您确定要发货该商品吗?", function () {
                $.ajax({
                    url: common_ops.buildUrl("/commodity/send"),
                    type: "POST",
                    data: {
                        id: com_id.substring(7)
                    },
                    dataType: "json",
                    success: function (res) {
                        var callback = null;
                        callback = function () {
                            window.location.reload()
                        }
                        if (res.code === 200) {
                            window.location.reload()
                        } else {
                            common_ops.alert(res.msg, callback);
                        }
                    }
                });
            });
        });
        // 运输按钮
        $(".com_ops_trans").click(function () {
            var btn_ops = $(this);
            var com_id = btn_ops.parent().attr("id");
            common_ops.alert("您确定要运输该商品吗?", function () {
                $.ajax({
                    url: common_ops.buildUrl("/commodity/trans"),
                    type: "POST",
                    data: {
                        id: com_id.substring(7)
                    },
                    dataType: "json",
                    success: function (res) {
                        var callback = null;
                        callback = function () {
                            window.location.reload()
                        }
                        if (res.code === 200) {
                            window.location.reload()
                        } else {
                            common_ops.alert(res.msg, callback);
                        }
                    }
                });
            });
        });
        // 入库按钮
        $(".com_ops_warehouse").click(function () {
            var btn_ops = $(this);
            var com_id = btn_ops.parent().attr("id");
            common_ops.alert("您确定要入库该商品吗?", function () {
                $.ajax({
                    url: common_ops.buildUrl("/commodity/warehouse"),
                    type: "POST",
                    data: {
                        id: com_id.substring(7)
                    },
                    dataType: "json",
                    success: function (res) {
                        var callback = null;
                        callback = function () {
                            window.location.reload()
                        }
                        if (res.code === 200) {
                            window.location.reload()
                        } else {
                            common_ops.alert(res.msg, callback);
                        }
                    }
                });
            });
        });
        // 分发按钮
        $(".com_ops_distribution").click(function () {
            var btn_ops = $(this);
            var com_id = btn_ops.parent().attr("id");
            common_ops.alert("您确定要分发该商品吗?", function () {
                $.ajax({
                    url: common_ops.buildUrl("/commodity/distribution"),
                    type: "POST",
                    data: {
                        id: com_id.substring(7)
                    },
                    dataType: "json",
                    success: function (res) {
                        var callback = null;
                        callback = function () {
                            window.location.reload()
                        }
                        if (res.code === 200) {
                            window.location.reload()
                        } else {
                            common_ops.alert(res.msg, callback);
                        }
                    }
                });
            });
        });
        // 销售按钮
        $(".com_ops_sale").click(function () {
            var btn_ops = $(this);
            var com_id = btn_ops.parent().attr("id");
            common_ops.alert("您确定要销售该商品吗?", function () {
                $.ajax({
                    url: common_ops.buildUrl("/commodity/sale"),
                    type: "POST",
                    data: {
                        id: com_id.substring(7)
                    },
                    dataType: "json",
                    success: function (res) {
                        var callback = null;
                        callback = function () {
                            window.location.reload()
                        }
                        if (res.code === 200) {
                            window.location.reload()
                        } else {
                            common_ops.alert(res.msg, callback);
                        }
                    }
                });
            });
        });
    }

};

$(document).ready(function () {
    commodiy_ops.init()
})