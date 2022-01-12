from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('I9Eq9cV6L0rBM96KueqmVGle118doEg3uVuL3oD7kS4D/LB21l5mZLdeUmxJlMVRhpdnvZVVdu/YH618aN4w/HXi2bG6rt5mY78tiHrTd1o+kAMhOzOzyX0VHvlJKrxxN5FCJ3hpTh63t0NYslt+fwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c38e7341b1ff0df2ddee214a41e9b29e')

@app.route("/")
def test():
    return "ok"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text =="ありがとう":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=f"どういたしまして"))
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()