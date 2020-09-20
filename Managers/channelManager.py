import os, sys, json, codecs, re

from linebot import (LineBotApi, WebhookHandler)
from linebot.models import *

#前往上層目錄
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
#導入env, model
from env import *
from model import *

#################### 金鑰相關 ####################
#取得金鑰
def GET_SECRET(name):
    query = """SELECT * FROM api_key WHERE name = %s"""
    values = (name,)
    dataRow = selectDB(query, values)
    return dataRow[0]['secret'] if len(dataRow) else ""

#################### 使用者相關 ####################
#建立新使用者
def create_channel(channelId):
    if get_channel(channelId)==None:
        query = """INSERT INTO tg_user (channel_id) VALUES (%s)"""
        values = (channelId,)
        operateDB(query, values)

#移除使用者
def remove_channel(channelId):
    querys = ["""DELETE s FROM line_temp_statement s LEFT JOIN tg_user u ON s.channel_pk = u.id WHERE u.channel_id = %s""",
              """DELETE s FROM line_temp_statement s LEFT JOIN tg_user u ON s.user_pk = u.id WHERE u.channel_id = %s""",
              """DELETE s FROM line_statement s LEFT JOIN tg_user u ON s.channel_pk = u.id WHERE u.channel_id = %s""",
              """DELETE s FROM line_statement s LEFT JOIN tg_user u ON s.user_pk = u.id WHERE u.channel_id = %s""",
              """DELETE s FROM tg_replied s LEFT JOIN tg_user u ON s.channel_pk = u.id WHERE u.channel_id = %s""",
              """DELETE s FROM tg_received s LEFT JOIN tg_user u ON s.channel_pk = u.id WHERE u.channel_id = %s""",
              """DELETE s FROM tg_received s LEFT JOIN tg_user u ON s.user_pk = u.id WHERE u.channel_id = %s""",
              """DELETE FROM tg_user WHERE channel_id = %s """]
    values = (channelId,)
    for query in querys:
        operateDB(query, values)

#查詢使用者
def get_channel(channelId):
    query = """SELECT * FROM tg_user WHERE channel_id = %s"""
    values = (channelId,)
    dataRow = selectDB(query, values)
    return dataRow[0] if len(dataRow) else None

#查詢user Table 主鍵
def get_pk_by_channel_id(channelId):
    if channelId == None: return None
    channelData = get_channel(channelId)
    return channelData["id"] if channelData else None

#依主鍵查詢user Table channelId
def get_channel_id_by_pk(pk):
    query = """SELECT * FROM tg_user WHERE id = %s"""
    values = (pk,)
    dataRow = selectDB(query, values)
    return dataRow[0]['channel_id'] if len(dataRow) else None

##修改說話狀態
def edit_channel_global_talk(channelId, value):
    query = """UPDATE tg_user SET global_talk=%s WHERE channel_id=%s"""
    values = (value, channelId,)
    operateDB(query, values)

##修改安靜狀態
def edit_channel_mute(channelId, value):
    query = """UPDATE tg_user SET mute=%s WHERE channel_id=%s"""
    values = (value, channelId,)
    operateDB(query, values)