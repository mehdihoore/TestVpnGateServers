import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, filters, CommandHandler, CallbackContext
import requests as rs
from telegram.ext import JobQueue
import pandas as pd
from bs4 import BeautifulSoup
import os
import sys
import jdatetime
import datetime
import pytz
from time import sleep
import textwrap
import re
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
def get_persian_date_time():
    # Get the current date and time in Persian (Jalali) calendar
    now = datetime.datetime.now()

    hour = now.hour + 3
    minute = now.minute + 30

    if minute >= 60:
        hour += 1
        minute -= 60

    if hour >= 24:
        hour -= 24
    nowp = jdatetime.datetime.now()
    nowt = datetime.datetime(now.year, now.month, now.day, hour, minute, now.second, now.microsecond)
    persian_date_time = nowp.strftime("%A, %d %B %Y ") + nowt.strftime("%H:%M:%S")
    return persian_date_time
#get url and download v2flyNG apk app
url = 'https://github.com/2dust/v2flyNG/tags'
response = rs.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
# Find link by tag and class
link = soup.find('a', class_='Link--primary', href=True)
download_url = 'https://github.com' + link['href']
# Get release page URL 
release_page = download_url
parts = release_page.split('/')
tag = parts[-1]
apk_url = f'{release_page}/v2flyNG_{tag}.apk'
apk_url = apk_url.replace('tag','download')
parts1 = apk_url.split('/')
tag1 = parts1[-1]
response = rs.get(apk_url)
with open(f'{tag1}', 'wb') as f:
    f.write(response.content)



def get_v2ray_data():
    v2ray_links = {
        'لیست همه وی‌پی‌ان‌ها در وبسایت ': 'https://list.sabaat.ir',
        'Invizible Pro Google Play':'https://play.google.com/store/apps/details?id=pan.alexander.tordnscrypt.gp',
        'sabat.ir Help Worker': 'https://fin.sabaat.ir/',
        'sabat.link Help Worker': 'https://f.sabaat.link/',
        'mahdibland Github': 'https://github.com/mahdibland/V2RayAggregator',
        'Bardiafa Github': 'https://github.com/Bardiafa/Free-V2ray-Config/blob/main/Persian-README.md',
        'TelegramBot Github': 'https://github.com/yebekhe/TelegramV2rayCollector',
    }
    if v2ray_links is None:
        v2ray_links = {}

    return v2ray_links
def warpplus():
    warplinks = {
        'برنامه وارپ را دانلود کنید android:': 'https://play.google.com/store/apps/details?id=com.cloudflare.onedotonedotonedotone',
        'به این ربات تلگرامی بروید و دستور /generate را بزنید ':'https://t.me/generatewarpplusbot',
        'شکل پاسخ به سوال: /generate 123 ':'https://t.me/generatewarpplusbot',
        'windows app': 'https://install.appcenter.ms/orgs/cloudflare/apps/1.1.1.1-windows-1/distribution_groups/release',
        'ios app': 'https://apps.apple.com/us/app/cloudflare-one-agent/id6443476492',
        'linux app' : 'https://pkg.cloudflareclient.com/'    
    }
    if warplinks is None:
        warplinks = {}
    return warplinks
