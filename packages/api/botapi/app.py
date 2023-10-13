from os import getenv
from flask import Flask

# import routes
from botapi.routes.meta import meta
from botapi.routes.chat import chat


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = getenv('SECRET_KEY')

    # TODO: fetch all post data from https://mykal.codes/feeds/main.json
    # TODO: parse this data into LangChain format
    # TODO: initialize a model with ChatGPT3 and the vectorized data
    # TODO: set this instance as a global variable in the flask app context

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
