# 公用配置
from datetime import timedelta
DEBUG = True  # DEBUG模式
SQLALCHEMY_ECHO = False  # 禁止输出SQL语句
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 跟踪
SQLALCHEMY_ENCODING = "utf8mb4"  # 文件编码
SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1/commodity"  # 数据库连接配置
SECRET_KEY = "123456"  # debug_toolbar 配置
AUTH_COOKIE_NAME = "cookie_auth"
DEBUG_TB_INTERCEPT_REDIRECTS = False
DOMAIN = {
    "www": "http://192.168.31.177:5000"
}
