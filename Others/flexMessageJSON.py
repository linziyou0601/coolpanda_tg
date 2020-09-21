from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

#==============================================#
#                     選單類                    #
#==============================================#
##主選單
def markupMainMenu():
    return ReplyKeyboardMarkup(
                [[KeyboardButton("熊貓會做什麼")],
                [KeyboardButton("目前狀態")]]
           )

##你會做什麼
def markupHowDo():
    # return ReplyKeyboardMarkup(
    #             [[KeyboardButton('怎麼聊天')],
    #             [KeyboardButton('怎麼查氣象')], 
    #             [KeyboardButton('怎麼抽籤')]]
    #        )
    return ReplyKeyboardMarkup(
                [[KeyboardButton('怎麼聊天')]]
           )

##狀態選單
def markupStatusMenu(object):
    return [
        "目前狀態：\n說話模式："+object["global_talk_text"]+"\n聊天狀態："+object["mute_text"],
        ReplyKeyboardMarkup(
                [[KeyboardButton('不可以說別人教的話' if object["global_talk"] else '可以說別人教的話'), KeyboardButton('熊貓講話' if object["mute"] else '熊貓安靜')],
                 [KeyboardButton('目前狀態'), KeyboardButton('主選單')]]
        )
    ]


#==============================================#
#                     聊天類                    #
#==============================================#
#==========回應+反饋==========#
def markupResponseFeedback(res, id):
    return [
        res,
        InlineKeyboardMarkup(
            [[InlineKeyboardButton("👍", callback_data="action=valid_response&id="+str(id)),
              InlineKeyboardButton("👎", callback_data="action=refuse_response&id="+str(id))]]
        )
    ]

#==========教學==========#
##聊天教學
def markupTeachChat():
    return [
        "【聊天功能】\n本熊貓會根據學過的話回答。點擊下方按鈕查看如何教我說話。",
        ReplyKeyboardMarkup(
                [[KeyboardButton('怎麼學說話')],
                 [KeyboardButton('目前狀態')], 
                 [KeyboardButton('主選單')]]
        )
    ]

##學說話教學
def markupTeachLearn():
    return [
        "【如何教我說話】\n啟動學習模式： `學說話` \n啟動後，請依提示文字，依序輸入「問」與「答」，並在最後進行確認。\n降低詞條優先度： `壞壞`",
        ReplyKeyboardMarkup(
                [[KeyboardButton('學說話'),KeyboardButton('熊貓會說什麼')], 
                 [KeyboardButton('目前狀態'),KeyboardButton('主選單')]]
        )
    ]

##抽籤式回答教學 [機率運勢類] [聊天類] 共同
def markupTeachChatRandom():
    return [
        "【抽籤式回答】\n指令： `熊貓[關鍵字]　或　抽籤[關鍵字]` \n說明：本功能可以在所有對應的回應中，隨機抽取一則回應出來！若有開啟「可以說別人教的話」的功能，則也會從其他聊天室教的詞條隨機抽選！",
        ReplyKeyboardMarkup(
                [[KeyboardButton('學說話')], 
                 [KeyboardButton('目前狀態'),KeyboardButton('主選單')]]
        )
    ]

##會說什麼
def markupWhatCanSay(object):
    #整理資料格式
    rslString=""
    if object["resData"]:
        for k, v in object["resData"].items():
            rslString = rslString + " `" + k  + "` " +  ' ↓\n' + '\n'.join(v) + '\n----------\n\n'
    return [
        object["nickname"]+"教我說的話：\n\n" + rslString, 
    ]

#==========功能==========#
#確認詞條內容
def markupLearnConfirm(key = '', res = '', tempId = ''):
    return [
        "確認詞條內容\n【我看到】 "+key+"\n【我要回】 "+res,
        InlineKeyboardMarkup(
            [[InlineKeyboardButton("是的沒錯", callback_data="action=confirm_learn&id="+str(tempId)),
              InlineKeyboardButton("這句母湯", callback_data="action=cancel_learn&id="+str(tempId))]]
        )
    ]


#==============================================#
#                   爬蟲關鍵類                  #
#==============================================#
#==========教學==========#
##氣象功能教學
def flexTeachMeteorology():
    return {
        "type": "bubble",
        "direction": "ltr",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "教學",
                "color": "#1DB446",
                "size": "sm",
                "weight": "bold"
            },
            {
                "type": "text",
                "text": "查氣象功能",
                "margin": "md",
                "size": "xxl",
                "weight": "bold"
            },
            {
                "type": "separator",
                "margin": "lg"
            },
            {
                "type": "text",
                "text": "說明",
                "size": "md",
                "weight": "bold",
                "color": "#825d5c",
                "margin": "lg"
            },
            {
                "type": "text",
                "text": "本熊貓會根據你輸入的位置，告訴你離你最近的氣象資訊。",
                "color": "#AAAAAA",
                "size": "sm",
                "flex": 2,
                "margin": "sm",
                "wrap": True
            },
            {
                "type": "text",
                "text": "氣象資訊包含「天氣資訊」及「空汙資訊」。",
                "color": "#AAAAAA",
                "size": "sm",
                "flex": 2,
                "margin": "sm",
                "wrap": True
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "separator",
                "margin": "sm"
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                "type": "message",
                "label": "怎麼查天氣",
                "text": "怎麼查天氣"
                }
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                "type": "message",
                "label": "怎麼查空汙",
                "text": "怎麼查空汙"
                }
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                "type": "message",
                "label": "主選單",
                "text": "主選單"
                }
            }
            ]
        }
    }

