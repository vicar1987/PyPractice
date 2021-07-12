import requests
from bs4 import BeautifulSoup
import pymongo
import pandas as pd
import csv
import json

client = pymongo.MongoClient("mongodb+srv://vicar1987:1ul3u03nji3@twfruit.i2omj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.TWFruits
test = db.test

form_data = {
    'keyword': '香蕉',
    'division_lv1': '*',
    'year': 102,
    'month': 1,
    'end_year': 110,
    'end_month': 6,
    'search_Submit': '查詢',
    'is_search': 'y'
}

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
}
url = 'https://www.coa.gov.tw/theme_list.php?theme=news&sub_theme=agri'
ss = requests.session()
res = ss.post(url=url, headers=headers, data=form_data)
soup = BeautifulSoup(res.text, 'html.parser')

ID = []
date = []
title = []
author = []
link = []
content = []


# 取文號
for a in soup.select('td[class="word"]'):
    ID.append(a.text)

# 取發布日期
for b in range(1, len(soup.select('td[align="center"]')), 3):
    newsDate = soup.select('td[align="center"]')[b]
    date.append(newsDate.text)

# 取發布機關
for c in range(2, len(soup.select('td[align="center"]')), 3):
    newsAuthor = soup.select('td[align="center"]')[c]
    author.append(newsAuthor.text)

# 取新聞標題、網址
for i in range(0, len(soup.select('a[class="main-c9-index"]'))):
    newsTitle = soup.select('a[class="main-c9-index"]')[i]['title']
    newsLink = 'https://www.coa.gov.tw/' + soup.select('a[class="main-c9-index"]')[i]['href']
    title.append(newsTitle)
    link.append(newsLink)

# 取新聞內容
for j in range(len(link)):
    page_res = ss.get(url=link[j], headers=headers)
    page_soap = BeautifulSoup(page_res.text, 'html.parser')
    for w in page_soap.select('div[class="word"]'):
        content.append (w.text)

dict = {'文號': ID, '發布日期': date, '標題': title, '發布機關': author, '網址': link, '內容': content}
df = pd.DataFrame(dict)
df.to_csv('測試用新聞_香蕉.csv', index=False)

data = pd.read_csv('測試用新聞_香蕉.csv',encoding = 'UTF-8')
data_json = json.loads(data.to_json(orient='records'))
test.insert_many(data_json)

client.close()