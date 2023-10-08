import requests
from bs4 import BeautifulSoup
import re
url = 'https://github.com/Gedsh/InviZible/tags'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

# Find link by tag and class
link = soup.find('a', class_='Link--primary', href=True)

download_url = 'https://github.com' + link['href']

print(download_url)



# Get release page URL 
release_page = download_url


parts = release_page.split('/')
tag = parts[-1]
tag = tag.replace('-beta','')
tag = tag.replace('v','')
# Remove 'tag' prefix
a = 'Invizible_Pro__beta_ver.2.0.0.apk'


apk_url = f'{release_page}/Invizible_Pro__beta_ver.{tag}.apk'
apk_url = apk_url.replace('tag','download')
print(apk_url)
parts1 = apk_url.split('/')
tag1 = parts1[-1]
print(tag1)
response = requests.get(apk_url)
import os
print(os.getcwd())
with open(f'D:\code\SSTP\{tag1}', 'wb') as f:
  f.write(response.content)