##查天氣教學
def flexTeachWeather():
    return {
        "type": "bubble",
        "direction": "ltr",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "教學",
                "color": "#1DB446",
                "size": "sm",
                "weight": "bold"
            },
            {
                "type": "text",
                "text": "如何查天氣",
                "margin": "md",
                "size": "xxl",
                "weight": "bold"
            },
            {
                "type": "separator",
                "margin": "lg"
            },
            {
                "type": "text",
                "text": "舉例一（啟動詞）",
                "size": "md",
                "weight": "bold",
                "color": "#825d5c",
                "margin": "lg"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "margin": "sm",
                "contents": [
                {
                    "type": "text",
                    "text": "即時天氣：",
                    "color": "#AAAAAA",
                    "size": "sm",
                    "flex": 2
                },
                {
                    "type": "text",
                    "text": "天氣查詢、目前天氣...",
                    "wrap": True,
                    "flex": 4,
                    "size": "sm",
                    "color": "#825d5c"
                }
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "margin": "sm",
                "contents": [
                {
                    "type": "text",
                    "text": "逐三小時：",
                    "color": "#AAAAAA",
                    "size": "sm",
                    "flex": 2
                },
                {
                    "type": "text",
                    "text": "未來天氣、明天天氣...",
                    "wrap": True,
                    "flex": 4,
                    "size": "sm",
                    "color": "#825d5c"
                }
                ]
            },
            {
                "type": "text",
                "text": "啟動後，請依提示文字輸入想查詢的「位置資訊」。",
                "color": "#AAAAAA",
                "size": "sm",
                "flex": 2,
                "margin": "sm",
                "wrap": True
            },
            {
                "type": "separator",
                "margin": "lg"
            },
            {
                "type": "text",
                "text": "舉例二（地名+啟動詞）",
                "size": "md",
                "weight": "bold",
                "color": "#825d5c",
                "margin": "lg"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "margin": "sm",
                "contents": [
                {
                    "type": "text",
                    "text": "即時天氣：",
                    "color": "#AAAAAA",
                    "size": "sm",
                    "flex": 2
                },
                {
                    "type": "text",
                    "text": "台北目前天氣",
                    "wrap": True,
                    "flex": 4,
                    "size": "sm",
                    "color": "#825d5c"
                }
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "margin": "sm",
                "contents": [
                {
                    "type": "text",
                    "text": "逐三小時：",
                    "color": "#AAAAAA",
                    "size": "sm",
                    "flex": 2
                },
                {
                    "type": "text",
                    "text": "台北明天會下雨嗎",
                    "wrap": True,
                    "flex": 4,
                    "size": "sm",
                    "color": "#825d5c"
                }
                ]
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "separator",
                "margin": "sm"
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                "type": "message",
                "label": "查詢天氣",
                "text": "查詢天氣"
                }
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                "type": "message",
                "label": "查詢未來天氣",
                "text": "查詢未來天氣"
                }
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                "type": "message",
                "label": "主選單",
                "text": "主選單"
                }
            }
            ]
        }
    }

##查空汙教學
def flexTeachAQI():
    return {
        "type": "bubble",
        "direction": "ltr",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "教學",
                "color": "#1DB446",
                "size": "sm",
                "weight": "bold"
            },
            {
                "type": "text",
                "text": "如何查空汙",
                "margin": "md",
                "size": "xxl",
                "weight": "bold"
            },
            {
                "type": "separator",
                "margin": "lg"
            },
            {
                "type": "text",
                "text": "舉例一（啟動詞）",
                "size": "md",
                "weight": "bold",
                "color": "#825d5c",
                "margin": "lg"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "margin": "sm",
                "contents": [
                {
                    "type": "text",
                    "text": "查詢指令：",
                    "color": "#AAAAAA",
                    "size": "sm",
                    "flex": 2
                },
                {
                    "type": "text",
                    "text": "空氣查詢、空汙查詢、",
                    "wrap": True,
                    "flex": 4,
                    "size": "sm",
                    "color": "#825d5c"
                }
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "margin": "sm",
                "contents": [
                {
                    "type": "text",
                    "color": "#AAAAAA",
                    "size": "sm",
                    "flex": 2,
                    "text": " "
                },
                {
                    "type": "text",
                    "text": "查詢PM2.5、查AQI",
                    "wrap": True,
                    "flex": 4,
                    "size": "sm",
                    "color": "#825d5c"
                }
                ]
            },
            {
                "type": "text",
                "text": "啟動後，請依提示文字輸入想查詢的「位置資訊」。",
                "color": "#AAAAAA",
                "size": "sm",
                "flex": 2,
                "margin": "sm",
                "wrap": True
            },
            {
                "type": "separator",
                "margin": "lg"
            },
            {
                "type": "text",
                "text": "舉例二（地名+啟動詞）",
                "size": "md",
                "weight": "bold",
                "color": "#825d5c",
                "margin": "lg"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "margin": "sm",
                "contents": [
                {
                    "type": "text",
                    "text": "查詢指令：",
                    "color": "#AAAAAA",
                    "size": "sm",
                    "flex": 2
                },
                {
                    "type": "text",
                    "text": "台北PM2.5",
                    "wrap": True,
                    "flex": 4,
                    "size": "sm",
                    "color": "#825d5c"
                }
                ]
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "separator",
                "margin": "sm"
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                "type": "message",
                "label": "查詢空汙",
                "text": "查詢空汙"
                }
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                "type": "message",
                "label": "主選單",
                "text": "主選單"
                }
            }
            ]
        }
    }

