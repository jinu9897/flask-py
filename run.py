from flask import Flask
from pybo.views.access import parse_access_log
from pybo.views.error import parse_error_log

app = Flask(__name__)

@app.route('/')
def index():
    return "Log Analysis Server Running"

@app.route('/access')
def access_logs():
    parse_access_log()
    return "Access logs parsed!"

@app.route('/error')
def error_logs():
    parse_error_log()
    return "Error logs parsed!"

if __name__ == "__main__":
    app.run()
