import requests
from bs4 import BeautifulSoup as bs
import urllib
import re
import sys
sys.path.insert(0,'..')
from security import localDirectories

urlAppend = 'https://maddenratings.weebly.com'
for i in range(8,21):
    print(i)

    url = 'https://maddenratings.weebly.com/madden-nfl-%s.html' % str(i).zfill(2)

    home_page = requests.get(url).text

    soup = bs(home_page,'html.parser')

    links = soup.find_all('a',attrs={'href': re.compile("xlsx$|xls$")})
    for link in links:
        newUrl = link.get('href')

        fileName = newUrl.split('/')[-1:][0]
        print(newUrl)
        print(fileName)



        r = requests.get(urlAppend + newUrl, allow_redirects=True)
        saveFile = localDirectories['madden_files'] + '%s.xlsx'
        open(saveFile % fileName,'wb').write(r.content)
