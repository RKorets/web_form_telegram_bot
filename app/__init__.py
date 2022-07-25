from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.LocalConfig')
    app.config['SECRET_KEY'] = 'dasfafqqqw'
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  #clear cache after reset

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from . import routes
        db.create_all()

    return app
