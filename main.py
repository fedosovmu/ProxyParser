import requests
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from replit import db


def get_free_proxy_url():
    try:
        get_proxy_url = 'https://api.getproxylist.com/proxy'
        proxy_info = requests.get(get_proxy_url).json()
        protocol = proxy_info['protocol']
        if protocol != 'http' and protocol != 'https':
            print('Неподходящий протокол проксисервера')
            return None
        proxy_url = '{}://{}:{}'.format(proxy_info['protocol'], proxy_info['ip'], proxy_info['port'])
        print('Ипользуемый прокси: ', proxy_url)
        return { proxy_info['protocol']: proxy_url }
    except:
        print('Проксисервер недоступен')
        return None

def get_random_user_agent():
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   
    
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    user_agent = user_agent_rotator.get_random_user_agent()
    return user_agent

def get_page():
    url = 'https://hidemy.name/ru/proxy-list/?type=hs#list'
    #url = 'http://example.com/'
    user_agent = {'User-agent': get_random_user_agent()}
    proxy = get_free_proxy_url()
    page = requests.get(url, headers = user_agent, proxies=proxy)
    return page.text

def parse_page(page):
    #soup = BeautifulSoup(page.text, 'lxml')
    soup = BeautifulSoup(page, 'lxml')
    print(soup.prettify())
    print('kek')

def save_page_to_txt_file(page):
    file = open("db/hiddenme_page.txt","a") 
    file.writelines(page)
    file.close()
    print('file saving')


#page = get_page() 
#db["hidemy_site_page"] = page
page = db["hidemy_site_page"]
parse_page(page)

print('end')








