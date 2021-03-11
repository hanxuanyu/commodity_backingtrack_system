# 生产环境配置文件
from config.base_setting import *
DEBUG = False  # DEBUG模式
RELEASE_VERSION = "20200415"
# 本地开发环境配置文件
from datetime import timedelta
from config.base_setting import *
SQLALCHEMY_ECHO = False  # 输出SQL语句
SQLALCHEMY_TRACK_MODIFICATIONS = True  # 跟踪
SQLALCHEMY_DATABASE_URI = "mysql://root:com.hxuanyu.123@127.0.0.1/commodity"  # 数据库连接配置
SECRET_KEY = "123456"  # debug_toolbar 配置
DOMAIN = {
    "www": "http://47.93.128.120:5000"
}
