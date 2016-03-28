from flask import Flask, render_template
app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('layouts/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('layouts/500.html'), 500

@app.route("/")
def hello():
    return render_template('pages/index.html')



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
