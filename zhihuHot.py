import requests
from bs4 import BeautifulSoup
import csv, codecs
import time, datetime, pytz

headers={"User-Agent":"","Cookie":""}
zh_url = "https://www.zhihu.com/billboard"
zh_response = requests.get(zh_url,headers=headers)

webcontent = zh_response.text
soup = BeautifulSoup(webcontent,"html.parser")
script_text = soup.find("script",id="js-initialData").get_text()
rule = r'"hotList":(.*?),"guestFeeds"'
result = re.findall(rule,script_text)
temp = result[0].replace("false","False").replace("true","True")
hot_list = eval(temp)

tz = pytz.timezone('Asia/Shanghai') #东八区
t = datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%Y%m%d_%H%M%S')
filename = 'zhihuHot_'+t+'.csv'

with  codecs.open(filename,'w','utf_8_sig') as zhihuHot:
  writer = csv.writer(zhihuHot)
  writer.writerow(['排名','答案数','热度','问题'])
  for i in range(50):
    index = i+1
    answerCount = hot_list[i]['feedSpecific']['answerCount']
    score = hot_list[i]['feedSpecific']['score']
    question = hot_list[i]['target']['titleArea']['text'] 
    list=[index, answerCount, score, question]
    writer.writerow(list)
