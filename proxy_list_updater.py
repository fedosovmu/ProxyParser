import requests
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import json
from datetime import date
import datetime


class ProxyListUpdater():
    _proxy_list_path = 'proxy_list.txt'

    def get_random_user_agent(self):
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

    def _get_page(self):
        url = 'https://hidemy.name/ru/proxy-list/?type=hs#list'
        #url = 'http://example.com/'
        user_agent = {'User-agent': self.get_random_user_agent()}
        #proxy = self._get_free_proxy_url()
        page = requests.get(url, headers=user_agent)
        return page.text

    def _parse_page(self, page):
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

    def _get_proxy_as_url(self, proxy):
	    protocol = proxy['protocols'].split(',')[-1].strip().lower()
	    return '{}://{}:{}'.format(protocol, proxy['ip'], proxy['port'])

    def _parse_proxy_list(self):
        page = self._get_page()
        proxy_list = self._parse_page(page)
        return proxy_list        

    def update_proxy_list(self):
        today = date.today()
        last_update = self.get_proxy_list_last_update_date()
        print(type(today))
        if last_update == today:
            print('Список прокси-серверов уже обновлен')
        else:
            print('Обновление списка прокси-серверов...')
            proxy_list = self._parse_proxy_list()
            self._save_proxy_list(today, proxy_list)
            print('Список обновлен')

    def get_proxy_list_last_update_date(self):
        with open(self._proxy_list_path, 'r') as proxy_list_file:
            proxy_list_json = json.load(proxy_list_file)
        last_update_date_str = proxy_list_json['last_update_date']
        last_update_date_obj = datetime.datetime.strptime(last_update_date_str, "%Y-%m-%d").date()
        return last_update_date_obj

    def _save_proxy_list(self, update_date, proxy_list):
        proxy_list_with_update_date = {
            'last_update_date': str(update_date),
            'proxies': list(map(self._get_proxy_as_url, proxy_list))
        }

        proxy_list_with_update_date_as_json = json.dumps(proxy_list_with_update_date, indent=4, sort_keys=True)

        with open(self._proxy_list_path, 'wt') as proxy_list_file:
            proxy_list_file.write(str(proxy_list_with_update_date_as_json))