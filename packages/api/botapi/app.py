from os import getenv
from flask import Flask
from flask_cors import CORS

# import routes
from botapi.routes.meta import meta
from botapi.routes.chat import chat

# import llm 
from botapi.llm import get_model


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = getenv('SECRET_KEY')
    app.config['MODEL'] = get_model()

    # set cors for routes / blueprints
    CORS(app, resources={
        r"/api/meta/*": {"origins": "*"},
        r"/api/chat/*": {"origins": "*"}
    })

    # register routes
    app.register_blueprint(meta)
    app.register_blueprint(chat)

    # handle errors
    @app.errorhandler(404)
    def not_found(e):
        return {"message": "Not Found"}, 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return {"message": "Internal Server Error"}, 500

    return app
