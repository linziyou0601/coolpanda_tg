import os, sys, json, codecs, re, random

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

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
from Managers.statementManager import *
# #導入Services
# from Services.crawlerService import *
# from Services.lotteryService import *

#################### 對答功能 ####################
#[對答] 學說話
def learn_statement_function(GET_EVENT, last_receives):
    if key(GET_EVENT["lineMessage"])=="學說話":
        GET_EVENT["replyList"] = [{"type": "text", "msg": "請告訴我要學的關鍵字"}]
        GET_EVENT["replyLog"] = ["請告訴我要學的關鍵字", 0, 'text']
    elif key(last_receives[0]['message'])=="學說話":
        GET_EVENT["replyList"] = [{"type": "text", "msg": "我要回應什麼？"}]
        GET_EVENT["replyLog"] = ["我要回應什麼？", 0, 'text']
    else:
        temp_id = create_temp_statement(last_receives[0]['message'], GET_EVENT["lineMessage"], GET_EVENT["channelPK"], last_receives[1]['user_pk'])
        markupObject = markupLearnConfirm(last_receives[0]['message'], GET_EVENT["lineMessage"], temp_id)
        GET_EVENT["replyList"] = [{"type": "markup", "msg": markupObject[0], "markup": markupObject[1]}]
        GET_EVENT["replyLog"] = ["確認詞條內容", 0, 'markup']
    return GET_EVENT

#[對答] 降低詞條優先度
def bad_statement_function(GET_EVENT):
    dataReceived = get_received(GET_EVENT["channelPK"], 1)
    dataReplied = get_replied(GET_EVENT["channelPK"], 1)
    adjust_priority(-3, dataReceived[0]['message'], dataReplied[0]['message'])
    GET_EVENT["replyList"] = [{"type": "text", "msg": "下次不會了～"+GET_EVENT["postfix"]}]
    GET_EVENT["replyLog"] = ["好哦～", 0, 'text']
    return GET_EVENT

# #################### 爬蟲查詢功能 ####################
# #[爬蟲查詢] 天氣查詢
# def crawler_weather_function(GET_EVENT, last_receives):
#     #若本語句中有問天氣
#     if re.search("(目前天氣|未來天氣)$", key(GET_EVENT["lineMessage"])):
#         future = True if "未來" in key(GET_EVENT["lineMessage"]) else False
#         this_site = re.sub("(目前天氣|未來天氣)", "", key(GET_EVENT["lineMessage"]))
#         #若本語句中有直接給地點
#         if this_site:
#             weather = getWeather(None, None, this_site, future)
#             if weather:
#                 flexObject = flexWeather72HR(weather) if future else flexWeather(weather)
#                 GET_EVENT["replyList"] = FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
#                 GET_EVENT["replyLog"] = [flexObject[0], 0, 'flex']
#         #問地點
#         else:
#             GET_EVENT["replyList"] = FlexSendMessage(alt_text = "請輸入要查詢的位址，或傳送位址訊息", contents = flexTellMeLocation())
#             GET_EVENT["replyLog"] = ["要查詢的地點是？", 0, 'flex']
#     #若上語句中有問天氣且沒給地點
#     else:
#         future = True if "未來" in key(last_receives[0]['message']) else False
#         weather = getWeather(None, None, GET_EVENT["lineMessage"], future)
#         if weather:
#             flexObject = flexWeather72HR(weather) if future else flexWeather(weather)
#             GET_EVENT["replyList"] = FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
#             GET_EVENT["replyLog"] = [flexObject[0], 0, 'flex']
#     return GET_EVENT

