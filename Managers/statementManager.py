import os, sys, json, codecs, re, random

#前往上層目錄
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
#導入env, model
from model import *
#導入Managers
from Managers.channelManager import *
from Managers.messageManager import *

#################### [查詢, 新增, 刪除, 調整權重, 取得回覆, 學過的詞]: [詞條] ####################
#查詢詞條
def get_statements(response, keyword='', channelPK=None):
    values = [response]
    hasKeyword = ''
    hasChannelPK = ''
    if keyword!="":
        hasKeyword = ' and keyword=%s'
        values.append(keyword)
    if channelPK!=None:
        hasChannelPK = ' and channel_pk=%s'
        values.append(channelPK)

    query = """SELECT * FROM line_statement WHERE response=%s""" +hasKeyword +hasChannelPK
    dataRow = selectDB(query, tuple(values))
    return dataRow if len(dataRow) else None

##新增詞條
def create_statement(keyword, responses, channelPK, userPK):
    for response in responses:
        #若詞條不存在於當前聊天室，才新增詞條
        if get_statements(response, keyword, channelPK)==None:
            query = "INSERT INTO line_statement(keyword, response, channel_pk, user_pk) VALUES(%s,%s,%s,%s)"
            values = (keyword, response, channelPK, userPK,)
            operateDB(query, values)
        #若詞條存在於當前聊天室，則權重+1
        else:
            adjust_priority(1, keyword, response, channelPK)
##刪除詞條
def delete_statement(keyword, responses, channelPK):
    for response in responses:
        query = """DELETE FROM line_statement WHERE keyword=%s and response=%s and channel_pk=%s"""
        values = (keyword, response, channelPK,)
        operateDB(query, values)

##調整詞條權重
def adjust_priority(case, keyword, response, channelPK=None):    
    #若詞條找不到，表示此句為自動接話模型、或廣泛搜尋模型，則增加一句自動學習詞條
    dataRow = get_statements(response, keyword, channelPK)
    if dataRow!=None:
        for data in dataRow:
            query = """UPDATE line_statement SET priority=%s WHERE id=%s"""
            new_priority = int(data['priority']) + case if int(data['priority'])>=0 else int(data['priority'])
            new_priority = 100 if new_priority>100 else new_priority
            values = (new_priority, data['id'],)
            operateDB(query, values)
    else:
        create_statement(keyword, [response], 0, 0)

