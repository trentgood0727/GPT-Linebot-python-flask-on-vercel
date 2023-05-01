from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, AudioSendMessage, QuickReply, QuickReplyButton, MessageAction, AudioMessage
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

import uuid
import json
import openai

#from mongodb_function import *
#from api.mongodb_function import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
working_status = os.getenv("DEFALUT_TALKING", default = "true").lower() == "true"

app = Flask(__name__)
chatgpt = ChatGPT()

"""
config = {}
with open("config.txt") as f:
    for line in f:
        list_line = line.strip().replace(" ","").split("=")
        config[list_line[0]] = list_line[1]
"""

translate_language = "English"
audio_language = "Traditional Chinese"

translate_id = {}

lan_dic = {"日文": "Japanese", "英文": "English", "繁體中文": "Traditional Chinese", "韓文": "Korean",
"法文":"French", "泰文": "Thai", "義大利文": "Italian", "西班牙文": "Spanish", "荷蘭文":"Dutch", "德文": "German"}
reverse_lan_dict = {value: key for key, value in lan_dic.items()}

def openai_whisper(audio_path):
    audio_file= open(audio_path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript["text"]


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
    
    # input info to MongoDB
    #write_one_data(eval(body.replace('false','False')))
    
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
    
    global translate_language, audio_language
    user_input = event.message.text

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

    elif response[0:2] == "密碼":
        pwd = annotator_pwd(response[2:])
        reply_arr.append(TextSendMessage(text=pwd))
        reply_arr.append(TextSendMessage(text="{p}小礦工~挖礦愉快(๑¯∀¯๑)".format(p=response[2:])))
        line_bot_api.reply_message(event.reply_token, reply_arr)
    
    elif response == "阿全密碼":
        message = TextSendMessage(text="87?\n還再吃土?")
        line_bot_api.reply_message(event.reply_token, message)

    #======MongoDB操作範例======
    """
    elif response == "/read":
        datas = read_many_datas()
        datas_len = len(datas)
        message = TextSendMessage(text=f'資料數量，一共{datas_len}條')
        line_bot_api.reply_message(event.reply_token, message)

    elif response == "/search":
        datas = col_find('events')
        message = TextSendMessage(text=str(datas))
        line_bot_api.reply_message(event.reply_token, message)

    elif response == "/record":
        datas = read_chat_records()
        #print(type(datas))
        #print(datas)
        n = 0
        text_list = []
        for data in datas:
            if '/' in data[0]:
                continue
            else:
                text_list.append(data)
            n+=1
        data_text = '\n'.join(text_list)
        if len(data_text) == 0:
            message = TextSendMessage(text="No data record.")
            line_bot_api.reply_message(event.reply_token, message)
        else:
            message = TextSendMessage(text=data_text[:5000])
            line_bot_api.reply_message(event.reply_token, message)

    elif response == "/del":
        text = delete_all_data()
        message = TextSendMessage(text=text)
        line_bot_api.reply_message(event.reply_token, message)
    
    else:
        message = TextSendMessage(text=response)
        line_bot_api.reply_message(event.reply_token, message)
    """
    #======MongoDB操作範例======

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
        human_msg = event.message.text[5:] + "\n"
        chatgpt.add_msg(human_msg)
        #reply_msg = chatgpt.get_response().replace("AI:", "", 1)
        reply_msg = chatgpt.get_response() + "\n"
        chatgpt.add_msg(reply_msg)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_msg))

    if (user_input == "/setting") or (user_input == "設定"):
        flex_message = TextSendMessage(text="請選擇語音辨識後的翻譯語言 (我方語言)",
                        quick_reply=QuickReply(items=[
                        QuickReplyButton(action=MessageAction(label="繁體中文", text="設定辨識翻譯 " + "繁體中文")),
                        QuickReplyButton(action=MessageAction(label="英文", text="設定辨識翻譯 " + "英文")),
                        QuickReplyButton(action=MessageAction(label="日文", text="設定辨識翻譯 " + "日文")),
                        QuickReplyButton(action=MessageAction(label="韓文", text="設定辨識翻譯 " + "韓文")),
                        QuickReplyButton(action=MessageAction(label="法文", text="設定辨識翻譯 " + "法文")),
                        QuickReplyButton(action=MessageAction(label="泰文", text="設定辨識翻譯 " + "泰文")),
                        QuickReplyButton(action=MessageAction(label="義大利文", text="設定辨識翻譯 " + "義大利文")),
                        QuickReplyButton(action=MessageAction(label="西班牙文", text="設定辨識翻譯 " + "西班牙文")),
                        QuickReplyButton(action=MessageAction(label="荷蘭文", text="設定辨識翻譯 " + "荷蘭文")),
                        QuickReplyButton(action=MessageAction(label="德文", text="設定辨識翻譯 " +"德文")),
                        ]))
        line_bot_api.reply_message(
            event.reply_token,
            flex_message)   
            
    elif ("設定辨識翻譯" in user_input):
        audio_language = lan_dic[user_input.split(" ")[1]]
        flex_message = TextSendMessage(text="請選擇打字後的翻譯語言 (對方語言)",
                        quick_reply=QuickReply(items=[
                        QuickReplyButton(action=MessageAction(label="繁體中文", text="設定打字翻譯 " + "繁體中文")),
                        QuickReplyButton(action=MessageAction(label="英文", text="設定打字翻譯 " + "英文")),
                        QuickReplyButton(action=MessageAction(label="日文", text="設定打字翻譯 " + "日文")),
                        QuickReplyButton(action=MessageAction(label="韓文", text="設定打字翻譯 " + "韓文")),
                        QuickReplyButton(action=MessageAction(label="法文", text="設定打字翻譯 " + "法文")),
                        QuickReplyButton(action=MessageAction(label="泰文", text="設定打字翻譯 " + "泰文")),
                        QuickReplyButton(action=MessageAction(label="義大利文", text="設定打字翻譯 " + "義大利文")),
                        QuickReplyButton(action=MessageAction(label="西班牙文", text="設定打字翻譯 " + "西班牙文")),
                        QuickReplyButton(action=MessageAction(label="荷蘭文", text="設定打字翻譯 " + "荷蘭文")),
                        QuickReplyButton(action=MessageAction(label="德文", text="設定打字翻譯 " +"德文")),
                        ]))
        line_bot_api.reply_message(
            event.reply_token,
            flex_message)

    elif ("設定打字翻譯" in user_input):
        translate_language = lan_dic[user_input.split(" ")[1]]
        response = f"""設定完成!!! 
我方語言: {reverse_lan_dict[audio_language]}
對方語言: {reverse_lan_dict[translate_language]}"""
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response))

    elif (user_input=="目前設定") or (user_input=="/current_setting"):
        response = f"我方語言: {reverse_lan_dict[audio_language]}, 對方語言: {reverse_lan_dict[translate_language]}"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response))
    elif (user_input[0:2]=="翻譯"):
        response = chatgpt.translate_openai(user_input, translate_language)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response))

@line_handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    global translate_language, audio_language
    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id)
    with open(f'/tmp/whisper_audio.m4a', 'wb') as f:
        f.write(message_content.content)
    whisper_text = openai_whisper(f'/tmp/whisper_audio.m4a')
    response_text_audio = chatgpt.translate_openai(whisper_text, audio_language)
    #response_text_translate = chatgpt.translate_openai(whisper_text, translate_language)
    
    reply_arr = []
    reply_arr.append(TextSendMessage(text=whisper_text))
    reply_arr.append(TextSendMessage(text=response_text_audio))
    #reply_arr.append(TextSendMessage(text=response_text_translate))
    line_bot_api.reply_message(
        event.reply_token,
        reply_arr)

def annotator_pwd(username):
    client = ntplib.NTPClient()
    response = client.request('uk.pool.ntp.org', version=3)
    anstmp = datetime.utcfromtimestamp(response.tx_time).isoformat(' ')[:13] + username
    ans = hashlib.md5(anstmp.encode('utf-8-sig')).hexdigest()
    return ans

if __name__ == "__main__":
    app.run()
