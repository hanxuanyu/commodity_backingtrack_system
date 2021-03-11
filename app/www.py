from application import app
from flask_debugtoolbar import DebugToolbarExtension

toolbar = DebugToolbarExtension(app)

'''
拦截器 & 错误处理
'''
from interceptors.Auth import *
from interceptors.errorHandler import *

'''
蓝图
'''
from controllers.index import index_page
from controllers.member import member_page
from controllers.commodity import com_page
from controllers.blockchain import block_chain_page

app.register_blueprint(index_page, url_prefix="/")
app.register_blueprint(member_page, url_prefix="/member")
app.register_blueprint(com_page, url_prefix="/commodity")
app.register_blueprint(block_chain_page, url_prefix="/blockchain")

'''
模板函数
'''
from common.lib.UrlManager import UrlManager
app.add_template_global(UrlManager.build_static_url, "build_static_url")
app.add_template_global(UrlManager.build_url, "build_url")
