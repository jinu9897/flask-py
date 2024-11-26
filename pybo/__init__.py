from flask import Flask

def create_app():
    app = Flask(__name__)

    # Access Blueprint 등록
    from pybo.views.access import bp as access_bp
    app.register_blueprint(access_bp)

    # Error Blueprint 등록
    from pybo.views.error import bp as error_bp
    app.register_blueprint(error_bp)

    return app
