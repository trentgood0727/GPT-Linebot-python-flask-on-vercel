from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.chatgpt import ChatGPT
#from chatgpt import ChatGPT

import os
import time
import socket
import sys
import struct
import ntplib
from datetime import datetime, timezone, timedelta
import hashlib

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
working_status = os.getenv("DEFALUT_TALKING", default = "true").lower() == "true"

app = Flask(__name__)
chatgpt = ChatGPT()

# domain root
@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global working_status

    response = event.message.text
    reply_arr = []
    if response == "宛玲密碼":
        pwd = annotator_pwd('crystal11300')
        reply_arr.append(TextSendMessage(text=pwd))
        reply_arr.append(TextSendMessage(text="宛玲小礦工~挖礦愉快(๑¯∀¯๑)"))
        line_bot_api.reply_message(event.reply_token, reply_arr)

    elif response == "純純密碼":
        pwd = annotator_pwd('cindy21562156')
        reply_arr.append(TextSendMessage(text=pwd))
        reply_arr.append(TextSendMessage(text="純純小礦工~挖礦愉快(๑¯∀¯๑)"))
        line_bot_api.reply_message(event.reply_token, reply_arr)

    elif response == "家茵密碼":
        pwd = annotator_pwd('hualien22')
        reply_arr.append(TextSendMessage(text=pwd))
        reply_arr.append(TextSendMessage(text="家茵小礦工~挖礦愉快(๑¯∀¯๑)"))
        line_bot_api.reply_message(event.reply_token, reply_arr)

    elif response == "念蓁密碼":
        pwd = annotator_pwd('snoopy19890119')
        reply_arr.append(TextSendMessage(text=pwd))
        reply_arr.append(TextSendMessage(text="念蓁小礦工~挖礦愉快(๑¯∀¯๑)"))
        line_bot_api.reply_message(event.reply_token, reply_arr)

    elif response == "惠禎密碼":
        pwd = annotator_pwd('kkmqo')
        reply_arr.append(TextSendMessage(text=pwd))
        reply_arr.append(TextSendMessage(text="惠禎小礦工~挖礦愉快(๑¯∀¯๑)"))
        line_bot_api.reply_message(event.reply_token, reply_arr)

    elif response == "阿全密碼":
        message = TextSendMessage(text="87?\n還再吃土?")
        line_bot_api.reply_message(event.reply_token, message)

    if event.message.type != "text":
        return

    if event.message.text == "說話":
        working_status = True
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="我可以說話囉，歡迎來跟我互動 ^_^ "))
        return

    if event.message.text == "閉嘴":
        working_status = False
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="好的，我乖乖閉嘴 > <，如果想要我繼續說話，請跟我說 「說話」 > <"))
        return

    if event.message.text == "忘記":
        chatgpt.clear_msg()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="已經什麼都忘記了，我就是一片浮雲～"))
        return

    if working_status and event.message.text[0:5] == "BB-87":
        human_msg = event.message.text[5:-1]
        chatgpt.add_msg(f"HUMAN:{human_msg}\n")
        #reply_msg = chatgpt.get_response().replace("AI:", "", 1)
        reply_msg = chatgpt.get_response()
        chatgpt.add_msg(f"AI:{reply_msg}\n")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_msg))

def annotator_pwd(username):
    client = ntplib.NTPClient()
    response = client.request('uk.pool.ntp.org', version=3)
    anstmp = datetime.utcfromtimestamp(response.tx_time).isoformat(' ')[:13] + username
    ans = hashlib.md5(anstmp.encode('utf-8-sig')).hexdigest()
    return ans

if __name__ == "__main__":
    app.run()