#==========功能==========#
##告訴我位置
def flexTellMeLocation():
    return {
        "type": "bubble",
        "size": "kilo",
        "direction": "ltr",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "查詢地點",
                "color": "#1DB446",
                "size": "sm",
                "weight": "bold"
            },
            {
                "type": "text",
                "text": "要查詢的地點是？",
                "margin": "md",
                "size": "xl",
                "weight": "bold",
                "wrap": True
            },
            {
                "type": "separator",
                "margin": "md"
            },
            {
                "type": "text",
                "text": "註：資料量大時可能會有查詢延遲",
                "margin": "md",
                "size": "sm",
                "wrap": True,
                "color": "#999999"
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "button",
                "action": {
                "type": "uri",
                "label": "傳送定位資訊",
                "uri": "line://nv/location"
                },
                "height": "sm",
                "style": "primary",
                "color": "#209799"
            }
            ]
        }
    }

##目前天氣
def flexWeather(weather):
    #整理資料格式
    weather['Temp'] = str(round(float(weather['Temp'])*10+0.5)/10) if weather['Temp']!='-99' else 'N/A'
    weather['Humd'] = str(round(float(weather['Humd'])*1000+0.5)/10) if weather['Humd']!='-99' else 'N/A'
    weather['24R'] = str(round(float(weather['24R'])*10+0.5)/10) if weather['24R']!='-99' else 'N/A'
    #建立回傳物件
    return [
        weather['locationName'] + "/" + weather['City'] + weather['Town'] + "目前天氣：\n" + weather['Temp'] + '° ' + weather['Wx'] + \
        "\n降雨率 " + str(weather['PoP6h']) + "%\n濕度 " + str(weather['PoP6h']) + '%',
        {
            "type": "bubble", "direction": "ltr",
            "body": {
                "type": "box", "layout": "vertical",
                "contents": [
                    #溫度
                    { "type": "text", "text": weather['Temp']+'°', "color": "#990066", "size": "5xl", "align": "center" },
                    { "type": "text", "text": weather['Wx'], "color": "#990066", "size": "lg", "weight": "bold", "align": "center" },
                    #目前天氣
                    {
                        "type": "box", "layout": "horizontal", "margin": "xxl",
                        "contents": [
                            #地區
                            {
                                "type": "box", "layout": "vertical", "flex": 5,
                                "contents": [
                                    { "type": "text", "text": weather['locationName'], "size": "xxl", "weight": "bold", "wrap": True },
                                    { "type": "text", "text": weather['City']+' '+weather['Town'], "weight": "bold", "size": "sm", "color": "#0D8186" }
                                ]
                            },
                            #降雨率
                            {
                                "type": "box", "layout": "vertical", "flex": 4,
                                "contents": [
                                    {
                                        "type": "box", "layout": "baseline",
                                        "contents": [
                                            { "type": "text", "text": "降雨率", "flex": 2, "size": "sm", "weight": "bold" },
                                            { "type": "text", "text": str(weather['PoP6h'])+'%', "flex": 3, "weight": "bold", "size": "xl", "color": "#0D8186" }
                                        ]
                                    },
                                    {
                                        "type": "box", "layout": "vertical", "height": "15px", "margin": "sm",
                                        "backgroundColor": "#9FD8E3", "cornerRadius": "10px",
                                        "contents": [
                                            {
                                                "type": "box", "layout": "vertical", "height": "15px",
                                                "backgroundColor": "#0D8186", "width": str(weather['PoP6h'] if int(weather['PoP6h'])>0 else "0.1")+'%', "cornerRadius": "10px",
                                                "contents": [ { "type": "filler" } ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    { "type": "separator", "margin": "md" },
                    #濕度、雨量
                    {
                        "type": "box", "layout": "horizontal", "margin": "md",
                        "contents": [
                            {
                                "type": "box", "layout": "vertical",
                                "contents": [
                                    { "type": "text", "text": "濕度", "size": "sm", "align": "center" },
                                    { "type": "text", "text": weather['Humd']+'%', "weight": "bold", "size": "lg", "color": "#990066", "align": "center" }
                                ]
                            },
                            {
                                "type": "box", "layout": "vertical",
                                "contents": [
                                    { "type": "text", "text": "日積雨量", "size": "sm", "align": "center" },
                                    { "type": "text", "text": weather['24R']+' mm', "weight": "bold", "size": "lg", "color": "#990066", "align": "center" }
                                ]
                            }
                        ]
                    },
                    { "type": "separator", "margin": "md" },
                    {
                        "type": "box", "layout": "vertical", "margin": "md",
                        "contents": [ { "type": "text", "text": '截至'+weather['TimeString'], "size": "sm", "color": "#AAAAAA", "align": "end" } ]
                    }
                ]
            }
        }
    ]

##未來天氣
def flexWeather72HR(weather72_list):
    #整理資料格式
    WeatherList=[]
    rslString=""
    for weather72 in weather72_list:
        rslString = weather72['locationName']
        WeatherList.append(
            {
                "type": "bubble", "size": "micro", "direction": "ltr",
                "body": {
                    "type": "box", "layout": "vertical",
                    "contents": [
                        #Title
                        {
                            "type": "box", "layout": "horizontal",
                            "contents": [
                                { "type": "text", "text": weather72['locationName'], "size": "sm", "align": "center", "flex": 4, "color": "#0D8186" },
                                { "type": "text", "text": weather72['startTime'][8:14]+'時', "color": "#1DB446", "size": "xs", "align": "center", "flex": 5 }
                            ]
                        },
                        #天氣內容
                        { "type": "text", "text": weather72['Temp']+'°', "size": "3xl", "color": "#990066", "align": "center" },
                        { "type": "text", "text": weather72['Wx'], "size": "sm", "weight": "bold", "align": "center", "color": "#990066" },
                        { "type": "separator", "margin": "md" },
                        {
                            "type": "box", "layout": "horizontal", "margin": "md",
                            "contents": [
                                {
                                    "type": "box", "layout": "vertical", "flex": 5,
                                    "contents": [
                                        { "type": "text", "text": "降雨率", "size": "xs", "color": "#666666", "align": "center" },
                                        { "type": "text", "text": weather72['PoP6h']+'%', "size": "md", "weight": "bold", "color": "#0D8186", "align": "center" }
                                    ]
                                },
                                { "type": "separator", "margin": "md" },
                                {
                                    "type": "box", "layout": "vertical", "flex": 5,
                                    "contents": [
                                        { "type": "text", "text": "舒適度", "size": "xs", "color": "#666666", "align": "center" },
                                        { "type": "text", "text": weather72['CI'], "size": "md", "weight": "bold", "color": "#0D8186", "align": "center" }
                                    ]
                                }
                            ]
                        },
                        { "type": "separator", "margin": "md" }
                    ]
                }
            }
        )
    
    #建立回傳物件
    return [rslString+"未來72小時天氣", { "type": "carousel", "contents": WeatherList }]

##空氣品質
def flexAQI(aqi):
    #整理資料格式
    aqi['SiteName'] = aqi['SiteName'][aqi['SiteName'].index('(')+1:aqi['SiteName'].index(')')] if '(' in aqi['SiteName'] else aqi['SiteName']
    aqi['AQI'] = '-1' if aqi['AQI']=='' else aqi['AQI']
    for x in ['SO2', 'SO2_AVG', 'CO', 'CO_8hr', 'O3', 'O3_8hr', 'PM10', 'PM10_AVG', 'PM2.5', 'PM2.5_AVG', 'NO2']:
        aqi[x] = 'NA' if aqi[x]=='' else aqi[x]
    AQIList = [[-1,"#888888"], [0,"#339933"], [51,"#EECC33"], [101,"#EE9933"], [151,"#DD3333"], [201,"#996699"], [301,"#990066"]]
    AQIcolor = list(filter(lambda x: int(aqi['AQI'])>=x[0], AQIList))[::-1][0][1]
    #建立回傳物件
    return [
        aqi['County'] + aqi['SiteName'] + "空氣品質：\n" + "AQI指數：" + aqi['AQI'] if aqi['AQI']!='-1' else 'NA' + " " +aqi['Status'],
        {
            "type": "bubble", "direction": "ltr",
            "body": {
                "type": "box", "layout": "vertical",
                "contents": [
                    # title
                    { "type": "text", "text": aqi['Status'], "weight": "bold", "size": "sm", "color": AQIcolor },
                    {
                        "type": "box", "layout": "horizontal", "margin": "md",
                        "contents": [
                            {
                                "type": "box", "layout": "vertical", "flex": 5,
                                "contents": [
                                    { "type": "text", "text": aqi['SiteName'], "size": "xxl", "weight": "bold" },
                                    { "type": "text", "text": aqi['County'], "size": "lg", "weight": "bold", "color": "#333399" }
                                ]
                            },
                            {
                                "type": "box", "layout": "vertical", "flex": 3,
                                "contents": [
                                    { "type": "text", "text": "AQI", "size": "lg", "align": "end", "color": AQIcolor  },
                                    { "type": "text", "text": aqi['AQI'] if aqi['AQI']!='-1' else 'NA', "size": "4xl", "weight": "bold", "color": AQIcolor, "align": "end" }
                                ]
                            }
                        ]
                    },
                    { "type": "separator", "margin": "md" },
                    # O3 臭氧
                    {
                        "type": "box", "layout": "horizontal", "margin": "md",
                        "contents": [
                            {
                                "type": "box", "layout": "vertical", "flex": 3,
                                "contents": [ { "type": "text", "text": "O3\n臭氧", "weight": "bold", "size": "lg", "wrap": True, "flex": 1, "align": "start", "color": "#336699" if "臭氧" in aqi['Pollutant'] else "#444444", "gravity": "center" } ]
                            },
                            {
                                "type": "box", "layout": "vertical", "flex": 2,
                                "contents": [
                                    { "type": "text", "text": "8小時\n移動平均", "size": "sm", "wrap": True, "flex": 1, "align": "end", "gravity": "center" },
                                    { "type": "text", "text": "小時濃度", "size": "sm", "wrap": True, "flex": 1, "align": "end", "gravity": "center" }
                                ]
                            },
                            {
                                "type": "box", "layout": "vertical", "flex": 2,
                                "contents": [
                                    { "type": "text", "text": aqi['O3_8hr'], "size": "xxl", "wrap": True, "flex": 1, "align": "end", "gravity": "center", "weight": "bold" },
                                    { "type": "text", "text": aqi['O3'], "size": "xxl", "wrap": True, "flex": 1, "align": "end", "gravity": "center", "weight": "bold" }
                                ]
                            }
                        ]
                    },
                    { "type": "separator", "margin": "md" },
                    # PM2.5 細懸浮微粒
                    {
                        "type": "box", "layout": "horizontal", "margin": "md",
                        "contents": [
                            {
                                "type": "box", "layout": "vertical", "flex": 3,
                                "contents": [ { "type": "text", "text": "PM2.5\n細懸浮微粒", "weight": "bold", "size": "lg", "wrap": True, "flex": 1, "align": "start", "color": "#336699" if "細懸浮微粒" in aqi['Pollutant'] else "#444444", "gravity": "center" } ]
                            },
                            {
                                "type": "box", "layout": "vertical", "flex": 2,
                                "contents": [
                                    { "type": "text", "text": "移動平均", "size": "sm", "wrap": True, "flex": 1, "align": "end", "gravity": "center" },
                                    { "type": "text", "text": "小時濃度", "size": "sm", "wrap": True, "flex": 1, "align": "end", "gravity": "center" }
                                ]
                            },
                            {
                                "type": "box", "layout": "vertical", "flex": 2,
                                "contents": [
                                    { "type": "text", "text": aqi['PM2.5_AVG'], "size": "xxl", "wrap": True, "flex": 1, "align": "end", "gravity": "center", "weight": "bold" },
                                    { "type": "text", "text": aqi['PM2.5'], "size": "xxl", "wrap": True, "flex": 1, "align": "end", "gravity": "center", "weight": "bold" }
                                ]
                            }
                        ]
                    },
                    { "type": "separator", "margin": "md" },
                    # PM10 懸浮微粒
                    {
                        "type": "box", "layout": "horizontal", "margin": "md",
                        "contents": [
                            {
                                "type": "box", "layout": "vertical", "flex": 3,
                                "contents": [ { "type": "text", "text": "PM10\n懸浮微粒", "weight": "bold", "size": "lg", "wrap": True, "flex": 1, "align": "start", "color": "#336699" if "懸浮微粒" in aqi['Pollutant'].replace("細懸浮微粒","") else "#444444", "gravity": "center" } ]
                            },
                            {
                                "type": "box", "layout": "vertical", "flex": 2,
                                "contents": [
                                    { "type": "text", "text": "移動平均", "size": "sm", "wrap": True, "flex": 1, "align": "end", "gravity": "center" },
                                    { "type": "text", "text": "小時濃度", "size": "sm", "wrap": True, "flex": 1, "align": "end", "gravity": "center" }
                                ]
                            },
                            {
                                "type": "box", "layout": "vertical", "flex": 2,
                                "contents": [
                                    { "type": "text", "text": aqi['PM10_AVG'], "size": "xxl", "wrap": True, "flex": 1, "align": "end", "gravity": "center", "weight": "bold" },
                                    { "type": "text", "text": aqi['PM10'], "size": "xxl", "wrap": True, "flex": 1, "align": "end", "gravity": "center", "weight": "bold" }
                                ]
                            }
                        ]
                    },
                    { "type": "separator", "margin": "md" },
                    # CO 一氧化碳
                    {
                        "type": "box", "layout": "horizontal", "margin": "md",
                        "contents": [
                            {
                                "type": "box", "layout": "vertical", "flex": 3,
                                "contents": [ { "type": "text", "text": "CO\n一氧化碳", "weight": "bold", "size": "lg", "wrap": True, "flex": 1, "align": "start", "color": "#336699" if "一氧化碳" in aqi['Pollutant'] else "#444444", "gravity": "center" } ]
                            },
                            {
                                "type": "box", "layout": "vertical", "flex": 2,
                                "contents": [
                                    { "type": "text", "text": "8小時\n移動平均", "size": "sm", "wrap": True, "flex": 1, "align": "end", "gravity": "center" },
                                    { "type": "text", "text": "小時濃度", "size": "sm", "wrap": True, "flex": 1, "align": "end", "gravity": "center" }
                                ]
                            },
                            {
                                "type": "box", "layout": "vertical", "flex": 2,
                                "contents": [
                                    { "type": "text", "text": aqi['CO_8hr'], "size": "xxl", "wrap": True, "flex": 1, "align": "end", "gravity": "center", "weight": "bold" },
                                    { "type": "text", "text": aqi['CO'], "size": "xxl", "wrap": True, "flex": 1, "align": "end", "gravity": "center", "weight": "bold" }
                                ]
                            }
                        ]
                    },
                    { "type": "separator", "margin": "md" },
                    # SO2 二氧化硫
                    {
                        "type": "box", "layout": "horizontal", "margin": "md",
                        "contents": [
                            {
                                "type": "box", "layout": "vertical", "flex": 3,
                                "contents": [ { "type": "text", "text": "SO2\n二氧化硫", "weight": "bold", "size": "lg", "wrap": True, "flex": 1, "align": "start", "color": "#336699" if "二氧化硫" in aqi['Pollutant'] else "#444444", "gravity": "center" } ]
                            },
                            {
                                "type": "box", "layout": "vertical", "flex": 2,
                                "contents": [
                                    { "type": "text", "text": "移動平均", "size": "sm", "wrap": True, "flex": 1, "align": "end", "gravity": "center" },
                                    { "type": "text", "text": "小時濃度", "size": "sm", "wrap": True, "flex": 1, "align": "end", "gravity": "center" }
                                ]
                            },
                            {
                                "type": "box", "layout": "vertical", "flex": 2,
                                "contents": [
                                    { "type": "text", "text": aqi['SO2_AVG'], "size": "xxl", "wrap": True, "flex": 1, "align": "end", "gravity": "center", "weight": "bold" },
                                    { "type": "text", "text": aqi['SO2'], "size": "xxl", "wrap": True, "flex": 1, "align": "end", "gravity": "center", "weight": "bold" }
                                ]
                            }
                        ]
                    },
                    { "type": "separator", "margin": "md" },
                    # NO2 二氧化氮
                    {
                        "type": "box", "layout": "horizontal", "margin": "md",
                        "contents": [
                            {
                                "type": "box", "layout": "vertical", "flex": 3,
                                "contents": [ { "type": "text", "text": "NO2\n二氧化氮", "weight": "bold", "size": "lg", "wrap": True, "flex": 1, "align": "start", "color": "#336699" if "二氧化氮" in aqi['Pollutant'] else "#444444", "gravity": "center" } ]
                            },
                            {
                                "type": "box", "layout": "vertical", "flex": 2,
                                "contents": [ { "type": "text", "text": "小時濃度", "size": "sm", "wrap": True, "flex": 1, "align": "end", "gravity": "center" } ]
                            },
                            {
                                "type": "box", "layout": "vertical", "flex": 2,
                                "contents": [ { "type": "text", "text": aqi['NO2'], "size": "xxl", "wrap": True, "flex": 1, "align": "end", "gravity": "center", "weight": "bold" } ]
                            }
                        ]
                    },
                    { "type": "separator", "margin": "md" },
                    { "type": "text", "text": '截至'+aqi['timeStr'], "margin": "xs", "size": "xs", "color": "#aaaaaa", "align": "end" }
                ]
            }
        }
    ]


#==============================================#
#                   機率運勢類                  #
#==============================================#
#==========教學==========#
##抽籤教學
def flexTeachLottery():
    return {
        "type": "bubble",
        "direction": "ltr",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "教學",
                "color": "#1DB446",
                "size": "sm",
                "weight": "bold"
            },
            {
                "type": "text",
                "text": "抽籤功能",
                "margin": "md",
                "size": "xxl",
                "weight": "bold"
            },
            {
                "type": "separator",
                "margin": "lg"
            },
            {
                "type": "text",
                "text": "說明",
                "size": "md",
                "weight": "bold",
                "color": "#825d5c",
                "margin": "lg"
            },
            {
                "type": "text",
                "text": "目前抽籤式的功能有「抽籤式回答」、「擲筊」、「抽塔羅」、「抽籤詩」等，點擊下方按鈕查看詳細說明",
                "color": "#AAAAAA",
                "size": "sm",
                "flex": 2,
                "margin": "sm",
                "wrap": True
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "separator",
                "margin": "sm"
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                "type": "message",
                "label": "怎麼抽籤式回答",
                "text": "抽籤式回答教學"
                }
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                "type": "message",
                "label": "怎麼擲筊",
                "text": "擲筊教學"
                }
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                "type": "message",
                "label": "怎麼抽籤詩",
                "text": "抽籤詩教學"
                }
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                "type": "message",
                "label": "怎麼抽塔羅",
                "text": "抽塔羅教學"
                }
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                "type": "message",
                "label": "主選單",
                "text": "主選單"
                }
            }
            ]
        }
    }