warplink= warpplus()
textv2fly = """ برنامه‌ای سریع و ساده برای اجرای سورهای v2ray
این برنامه را نصب کنید و سپس یکی از فایلهای .txt
را باز کرده و محتوای آن را در برنامه کپی کنید یا اگر زیاد بود share کنید."""
def send_server_list(bot):

    persian_date = get_persian_date_time()
    sabat='https://list.sabaat.ir'
    # Send SSTP document
    channel = bot.get_chat("@SSTPV2RAY")
    bot.send_message(chat_id=channel.id, text=f'{persian_date} ✅')
    
    bot.send_document(chat_id=channel.id, document=open('filtered_sstp.html', 'rb'),
                      caption=f'SSTP Servers - {persian_date}')
    proxi=rs.get('https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/index.html')
    with open('index.html', 'wb') as f:
                f.write(proxi.content)
    os.rename('index.html','Mtproto.html')
    bot.send_document(chat_id=channel.id, document=open('Mtproto.html', 'rb'),
                      caption=f'MtProto Telegram Proxies - {persian_date}')
    bot.send_document(chat_id=channel.id, document=open('iran_proxies.txt', 'rb'),
                      caption=f'پروکسی سرورهای ایران/برای زمان اینترانت - {persian_date}')
    bot.send_document(chat_id=channel.id, document=open('proxies.txt', 'rb'),
                      caption=f'همه پروکسی سرورها- {persian_date}\n {apk_url}')
    try:
        bot.send_document(chat_id=channel.id, document=open(f'{tag1}', 'rb'),
                          caption=f'{textv2fly}-{persian_date}\n {apk_url}')
    except:
            print('can not send')
    v2ray_links = get_v2ray_data()
    links = [
        'https://link.mehdi-hoore.workers.dev/sub/f.sabaat.link',
        'https://fin.hore.workers.dev/sub/fin.sabaat.ir',
        'https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity',

    'https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity.txt',

    'https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/splitted/ssr.txt',

    'https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/splitted/ss.txt',

    'https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/splitted/trojan.txt',

    'https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/splitted/vmess.txt'
      ]
    names = ['Worker .ir' , 'Worker .link', 'mahdibland Eternity',
         'mahdibland Eternity txt', 'mahdibland ssr', 'mahdibland ss',
         'mahdibland trojan', 'mahdibland vmess'
         ]

    # Get the latest APK version and download URL

    additional_file_urls = [
        'https://github.com/Gedsh/InviZible/releases/download/v2.0.0-beta/Invizible_Pro__beta_ver.2.0.0.apk',
        'https://github.com/Gedsh/InviZible/releases/download/v2.0.0-beta/Invizible_Pro__beta_ver.2.0.0_arm64.apk'
    ]
    additional_file_names = ['Invizible_Pro__beta_ver.2.0.0.apk',
        'Invizible_Pro__beta_ver.2.0.0_arm64.apk'
    ]


    tt = '''
•	تور به نسخه 4.8.7 بروز شد
•	پرپل آی۲پی به نسخه 2.49.0 بروز شد
•	اتصال پل اسنوفلیک آپدیت شد
•	اضافه کردن پل‌های جدید اسنوفلیک آپدیت شد
•	اتصال پل کانجر آپدیت شد
•	تعمیرات و بهینه‌سازی‌ها

    '''

    wrapped_tt = textwrap.fill(tt, initial_indent="    ", subsequent_indent="    ")
    for url, name in zip(additional_file_urls, additional_file_names):
        try:
            response = rs.get(url)
            with open(name, 'wb') as f:
                f.write(response.content)
            bot.send_document(chat_id=channel.id, document=open(name, 'rb'), caption=f'{persian_date} \n{name}\n {url}\n {tt}')
        except Exception as e:
            print(f"Error sending {name}: {e}")
    count = 0

    for link in links:
        try:
            response = rs.get(link)
            content = response.text
        except rs.exceptions.RequestException as e:
            print(f"Error retrieving {link}: {e}")
            continue

        # Save to file
        with open(f'{link.split("/")[-1]}.txt', 'w') as f:
            try:
                f.write(content)
            except UnicodeEncodeError as e:
                print(f"Error retrieving {link}: {e}")
                continue
        # Send file
        try:
            bot.send_document(chat_id=channel.id, document=open(f'{link.split("/")[-1]}.txt', 'rb'), caption=f'{persian_date} \n{names[count]}\n {link}')
        except Exception as e:
            sleep(60)

        count += 1
    inb=[]
    try: 
        inb=[]

        for name, link in warplink.items():
            inb.append([InlineKeyboardButton(name, url=link)])
        r_markup = InlineKeyboardMarkup(inb)
        bot.send_message(chat_id=channel.id, text=f'وارپ پر سرعت بدون عوض کردن ای پی ', reply_markup=r_markup)


    except:
        print("nothing is in here")
    inline_buttons = []

    for name, link in v2ray_links.items():
        inline_buttons.append([InlineKeyboardButton(name, url=link)])
    reply_markup = InlineKeyboardMarkup(inline_buttons)
   



    bot.send_message(chat_id=channel.id, text=f'{persian_date} ✅', reply_markup=reply_markup)

