from flask import Flask
from . import config

from .flago.flago_do import FlagoDo
from .flago.request_bind import request_bind

db = FlagoDo()

def create_app(config_name='dev'):
    app = Flask(__name__)
    app.config.from_object(config.from_object(config_name))
    db.init_app(app)

    app.add_url_rule("/",view_func=request_bind, methods=['GET','POST','PUT','DELETE'])
    app.add_url_rule("/<path:path>/", view_func=request_bind, methods=['GET','POST','PUT','DELETE'])
    
    return app