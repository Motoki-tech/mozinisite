from flask import Flask, request, abort
from google.cloud import vision

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import io


app = Flask(__name__)

line_bot_api = LineBotApi('ACCESS_TOKEN')
handler = WebhookHandler('CHANNEL_SECRET')
output_texts = []

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

            #画像データを取得
            message_content = line_bot_api.get_message_content(event.message.id)

            # print(message_content)
            with open(f"/{event.message.id}.jpg", 'wb') as fd:
                for chunk in message_content.iter_content():
                    fd.write(chunk)
            
            with io.open(f"/{event.message.id}.jpg", "wb") as image_file:
                content = image_file.read()


            image = vision.Image(content=content)

            #ImageAnnotatorClientのインスタンスを生成
            annotator_client = vision.ImageAnnotatorClient()

            response_data = annotator_client.document_text_detection(image=image, image_context={'language_hints': ['ja']})

            print('-----RESULT------')
            output_text=''
            for page in response_data.full_text_annotation.pages:
                for block in page.blocks:
                    for paragraph in block.paragraphs:
                        for word in paragraph.words:
                            output_text += ''.join([symbol.text for symbol in word.symbols])
                            output_text += '\n'
            print(output_text)

            print('-----RESULT------')

            if len(output_text) > 0:
                output_texts.append(output_text.rstrip('/n'))
            else:
                output_texts.append('読み取れませんでした！')

            if len(output_texts) == 0:
                output_texts.append('画像データを送ってね')

            print(output_texts)
            reply_message = []
            for output_text in output_texts:
                reply_message.append(TextSendMessage(text=output_text))
            line_bot_api.reply_message(event.reply_token, reply_message)

            return {
                'statusCode': 200
            }

if __name__ == "__main__":
       app.run()