# #[爬蟲查詢] 空汙查詢
# def crawler_AQI_function(GET_EVENT):
#     #若本語句中有問空汙
#     if re.search("(空汙查詢)$", key(GET_EVENT["lineMessage"])):
#         this_site = re.sub("(空汙查詢)", "", key(GET_EVENT["lineMessage"]))
#         #若本語句中有直接給地點
#         if this_site:
#             aqi = getAQI(None, None, this_site)
#             if aqi:
#                 flexObject = flexAQI(aqi)
#                 GET_EVENT["replyList"] = FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
#                 GET_EVENT["replyLog"] = [flexObject[0], 0, 'flex']
#         #問地點
#         else:
#             GET_EVENT["replyList"] = FlexSendMessage(alt_text = "請輸入要查詢的位址，或傳送位址訊息", contents = flexTellMeLocation())
#             GET_EVENT["replyLog"] = ["要查詢的地點是？", 0, 'flex']
#     #若上語句中有問空汙且沒給地點
#     else:
#         aqi = getAQI(None, None, GET_EVENT["lineMessage"])
#         if aqi:
#             flexObject = flexAQI(aqi)
#             GET_EVENT["replyList"] = FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
#             GET_EVENT["replyLog"] = [flexObject[0], 0, 'flex']
#     return GET_EVENT

#################### 功能設定 ####################
#[功能設定] 目前狀態
def current_status_function(GET_EVENT):
    status = {
        "global_talk_text": "所有人教的" if GET_EVENT['global_talk'] else "本頻道教的", 
        "mute_text": "安靜" if GET_EVENT['mute'] else "可以說話", 
        "global_talk": GET_EVENT['global_talk'], 
        "mute": GET_EVENT['mute']
    }
    markupObject = markupStatusMenu(status)
    GET_EVENT["replyList"] = [{"type": "markup", "msg": markupObject[0], "markup": markupObject[1]}]
    GET_EVENT["replyLog"] = ["目前狀態", 0, 'markup']
    return GET_EVENT
#[功能設定] 說話模式調整
def edit_global_talk_function(GET_EVENT):
    if any((s+"說別人教的話") in GET_EVENT["lineMessage"] for s in ["不可以", "不能", "不行", "不要", "不准"]): edit_channel_global_talk(GET_EVENT["channelId"], 0)
    elif "說別人教的話" in GET_EVENT["lineMessage"]: edit_channel_global_talk(GET_EVENT["channelId"], 1)
    GET_EVENT["replyList"] = [{"type": "text", "msg": "好哦～"+GET_EVENT["postfix"]}]
    GET_EVENT["replyLog"] = ["好哦～", 0, 'text']
    return GET_EVENT
#[功能設定] 安靜開關
def edit_mute_function(GET_EVENT):
    if any(s in GET_EVENT["lineMessage"] for s in ["熊貓說話", "熊貓講話"]): edit_channel_mute(GET_EVENT["channelId"], 0)
    elif any(s in GET_EVENT["lineMessage"] for s in ["熊貓安靜", "熊貓閉嘴"]): edit_channel_mute(GET_EVENT["channelId"], 1)
    GET_EVENT["replyList"] = [{"type": "text", "msg": "好哦～"+GET_EVENT["postfix"]}]
    GET_EVENT["replyLog"] = ["好哦～", 0, 'text']
    return GET_EVENT

#################### 聊天 ####################
##齊推
def chat_echo2(lineMessage, channelPK):
    if not get_received(channelPK, 3) or all(lineMessage!=msg['message'] or msg['type']!='text' for msg in get_received(channelPK, 3)): return False
    elif not get_replied(channelPK, 1) or get_replied(channelPK, 1)[0]['message']==lineMessage: return False
    else: return True
##聊天回覆
def chat_function(GET_EVENT):
    #資料庫回覆(或隨機回覆)
    rand = 1 if GET_EVENT["lineMessage"][0:2] in ['熊貓', '抽籤'] else 0
    firstIndex = 0 if not rand else 2
    response = get_statement_response(GET_EVENT["lineMessage"][firstIndex:], GET_EVENT["channelPK"], GET_EVENT["global_talk"], rand)
    valid = 0 if response=="我聽不懂啦！" else 2
    res_type = 'image' if response[0:8]=='https://' and any(x in str.lower(response) for x in ['.jpg','.jpeg','.png']) else 'text'
    GET_EVENT["replyLog"] = [response, valid, res_type]
    #齊推
    if not GET_EVENT["replyLog"][1] and chat_echo2(GET_EVENT["lineMessage"], GET_EVENT["channelPK"]):
        GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'text']
    #本次要回的話
    if GET_EVENT["replyLog"][2]=='image':
        GET_EVENT["replyList"] = [{"type": "image", "msg": GET_EVENT["replyLog"][0]}]  
    else:
        GET_EVENT["replyList"] = [{"type": "text", "msg": GET_EVENT["replyLog"][0]+GET_EVENT["postfix"]}] if GET_EVENT["replyLog"][0]!='我聽不懂啦！' or GET_EVENT["channelId"][0]=='U' else []
    return GET_EVENT


