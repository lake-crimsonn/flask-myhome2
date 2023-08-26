from flask import Blueprint, render_template, request
from flask_socketio import SocketIO
from ..features.wc_server import start_video_call


bp = Blueprint('wc', __name__, url_prefix='/wc')


@bp.route('/')
def wc_route():
    # client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    start_video_call('192.168.0.42')
    return None
