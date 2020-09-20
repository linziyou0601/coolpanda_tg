import os, sys, json, codecs, re, random

#前往上層目錄
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
#導入env, model
from model import *
#導入Others
from Others.flexMessageJSON import *
from Others.keywordFinder import *
#導入Managers
from Managers.channelManager import *
from Managers.messageManager import *
#導入Services
from Services.crawlerService import *

#################### 爬蟲查詢功能 ####################
#[爬蟲查詢] 天氣查詢
def crawler_weather_function(GET_EVENT, last_receives, LOCATION_INFO):
    #若上語句中有問天氣且沒給地點
    future = True if "未來" in key(last_receives[0]['message']) else False
    flexObject = flexWeather72HR(getWeather(LOCATION_INFO["lat"], LOCATION_INFO["lng"], None, future)) if future else flexWeather(getWeather(LOCATION_INFO["lat"], LOCATION_INFO["lng"], None, future))
    GET_EVENT["replyList"] = FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
    GET_EVENT["replyLog"] = [flexObject[0], 0, 'flex']
    return GET_EVENT

#[爬蟲查詢] 空汙查詢
def crawler_AQI_function(GET_EVENT, LOCATION_INFO):
    #若上語句中有問空汙且沒給地點
    flexObject = flexAQI(getAQI(LOCATION_INFO["lat"], LOCATION_INFO["lng"], None))
    GET_EVENT["replyList"] = FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
    GET_EVENT["replyLog"] = [flexObject[0], 0, 'flex']
    return GET_EVENT

#[爬蟲查詢] 特約藥局查詢
# def crawler_mask_function(GET_EVENT, LOCATION_INFO):
#     mask_list = getMask(LOCATION_INFO["lat"], LOCATION_INFO["lng"], None)
#     GET_EVENT["replyList"] = [
#         TextSendMessage(text="以下是距離最近的10間藥局"),
#         FlexSendMessage(alt_text="以下是距離最近的10間藥局", contents = flexWhereMask(mask_list))
#     ]
#     GET_EVENT["replyLog"] = ["特約藥局查詢", 0, 'flex']
#     return GET_EVENT


#################### 處理區 ####################
def location_processer(GET_EVENT, LOCATION_INFO):
    last_receives = get_received(GET_EVENT["channelPK"], 5)
    create_location(LOCATION_INFO["addr"], LOCATION_INFO["lat"], LOCATION_INFO["lng"])
    
    #天氣查詢 [不限個人, 等級0+]    # 若上一句key值為「(目前天氣|未來天氣)$」且不為「地名(目前天氣|未來天氣)$」
    if any((re.search("(目前天氣|未來天氣)$", key(s['message'])) and not re.sub("(目前天氣|未來天氣)", "", key(s['message']))) for s in last_receives[0:1]):
        GET_EVENT = crawler_weather_function(GET_EVENT, last_receives, LOCATION_INFO)
    #空汙查詢 [不限個人, 等級0+]    # 若上一句key值為「(空汙查詢)$」且不為「地名(空汙查詢)$」 或 本句key值為「(地名)*(空汙查詢)$」
    elif any((re.search("(空汙查詢)$", key(s['message'])) and not re.sub("(空汙查詢)", "", key(s['message']))) for s in last_receives[0:1]):
        GET_EVENT = crawler_AQI_function(GET_EVENT, LOCATION_INFO)
    #特約藥局查詢 [不限個人, 等級0+]
    # elif any(key(s['message'])=="特約藥局查詢" for s in last_receives[0:1]):
    #     GET_EVENT = crawler_mask_function(GET_EVENT, LOCATION_INFO)
    
    ##回傳
    return GET_EVENT