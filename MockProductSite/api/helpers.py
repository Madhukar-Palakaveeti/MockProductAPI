from bs4 import BeautifulSoup
from requests_html import HTMLSession


CLASS_LIST = ['s1Q9rs', '_2UzuFa', '_1fQZEK']
HEADERS = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',  
           'Accept-Language' : 'en-US,en;q=0.5'}
session = HTMLSession()


def get_links(url):
    URL_LIST = []
    page = session.get(url,headers=HEADERS)
    soup = BeautifulSoup(page.text,'html.parser')
    links_tag = soup.find_all('a', class_ = CLASS_LIST)
    for link in links_tag:
        new_link = f'https://www.flipkart.com'+link['href']
        URL_LIST.append(new_link)
    return URL_LIST




