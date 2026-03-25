'''import requests
from bs4 import BeautifulSoup
response = requests.get('http://localhost:8888/notebooks/python/%E7%88%AC%E8%99%AB.ipynb')
#print(response.status_code)
#print(response.text)
html = response.text
soup = BeautifulSoup(html,'html.parser')
all_titles = soup.findAll('button',attrs= {'type':'submit'})
for title in all_titles:
    print(title.string)
'''

'''
import pandas as pd
import requests
from bs4 import BeautifulSoup
for start_num in range(1,852,1):
    response = requests.get(f'https://www.ijcai.org/proceedings/2023/{start_num}')
    #print(response.status_code)
    #print(response.text)
    html = response.text
    soup = BeautifulSoup(html,'html.parser')
    all_titles = soup.findAll('h1')
    all_authors = soup.findAll('h2')
    all_contents = soup.findAll('div',attrs={'class':'col-md-12'})
    all_keywords = soup.findAll('div', attrs={'class': 'topic'})
    for all_title in all_titles:
        print(all_title.string,end = '')
    for all_author in all_authors:
        print(all_author.string,end = '')
    for all_content in all_contents:
        print(all_content.string,end = '')
    for all_keyword in all_keywords:
        print(all_keyword.string)
    data = {f'start_num': [all_title.string, all_author.string, all_content.string, all_keyword.string]}
    df = pd.DataFrame(data)
    df.to_excel("C://Users//86159//Desktop//爬虫.xlsx")
'''
'''
import pandas as pd
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
    df.to_excel("C://Users//86159//Desktop//爬虫.xlsx")
'''

# 爬取网页中每一个链接的标题，作者，内容和关键词
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 创建一个空的DataFrame用于存储爬取的数据
df = pd.DataFrame(columns=['Title', 'Author', 'Content', 'Keyword'])

# 从第一个一直爬到第851个
for start_num in range(1, 852, 1):
    # 根据每一个网页路径，得到response
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.0.9211 SLBChan/105'
    }
    response = requests.get(f'https://www.ijcai.org/proceedings/2023/{start_num}', headers = headers)
    # 查看是否能够正常爬取
    # print(response.status_code)
    # print(response.text)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # 根据html源码进行分析和爬取
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
        df = df.append({'Title': title, 'Author': author, 'Content': content, 'Keyword': keyword},ignore_index=True)

    # 将DataFrame导出为csv文件
    df.to_csv("C://Users//86159//Desktop//爬虫.csv")
