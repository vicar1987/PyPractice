import requests
from bs4 import BeautifulSoup
# import time
import csv
# import re

# start_time = time.time()

with open('104.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['職稱', '公司', '薪資', '工作內容'])

for page in range(1,11):
    url = 'https://www.104.com.tw/jobs/search/?ro=0&keyword=藝術行政&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=12&asc=0&page=' + str(
        page) + '&mode=s&jobsource=2018indexpoc'
    headers = {
        'User-Anget': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    blocks = soup.findAll('div', {'class': 'b-block__left'})
    for block in blocks:
        job = block.find("a", {"class": "js-job-link"})  #職缺名稱
        if job is None:
            continue
        company = block.find_all("li")[1]  #公司名稱
        salary = block.find("span", {"class": "b-tag--default"})  #薪資
        content = block.find("p", {"class": "job-list-item__info b-clearfix b-content"}) #工作內容

        # print(content.getText())
        # print((job.getText(),) + (company.getText().strip(),) + (salary.getText(),) + (content.getText()))

        with open('104.csv', 'a', newline='', encoding='utf-8') as csvfile:
          writer = csv.writer(csvfile)
          writer.writerow([job.getText(), company.getText().strip(), salary.getText(), content.getText()])




