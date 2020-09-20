import os, sys, json, codecs, re

from linebot import (LineBotApi, WebhookHandler)
from linebot.models import *

#前往上層目錄
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
#導入env, model
from env import *
from model import *

#################### 取得資料庫中的經緯資訊 ####################
#經緯資訊
def get_all_location():
    query = """SELECT address, lat, lng FROM line_location"""
    dataRow = selectDB(query, None)
    result_dict = {}
    if len(dataRow):
        for row in dataRow:
            result_dict[row['address']] = {'lat': row['lat'], 'lng': row['lng']}
    return result_dict
#經緯資訊
def get_location(location):
    query = """SELECT lat, lng FROM line_location WHERE address = %s"""
    dataRow = selectDB(query, (location,))
    return dataRow[0] if len(dataRow) else None
#建立經緯資訊
def create_location(address, lat, lng):
    if not get_location(address):
        query = """INSERT INTO line_location (address, lat, lng) VALUES (%s, %s, %s)"""
        values = (address, lat, lng,)
        operateDB(query, values) 