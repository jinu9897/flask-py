from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    # Access와 Error Blueprint 등록
    from pybo.views.access import bp as access_bp
    from pybo.views.error import bp as error_bp
    app.register_blueprint(access_bp)
    app.register_blueprint(error_bp)

    # 기본 경로('/')
    @app.route('/')
    def index():
        return render_template('index.html')

    return app
