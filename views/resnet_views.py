from flask import Blueprint, request, render_template
from werkzeug.utils import secure_filename
from PIL import Image
from torchvision import transforms

import json
import base64
import io
import torch
import numpy as np

bp = Blueprint('resnet', __name__, url_prefix='/resnet')

model = torch.load('data/models/model_car.pt',
                   map_location=torch.device('cpu'))


@bp.route('/')
def resnet_route():
    return render_template('resnet.html')


@bp.route('/fileupload', methods=['POST'])
def resnet_fileupload():
    print(request.files)
    preds_arr = []

    for file in request.files:
        file = request.files[file]
        print(file.filename)
        file.save(file.filename)

        img = Image.open(file.filename)
        transforms_test = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [
                0.229, 0.224, 0.225])
        ])

        img = transforms_test(img).unsqueeze(0).to('cpu')
        print('img size: ', np.shape(img))

        with torch.no_grad():
            outputs = model(img)
            print('output: ', outputs)
            _, preds = torch.max(outputs, 1)
            classname = ['k5', 'model3']
            print('추론한 이름: ', classname[preds[0]])
            preds_arr.append(classname[preds[0]])

    return preds_arr
