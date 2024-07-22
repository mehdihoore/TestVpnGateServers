import logging
import requests as rs
from bs4 import BeautifulSoup
import datetime
import jdatetime
import os
import textwrap
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import pytz
from time import sleep
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
    nowt = datetime.datetime(now.year, now.month, now.day,
                             hour, minute, now.second, now.microsecond)
    persian_date_time = nowp.strftime(
        "%A, %d %B %Y ") + nowt.strftime("%H:%M:%S")
    return persian_date_time


def get_latest_oblivion_apk():
    url = 'https://github.com/bepass-org/oblivion/releases/latest'
    response = rs.get(url)

    if response.status_code != 200:
        logging.error(f'Failed to fetch the latest release page. Status code: {response.status_code}')
        return None, None

    soup = BeautifulSoup(response.text, 'html.parser')

    breadcrumb_item = soup.find(
        'li', class_='breadcrumb-item breadcrumb-item-selected')
    if not breadcrumb_item:
        logging.error('No breadcrumb item found in the latest release.')
        return None, None

    release_tag = breadcrumb_item.find('a')['href']
    release_url = f'https://github.com{release_tag}'.replace('tag', 'expanded_assets')

    response = rs.get(release_url)
    if response.status_code != 200:
        logging.error(f'Failed to fetch the release page. Status code: {response.status_code}')
        return None, None

    soup = BeautifulSoup(response.text, 'html.parser')

    apk_link = None
    for div in soup.find_all('div', class_='d-flex flex-justify-start col-12 col-lg-9'):
        a_tag = div.find('a', href=True)
        if a_tag and a_tag['href'].endswith('.apk'):
            apk_link = 'https://github.com' + a_tag['href']
            break

    if not apk_link:
        logging.error('No APK file found in the latest release.')
        return None, None

    logging.info(f'APK URL: {apk_link}')

    response = rs.get(apk_link)
    if response.status_code != 200:
        logging.error(f'Failed to download the APK file. Status code: {response.status_code}')
        return None, None

    apk_filename = os.path.basename(a_tag['href'])
    with open(apk_filename, 'wb') as f:
        f.write(response.content)

    logging.info(f'APK file downloaded: {apk_filename}')
    return apk_filename, apk_link


apk_filename, apk_link = get_latest_oblivion_apk()


def send_apk_to_telegram_channel(apk_filename, bot_token, chat_id):
    persian_date = get_persian_date_time()
    url = f'https://api.telegram.org/bot{bot_token}/sendDocument'
    files = {'document': open(apk_filename, 'rb')}
    data = {'chat_id': chat_id,'caption': f"\n {apk_link}\n{persian_date}\n برنامه oblivion جایگزین وارپ"}

    response = rs.post(url, files=files, data=data)
    if response.status_code == 200:
        logging.info('APK file sent successfully.')
    else:
        logging.error(f'Failed to send APK file. Status code: {response.status_code}, Response: {response.text}')

def get_latest_v2ray_apk():
    url = 'https://github.com/2dust/v2rayNG/releases/'
    response = rs.get(url)

    if response.status_code != 200:
        logging.error(f'Failed to fetch the latest release page. Status code: {response.status_code}')
        return None, None

    soup = BeautifulSoup(response.text, 'html.parser')

    release_tag_element = soup.find(
        'a', class_='Link--primary', href=lambda href: href and '/releases/tag/' in href)
    if not release_tag_element:
        logging.error('No release tag found in the latest release.')
        return None, None

    release_tag = release_tag_element['href']
    release_url = f'https://github.com{
        release_tag}'.replace('/tag/', '/expanded_assets/')

    response = rs.get(release_url)
    if response.status_code != 200:
        logging.error(f'Failed to fetch the release page. Status code: {response.status_code}')
        return None, None

    soup = BeautifulSoup(response.text, 'html.parser')

    apk_link = None
    priorities = ['universal', 'arm64-v8a', 'armeabi-v7a', 'x86_64', 'x86']

    for priority in priorities:
        for a_tag in soup.find_all('a', href=True):
            if a_tag['href'].endswith('.apk') and priority in a_tag['href'].lower():
                apk_link = 'https://github.com' + a_tag['href']
                break
        if apk_link:
            break

    if not apk_link:
        # If no prioritized APK found, fall back to any APK
        for a_tag in soup.find_all('a', href=True):
            if a_tag['href'].endswith('.apk'):
                apk_link = 'https://github.com' + a_tag['href']
                break

    if not apk_link:
        logging.error('No APK file found in the latest release.')
        return None, None

    logging.info(f'APK URL: {apk_link}')

    response = rs.get(apk_link)
    if response.status_code != 200:
        logging.error(f'Failed to download the APK file. Status code: {response.status_code}')
        return None, None

    apkv2ray_filename = os.path.basename(apk_link)
    apkv2ray_link = apk_link
    with open(apkv2ray_filename, 'wb') as f:
        f.write(response.content)

    logging.info(f'APK file downloaded: {apkv2ray_filename}')
    return apkv2ray_filename, apkv2ray_link


apkv2ray_filename, apkv2ray_link = get_latest_v2ray_apk()


def send_apkv2ray_to_telegram_channel(apk_filename, bot_token, chat_id):
    persian_date = get_persian_date_time()
    url = f'https://api.telegram.org/bot{bot_token}/sendDocument'
    files = {'document': open(apkv2ray_filename, 'rb')}
    data = {'chat_id': chat_id,
            'caption': f"\n {apkv2ray_link}\n{persian_date}\n برنامه‌ای سریع و ساده برای اجرای سورهای v2ray\nاین برنامه را نصب کنید و سپس یکی از فایلهای .txt را باز کرده و محتوای آن را در برنامه کپی کنید یا اگر زیاد بود share کنید. "}

    response = rs.post(url, files=files, data=data)
    if response.status_code == 200:
        logging.info('APK file sent successfully.')
    else:
        logging.error(f'Failed to send APK file. Status code: {response.status_code}, Response: {response.text}')

