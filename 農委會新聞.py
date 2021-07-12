import requests
from bs4 import BeautifulSoup
# form Data參考下面圖示
form_data = {
    'keyword': '',
    'division_lv1': '*',
    'year': 110,
    'month': 1,
    'end_year': 110,
    'end_month': 6,
    'search_Submit': '查詢',
    'is_search': 'y'
    }

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
}
url ='https://www.coa.gov.tw/theme_list.php?theme=news&sub_theme=agri'
ss = requests.session()
res = ss.post(url=url, headers=headers, data=form_data)
soup = BeautifulSoup(res.text, 'html.parser')
# 從下面的select把url選出來，再一一訪問各個連結就可以得到內文資料
# print(soup.select('a[class="main-c9-index"]'))
newstitle = soup.select('a[class="main-c9-index"]')

