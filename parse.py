# Парс текста заголовка и ссылки на новость с lenta.ru

from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
data_lenta = pd.read_csv("1.csv")
print(data_lenta.head())
links_lenta=[]
data_lenta.info()
links_lenta = data_lenta["link"]
f = open('lenta_clean-1.csv', 'w')
writer = csv.writer(f)
for i in range(0,len(links_lenta)):
   current_page = 1
   url = links_lenta[i]
   req = requests.get(url)
   page_content = BeautifulSoup(req.content, 'html.parser')
   post_url = links_lenta[i]
   post_req = requests.get(post_url)
   post = BeautifulSoup(post_req.content, 'html.parser')
   post_content = post.find("p", {"class": "topic-body__content-text"})
   post_title=post.find("span", {"class": "topic-body__title"})
   if post_content:
                post_content = post_content.text.replace('\n', '').replace(u'\xa0', ' ').replace('"', '“').strip()
   else:
                failed_news.append(post_url)
   print(i)
   writer.writerow([post_content,'+', post_url,'+', post_title])

# парс текста заголовка и ссылки на новость с dni.ru

from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
data_lenta = pd.read_csv("2.csv")
print(data_lenta.head())
links_lenta=[]
data_lenta.info()
links_lenta = data_lenta["link"]
f = open('dni_clean-2.csv', 'w')
writer = csv.writer(f)
for i in range(0,len(links_lenta)):
   current_page = 1
   url = links_lenta[i]
   req = requests.get(url)
   page_content = BeautifulSoup(req.content, 'html.parser')
   post_url = links_lenta[i]
   post_req = requests.get(post_url)
   post = BeautifulSoup(post_req.content, 'html.parser')
   post_title = post.find("h1").get_text()
   post_content = post.find("div", attrs={"class": "article__text"})
   if post_content is None:
      post_content = "none"
   else:
      for t in post_content.findAll('p'):
         post_text =[]
         post_text = t.text
   writer.writerow([post_text, '+', post_url, '+', post_title])
   print(i)

# парс текста заголовка и ссылки на новость с panorama.ru

import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://panorama.pub"
CATEGORIES = [
    '/politics',
    '/society',
    '/science',
    '/economics',
]
FILE_NAME = 'panorama.csv'  # Must be created prior
PAGE_PARAM = '?page='
news = []
failed_news = []
file = open('panorama.csv', 'w', encoding='utf8', newline='')
writer = csv.writer(file, quoting=csv.QUOTE_ALL)
for category in CATEGORIES:
    current_page = 1
    url = BASE_URL + category + PAGE_PARAM + str(current_page)
    req = requests.get(url)
    while req.status_code == 200:
        page_content = BeautifulSoup(req.content, 'html.parser')
        post_urls = [BASE_URL + a['href'] for a in page_content.findAll('a', {"class": ["rounded-md", "hover:text-secondary"]})]
        for post_url in post_urls:
            post_req = requests.get(post_url)

            if post_req.status_code != 200:
                continue
            post = BeautifulSoup(post_req.content, 'html.parser')
            post_content = post.find("div", {"class": "entry-contents"})
            post_title = post.find('h1',{'class':'font-bold text-2xl md:text-3xl lg:text-4xl pl-1 pr-2 self-center'})
            if post_content:
                post_content = post_content.text.replace('\n', '').replace(u'\xa0', ' ').replace('"', '“').strip()
            else:
                failed_news.append(post_url)
            print(post_url)
            writer.writerow([post_content,'+', post_url, '+', post_title])

        print(category + ", page " + str(current_page))
        current_page += 1
        url = BASE_URL + category + PAGE_PARAM + str(current_page)
        req = requests.get(url)
print(failed_news)
file.close()

# парс ссылок на картинки lenta.ru

from bs4 import BeautifulSoup
import urllib.request
import re
import csv
import requests
import pandas as pd

data_lenta = pd.read_csv("lenta.csv")
print(data_lenta.head())
links_lenta=[]
links_lenta = data_lenta["Column2"].str[:-2]
print(links_lenta[0])



f = open('lenta_im.csv', 'w')
writer = csv.writer(f)
for i in range(0, len(links_lenta)):
    html_page = urllib.request.urlopen(links_lenta[i])
    soup = BeautifulSoup(html_page, features="html.parser")
    images = []
    for img in soup.findAll('img'):
        images.append(img.get('src'))
    i = i + 1
    print(images)
    writer.writerow(images)

# загрузка картинок с спаршенных ссылок lenta.ru

from bs4 import BeautifulSoup
import urllib.request
import re
import csv
import requests
import pandas as pd

data_lenta_im = pd.read_csv("Lenta_img_clean.csv")
print(data_lenta_im.head())
links = []
a=0
links = data_lenta_im["Column1"]
for i in range(0, len(links)):
 img_data = requests.get(links[i]).content
 with open(str(a) + '.jpg', 'wb') as handler:
    handler.write(img_data)
    i = i + 1
    a = a + 1

# парас картинки с панорамы

from bs4 import BeautifulSoup
import csv
import pandas as pd
from urllib.request import Request, urlopen
import urllib.request
import re
import requests

data = []
images = []
df = pd.read_csv("panorama-sscience.csv")
data = df["link"]

f = open('fake-science.csv', 'w')
writer = csv.writer(f)
for i in range(0, len(data)):
    req = Request(url=data[i], headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()
    soup = BeautifulSoup(html_page, features="html.parser")
    images.append(soup.findAll('div', class_='container mx-auto h-[250px] md:h-[325px] lg:h-[400px] bg-cover lg:bg-contain bg-no-repeat bg-left-top'))
    f.write(str(images[i])+'+')
    print(i)

# парс картинок с ленты

from bs4 import BeautifulSoup
import csv
import pandas as pd
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import urllib.request
import re
import requests

data = []
images = []
df = pd.read_excel("img-links.xlsx")



links = []
links= df["img-true-mir"]

a=0
for i in range(0, len(links )):
    img_data = requests.get(links[i]).content
    with open(str(a) + '.jpg', 'wb') as handler:
        handler.write(img_data)
        a = a + 1
    print(i)
