from flask import Flask, request, abort
from flask_cors import cross_origin
from urllib.parse import parse_qs
import os, json, codecs, re, random

import telegram
from telegram.ext import Dispatcher, MessageHandler, Filters, Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

#導入env, model
from env import *
from model import *
# #導入Others
# from Others.flexMessageJSON import *
#導入Controllers
from Controllers.messageController import *
# from Controllers.locationController import *
from Controllers.postbackController import *
#導入Managers
from Managers.channelManager import *
from Managers.messageManager import *
# from Managers.statementManager import *
# #導入Services
# from Services.geocodingService import *

app = Flask(__name__)

bot = telegram.Bot(token=(GET_SECRET("TELEGRAM_TOKEN")))
bot.send_message(chat_id = '863052781', text ='你可以開始了')

####################檢查uWSGI->Flask是否正常運作####################
@app.route("/")
def index():
    return 'BotApp is Working!'

####################一般callback####################
@app.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return 'ok'

# ####################推播####################
# @app.route("/pushing", methods=['POST'])
# def pushing():
#     data = json.loads(request.get_data())
#     mtype = data.get('type', 'text')
#     title = data.get('title', '')
#     message = data.get('message', '')
#     channel_id = data.get('channel_id', '')
#     template = data.get('template', None)
#     status = pushing_process(mtype, title, message, channel_id) if template == None else pushing_template(title, message, channel_id, template)
#     return json.dumps({'msg': status})

####################小功能####################
##隨機產生後綴字
def getPostfix():
    p = random.randint(1,10)
    postfix = get_postfix() if get_postfix() and p%5==0 else ""
    return postfix

# #貼圖unicode轉line編碼 [請傳入 sticon(u"\U數字") ]
# def sticon(unic):
#     return codecs.decode(json.dumps(unic).strip('"'), 'unicode_escape')

#取得ChannelId [如果是群組或聊天室，一樣回傳channelId，不是userId]
def getChannelId(update, msg_type):
    if msg_type == "callback":
        return str(update.callback_query.message.chat_id)
    else:
        return str(update.message.chat_id)

#取得UserId
def getUserId(update, msg_type):
    if msg_type == "callback":
        return str(update.callback_query.from_user.id)
    else:
        return str(update.message.from_user.id)

####################取得EVENT物件、發送訊息####################
def get_event_obj(update, msg_type = None):
    ##取得頻道及使用者ID
    channelId = getChannelId(update, msg_type)
    userId = getUserId(update, msg_type)
    ##建頻道資料
    if userId: create_channel(userId)
    if channelId: create_channel(channelId)
    ##取得頻道資料
    channelData = get_channel(channelId)
    userData = get_channel(userId) if userId else None
    ##取得名稱
    profileName = ""
    try: profileName = str(update.message.from_user.first_name+" "+update.message.from_user.first_name) if userId else ""
    except: profileName = ""
    ##回傳
    return {
        "channelPK": get_pk_by_channel_id(channelId),
        "userPK": get_pk_by_channel_id(userId),
        "channelId": channelId,
        "userId": userId,
        "lineMessage": "",                              #取得收到的訊息
        "lineMessageType": msg_type,
        "mute": channelData['mute'],
        "global_talk": channelData['global_talk'],
        "replyList": [],                                #初始化傳送內容（可為List或單一Message Object）
        "replyLog": ["", 0, ""],                        #發出去的物件準備寫入紀錄用 [訊息, 有效度(0=功能型, 1=關鍵字, 2=一般型), 訊息類型]
        "postfix": getPostfix()
    }

def send_reply(update, GET_EVENT, STORE_LOG = False):
    ##儲存訊息
    if STORE_LOG:
        if GET_EVENT["replyLog"][0]: store_replied(GET_EVENT["replyLog"][0], GET_EVENT["replyLog"][1], GET_EVENT["replyLog"][2], GET_EVENT["channelPK"])  #記錄機器人本次回的訊息
        store_received(GET_EVENT["lineMessage"], GET_EVENT["lineMessageType"], GET_EVENT["channelPK"], GET_EVENT["userPK"])                               #儲存本次收到的語句
    ####回傳給TELEGRAM
    for replyMsg in GET_EVENT["replyList"]:
        if replyMsg["type"] == "text":
            update.message.reply_text(replyMsg["msg"])
        if replyMsg["type"] == "image":
            update.message.reply_text(replyMsg["msg"])
        if replyMsg["type"] == "markup":
            update.message.reply_text(replyMsg["msg"], reply_markup = replyMsg["markup"])
        if replyMsg["type"] == "edit_message_text":
            update.callback_query.edit_message_text(replyMsg["msg"])

