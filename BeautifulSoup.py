import requests # for using HTTP requests
from bs4 import BeautifulSoup # for searching through response

# HTTP request
url = 'https://en.wikipedia.org/wiki/Wikipedia:Vital_articles/List_of_all_articles'
response = requests.get(url)

characterHtmlClass = 'mw-content-ltr mw-parser-output' # 0, 1, ... a, b, ...

# parsing
soupParser = BeautifulSoup(response.content, 'html.parser')

divs = soupParser.find('div', class_ = characterHtmlClass)
content = divs.find_all('p')

print(content)

for c in content:
    if 'a href="/wiki/' not in c:
        content.remove(c)

print(len(content))


