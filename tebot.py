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
# SSTP function (same as before)




def get_v2ray_data():
    v2ray_links = {
        'Invizible Pro':'https://github.com/Gedsh/InviZible/releases',
        'sabat.ir Help Worker': 'https://fin.sabaat.ir/',
        'sabat.link Help Worker': 'https://f.sabaat.link/',
        'mahdibland Github': 'https://github.com/mahdibland/V2RayAggregator',
        'Bardiafa Github': 'https://github.com/Bardiafa/Free-V2ray-Config/blob/main/Persian-README.md',
        'TelegramBot Github': 'https://github.com/yebekhe/TelegramV2rayCollector',
    }
    if v2ray_links is None:
        v2ray_links = {}

    return v2ray_links

def send_server_list(bot):

    persian_date = get_persian_date_time()

    # Send SSTP document
    channel = bot.get_chat("@SSTPV2RAY")
    bot.send_message(chat_id=channel.id, text=f'{persian_date} ✅')

    bot.send_document(chat_id=channel.id, document=open('sstp.html', 'rb'),
                      caption=f'SSTP Servers - {persian_date}')

    v2ray_links = get_v2ray_data()
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
•	تور به نسخه 4.8.5 به‌روزرسانی شد.
این نسخه شامل بهبودهای امنیتی و عملکردی است.
•	استفاده از SNI سفارشی برای اتصال Tor
 مکانیسمی که به وب‌سایت‌ها اجازه می‌دهد بدانند شما از تور استفاده می‌کنید، بدون اینکه آدرس ای‌پی واقعی شما را فاش کنند.
•	اتصال Tor با TLS fingerprint Chromium
 یک ویژگی امنیتی که نشان می‌دهد در حال اتصال به یک سرور Tor واقعی هستید.
•	پل Tor WebTunnel به‌روزرسانی شد..
Tor WebTunnel یک سرویس تور امکان می‌دهد از Tor در مرورگر وب خود استفاده کنید.
•	خطای ANR در Android 4.4.2 برطرف شد.
 یک خطای سیستمی مربوط به زمانیکه برنامه برای مدت طولانی پاسخ نمی‌دهد.
•	خطای دکمه درخواست پل‌های جدید در موارد نادر برطرف شد.
این دکمه به شما امکان می‌دهد تا پل‌های جدید  را درخواست کنید.

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
    context.bot.send_document(chat_id=update.effective_chat.id, document=open('sstp.html', 'rb'), caption="SSTP Servers")
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
•	تور به نسخه 4.8.5 به‌روزرسانی شد.
این نسخه شامل بهبودهای امنیتی و عملکردی است.
•	استفاده از SNI سفارشی برای اتصال Tor
 مکانیسمی که به وب‌سایت‌ها اجازه می‌دهد بدانند شما از تور استفاده می‌کنید، بدون اینکه آدرس ای‌پی واقعی شما را فاش کنند.
•	اتصال Tor با TLS fingerprint Chromium
 یک ویژگی امنیتی که نشان می‌دهد در حال اتصال به یک سرور Tor واقعی هستید.
•	پل Tor WebTunnel به‌روزرسانی شد..
Tor WebTunnel یک سرویس تور امکان می‌دهد از Tor در مرورگر وب خود استفاده کنید.
•	خطای ANR در Android 4.4.2 برطرف شد.
 یک خطای سیستمی مربوط به زمانیکه برنامه برای مدت طولانی پاسخ نمی‌دهد.
•	خطای دکمه درخواست پل‌های جدید در موارد نادر برطرف شد.
این دکمه به شما امکان می‌دهد تا پل‌های جدید  را درخواست کنید.

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

    # Add your handlers here (start_handler, restart_handler, etc.)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)

    dispatcher.add_handler(start_handler)
    # Call send_server_list to send the first message immediately
    send_server_list(updater.bot)
   

    # Retry mechanism
    max_retries = 3
    retries = 0

    while retries < max_retries:
        try:
            updater.start_polling()
        except telegram.error.TimedOut:
            # Retry after a short delay
            time.sleep(5)
            retries += 1
            continue
        else:
            break
    else:
        print("Exceeded maximum retries. Failed to start polling.")

    updater.idle()
