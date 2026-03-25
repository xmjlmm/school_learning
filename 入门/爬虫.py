import requests
from bs4 import BeautifulSoup
headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.0.9211 SLBChan/105"
}
for start_num in range(0,250,25):
    response = requests.get(f'https://movie.douban.com/top250?start={start_num}',headers = headers)
    #print(response.status_code)
    #print(response.text)
    html = response.text
    soup = BeautifulSoup(html,'html.parser')
    #print(soup)
    all_titles = soup.findAll('span',attrs = {'class': 'title'})
    for title in all_titles:
        title_string = title.string
        if '/' not in title_string:
            print(title_string)