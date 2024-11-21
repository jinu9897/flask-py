from flask import Flask

def create_app():
    app = Flask(__name__)

    # Blueprint 등록
    from pybo.views.access import bp as access_bp
    from pybo.views.error import bp as error_bp
    app.register_blueprint(access_bp, url_prefix='/access')
    app.register_blueprint(error_bp, url_prefix='/error')

    return app
