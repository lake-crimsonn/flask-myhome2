from flask import Blueprint, render_template


bp = Blueprint('myhome', __name__, url_prefix='/myhome')


@bp.route('/main')
def myhome_views_main():
    return render_template('myhome_main.html')