from flask import Flask


def create_app():
    app = Flask(__name__)

    from .views import myhome_views, main_views, chatbot_views, webtoon_views, sms_views, stt2tts_views, resnet_views, wc_views

    app.register_blueprint(myhome_views.bp)
    app.register_blueprint(main_views.bp)
    app.register_blueprint(chatbot_views.bp)
    app.register_blueprint(webtoon_views.bp)
    app.register_blueprint(sms_views.bp)
    app.register_blueprint(stt2tts_views.bp)
    app.register_blueprint(resnet_views.bp)
    app.register_blueprint(wc_views.bp)

    return app
