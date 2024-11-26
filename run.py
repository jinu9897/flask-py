from flask import Flask, render_template
from views.access import access_analysis
from views.error import error_analysis
from pybo import create_app

app = Flask(__name__)

@app.route('/access')
def access_log():
    access_graphs = access_analysis()
    return render_template('access.html', graphs=access_graphs)

@app.route('/error')
def error_log():
    error_graphs = error_analysis()
    return render_template('error.html', graphs=error_graphs)

if __name__ == '__main__':
    app.run(debug=True)