def start(update: Update, context: CallbackContext):
    # Send the initial message with instructio
    initial_message = "درود برای شروع کار با ربات از کامند :\n"
    initial_message += "/start"
    initial_message += "\n استفاده کنید. کارکرد ربات:\n"
    initial_message += "1. بعد از شروع رباتیک فایل html شامل سرورهای SSTP برای استفاده در ویندوز و اندروید ارسال می‌کند. فایل شامل یکفیلتر جستجو است که میتوانید کشورها را با آن انتخاب کنید.\n"
    initial_message += "2. سپس لیستی از سرورها برای استفاده در کلاینت ‌V2ray است که لینک آنها یکی یکی نشان داده می شود.  .\n"
    initial_message += "لطفا توجه داشته باشید که لینکها هر چند ساعت آپدیت می‌شود پس برای تهیه جدید ترین سرورها گر سرورهای قبلی از کار افتاد دوباره کامند استارت را وارد کنید و فایل جدید بگیرید.\n"
    initial_message += "\n لطفاً کمی تآمل کنید . . . !"
    context.bot.send_message(chat_id=update.effective_chat.id, text=initial_message)

    # Get SSTP data
   

    # Get V2ray links
    v2ray_links = get_v2ray_data()



    # Create inline buttons for V2ray options
    inline_buttons = []
    for name, link in v2ray_links.items():
        inline_buttons.append([InlineKeyboardButton(name, url=link)])

    # Create inline keyboard markup
    reply_markup = InlineKeyboardMarkup(inline_buttons)

    # Send the SSTP data as an HTML file
    context.bot.send_document(chat_id=update.effective_chat.id, document=open('filtered_sstp.html', 'rb'), caption="SSTP Servers")
    links = [
        'https://link.mehdi-hoore.workers.dev/sub/f.sabaat.link',
        'https://fin.hore.workers.dev/sub/fin.sabaat.ir',
        'https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity',

    'https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity.txt',

    'https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/splitted/ssr.txt',

    'https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/splitted/ss.txt',

    'https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/splitted/trojan.txt',

    'https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/splitted/vmess.txt',
        'https://raw.githubusercontent.com/Bardiafa/Free-V2ray-Config/main/Splitted-By-Protocol/vmess.txt',

        'https://raw.githubusercontent.com/yebekhe/V2Hub/main/merged_base64',
        'https://raw.githubusercontent.com/yebekhe/V2Hub/main/Split/Base64/vmess',


      ]
    names = ['Worker .ir' , 'Worker .link', 'mahdibland Eternity',
         'mahdibland Eternity txt', 'mahdibland ssr', 'mahdibland ss',
         'mahdibland trojan', 'mahdibland vmess',
         'Bardiafa vemss',

         'Telegram collector: merged_base64',
         'Telegram collector: Base64_vmess',

         ]

    # Get the latest APK version and download URL

    additional_file_urls = [
        'https://github.com/Gedsh/InviZible/releases/download/v1.9.8-beta/Invizible_Pro__beta_ver.1.9.8.apk',
        'https://github.com/Gedsh/InviZible/releases/download/v1.9.8-beta/Invizible_Pro__beta_ver.1.9.8_arm64.apk'
    ]
    additional_file_names = ['Invizible_Pro__beta_ver.1.9.8.apk',
        'Invizible_Pro__beta_ver.1.9.8_arm64.apk'
    ]
    tt = '''
•	تور به نسخه 4.8.7 بروز شد
•	پرپل آی۲پی به نسخه 2.49.0 بروز شد
•	اتصال پل اسنوفلیک آپدیت شد
•	اضافه کردن پل‌های جدید اسنوفلیک آپدیت شد
•	اتصال پل کانجر آپدیت شد
•	تعمیرات و بهینه‌سازی‌ها

    '''

    for link in links:
        try:
            response = rs.get(link)
            content = response.text
        except rs.exceptions.RequestException as e:
            print(f"Error retrieving {link}: {e}")
            continue

        # Save to file
        with open(f'{link.split("/")[-1]}.txt', 'w') as f:
            try:
                f.write(content)
            except UnicodeEncodeError as e:
                print(f"Error retrieving {link}: {e}")
                continue

        # Send file
        try:
            context.bot.send_document(chat_id=update.effective_chat.id, document=open(f'{link.split("/")[-1]}.txt', 'rb'), caption=f'{persian_date} \n{names[count]}\n {link}')
        except Exception as e:
            sleep(60)
    # Send the V2ray options with inline keyboard
    context.bot.send_message(chat_id=update.effective_chat.id, text="Select V2ray option:", reply_markup=reply_markup)

if __name__ == '__main__':
    updater = Updater(token='6210383014:AAHGwo4q87zwKTjO1WgJWrbjEgx5V-TO8_A', request_kwargs={'read_timeout': 30})

    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)

    dispatcher.add_handler(start_handler)
    send_server_list(updater.bot) 
