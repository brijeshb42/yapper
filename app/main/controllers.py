from flask import render_template
from . import main_blueprint

@main_blueprint.route('/')
def index():
    return render_template('main/index.html')
