import requests

import re
url2 = 'https://web.archive.org/web/%s/https://subscribers.footballguys.com/apps/depthchart.php'

from bs4 import BeautifulSoup as bs, Comment

url = 'http://web.archive.org/cdx/search/cdx?url=https://subscribers.footballguys.com/apps/depthchart.php&collapse=digest&output=json'
r = requests.get(url).json()


pages = [i[1] for i in r[1:]]
print(pages)
