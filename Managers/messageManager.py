import os, sys, json, codecs, re

import telegram
from telegram.ext import Dispatcher, MessageHandler, Filters, Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ParseMode

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
    query = """INSERT INTO tg_received (type, message, channel_pk, user_pk) VALUES (%s,%s,%s,%s)"""
    values = (type, msg, channelPK, userPK,)
    operateDB(query, values)

##儲存機器人回覆
def store_replied(msg, valid, type, channelPK):
    query = """INSERT INTO tg_replied (type, message, valid, channel_pk) VALUES (%s,%s,%s,%s)"""
    values = (type, msg, valid, channelPK,)
    operateDB(query, values)

##查詢收到的訊息
def get_received(channelPK, num):
    query = """SELECT * FROM tg_received WHERE channel_pk=%s ORDER BY id DESC limit %s"""
    values = (channelPK, num,)
    dataRow = selectDB(query, values)
    return dataRow if len(dataRow) else []

##查詢機器人回覆
def get_replied(channelPK, num):
    query = """SELECT * FROM tg_replied WHERE channel_pk=%s ORDER BY id DESC limit %s"""
    values = (channelPK, num,)
    dataRow = selectDB(query, values)
    return dataRow if len(dataRow) else []

##儲存收到的訊息
def store_pushed(type, record, channelId):
    query = """INSERT INTO tg_pushed (type, record, channel_id) VALUES (%s,%s,%s)"""
    values = (type, record, channelId,)
    operateDB(query, values)

##取得所有推播紀錄
def get_line_pushed_table():
    query = """SELECT id, type, record, channel_id FROM tg_pushed"""
    dataRow = selectDB(query, None)
    return dataRow if len(dataRow) else []

#################### 推播相關 ####################
bot = telegram.Bot(token=(GET_SECRET("TELEGRAM_TOKEN")))

#一般推播處理
def pushing_process(type, content, channelId):
    message = ""
    markup = None
    record = ""
    if type == 'text':
        message = content["msg"]
    elif type == 'markup':
        message = content["msg"]
        markup = json.dumps(content["markup"])
    elif type == 'image':
        if 'https://' in content["msg"] and any(x in content["msg"] for x in ['.jpg','.jpeg','.png']):
            message = content["msg"]
        else:
            return 'fail'
    
    record = json.dumps(content)

    return pushing_to_channel(type, message, markup, channelId, record)

#發送推播
def pushing_to_channel(type, message, markup, channel_id, record):
    try:
        if channel_id!=None:
            if channel_id=="ALL": pushing_to_all(type, message, markup, record)                   #廣播
            else: 
                if type == 'image': bot.send_photo(chat_id = channel_id, photo = message, reply_markup = markup)#圖片推播
                else: bot.send_message(chat_id = channel_id, text = message, reply_markup = markup)             #推播
        store_pushed(type, record, channel_id)
        return 'ok'
    except:
        return 'fail'

#發送廣播
def pushing_to_all(type, message, markup, record):
    try:
        query = """SELECT channel_id FROM line_user"""
        dataRow = selectDB(query, None)
        datas = dataRow if len(dataRow) else []
        for data in datas:
            if type == 'image': bot.send_photo(chat_id = data["channel_id"], photo = message, reply_markup = markup)#圖片推播
            else: bot.send_message(chat_id = data["channel_id"], text = message, reply_markup = markup)             #推播
        store_pushed(type, record, "ALL")
        return 'ok'
    except:
        return 'fail'