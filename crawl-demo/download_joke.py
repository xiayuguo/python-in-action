import urllib.request
import os
import json
import re
from bs4 import BeautifulSoup


class Download():
    def __init__(self):
        self.id = 1

    def url_open(self, url):
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/6.0')

        # proxies = ['120.24.221.241:8888', '121.69.36.122:8118', '58.220.10.7:80']
        # proxy = random.choice(proxies)
        #
        # proxy_support = urllib.request.ProxyHandler({'http': proxy})
        # opener = urllib.request.build_opener(proxy_support)
        # urllib.request.install_opener(opener)
        response = urllib.request.urlopen(req)
        html = response.read()
        return html

    def get_page(self, url):
        html = self.url_open(url).decode('utf-8')
        soup = BeautifulSoup(html, from_encoding='utf-8')
        link = soup.find('span', class_='current')
        page = link.get_text()
        return page

    def find_jokes(self, url):
        html = self.url_open(url).decode('utf-8')
        jokes = []
        soup = BeautifulSoup(html, from_encoding='utf-8')
        links = soup.find_all('div', class_='article block untagged mb15')

        for link in links:
            thumb = link.find('div', class_='thumb')
            '''通过判断是否含有thumb属性,去除夹杂图片的冷笑话'''
            if thumb is None:
                a = link.find('div', class_='author clearfix')
                author = None if a is None else a.find('a')
                content = link.find('div', class_='content')
                var_url = None if author is None else ("http://www.qiushibaike.com" + author['href'])
                text = content.get_text()
                jokes.append({'id': self.id, 'via': '糗事百科', 'answer': '', 'content': text, 'via_url': var_url})
                self.id += 1
            else:
                pass

        return jokes

    def save_jokes(self, folder, jokes):
        with open('qiushibaike.json', 'w', encoding='utf-8') as f:
            json.dump(jokes, f)

    def download_joke(self, folder='joke', pages=10):
        try:
            os.mkdir(folder)
        except FileExistsError as e:
            print(e)
        finally:
            os.chdir(folder)

        url = "http://www.qiushibaike.com/"
        page_num = int(self.get_page(url))
        jokes = []

        for i in range(pages):
            page_num += 1
            page_url = url + '8hr/page/' + str(page_num)
            jokes += self.find_jokes(page_url)
        jokes_dict = {'jokes': jokes}
        self.save_jokes(folder, jokes_dict)


if __name__ == '__main__':
    Download().download_joke()