##取得詞條回覆
def get_statement_response(keyword, channelPK, globalTalk, rand):
    #若關閉可以說其他人教過的話的功能，則以限制channelId的方式查詢
    strGlobalTalk = " and channel_pk!=0" if globalTalk else " and channel_pk=%s and channel_pk!=0"
    strRandomReply = ' and priority>=4 ORDER BY RAND() limit 1' if rand else ' and priority>0 ORDER BY likestrong DESC, RAND() DESC'
    
    query = """
    SELECT response, likestrong, priority FROM (  SELECT *,
                            CASE
                                WHEN UPPER(keyword) = UPPER(%s) THEN 5						# 完全相符
                                WHEN UPPER(%s) LIKE CONCAT('_',UPPER(keyword)) THEN 4		# input == .keyword (input去掉第一個字==keyword)
                                WHEN UPPER(keyword) LIKE CONCAT('_',UPPER(%s)) THEN 4		# .input == keyword (keyword去掉第一個字==input)
                                WHEN UPPER(%s) LIKE CONCAT(UPPER(keyword),'_') THEN 4		# input == keyword. (input去掉最後一個字==keyword)
                                WHEN UPPER(keyword) LIKE CONCAT(UPPER(%s),'_') THEN 4		# input. == keyword (keyword去掉最後一個字==input)
                                WHEN UPPER(%s) LIKE CONCAT('_',UPPER(keyword),'_') THEN 3	# input == .keyword. (input頭尾各去一個字==keyword)
                      			WHEN UPPER(keyword) LIKE CONCAT('_',UPPER(%s),'_') THEN 3	# .input. == keyword (keyword頭尾各去一個字==input)
                                WHEN UPPER(%s) LIKE CONCAT('__',UPPER(keyword)) THEN 2		# input == .keyword (input去掉前兩個字==keyword)
                                WHEN UPPER(keyword) LIKE CONCAT('__',UPPER(%s)) THEN 2		# .input == keyword (keyword去掉前兩個字==input)
                                WHEN UPPER(%s) LIKE CONCAT(UPPER(keyword),'__') THEN 2		# input == keyword. (input去掉最後兩個字==keyword)
                                WHEN UPPER(keyword) LIKE CONCAT(UPPER(%s),'__') THEN 2		# input. == keyword (keyword去掉最後兩個字==input)
                                WHEN UPPER(%s) LIKE CONCAT('__',UPPER(keyword),'__') THEN 1	# input == .keyword. (input頭尾各去兩個字==keyword)
                      			WHEN UPPER(keyword) LIKE CONCAT('__',UPPER(%s),'__') THEN 1	# .input. == keyword (keyword頭尾各去兩個字==input)
                                ELSE 0 
                            END AS likestrong
                    FROM line_statement) AS foo WHERE likestrong>0""" + strGlobalTalk + strRandomReply
    values = [keyword for i in range(0,13)] if globalTalk else [keyword for i in range(0,13)] + [channelPK]
    dataRow = selectDB(query, tuple(values))

    #找不到的話找找看自動學習的語料
    if not len(dataRow):
        query = """
        SELECT response, likestrong, priority FROM (  SELECT *,
                                CASE
                                WHEN UPPER(keyword) = UPPER(%s) THEN 5						# 完全相符
                                WHEN UPPER(%s) LIKE CONCAT('_',UPPER(keyword)) THEN 4		# input == .keyword (input去掉第一個字==keyword)
                                WHEN UPPER(keyword) LIKE CONCAT('_',UPPER(%s)) THEN 4		# .input == keyword (keyword去掉第一個字==input)
                                WHEN UPPER(%s) LIKE CONCAT(UPPER(keyword),'_') THEN 4		# input == keyword. (input去掉最後一個字==keyword)
                                WHEN UPPER(keyword) LIKE CONCAT(UPPER(%s),'_') THEN 4		# input. == keyword (keyword去掉最後一個字==input)
                                WHEN UPPER(%s) LIKE CONCAT('_',UPPER(keyword),'_') THEN 3	# input == .keyword. (input頭尾各去一個字==keyword)
                      			WHEN UPPER(keyword) LIKE CONCAT('_',UPPER(%s),'_') THEN 3	# .input. == keyword (keyword頭尾各去一個字==input)
                                WHEN UPPER(%s) LIKE CONCAT('__',UPPER(keyword)) THEN 2		# input == .keyword (input去掉前兩個字==keyword)
                                WHEN UPPER(keyword) LIKE CONCAT('__',UPPER(%s)) THEN 2		# .input == keyword (keyword去掉前兩個字==input)
                                WHEN UPPER(%s) LIKE CONCAT(UPPER(keyword),'__') THEN 2		# input == keyword. (input去掉最後兩個字==keyword)
                                WHEN UPPER(keyword) LIKE CONCAT(UPPER(%s),'__') THEN 2		# input. == keyword (keyword去掉最後兩個字==input)
                                WHEN UPPER(%s) LIKE CONCAT('__',UPPER(keyword),'__') THEN 1	# input == .keyword. (input頭尾各去兩個字==keyword)
                      			WHEN UPPER(keyword) LIKE CONCAT('__',UPPER(%s),'__') THEN 1	# .input. == keyword (keyword頭尾各去兩個字==input)
                                ELSE 0 
                                END AS likestrong
                        FROM line_statement) AS foo WHERE likestrong>0 and channel_pk=0 and priority>2 """
        query = query + " ORDER BY likestrong DESC, RAND() DESC"
        values = [keyword for i in range(0,13)]
        dataRow = selectDB(query, tuple(values))

    #加權取值
    if(len(dataRow)):
        totalWeight=0                                   #總權重
        totalDataRow=[]                                 #按權重數重新擺一次的DataRow
        topLikeStrong = int(dataRow[0]['likestrong'])   #只取本次抓取的詞條中，likestrong最高者
        for item in dataRow:
            if item['likestrong'] == topLikeStrong:         #捨棄likestrong非最高者
                totalWeight += int(item['priority'])                                #計入權重
                totalDataRow += [item for i in range(0, int(item['priority']))]     #依權重數依序丟入TotalDataRow
        random.shuffle(totalDataRow)                    #打亂TotalDataRow List
        ptr = random.randint(0, totalWeight-1)          #抽數字
        return totalDataRow[ptr]['response']            #取出
    else:
        return "我聽不懂啦！"

