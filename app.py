import json
from flask import Flask, render_template, request, url_for


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
    instagram_posts = instagram.get_user_posts(
        user_id=config.instagram.get('user_id'),
        count='12',
        tags='art,illustration,characterdesign',
        expiry=3600)
    return render_template('pages/index.html', instagram_posts=instagram_posts)


@app.route("/instagram")
def instagram_posts():
    """Get Instagram posts.

    example url:
        /instagram?count=6&tags=art,illustration,characterdesign

    Returns:
        Response: the JSON items representing instagram posts.
    """
    response = instagram.get_user_posts(
        user_id=config.instagram.get('user_id'),
        count=request.args.get('count', 6),
        tags=request.args.get('tags', None),
        expiry=10)
    return json.dumps(response), 200, {'Content-Type': 'application/json'}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