def get_v2ray_data():
    v2ray_links = {
        'لیست وی‌پی‌ان‌ها در وبسایت ': 'https://list.sabaat.ir',
        'sabat.ir Help Worker': 'https://fin.sabaat.ir/',
        'sabat.link Help Worker': 'https://f.sabaat.link/',
        'mahdibland Github': 'https://github.com/mahdibland/V2RayAggregator',
        ' اندروید کلاینت V2ray ': 'https://play.google.com/store/apps/details?id=com.v2ray.ang',
        'کلاینت SSTP': 'https://play.google.com/store/apps/details?id=it.colucciweb.vpnclientpro&pcampaignid=web_share',
        'Oblivion وارپ جدید': apk_link
    }
    return v2ray_links


def warpplus():
    warplinks = {'نرم افزار warp با اسم Oblivion برای اندروید ساخته شد از لینک زیر دانلود کنید. ': apk_link,
                 'لیست کشورها (دو حرفی ) در لینک .خواستی لوکیشن رو عوض کنی از طریق تنظیمات، سایفون رو فعال کنید.': 'https://github.com/Ptechgithub/wireguard-go',
                 }
    return warplinks


def send_server_list(bot_token, chat_id):
    persian_date = get_persian_date_time()
    v2ray_links = get_v2ray_data()
    warplink = warpplus()

    url = f'https://api.telegram.org/bot{bot_token}/sendDocument'
    send_document(chat_id, "sstp.csv",f'SSTP Servers https://evhr.sabaat.ir/ ✅- {persian_date}')
    proxi = rs.get('https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/proxies')

    soup = BeautifulSoup(proxi.content, "html.parser")
    mtprototext = soup.get_text()
    with open("mtproto.txt", "w") as f:
        f.write(mtprototext)

    send_document(chat_id, 'mtproto.txt', f'پروکسی تلگرام \n https://mtproto.sabaat.ir/\n - {persian_date}')


    links = [
        'https://vl.sabaat.ir/sub',
        'https://fin.hore.workers.dev/sub/fin.sabaat.ir',
        'https://raw.githubusercontent.com/mahdibland/SSAggregator/master/sub/sub_merge_base64.txt',
        'https://raw.githubusercontent.com/mahdibland/SSAggregator/master/sub/sub_merge.txt',
        'https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/splitted/ssr.txt',
        'https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/splitted/ss.txt',
        'https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/splitted/trojan.txt',
        'https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/splitted/vmess.txt'
    ]

    names = ['Worker .ir', 'Worker .link', 'mahdibland Base64', 'mahdibland MIX', 'mahdibland ssr', 'mahdibland ss', 'mahdibland trojan', 'mahdibland vmess']

    for link, name in zip(links, names):
        try:
            response = rs.get(link)
            content = response.text
            file_name = f'{link.split("/")[-1]}.txt'
            with open(file_name, 'w') as f:
                f.write(content)
            send_document(chat_id, file_name, f'برای استفاده در برنامه‌های v2ray \n{persian_date} \n{name}\n {link}')
        except rs.exceptions.RequestException as e:
            logging.error(f"Error retrieving {link}: {e}")
        except UnicodeEncodeError as e:
            logging.error(f"Error writing {link} content: {e}")

    inb = []
    try:
        for name, link in warplink.items():
            inb.append([InlineKeyboardButton(name, url=link)])
        r_markup = InlineKeyboardMarkup(inb)
        send_message(chat_id, f'وارپ پر سرعت بدون عوض کردن ای پی', r_markup)
    except:
        logging.error("Error sending warp links")

    inline_buttons = []
    for name, link in v2ray_links.items():
        inline_buttons.append([InlineKeyboardButton(name, url=link)])
    reply_markup = InlineKeyboardMarkup(inline_buttons)
    send_message(chat_id, f'{persian_date} ✅', reply_markup)


def send_document(chat_id, document_path, caption):
    url = f'https://api.telegram.org/bot{bot_token}/sendDocument'
    files = {'document': open(document_path, 'rb')}
    data = {'chat_id': chat_id, 'caption': caption}
    response = rs.post(url, files=files, data=data)

    if response.status_code == 200:
        logging.info(f'Document {document_path} sent successfully.')
    else:
        logging.error(f'Failed to send document {document_path}. Status code: {response.status_code}, Response: {response.text}')


def send_message(chat_id, text, reply_markup=None):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {'chat_id': chat_id, 'text': text,
            'reply_markup': reply_markup.to_json() if reply_markup else None}
    response = rs.post(url, data=data)

    if response.status_code == 200:
        logging.info('Message sent successfully.')
    else:
        logging.error(f'Failed to send message. Status code: {response.status_code}, Response: {response.text}')


if __name__ == '__main__':
    bot_token = '6210383014:AAHGwo4q87zwKTjO1WgJWrbjEgx5V-TO8_A'
    chat_id = '@SSTPV2RAY'

    
    apkv2ray_filename, apkv2ray_link = get_latest_v2ray_apk()
    apk_filename, apk_link = get_latest_oblivion_apk()
    if apk_filename and apk_link:
        send_apk_to_telegram_channel(apk_filename, bot_token, chat_id)
        os.remove(apk_filename)
    if apkv2ray_filename and apkv2ray_link:
        send_apk_to_telegram_channel(apkv2ray_filename, bot_token, chat_id)
        os.remove(apk_filename)

    send_server_list(bot_token, chat_id)


