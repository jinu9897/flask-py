from flask import Flask

def create_app():
    app = Flask(__name__)

    # 기존 라우트
    from .views.access import bp as main_bp
    app.register_blueprint(main_bp)

    # 새로 추가된 라우트
    from .views.error import bp as error_bp
    app.register_blueprint(error_bp)

    return app