#==========選單==========#
##擲筊選單
def flexMenuDevinate():
    return {
        "type": "bubble",
        "direction": "ltr",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "擲筊",
                "color": "#1DB446",
                "size": "sm",
                "weight": "bold"
            },
            {
                "type": "text",
                "text": "擲筊功能",
                "margin": "md",
                "size": "xxl",
                "weight": "bold"
            },
            {
                "type": "separator",
                "margin": "lg"
            },
            {
                "type": "text",
                "text": "說明",
                "size": "md",
                "weight": "bold",
                "color": "#825d5c",
                "margin": "lg"
            },
            {
                "type": "text",
                "text": "按下下方擲筊鈕，即可擲筊",
                "color": "#AAAAAA",
                "size": "sm",
                "flex": 2,
                "margin": "sm",
                "wrap": True
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "separator",
                "margin": "sm"
            },
            {
                "type": "button",
                "action": {
                "type": "postback",
                "label": "馬上擲筊",
                "data": "action=devinate"
                },
                "style": "primary",
                "height": "sm",
                "color": "#BB3333",
                "margin": "md"
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                "type": "message",
                "label": "主選單",
                "text": "主選單"
                }
            }
            ]
        }
    }

##擲筊選單
def flexMenuFortuneStick():
    return {
        "type": "bubble",
        "direction": "ltr",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "擲筊",
                "color": "#1DB446",
                "size": "sm",
                "weight": "bold"
            },
            {
                "type": "text",
                "text": "抽籤詩功能",
                "margin": "md",
                "size": "xxl",
                "weight": "bold"
            },
            {
                "type": "separator",
                "margin": "lg"
            },
            {
                "type": "text",
                "text": "說明",
                "size": "md",
                "weight": "bold",
                "color": "#825d5c",
                "margin": "lg"
            },
            {
                "type": "text",
                "text": "按下下方抽籤詩鈕，即可抽取",
                "color": "#AAAAAA",
                "size": "sm",
                "flex": 2,
                "margin": "sm",
                "wrap": True
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "separator",
                "margin": "sm"
            },
            {
                "type": "button",
                "action": {
                "type": "postback",
                "label": "抽籤詩",
                "data": "action=fortuneStick"
                },
                "style": "primary",
                "height": "sm",
                "color": "#BB3333",
                "margin": "md"
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                "type": "message",
                "label": "主選單",
                "text": "主選單"
                }
            }
            ]
        }
    }

