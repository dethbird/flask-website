from flask import Flask, render_template

from flask_website import config
from flask_website.connector import instagram

app = Flask(__name__, static_url_path = "/assets", static_folder = "assets")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('layouts/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('layouts/500.html'), 500

@app.route("/")
def index():
    # response = instagram.get_recent_media(124,6,None)
    # import pdb; pdb.set_trace()
    return render_template('pages/index.html')

@app.route("/instagram")
def instagram():
    response = instagram.get_recent_media(124,6,None)
    # import pdb; pdb.set_trace()
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
