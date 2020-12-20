import requests
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import json
from datetime import date
import datetime


class ProxyListUpdater():
    _proxy_list_file_path = 'proxy_list.txt'

    @staticmethod
    def get_random_user_agent():
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [
            OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value
        ]

        user_agent_rotator = UserAgent(
            software_names=software_names,
            operating_systems=operating_systems,
            limit=100)
        user_agent = user_agent_rotator.get_random_user_agent()
        return user_agent

    @classmethod
    def _get_page(cls):
        url = 'https://hidemy.name/ru/proxy-list/?type=hs#list'
        user_agent = {'User-agent': cls.get_random_user_agent()}
        page = requests.get(url, headers=user_agent)
        return page.text

    @classmethod
    def _parse_page(cls, page):
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
                'protocols': columns[4],
                'speed': columns[5],
                'refresh_time': columns[6]
            }
            proxy_servers_list.append(proxy_server)
        return proxy_servers_list

    @classmethod
    def _get_proxy_as_url(cls, proxy):
	    protocol = proxy['protocols'].split(',')[-1].strip().lower()
	    return '{}://{}:{}'.format(protocol, proxy['ip'], proxy['port'])

    @classmethod
    def _parse_proxy_list(cls):
        page = cls._get_page()
        proxy_list = cls._parse_page(page)
        return proxy_list        

    @classmethod
    def update_proxy_list(cls):
        today = date.today()
        last_update = cls.get_proxy_list_last_update_date()
        if last_update == today:
            print('Список прокси-серверов уже обновлен')
        else:
            print('Обновление списка прокси-серверов...')
            proxy_list = cls._parse_proxy_list()
            cls._save_proxy_list(today, proxy_list)
            print('Список обновлен')

    @classmethod
    def get_proxy_list_last_update_date(cls):
        with open(cls._proxy_list_file_path, 'r') as proxy_list_file:
            proxy_list_json = json.load(proxy_list_file)
        last_update_date_str = proxy_list_json['last_update_date']
        last_update_date_obj = datetime.datetime.strptime(last_update_date_str, "%Y-%m-%d").date()
        return last_update_date_obj

    @classmethod
    def _save_proxy_list(cls, update_date, proxy_list):
        proxy_list_with_update_date = {
            'last_update_date': str(update_date),
            'proxies': list(map(cls._get_proxy_as_url, proxy_list))
        }

        proxy_list_with_update_date_as_json = json.dumps(proxy_list_with_update_date, indent=4, sort_keys=True)

        with open(cls._proxy_list_file_path, 'wt') as proxy_list_file:
            proxy_list_file.write(str(proxy_list_with_update_date_as_json))

    @classmethod
    def load_proxy_list(cls):
        with open(cls._proxy_list_file_path, 'r') as proxy_list_file:
            proxy_list_json = json.load(proxy_list_file)
            return proxy_list_json['proxies']