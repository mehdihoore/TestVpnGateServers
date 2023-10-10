from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import datetime
import re
import jdatetime



chromedriver_path = 'C:\Program Files (x86)\chromedriver\chromedriver.exe'
service = webdriver.ChromeService(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)




# Go to the website
today = datetime.date.today()

try:
    today_str = today.strftime("%Y-%m-%d")
    url = f'https://hidemy.io/en/proxy-list/'

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
    with open(r'D:\code\SSTP\testvpngate\TestVpnGateServers\proxies.txt', 'w', encoding='utf-8') as f:
        # Iterate over the list of proxies and write each proxy to the file, one per line
        for proxy in proxies:
            f.write(proxy + '\n')

except Exception as e:
    print('Error saving proxies:', e)

driver.quit()

import subprocess
from datetime import datetime, timezone, timedelta
import os
from jinja2 import Environment, FileSystemLoader

repo_dir = r'D:\code\SSTP\testvpngate\TestVpnGateServers'
os.chdir(repo_dir)



# Load the Jinja2 template from the file
template_dir = r'D:\code\SSTP\testvpngate\TestVpnGateServers'
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template('proxies_template.html')

# Read the proxies from proxies.txt and parse them into a list of dictionaries
proxies = []
with open(r'D:\code\SSTP\testvpngate\TestVpnGateServers\proxies.txt', 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split()
        
        proxy = {
            'ip': parts[0],
            'location': parts[1],
            'proxy_type': parts[2],
            'proxy_kind': parts[3],
            'timeout': parts[4] 
        }
        proxies.append(proxy)

# Render the template with the proxies data and save it to proxies.html
rendered_template = template.render(proxies=proxies)
with open(r'D:\code\SSTP\testvpngate\TestVpnGateServers\proxies.html', 'w', encoding='utf-8') as output_file:
    output_file.write(rendered_template)




chromedriver_path1 = '"D:\code\chromedriver\chromedriver.exe"'
service1 = webdriver.ChromeService(executable_path=chromedriver_path1)
driver = webdriver.Chrome(service=service1)




# Go to the website


try:
    today_str = today.strftime("%Y-%m-%d")
    url = f'https://hidemy.io/en/proxy-list/?country=IR#list'

    driver.get(url)

except Exception as e:
    print('Error getting proxies for today:', e)

   

# Find the tbody element
time.sleep(20)

# Get the page source and create a BeautifulSoup object
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

table = soup.find('table')
rows = table.find_all('tr')

# Create a list to store the proxies
proxiesiran = []

# Iterate over the rows in the table and extract the proxy information
for row in rows:
    cols = row.find_all('td')
    proxyi_string = f'{cols[0].text} {cols[1].text} {cols[2].text} {cols[3].text} {cols[4].text}'
    proxiesiran.append(proxyi_string)

# Try to open the file where the proxies will be saved
try:
    with open(r'D:\code\SSTP\testvpngate\TestVpnGateServers\iran_proxies.txt', 'w', encoding='utf-8') as f:
        # Iterate over the list of proxies and write each proxy to the file, one per line
        for proxy in proxiesiran:
            f.write(proxy + '\n')

except Exception as e:
    print('Error saving proxies:', e)

# Close the browser
driver.quit()




iran_tz = timezone(timedelta(hours=3, minutes=30))
now_utc = datetime.now(timezone.utc)
now_iran = now_utc.astimezone(iran_tz)
now_iranf = now_iran.strftime("%Y-%m-%d %H:%M:%S")
subprocess.run(["git", "fetch", "origin"])
subprocess.run(["git", "rebase", "origin/main"])
subprocess.run(["git", "add", "proxies.html"])
subprocess.run(["git", "add", "proxies.txt"])
subprocess.run(["git", "add", "iran_proxies.txt"])

subprocess.run(["git", "commit", "-m", f"🚀 proxies Updated-{now_iranf}"])

subprocess.run(["git", "push", "origin", "main"])