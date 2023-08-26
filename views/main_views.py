from flask import Blueprint, render_template


bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def myhome_main():
    return render_template('index.html')