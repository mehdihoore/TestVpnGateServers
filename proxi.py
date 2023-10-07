from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import datetime
import re



chromedriver_path = 'C:\Program Files (x86)\chromedriver\chromedriver.exe'
service = webdriver.ChromeService(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)




# Go to the website
today = datetime.date.today()

try:
    today_str = today.strftime("%Y-%m-%d")
    url = f'https://checkerproxy.net/archive/{today_str}'

    driver.get(url)

except Exception as e:
    print('Error getting proxies for today:', e)

    yesterday = today - datetime.timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")

    url = f'https://checkerproxy.net/archive/{yesterday_str}'
    driver.get(url)

# Find the tbody element
time.sleep(20)

# Get the page source and create a BeautifulSoup object
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

table = soup.find('table')
rows = table.find_all('tr')

# Create a list to store the proxies
proxies = []

# Iterate over the rows in the table and extract the proxy information
for row in rows:
    cols = row.find_all('td')
    proxy_string = f'{cols[0].text} {cols[1].text} {cols[2].text} {cols[3].text} {cols[4].text}'
    proxies.append(proxy_string)

# Try to open the file where the proxies will be saved
try:
    with open('D:\code\SSTP\proxies\proxies.txt', 'w', encoding='utf-8') as f:
        # Iterate over the list of proxies and write each proxy to the file, one per line
        for proxy in proxies:
            f.write(proxy + '\n')

except Exception as e:
    print('Error saving proxies:', e)
iran_proxies = []

# Iterate over the list of proxies and extract the Iran proxies
for proxy in proxies:
    if re.search('Iran', proxy):
        iran_proxies.append(proxy)

# Try to open the file where the Iran proxies will be saved
try:
    with open('D:\code\SSTP\proxies\iran_proxies.txt', 'w', encoding='utf-8') as f:
        # Iterate over the list of Iran proxies and write each proxy to the file, one per line
        for proxy in iran_proxies:
            f.write(proxy + '\n')

except Exception as e:
    print('Error saving Iran proxies:', e)
# Close the browser
driver.quit()

import subprocess

subprocess.run(["git", "add", "D:\code\SSTP\proxies\proxies.txt"])
subprocess.run(["git", "add", "D:\code\SSTP\proxies\iran_proxies.txt"])
subprocess.run(["git", "commit", "-m", "Add Iran proxies and general proxies"])
subprocess.run(["git", "push", "origin", "master"])