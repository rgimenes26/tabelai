from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_caching import Cache
from pathlib import Path
# from . import config as appConfig


app = Flask(__name__)
app.config['SECRET_KEY'] = 'cd91d3091302141ec5fcab75a58b72a65116f3bc485a9d08cb87610924145e62'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://rafael:Biosinfo_321@192.168.168.3/bios"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# base_path = Path(__file__).parent
# caching_path = (base_path / "data").resolve()
# cache = Cache(app, config={
#     "CACHE_TYPE": "FileSystemCache",
#     "CACHE_DEFAULT_TIMEOUT": 600,
#     "CACHE_DIR" : caching_path,
#     "CACHE_THRESHOLD" : 200,
# })
# cache.clear()

from webapp import routes

from .notaria.app import init_dash_app
tabelai = init_dash_app(app)