##抽塔羅
def flexMenuTarot():
    return {
        "type": "bubble",
        "direction": "ltr",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "抽塔羅",
                "color": "#1DB446",
                "size": "sm",
                "weight": "bold"
            },
            {
                "type": "text",
                "text": "抽塔羅功能",
                "margin": "md",
                "size": "xxl",
                "weight": "bold"
            },
            {
                "type": "separator",
                "margin": "lg"
            },
            {
                "type": "text",
                "text": "說明",
                "size": "md",
                "weight": "bold",
                "color": "#825d5c",
                "margin": "lg"
            },
            {
                "type": "text",
                "text": "可以下方按鈕選擇抽1、3、5張牌。",
                "color": "#AAAAAA",
                "size": "sm",
                "flex": 2,
                "margin": "sm",
                "wrap": True
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "separator",
                "margin": "sm"
            },
            {
                "type": "button",
                "action": {
                "type": "postback",
                "label": "抽一張",
                "data": "action=draw_tarot&num=1"
                },
                "style": "primary",
                "height": "sm",
                "color": "#9778d6"
            },
            {
                "type": "button",
                "action": {
                "type": "postback",
                "label": "抽三張",
                "data": "action=draw_tarot&num=3"
                },
                "style": "primary",
                "height": "sm",
                "color": "#7b60b3",
                "margin": "md"
            },
            {
                "type": "button",
                "action": {
                "type": "postback",
                "label": "抽五張",
                "data": "action=draw_tarot&num=5"
                },
                "style": "primary",
                "height": "sm",
                "color": "#64499e",
                "margin": "md"
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                "type": "message",
                "label": "主選單",
                "text": "主選單"
                },
                "margin": "md"
            }
            ]
        }
    }

