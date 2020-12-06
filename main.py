import requests
import lxml.html

#url = "https://hidemy.name/ru/proxy-list/?type=hs#list"
url = 'http://example.com/'

#page = requests.get(url)
#tree = etree.fromstring(page.text)

html = lxml.html.fromstring('''\
    <html><body onload="" color="white">
      <p>Hi  !</p>
    </body></html>
 ''')

print(html.tag)











