;
var common_ops = {
    buildUrl: function (path, params) {
        // params = {"1":"1a","2":"2b"}
        // url: ?1=1a&2=2b
        var url = "" + path;
        var _param_url = "";
        if(params){
            Object.keys(params).map(function (k) {
                return [encodeURIComponent(k), encodeURIComponent(params[k])].join("=");
            }).join("&");
            _param_url = "?" + _param_url;
        }

        return url + _param_url;
    },
    alert:function (msg, cb) {
        layer.alert(msg,{
            yes:function (index) {
                if(typeof cb == "function"){
                    cb();
                }
                layer.close(index)
            }
        })
    }
}