#==========功能==========#
##擲筊結果
def flexDevinate(devinate):
    return [
        "擲筊結果：" + devinate['text'],
        {
            "type": "bubble",
            "size": "kilo",
            "direction": "ltr",
            "hero": {
                "type": "image",
                "url": "https://linziyou.info/u/ln/" + devinate['url'],
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "20:13"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#c4241b",
                "contents": [
                    {
                        "type": "text",
                        "text": devinate['text'],
                        "size": "4xl",
                        "color": "#ffffff",
                        "weight": "bold",
                        "align": "center"
                    },
                    {
                        "type": "separator",
                        "color": "#ffffff",
                        "margin": "md"
                    },
                    {
                        "type": "button",
                        "action": {
                        "type": "postback",
                        "label": "再擲一次",
                        "data": "action=devinate"
                        },
                        "style": "primary",
                        "height": "sm",
                        "color": "#BB3333",
                        "margin": "md"
                    }
                ]
            }
        }
    ]

##抽塔羅結果
def flexTarot(tarot_list):
    alt = ""
    content = []
    for tarot in tarot_list:
        alt += "[" + tarot['position'] + "] " + tarot['cht'] + " " + tarot['eng'] + "\n"
        content.append(
            {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "image",
                    "url": "https://linziyou.info/u/ln/tarot/"+tarot['url'],
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "1:2",
                    "gravity": "top"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": tarot['cht'],
                            "size": "xxl",
                            "color": "#ffffff",
                            "weight": "bold"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "text",
                            "text": tarot['eng'],
                            "size": "sm",
                            "flex": 0,
                            "color": "#FFFFFF",
                            "weight": "bold"
                        }
                        ],
                        "spacing": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "button",
                            "action": {
                            "type": "postback",
                            "label": "查看牌義",
                            "data": "action=meaning_tarot&id="+str(tarot['id'])
                            },
                            "style": "primary",
                            "color": "#FFFFFF00",
                            "height": "sm"
                        }
                        ],
                        "borderWidth": "2px",
                        "cornerRadius": "10px",
                        "borderColor": "#ffffff",
                        "margin": "md"
                    }
                    ],
                    "position": "absolute",
                    "offsetBottom": "0px",
                    "offsetStart": "0px",
                    "offsetEnd": "0px",
                    "backgroundColor": "#807467DD",
                    "paddingAll": "20px",
                    "paddingTop": "18px"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": tarot['position'],
                        "color": "#ffffff",
                        "align": "center",
                        "size": "xs",
                        "offsetTop": "3px"
                    }
                    ],
                    "position": "absolute",
                    "cornerRadius": "20px",
                    "offsetTop": "18px",
                    "backgroundColor": "#807467CC",
                    "offsetStart": "18px",
                    "height": "25px",
                    "paddingStart": "10px",
                    "paddingEnd": "10px",
                    "width": "50px"
                }
                ],
                "paddingAll": "0px"
            }
            }
        )
    
    return [
        alt, 
        {
            "type": "carousel",
            "contents": content
        }
    ]