# ####################[加入, 退出]: [好友, 聊天窗]####################
# @handler.add(FollowEvent)
# def handle_follow(event):
#     ##取得EVENT物件
#     GET_EVENT = get_event_obj(event)
#     flexObject = flexStatusMenu({
#         "global_talk_text": "所有人教的" if GET_EVENT['global_talk'] else "本頻道教的", 
#         "mute_text": "安靜" if GET_EVENT['mute'] else "可以說話", 
#         "global_talk": GET_EVENT['global_talk'], 
#         "mute": GET_EVENT['mute']
#     })
#     GET_EVENT["replyList"] = [
#         TextSendMessage(text=GET_EVENT["nickname"] + "，歡迎您成為本熊貓的好友！" + sticon(u"\U00100097")),
#         FlexSendMessage(alt_text = "主選單", contents = flexMainMenu(GET_EVENT["channelId"], GET_EVENT["level"])),
#         FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
#     ]
#     ##發送回覆
#     send_reply(GET_EVENT, False)
# @handler.add(JoinEvent)
# def handle_join(event):
#     ##取得EVENT物件
#     GET_EVENT = get_event_obj(event)
#     flexObject = flexStatusMenu({
#         "global_talk_text": "所有人教的" if GET_EVENT['global_talk'] else "本頻道教的", 
#         "mute_text": "安靜" if GET_EVENT['mute'] else "可以說話", 
#         "global_talk": GET_EVENT['global_talk'], 
#         "mute": GET_EVENT['mute']
#     })
#     GET_EVENT["replyList"] = [
#         TextSendMessage(text="大家好我叫酷熊貓" + sticon(u"\U00100097")),
#         FlexSendMessage(alt_text = "主選單", contents = flexMainMenu(GET_EVENT["channelId"], GET_EVENT["level"])),
#         FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
#     ]
#     ##發送回覆
#     send_reply(GET_EVENT, False)
# @handler.add(UnfollowEvent)
# def handle_unfollow(event):
#     remove_channel(getChannelId(event))
# @handler.add(LeaveEvent)
# def handle_leave(event):
#     pass
#     #remove_channel(getChannelId(event))

####################CallbackEvent處理區#################### 
def handle_callback(bot, update):
    ##取得EVENT物件
    GET_EVENT = get_event_obj(update, "callback")
    data = parse_qs(update.callback_query.data)
    print(data)
    
    ##發送回覆
    GET_EVENT = postback_processer(GET_EVENT, data)
    send_reply(update, GET_EVENT, False)

####################文字訊息處理區####################
def handle_message(bot, update):
    ##取得EVENT物件
    GET_EVENT = get_event_obj(update, "text")
    GET_EVENT["lineMessage"] = update.message.text

    ##發送
    GET_EVENT = message_processer(GET_EVENT)
    send_reply(update, GET_EVENT, True)

# ####################貼圖訊息處理區#################### 
# @handler.add(MessageEvent, message=StickerMessage)
# def handle_sticker_message(event):
#     ##取得EVENT物件
#     GET_EVENT = get_event_obj(event)
#     GET_EVENT["lineMessage"] = event.message.package_id + ',' + event.message.sticker_id
#     GET_EVENT["replyList"] = StickerSendMessage(package_id=event.message.package_id, sticker_id=event.message.sticker_id)
#     GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 2, 'sticker']
#     GET_EVENT["replyList"] = [GET_EVENT["replyList"], TextSendMessage(text=GET_EVENT["postfix"])] if GET_EVENT["postfix"] else GET_EVENT["replyList"]
#     ##發送
#     send_reply(GET_EVENT, True)

# ####################位置訊息處理區#################### 
# @handler.add(MessageEvent, message=LocationMessage)
# def handle_location_message(event):
#     ##取得EVENT物件
#     LOCATION_INFO = {
#         "title": str(event.message.title),
#         "addr": addr_format(str(event.message.address)),
#         "lat": float(event.message.latitude),
#         "lng": float(event.message.longitude)
#     }
#     GET_EVENT = get_event_obj(event)
#     GET_EVENT["lineMessage"] = LOCATION_INFO["title"] + ',' + LOCATION_INFO["addr"] + ',' + str(LOCATION_INFO["lat"]) + ',' + str(LOCATION_INFO["lng"])
    
#     ##發送
#     GET_EVENT = location_processer(GET_EVENT, LOCATION_INFO)
#     send_reply(GET_EVENT, True)


# New a dispatcher for bot
dispatcher = Dispatcher(bot, None)

# Add handler for handling message, there are many kinds of message. For this handler, it particular handle text
# message.
dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
dispatcher.add_handler(CallbackQueryHandler(handle_callback))

if __name__ == "__main__":
    app.run()