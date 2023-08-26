import base64
import io

from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import secure_filename
from ..features.gen_translate import generate_translate
from PIL import Image
bp = Blueprint('webtoon', __name__, url_prefix="/webtoon")


@bp.route('/')
def webtoon_main():
    image = Image.open('static/img/webtoon1.png')
    data = io.BytesIO()
    image.save(data, 'jpeg')
    encoded_img_data = base64.b64encode(data.getvalue())
    return render_template('webtoon.html', image=encoded_img_data.decode('utf-8'))


@bp.route('/fileupload', methods=['POST'])
def fileupload():
    if request.method == 'POST':
        file = request.files['file']
        image = secure_filename(file.filename)
        file.save('static/img/'+image)
        trans_image = generate_translate(image)
        data = io.BytesIO()
        trans_image.save(data, 'jpeg')
        encoded_img_data = base64.b64encode(data.getvalue())
        return render_template('webtoon.html', image=encoded_img_data.decode('utf-8'))
    else:
        return render_template('webtoon.html')
