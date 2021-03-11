from application import app
from common.lib.DataHelper import get_current_time
import os


class UrlManager(object):

    @staticmethod
    def build_url(path):
        config_domain = app.config["DOMAIN"]
        return "%s%s" % (config_domain["www"], path)

    @staticmethod
    def build_static_url(path):
        path = "/static" + path + "?ver=" + UrlManager.get_release_version()
        return UrlManager.build_url(path)

    @staticmethod
    def get_release_version():
        # 开发模式使用时间戳管理版本，生产环境使用固定版本号
        ver = "%s" % (get_current_time("%Y%m%d%H%M%S%f"))
        release_version = app.config.get("RELEASE_VERSION")
        if release_version and "production" == os.environ["ops_config"]:
            ver = release_version
        return ver
