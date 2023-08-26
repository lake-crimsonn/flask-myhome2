from flask import Blueprint, Response, render_template, send_file, redirect, url_for
from gtts import gTTS
import speech_recognition as sr
import time
import playsound
import os
import io
import base64

bp = Blueprint('stt2tts', __name__, url_prefix='/stt2tts')

data_arr = []

filename = "test.mp3"
savefile_path = os.path.join('.', 'data', 'stt2tts', filename)


@bp.route('/')
def stt2tts_route():
    return render_template('stt2tts.html')


"""
   플레이사운드 버전을 낮춰야 된다.
   pip install playsound==1.2.2 
"""


@bp.route('/play')
def play_route():

    recog = sr.Recognizer()

    with sr.Microphone() as source:
        print("말 좀 해봐바")
        audio = recog.listen(source)
        result = recog.recognize_google(audio, language="ko-KR")
        print(f"입력된 음성 : {result}")

        if '메타버스' in result:
            tts = gTTS(text="반갑습니다", lang="ko")
            tts.save(savefile_path)
            time.sleep(3)
            playsound.playsound(savefile_path)
    return redirect(url_for('stt2tts.stt2tts_route'))


@bp.route('/send')
def send_stt():
    # data = io.BytesIO()
    # savefile_path.save(data, 'mp3')
    # encoded_img_data = base64.b64encode(data.getvalue())

    # return render_template('stt2tts.html', image=encoded_img_data.decode('utf-8'))
    return send_file(savefile_path)
