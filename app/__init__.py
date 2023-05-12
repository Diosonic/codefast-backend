from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from config import Config
# from flask_migrate import Migrate
# from flask_cors import CORS
# from flask_mysqldb import MySwQL


# db = SQLAlchemy()
# migrate = Migrate()
# mysql = MySQL()

def create_app():
    app = Flask(__name__)

    
    # db.init_app(app)
    # migrate.init_app(app, db)
    # CORS(app)
    
  
    # from app import models


    # Blueprint
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app