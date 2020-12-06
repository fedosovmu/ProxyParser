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

def save_page_to_txt_file(page):
    file = open("db/hiddenme_page.txt","a") 
    file.writelines(page)
    file.close()
    print('file saving')

def parse_page(page):
    soup = BeautifulSoup(page, 'lxml')
    table = soup.find('table')
    rows = table.find('tbody').find_all('tr')
    proxy_servers_list = []
    for row in rows:
        columns = row.find_all('td')
        columns = list(map(lambda x: x.text.strip(), columns))
        proxy_server = {
            'ip': columns[0],
            'port': columns[1],
            'country': columns[2],
            'delay': columns[3],
            'protocol': columns[4].split(',')[-1].strip().lower(),
            'speed': columns[5],
            'refresh_time': columns[6]
        }
        proxy_servers_list.append(proxy_server)
    return proxy_servers_list

def print_proxy_as_url(proxy):
    print('{}://{}:{}'.format(proxy['protocol'], proxy['ip'], proxy['port']))

page = get_page() 
#db["hidemy_site_page"] = page
#page = db["hidemy_site_page"]
proxy_list = parse_page(page)

print('Получены прокси серверы:')
for proxy in proxy_list:
    print_proxy_as_url(proxy)








