from flask import Blueprint, render_template, request
from ..features.wc_server import start_video_call


bp = Blueprint('wc', __name__, url_prefix='/wc')


@bp.route('/')
def wc_route():
    client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    print(f"client ip: {client_ip}")
    start_video_call(client_ip)
    return render_template('wc.html')
