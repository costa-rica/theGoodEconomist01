from flask import Flask
from folioApp.config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    from folioApp.main.routes import main
    from folioApp.datatools.routes import datatools
    app.register_blueprint(main)
    app.register_blueprint(datatools)
    
    return app