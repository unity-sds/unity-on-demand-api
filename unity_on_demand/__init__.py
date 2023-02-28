from flask import Flask
from flask_restx import apidoc
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    cors = CORS().init_app(app)

    # register our blueprints
    from .controllers.main import main

    app.register_blueprint(main)

    from .controllers.api_v01 import services as api_v01

    app.register_blueprint(api_v01)

    app.register_blueprint(apidoc.apidoc, name="od_restx_doc")

    return app


if __name__ == "__main__":
    app = create_app()

    app.run()
