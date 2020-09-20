import os, sys, json, codecs, re

from linebot import (LineBotApi, WebhookHandler)
from linebot.models import *

#前往上層目錄
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
#導入env, model
from env import *
from model import *
#導入Managers
from Managers.channelManager import *
#導入Others
from Others.flexMessageJSON import *

#################### 訊息相關 ####################
##儲存收到的訊息
def store_received(msg, type, channelPK, userPK):
    query = """INSERT INTO line_received (type, message, channel_pk, user_pk) VALUES (%s,%s,%s,%s)"""
    values = (type, msg, channelPK, userPK,)
    operateDB(query, values)

##儲存機器人回覆
def store_replied(msg, valid, type, channelPK):
    query = """INSERT INTO line_replied (type, message, valid, channel_pk) VALUES (%s,%s,%s,%s)"""
    values = (type, msg, valid, channelPK,)
    operateDB(query, values)

##查詢收到的訊息
def get_received(channelPK, num):
    query = """SELECT * FROM line_received WHERE channel_pk=%s ORDER BY id DESC limit %s"""
    values = (channelPK, num,)
    dataRow = selectDB(query, values)
    return dataRow if len(dataRow) else []

##查詢機器人回覆
def get_replied(channelPK, num):
    query = """SELECT * FROM line_replied WHERE channel_pk=%s ORDER BY id DESC limit %s"""
    values = (channelPK, num,)
    dataRow = selectDB(query, values)
    return dataRow if len(dataRow) else []


##儲存收到的訊息
def store_pushed(type, title, message, channelId):
    query = """INSERT INTO line_pushed (type, title, message, channel_id) VALUES (%s,%s,%s,%s)"""
    values = (type, title, message, channelId,)
    operateDB(query, values)

##取得所有推播紀錄
def get_line_pushed_table():
    query = """SELECT id, type, title, message, channel_id FROM line_pushed"""
    dataRow = selectDB(query, None)
    return dataRow if len(dataRow) else []

#################### 推播相關 ####################
line_bot_api = LineBotApi(GET_SECRET("ACCESS_TOKEN"))

#一般推播處理
def pushing_process(type, title, content, channelId):
    message = []
    record = ''
    if type == 'text':
        message = TextSendMessage(text='【' + title + '】\n' + content)
        record = content
    elif type == 'flex':
        try:
            obj = json.loads(content)
            message = FlexSendMessage(alt_text=title, contents=obj)
            record = json.dumps(obj)
        except:
            return 'fail'
    elif type == 'image':
        if 'https://' in content and any(x in content for x in ['.jpg','.jpeg','.png']):
            message = ImageSendMessage(original_content_url=content, preview_image_url=content)
            record = content
        else:
            return 'fail'

    return pushing_to_channel(type, title, message, channelId, record)

#樣板推播處理
def pushing_template(title, content, channelId, template):
    message = []
    type = "flex"
    obj = content
    record = ''
    if template == "earthquake":
        try:
            message = FlexSendMessage(alt_text=title, contents=templateEarthquake(obj.get('location', ''), obj.get('M', '0'))) 
            record = json.dumps(templateEarthquake(obj.get('location', ''), obj.get('M', '0')))
        except:
            return 'fail'
    if template == "announcement":
        try:
            message = FlexSendMessage(alt_text=title, contents=templateAnnouncement(obj.get('title', ''), obj.get('content', ''), obj.get('date', '')))
            record = json.dumps(templateAnnouncement(obj.get('title', ''), obj.get('content', ''), obj.get('date', '')))
        except:
            return 'fail'
    
    return pushing_to_channel(type, title, message, channelId, record)

#發送推播
def pushing_to_channel(type, title, message, channel_id, record):
    try:
        if channel_id!=None:
            if channel_id=="ALL": pushing_to_all(type, title, message, record)  #廣播
            else: line_bot_api.push_message(channel_id, message)                #推播
        store_pushed(type, title, record, channel_id)
        return 'ok'
    except:
        return 'fail'

#發送廣播
def pushing_to_all(type, title, message, record):
    try:
        query = """SELECT channel_id FROM line_user"""
        dataRow = selectDB(query, None)
        datas = dataRow if len(dataRow) else []
        for data in datas:
            line_bot_api.push_message(data["channel_id"], message)
        store_pushed(type, title, record, "ALL")
        return 'ok'
    except:
        return 'fail'