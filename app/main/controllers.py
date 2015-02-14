from flask import render_template, send_from_directory
from . import main_blueprint


@main_blueprint.route('/')
def index():
    return render_template('main/index.html')


@main_blueprint.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )