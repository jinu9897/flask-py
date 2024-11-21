from flask import Flask

def create_app(config_class='config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 블루프린트 등록
    from .views.access import bp as access_bp
    app.register_blueprint(access_bp)

    from .views.error import bp as error_bp
    app.register_blueprint(error_bp)

    return app
