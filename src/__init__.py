from flask import Flask
from src.routes import app
def create_app():
    mainapp = Flask(__name__)
    mainapp.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    mainapp.config["SQLALCHEMY_DATABASE_URI"]='postgresql://mohtashimkamran:kamran@127.0.0.1/test2.db'

    from src.models import db,marsh

    db.app = mainapp
    db.init_app(mainapp)
    marsh.init_app(mainapp)

    mainapp.register_blueprint(app)

    return mainapp