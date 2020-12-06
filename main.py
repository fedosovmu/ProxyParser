import requests
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


def get_free_proxy_url():
    try:
        get_proxy_url = 'https://api.getproxylist.com/proxy'
        proxy_info = requests.get(get_proxy_url).json()
        proxy_url = '{}://{}:{}'.format(proxy_info['protocol'], proxy_info['ip'], proxy_info['port'])
        print('Ипользуемый прокси: ', proxy_url)
        return proxy_url
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
    #url = 'https://hidemy.name/ru/proxy-list/?type=hs#list'
    url = 'http://example.com/'
    user_agent = {'User-agent': 'Mozilla/5.0'}
    proxy = None
    page = requests.get(url, headers = user_agent, proxies=proxy)

    soup = BeautifulSoup(page.text, 'lxml')
    print(soup.prettify())

get_page()








