'''import pandas as pd
import requests
from bs4 import BeautifulSoup

# 创建一个空的DataFrame用于存储爬取的数据
df = pd.DataFrame(columns=['Title', 'Author', 'Content', 'Keyword'])

for start_num in range(1, 852, 1):
    response = requests.get(f'https://www.ijcai.org/proceedings/2023/{start_num}')
    # print(response.status_code)
    # print(response.text)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    all_titles = soup.findAll('h1', attrs={'class': 'page-title'})
    all_authors = soup.findAll('h2')
    all_contents = soup.findAll('div', attrs={'class': 'col-md-12'})
    all_keywords = soup.findAll('div', attrs={'class': 'topic'})
    for all_title, all_author, all_content, all_keyword in zip(all_titles, all_authors, all_contents, all_keywords):
        title = all_title.string if all_title else ''
        author = all_author.string if all_author else ''
        content = all_content.string if all_content else ''
        keyword = all_keyword.string if all_keyword else ''

        # 将每条数据添加到DataFrame中
        df = df._append({'Title': title, 'Author': author, 'Content': content, 'Keyword': keyword},ignore_index=True)

    #将DataFrame导出为Excel文件
    df.to_excel("C://Users//86159//Desktop//爬虫.xlsx")'''

import requests
from bs4 import BeautifulSoup
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.0.9211 SLBChan/105'
}

response = requests.get('https://tyjrswj.nantong.gov.cn/ntstyjrswj/', headers = headers)
print(response.status_code)

#print(response.text)
#html = response.text
#soup = BeautifulSoup(html, 'html.parser')