from flask import Flask, request, abort
from flask_cors import cross_origin
from urllib.parse import parse_qs
import os, json, codecs, re, random

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

#導入env, model
from env import *
from model import *
#導入Others
from Others.flexMessageJSON import *
#導入Controllers
from Controllers.messageController import *
from Controllers.locationController import *
from Controllers.postbackController import *
#導入Managers
from Managers.channelManager import *
from Managers.messageManager import *
from Managers.statementManager import *
#導入Services
from Services.geocodingService import *

app = Flask(__name__)

line_bot_api = LineBotApi(GET_SECRET("ACCESS_TOKEN")) 
handler = WebhookHandler(GET_SECRET("API_SECRET"))

####################檢查uWSGI->Flask是否正常運作####################
@app.route("/")
def index():
    return 'BotApp is Working!'

####################一般callback####################
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        create_table()
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

####################推播####################
@app.route("/pushing", methods=['POST'])
def pushing():
    data = json.loads(request.get_data())
    mtype = data.get('type', 'text')
    title = data.get('title', '')
    message = data.get('message', '')
    channel_id = data.get('channel_id', '')
    template = data.get('template', None)
    status = pushing_process(mtype, title, message, channel_id) if template == None else pushing_template(title, message, channel_id, template)
    return json.dumps({'msg': status})

####################[匯入, 拉黑, JSON]: [詞條]####################
#詞條拉黑
@app.route("/operateStatement", methods=['POST'])
def operateStatement():
    data = json.loads(request.get_data())
    action = data["action"]
    adjust = data["adjust"]
    statement_id = data["statement_id"]
    operate_statement(action, adjust, statement_id)
    return json.dumps({'msg': 'ok'})

#匯入詞條
@app.route("/importStatement", methods=['POST'])
def importStatement():
    data = json.loads(request.get_data())
    for item in data["data"]:
        create_statement(item["keyword"], item["response"], 0, 0)
    return json.dumps({'msg': 'ok'})

#詞條轉JSON
@app.route("/getStatementJSON", methods=['POST'])
def getStatementJSON():
    data = json.loads(request.get_data())
    channel_id = data["channel_id"] if data["channel_id"] and data["channel_id"]!="ALL" else "ALL"
    return json.dumps(get_line_statement_table(channel_id))

#推播紀錄轉JSON
@app.route("/getPushedJSON", methods=['POST'])
def getPushedJSON():
    return json.dumps(get_line_pushed_table())

####################小功能####################
##隨機產生後綴字
def getPostfix():
    p = random.randint(1,10)
    postfix = get_postfix() if get_postfix() and p%5==0 else ""
    return postfix

#貼圖unicode轉line編碼 [請傳入 sticon(u"\U數字") ]
def sticon(unic):
    return codecs.decode(json.dumps(unic).strip('"'), 'unicode_escape')

#取得ChannelId [如果是群組或聊天室，一樣回傳channelId，不是userId]
def getChannelId(event):
    e_source = event.source
    return e_source.room_id if e_source.type == "room" else e_source.group_id if e_source.type == "group" else e_source.user_id

#取得UserId
def getUserId(event):
    return event.source.user_id if hasattr(event.source, 'user_id') else None

####################取得EVENT物件、發送訊息####################
def get_event_obj(event):
    ##取得頻道及使用者ID
    channelId = getChannelId(event)
    userId = getUserId(event)
    ##建頻道資料
    if userId: create_channel(userId)
    create_channel(channelId)
    ##取得頻道資料
    channelData = get_channel(channelId)
    userData = get_channel(userId) if userId else None
    
    profileName = ""
    try: profileName = line_bot_api.get_profile(userId).display_name if userId else ""
    except: profileName = ""

    return {
        "reply_token": event.reply_token,
        "channelPK": get_pk_by_channel_id(channelId),
        "userPK": get_pk_by_channel_id(userId),
        "channelId": channelId,
        "userId": userId,
        "lineMessage": "",                              #取得收到的訊息
        "lineMessageType": event.message.type if hasattr(event, 'message') else None,
        "level": int(int(userData['exp'])/10) if userData else int(int(channelData['exp'])/10),     #等級
        "exp": int(userData['exp'])%10 if userData else int(channelData['exp'])%10,          #經驗值每+10升一級
        "nickname": userData['nickname'] if userData and int(int(userData['exp'])/10)>=2 and userData['nickname'] else profileName,
        "mute": channelData['mute'],
        "global_talk": channelData['global_talk'],
        "replyList": [],                                #初始化傳送內容（可為List或單一Message Object）
        "replyLog": ["", 0, ""],                        #發出去的物件準備寫入紀錄用 [訊息, 有效度(0=功能型, 1=關鍵字, 2=一般型), 訊息類型]
        "postfix": getPostfix()
    }