#################### 處理區 ####################
def message_processer(GET_EVENT):
    last_receives = get_received(GET_EVENT["channelPK"], 5)

    ## ==================== 對答 ==================== ##
    #學說話 [不限個人, 等級0+]
    if any(key(s['message'])=="學說話" for s in last_receives[0:2]) or key(GET_EVENT["lineMessage"])=="學說話":
        GET_EVENT = learn_statement_function(GET_EVENT, last_receives)
    #降低詞條優先度 [不限個人, 等級0+]
    elif key(GET_EVENT["lineMessage"])=="壞壞":
        GET_EVENT = bad_statement_function(GET_EVENT)


    # ## ==================== 爬蟲查詢 ==================== ##
    # #天氣查詢 [不限個人, 等級0+]    # 若上一句key值為「(目前天氣|未來天氣)$」且不為「地名(目前天氣|未來天氣)$」 或 本句key值為「(地名)*(目前天氣|未來天氣)$」
    # elif any((re.search("(目前天氣|未來天氣)$", key(s['message'])) and not re.sub("(目前天氣|未來天氣)", "", key(s['message']))) for s in last_receives[0:1]) or re.search("(目前天氣|未來天氣)$", key(GET_EVENT["lineMessage"])):
    #     GET_EVENT = crawler_weather_function(GET_EVENT, last_receives)
    # #空汙查詢 [不限個人, 等級0+]    # 若上一句key值為「(空汙查詢)$」且不為「地名(空汙查詢)$」 或 本句key值為「(地名)*(空汙查詢)$」
    # elif any((re.search("(空汙查詢)$", key(s['message'])) and not re.sub("(空汙查詢)", "", key(s['message']))) for s in last_receives[0:1]) or re.search("(空汙查詢)$", key(GET_EVENT["lineMessage"])):
    #     GET_EVENT = crawler_AQI_function(GET_EVENT)


    # ## ==================== 機率運勢 [function未拆出] ==================== ##
    # #擲筊選單 [不限個人, 等級0+] 
    # elif key(GET_EVENT["lineMessage"])=="擲筊": 
    #     GET_EVENT["replyList"] = FlexSendMessage(alt_text= "擲筊選單", contents=flexMenuDevinate())
    #     GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'flex']
    # #抽籤詩選單 [不限個人, 等級0+]
    # elif key(GET_EVENT["lineMessage"])=="抽籤詩":
    #     GET_EVENT["replyList"] = FlexSendMessage(alt_text= "抽籤詩選單", contents=flexMenuFortuneStick())
    #     GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'flex']
    # #抽塔羅選單 [不限個人, 等級0+]
    # elif key(GET_EVENT["lineMessage"])=="抽塔羅":
    #     GET_EVENT["replyList"] = FlexSendMessage(alt_text= "抽塔羅選單", contents=flexMenuTarot())
    #     GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'flex']
    
    
    ## ==================== 教學選單 [function未拆出] ==================== ##
    #主選單 [不限個人, 等級0+]
    elif key(GET_EVENT["lineMessage"])=="主選單":
        GET_EVENT["replyList"] = [{"type": "markup", "msg": "【主選單】\n嗨，我是酷熊貓！ ", "markup": markupMainMenu()}]
        GET_EVENT["replyLog"] = ["主選單", 0, 'markup']
    #酷熊貓會做什麼選單 [不限個人, 等級0+]
    elif key(GET_EVENT["lineMessage"])=="功能一覽":
        GET_EVENT["replyList"] = [{"type": "markup", "msg": "功能一覽", "markup": markupHowDo()}]
        GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'markup']
    #聊天教學選單 [不限個人, 等級0+] 
    elif key(GET_EVENT["lineMessage"])=="怎麼聊天": 
        markupObject = markupTeachChat()
        GET_EVENT["replyList"] = [{"type": "markup", "msg": markupObject[0], "markup": markupObject[1]}]
        GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'markup']
    # #抽籤教學選單 [不限個人, 等級0+] 
    # elif key(GET_EVENT["lineMessage"])=="怎麼抽籤": 
    #     GET_EVENT["replyList"] = FlexSendMessage(alt_text= "怎麼抽籤", contents=flexTeachLottery())
    #     GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'flex']
    #學說話教學選單 [不限個人, 等級0+] 
    elif key(GET_EVENT["lineMessage"])=="怎麼學說話": 
        markupObject = markupTeachLearn()
        GET_EVENT["replyList"] = [{"type": "markup", "msg": markupObject[0], "markup": markupObject[1]}]
        GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'markup']
    #本聊天窗所有教過的東西 [不限個人, 等級0+]
    elif key(GET_EVENT["lineMessage"])=="學過的話":
        ##你會說什麼
        nickname = "這裡" if GET_EVENT["channelId"][0]!='U' else "你"
        markupObject = markupWhatCanSay(get_all_statement(GET_EVENT["channelPK"], nickname))
        GET_EVENT["replyList"] = [{"type": "text", "msg": markupObject[0]}]
        GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'markup']
    #抽籤式回答教學選單 [不限個人, 等級0+]
    elif key(GET_EVENT["lineMessage"])=="怎麼抽籤式回答":
        markupObject = markupTeachChatRandom()
        GET_EVENT["replyList"] = [{"type": "markup", "msg": markupObject[0], "markup": markupObject[1]}]
        GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'markup']
    # #查氣象教學選單 [不限個人, 等級0+] 
    # elif key(GET_EVENT["lineMessage"])=="怎麼查氣象": 
    #     GET_EVENT["replyList"] = FlexSendMessage(alt_text= "怎麼查氣象", contents=flexTeachMeteorology())
    #     GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'flex']
    # #查天氣教學選單 [不限個人, 等級0+] 
    # elif key(GET_EVENT["lineMessage"])=="怎麼查天氣": 
    #     GET_EVENT["replyList"] = FlexSendMessage(alt_text= "怎麼查天氣", contents=flexTeachWeather())
    #     GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'flex']
    # #查空汙教學選單 [不限個人, 等級0+] 
    # elif key(GET_EVENT["lineMessage"])=="怎麼查空汙": 
    #     GET_EVENT["replyList"] = FlexSendMessage(alt_text= "怎麼查空汙", contents=flexTeachAQI())
    #     GET_EVENT["replyLog"] = [GET_EVENT["lineMessage"], 0, 'flex']
    

    ## ==================== 功能設定 ==================== ##
    #目前狀態 [不限個人, 等級0+]
    elif key(GET_EVENT["lineMessage"])=="目前狀態":
        GET_EVENT = current_status_function(GET_EVENT)
    #說話模式調整 [不限個人, 等級0+]
    elif key(GET_EVENT["lineMessage"])=="說話模式調整":
        GET_EVENT = edit_global_talk_function(GET_EVENT)
    #安靜開關 [不限個人, 等級0+]
    elif key(GET_EVENT["lineMessage"])=="聊天狀態調整":
        GET_EVENT = edit_mute_function(GET_EVENT)


    ## ==================== 聊天 ==================== ##
    #非安靜狀態
    elif not GET_EVENT['mute']: 
        GET_EVENT = chat_function(GET_EVENT)


    ## ==================== 訊息反饋建立區 ==================== ##
    if GET_EVENT["replyLog"][1]:
        temp_id = create_temp_statement(GET_EVENT["lineMessage"], GET_EVENT["replyLog"][0], 0, 0)
        markupObject = markupResponseFeedback(GET_EVENT["replyList"][0]["msg"], temp_id)
        GET_EVENT["replyList"] = [{"type": "markup", "msg": markupObject[0], "markup": markupObject[1]}]
    
    ##回傳
    return GET_EVENT