import requests
from bs4 import BeautifulSoup
import csv, codecs
import time, datetime, pytz

tz = pytz.timezone('Asia/Shanghai') #东八区
t = datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%Y%m%d_%H%M%S')
filename = 'zhihuHotBS_'+t+'.csv'

soup = BeautifulSoup(html.text,"html.parser")
con = soup.find(id = 'root').find('main').find('div').find_all('a')

with  codecs.open(filename,'w','utf_8_sig') as zhihuHot:
  writer = csv.writer(zhihuHot)
  writer.writerow(['排名','热度','问题'])
  # for i in range(50):
  for i in con:
    index = i.find_all('div')[1].string
    question = i.find_all('div')[3].find('div').string
    score = i.find_all('div')[5].string
    list=[index, question, score]
    writer.writerow(list)