##塔羅牌義
def flexMeaningTarot(tarot):
    return [
        "[" + tarot['position'] + "] " + tarot['cht'] + " " + tarot['eng'] + " 牌義查詢", 
        {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "image",
                    "url": "https://linziyou.info/u/ln/tarot/"+tarot['url'],
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "1:2",
                    "gravity": "top"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": tarot['meaning'],
                        "size": "sm",
                        "color": "#FFFFFF",
                        "wrap": True,
                        "margin": "lg"
                    }
                    ],
                    "position": "absolute",
                    "offsetBottom": "0px",
                    "offsetStart": "0px",
                    "offsetEnd": "0px",
                    "backgroundColor": "#03303Acc",
                    "paddingAll": "15px",
                    "paddingTop": "70px",
                    "offsetTop": "0px"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": tarot['position'],
                                "color": "#ffffff",
                                "align": "center",
                                "size": "xs",
                                "offsetTop": "3px"
                            }
                            ],
                            "cornerRadius": "20px",
                            "backgroundColor": "#807467CC",
                            "height": "25px",
                            "width": "50px"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": tarot['cht'],
                                "size": "xl",
                                "color": "#ffffff",
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": tarot['eng'],
                                "size": "xxs",
                                "color": "#FFFFFF",
                                "weight": "bold"
                            }
                            ],
                            "offsetStart": "10px"
                        }
                        ]
                    }
                    ],
                    "offsetTop": "15px",
                    "position": "absolute",
                    "offsetStart": "15px",
                    "offsetEnd": "15px"
                }
                ],
                "paddingAll": "0px"
            }
        }
    ]

