import sys, os, requests, json

#with open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'eew_report.txt'), "w+", encoding="UTF-8") as f:
#    f.write('震度：'+sys.argv[1]+'\n秒數：'+sys.argv[2])

location = "雲林縣斗六市"
M = str(sys.argv[1]).replace("+", "強").replace("-", "弱")
data = {  
    "type": None,
    "title": "【地震速報】\n警報器所在地："+location+"\n預估震度："+M,
    "message": {
        "location": location,
        "M": M
    },
    "channel_id": "ALL",
    "template": "earthquake"
}

#=============== Main Function ===============#
r = requests.post('https://linziyou.info:4567/pushing', json = data)