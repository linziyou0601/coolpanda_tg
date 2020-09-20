import os, sys, json, codecs, re, random

#前往上層目錄
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
#導入env, model
from model import *
#導入Others
from Others.flexMessageJSON import *
#導入Managers
from Managers.channelManager import *
from Managers.messageManager import *
from Managers.statementManager import *
#導入Services
from Services.crawlerService import *
from Services.lotteryService import *
from Services.learnService import *

#################### 處理區 ####################
def postback_processer(GET_EVENT, data):
    #----------------------------------------#
    ##確認詞條內容
    if data['action'][0]=='confirm_learn':
        temp_statement = get_temp_statement(data['id'][0])
        if temp_statement:
            create_statement(temp_statement['keyword'], [temp_statement['response']], temp_statement['channel_pk'], temp_statement['user_pk'])
            adjust_exp(temp_statement['user_pk'], 1)
            GET_EVENT["replyList"] = TextSendMessage(text="好哦已新增～"+GET_EVENT['postfix'])
    ##放棄詞條內容
    if data['action'][0]=='cancel_learn':
        temp_statement = get_temp_statement(data['id'][0])
        if temp_statement:
            delete_temp_statement(data['id'][0])
            GET_EVENT["replyList"] = TextSendMessage(text="已放棄新增～"+GET_EVENT['postfix'])
    #----------------------------------------#
    ##詞條有幫助
    if data['action'][0]=='valid_response':
        temp_statement = get_temp_statement(data['id'][0])
        if temp_statement:
            feedback_learn_model(temp_statement['keyword'], temp_statement['response'])
            GET_EVENT["replyList"] = TextSendMessage(text="感謝您的回饋～"+GET_EVENT['postfix'])
    ##詞條無幫助
    if data['action'][0]=='refuse_response':
        temp_statement = get_temp_statement(data['id'][0])
        if temp_statement:
            delete_temp_statement(data['id'][0])
            feedback_abandon_model(temp_statement['keyword'], temp_statement['response'])
            GET_EVENT["replyList"] = TextSendMessage(text="感謝您的回饋～"+GET_EVENT['postfix'])
    #----------------------------------------#
    ##傳送地點內容
    if data['action'][0]=='get_map':
        GET_EVENT["replyList"] = LocationSendMessage(title=data['title'][0], address=data['addr'][0], latitude=data['lat'][0], longitude=data['lng'][0])
    #----------------------------------------#
    ##擲筊
    if data['action'][0]=='devinate':
        flexObject = flexDevinate(getDevinate())
        GET_EVENT["replyList"] = FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
    ##抽籤詩
    if data['action'][0]=='fortuneStick':
        flexObject = flexFortuneStick(getFortuneStick())
        GET_EVENT["replyList"] = FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1]) 
    ##籤解
    if data['action'][0]=='meaning_fortuneStick':
        flexObject = flexMeaningFortuneStick(getMeaningFortuneStick(int(data['id'][0])))
        GET_EVENT["replyList"] = FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
    ##抽塔羅
    if data['action'][0]=='draw_tarot':
        flexObject = flexTarot(getTarot(int(data['num'][0])))
        GET_EVENT["replyList"] = FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
    ##塔羅牌義
    if data['action'][0]=='meaning_tarot':
        flexObject = flexMeaningTarot(getMeaningTarot(int(data['id'][0])))
        GET_EVENT["replyList"] = FlexSendMessage(alt_text = flexObject[0], contents = flexObject[1])
    
    
    ##回傳
    return GET_EVENT