import requests # for using HTTP requests
from lxml import html # for searching through response

# HTTP request
url = 'https://en.wikipedia.org/wiki/Wikipedia:Vital_articles/List_of_all_articles'
response = requests.get(url)

characterHtmlClass = 'mw-content-ltr mw-parser-output' # 0, 1, ... a, b, ...

# parsing
tree = html.fromstring(response.content)


link_titles = tree.xpath('//a/text()')

# Print the extracted link titles
for title in link_titles:
    print(title)