##取得所有學過的詞
def get_all_statement(channelPK, nickname):
    query = """SELECT keyword, response FROM line_statement WHERE channel_pk=%s and priority>=0 ORDER BY keyword"""
    values = (channelPK,)
    dataRow = selectDB(query, values)
    
    #建立回傳物件
    resCount = 0
    resData = {}
    dt = datetime.now(pytz.timezone("Asia/Taipei"))
    for data in dataRow:
        resCount+=1
        if data['keyword'] in resData: resData[data['keyword']].append(data['response'])
        else: resData[data['keyword']]=[data['response']]
    keyCount=len(resData)

    #建立訊息總數物件
    query = """SELECT count(*) AS all_statement FROM line_statement WHERE priority>=0"""
    dataRow = selectDB(query, None)
    count_statement = dataRow[0]['all_statement'] if len(dataRow) else 0

    query = """SELECT count(*) AS all_channel FROM line_statement WHERE priority>=0 GROUP BY channel_pk"""
    dataRow = selectDB(query, None)
    count_channel = len(dataRow)
    
    #回傳物件
    return {
        "keyCount": keyCount,
        "resCount": resCount,
        "datetime": datetime.strftime(dt, '%Y{y}%m{m}%d{d} %H:%M').format(y='年', m='月', d='日'),
        "resData": resData if len(resData) else None,
        "count_statement": count_statement,
        "count_channel": count_channel,
        "nickname": nickname
    }

##取得所有學過的詞
def get_line_statement_table(userId=None):
    if not userId:
        return []
    userPK = get_pk_by_channel_id(userId)
    strUserPK = "" if userId=="ALL" else " WHERE user_pk='"+userPK+"'"
    query = """SELECT id, keyword, response, channel_pk, user_pk, checked, priority FROM line_statement""" + strUserPK
    dataRow = selectDB(query, None)
    return dataRow if len(dataRow) else []

#後綴字詞
def get_postfix():
    query = """SELECT content FROM line_postfix WHERE CURRENT_TIMESTAMP()>=start_date and CURRENT_TIMESTAMP()<=last_date ORDER BY RAND() limit 1"""
    dataRow = selectDB(query, None)
    return dataRow[0]['content'] if len(dataRow) else None


#################### 依詞條ID進行操作 ####################
##調整詞條黑名單
def operate_statement(action, adjust, statement_id):
    if action == "delete":
        query = "DELETE FROM line_statement WHERE id=%s"
        for id in statement_id:
            values = (id,)
            operateDB(query, values)
    elif action == "checked":
        for id in statement_id:
            #取原權重
            query = """SELECT priority FROM line_statement WHERE id=%s"""
            dataRow = selectDB(query, (id,))
            iniPriority = dataRow[0]['priority']
            #if 指定權重 -> 指定權重； else if 無指定權重但原權重<0 -> 指定權重為5； else 不指定權重
            strPriority = ", priority='"+str(adjust)+"'" if adjust else ", priority='4'" if iniPriority<0 else ""
            query = "UPDATE line_statement SET checked='checked'"+strPriority+" WHERE id=%s"
            values = (id,)
            operateDB(query, values)

#################### 主聊天功能 ####################
##學說話暫存詞條
def create_temp_statement(keyword, response, channelPK, userPK):
    delete_expired_temp_statement() #先刪除暫存詞條
    query = "INSERT INTO line_temp_statement(keyword, response, channel_pk, user_pk) VALUES(%s,%s,%s,%s)"
    values = (keyword, response, channelPK, userPK)
    id = operateDB(query, values)
    return id

##學說話取得暫存詞條
def get_temp_statement(id):
    query = """SELECT * FROM line_temp_statement WHERE id=%s"""
    dataRow = selectDB(query, (id,))
    delete_temp_statement(id)
    return dataRow[0] if len(dataRow) else None

##學說話刪除暫存詞條
def delete_temp_statement(id):
    query = """DELETE FROM line_temp_statement WHERE id=%s"""
    operateDB(query, (id,))

##刪除3天以上沒人按的暫存詞條
def delete_expired_temp_statement():
    query = """DELETE FROM line_temp_statement WHERE create_at < DATE_SUB(NOW(), INTERVAL 3 DAY)"""
    operateDB(query, None)