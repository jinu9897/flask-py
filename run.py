
from flask import Flask, render_template
from views.access import access_analysis
from views.error import error_analysis

app = Flask(__name__)
@app.route('/error')
def error_log():
    error_graphs = error_analysis()
    return render_template('error.html', graphs=error_graphs)

@app.route('/')
def access_log():
    access_graphs = access_analysis()
    return render_template('index.html', graphs=access_graphs)

if __name__ == '__main__':
    app.run(debug=True)
