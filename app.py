from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from crawler import crawler

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('6G6r3dV4V2Yh/02rSTOBOFq1TQBL+rzoZiJO5LkntYoF85oIBEfrsbLlJplmHFVd6BD8v391QUkiQc4qVdkAiyv9wKVz7w3cCQq4VF5eyOqISUN9QGx6yuieTLwQ8WN/nJLDbJ/rwbI4uRQ/0lm0KQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('b8d635d616a122e7fbf0d10dcf7439f1')

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # message = TextSendMessage(text=event.message.text)
    if "資訊" == event.message.text:
        DcardCrawler=crawler()
        result=DcardCrawler.information
    else:
        DcardCrawler=crawler()
        result=DcardCrawler.crawl_specific_form(event.message.text)
    message=TextSendMessage(text=result)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
