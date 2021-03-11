# 本地开发环境配置文件
from datetime import timedelta
from config.base_setting import *
DEBUG = True  # DEBUG模式
RELEASE_VERSION = "20200415"
SQLALCHEMY_ECHO = True  # 输出SQL语句
SQLALCHEMY_TRACK_MODIFICATIONS = True  # 跟踪
SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1/commodity"  # 数据库连接配置
SECRET_KEY = "123456"  # debug_toolbar 配置

DOMAIN = {
    "www": "http://192.168.137.1:5000"
}