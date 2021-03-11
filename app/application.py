from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
import os


app = Flask(__name__)

app.config.from_pyfile("config/base_setting.py")
# ops_config = local|production
# set ops_config = local


if "ops_config" in os.environ:
    print("加载配置config/%s_setting.py" % (os.environ["ops_config"]))
    app.config.from_pyfile("config/%s_setting.py" % (os.environ["ops_config"]))

manager = Manager(app)



db = SQLAlchemy(app)