def send_reply(GET_EVENT, STORE_LOG = False):
    ##儲存訊息
    if STORE_LOG:
        if GET_EVENT["replyLog"][0]: store_replied(GET_EVENT["replyLog"][0], GET_EVENT["replyLog"][1], GET_EVENT["replyLog"][2], GET_EVENT["channelPK"])  #記錄機器人本次回的訊息
        store_received(GET_EVENT["lineMessage"], GET_EVENT["lineMessageType"], GET_EVENT["channelPK"], GET_EVENT["userPK"])                               #儲存本次收到的語句
    ####回傳給LINE
    line_bot_api.reply_message(GET_EVENT["reply_token"], GET_EVENT["replyList"])

####################[加入, 退出]: [好友, 聊天窗]####################
@handler.add(FollowEvent)
def handle_follow(event):
    ##取得EVENT物件
    GET_EVENT = get_event_obj(event)
    flexObject = flexStatusMenu({
        "global_talk_text": "所有人教的" if GET_EVENT['global_talk'] else "本頻道教的", 
        "mute_text": "安靜" if GET_EVENT['mute'] else "可以說話", 
        "global_talk": GET_EVENT['global_talk'], 
        "mute": GET_EVENT['mute']
    })
    GET_EVENT["replyList"] = [
        TextSendMessage(text=GET_EVENT["nickname"] + "，歡迎您成為本熊貓的好友！" + sticon(u"\U00100097")),
        FlexSendMessage(alt_text = "主選單", contents = flexMainMenu(GET_EVENT["channelId"], GET_EVENT["level"])),
        FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
    ]
    ##發送回覆
    send_reply(GET_EVENT, False)
@handler.add(JoinEvent)
def handle_join(event):
    ##取得EVENT物件
    GET_EVENT = get_event_obj(event)
    flexObject = flexStatusMenu({
        "global_talk_text": "所有人教的" if GET_EVENT['global_talk'] else "本頻道教的", 
        "mute_text": "安靜" if GET_EVENT['mute'] else "可以說話", 
        "global_talk": GET_EVENT['global_talk'], 
        "mute": GET_EVENT['mute']
    })
    GET_EVENT["replyList"] = [
        TextSendMessage(text="大家好我叫酷熊貓" + sticon(u"\U00100097")),
        FlexSendMessage(alt_text = "主選單", contents = flexMainMenu(GET_EVENT["channelId"], GET_EVENT["level"])),
        FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
    ]
    ##發送回覆
    send_reply(GET_EVENT, False)
@handler.add(UnfollowEvent)
def handle_unfollow(event):
    remove_channel(getChannelId(event))
@handler.add(LeaveEvent)
def handle_leave(event):
    pass
    #remove_channel(getChannelId(event))

####################PostbackEvent處理區#################### 
@handler.add(PostbackEvent)
def handle_postback(event):
    ##取得EVENT物件
    GET_EVENT = get_event_obj(event)
    data = parse_qs(event.postback.data)
    
    ##發送回覆
    GET_EVENT = postback_processer(GET_EVENT, data)
    send_reply(GET_EVENT, False)

####################文字訊息處理區#################### 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    ##取得EVENT物件
    GET_EVENT = get_event_obj(event)
    GET_EVENT["lineMessage"] = event.message.text

    ##發送
    GET_EVENT = message_processer(GET_EVENT)
    send_reply(GET_EVENT, True)

####################貼圖訊息處理區#################### 
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    ##取得EVENT物件
    GET_EVENT = get_event_obj(event)
    GET_EVENT["lineMessage"] = event.message.package_id + ',' + event.message.sticker_id
    GET_EVENT["replyList"] = StickerSendMessage(package_id=event.message.package_id, sticker_id=event.message.sticker_id)
    GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 2, 'sticker']
    GET_EVENT["replyList"] = [GET_EVENT["replyList"], TextSendMessage(text=GET_EVENT["postfix"])] if GET_EVENT["postfix"] else GET_EVENT["replyList"]
    ##發送
    send_reply(GET_EVENT, True)

####################位置訊息處理區#################### 
@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    ##取得EVENT物件
    LOCATION_INFO = {
        "title": str(event.message.title),
        "addr": addr_format(str(event.message.address)),
        "lat": float(event.message.latitude),
        "lng": float(event.message.longitude)
    }
    GET_EVENT = get_event_obj(event)
    GET_EVENT["lineMessage"] = LOCATION_INFO["title"] + ',' + LOCATION_INFO["addr"] + ',' + str(LOCATION_INFO["lat"]) + ',' + str(LOCATION_INFO["lng"])
    
    ##發送
    GET_EVENT = location_processer(GET_EVENT, LOCATION_INFO)
    send_reply(GET_EVENT, True)


if __name__ == "__main__":
    app.run()