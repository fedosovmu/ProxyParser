import requests
from bs4 import BeautifulSoup

url = 'http://example.com/'
page = requests.get(url)

soup = BeautifulSoup(page.text, 'lxml')
print(soup.prettify())