##抽籤詩結果
def flexFortuneStick(fortuneStick):
    return [
        "第"+str(fortuneStick["id"])+"籤（" + fortuneStick['sexagenary']+"）\n"+fortuneStick['poem'],
        {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "image",
                    "url": "https://linziyou.info/u/ln/fortunestick/"+str(fortuneStick["id"])+".jpg",
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "480:655",
                    "gravity": "top"
                }
                ],
                "paddingAll": "0px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "button",
                    "action": {
                    "type": "postback",
                    "label": "查看解釋",
                    "data": "action=meaning_fortuneStick&id="+str(fortuneStick["id"])
                    },
                    "style": "primary",
                    "color": "#FFFFFF00",
                    "height": "sm"
                },
                {
                    "type": "separator",
                    "color": "#ffffff",
                    "margin": "md"
                },
                {
                    "type": "button",
                    "action": {
                    "type": "postback",
                    "label": "擲筊",
                    "data": "action=devinate"
                    },
                    "style": "primary",
                    "color": "#FFFFFF00",
                    "height": "sm",
                    "margin": "md"
                }
                ],
                "cornerRadius": "10px",
                "margin": "md"
            },
            "styles": {
                "footer": {
                "backgroundColor": "#c4241b"
                }
            }
        }
    ]

##塔羅牌義
def flexMeaningFortuneStick(fortuneStick):
    result = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "【語譯】",
                "color": "#FFFFFF",
                "size": "sm",
                "margin": "md"
            },
            {
                "type": "text",
                "text": fortuneStick["explanation"],
                "size": "sm",
                "color": "#FFFFFF",
                "wrap": True,
                "margin": "md"
            },
            {
                "type": "separator",
                "margin": "lg"
            },
            {
                "type": "text",
                "text": "【籤解】",
                "color": "#FFFFFF",
                "size": "sm",
                "margin": "lg"
            }
            ],
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "backgroundColor": "#210207cc",
            "paddingAll": "15px",
            "paddingTop": "20px",
            "offsetTop": "0px"
        }
    }
    box = {
        "type": "box", "layout": "horizontal", "contents": [], "margin": "md"
    }
    for i, sol in enumerate(fortuneStick["solve"]):
        box["contents"].append(
            {
                "type": "text",
                "text": "【" + sol["key"] + "】\n" + sol["value"],
                "size": "sm",
                "color": "#FFFFFF",
                "wrap": True,
                "margin": "sm",
                "flex": 1
            }
        )
        if i%2==1 or i==28:
            result["body"]["contents"].append(box)
            box = {
                "type": "box", "layout": "horizontal", "contents": [], "margin": "md"
            }
    
    return [
        "第"+str(fortuneStick["id"])+"籤（" + fortuneStick['sexagenary']+"）\n"+fortuneStick['poem']+"\n【語譯】\n"+fortuneStick["explanation"], 
        result
    ]
