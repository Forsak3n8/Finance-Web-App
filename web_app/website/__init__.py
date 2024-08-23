from flask import Flask
from .models import db_helper

# define and initialize app variable
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SUPERSECRET'

    # Register views blueprint
    from .views import views
    app.register_blueprint(views, url_prefix="/")

    return app


    