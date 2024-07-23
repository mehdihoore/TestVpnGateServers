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
from requests.exceptions import RequestException, SSLError

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def get_file_size(file_path):
    return os.path.getsize(file_path) / (1024 * 1024)  # Size in MB


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
    nowt = datetime.datetime(now.year, now.month, now.day,hour, minute, now.second, now.microsecond)
    persian_date_time = nowp.strftime("%A, %d %B %Y ") + nowt.strftime("%H:%M:%S")
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

    apk_filename = os.path.basename(a_tag['href'])

    # Check if file already exists
    if os.path.exists(apk_filename):
        logging.info(f'APK file already exists: {apk_filename}')
        return apk_filename, apk_link

    response = rs.get(apk_link)
    if response.status_code != 200:
        logging.error(f'Failed to download the APK file. Status code: {response.status_code}')
        return None, None

    with open(apk_filename, 'wb') as f:
        f.write(response.content)

    logging.info(f'APK file downloaded: {apk_filename}')
    return apk_filename, apk_link


apk_filename, apk_link = get_latest_oblivion_apk()


def send_apk_to_telegram_channel(apk_filename, bot_token, chat_id):
    persian_date = get_persian_date_time()
    url = f'https://api.telegram.org/bot{bot_token}/sendDocument'

    if get_file_size(apk_filename) > 50:  # Adjust 50 MB limit as necessary
        logging.info(
            f'File size {apk_filename} is too large. Sending link instead.')
        send_message(chat_id, f"\n {apk_link}\n{persian_date}\n برنامه oblivion جایگزین وارپ")
        return

    files = {'document': open(apk_filename, 'rb')}
    data = {'chat_id': chat_id,
            'caption': f"\n {apk_link}\n{persian_date}\n برنامه oblivion جایگزین وارپ"}

    response = rs.post(url, files=files, data=data)
    if response.status_code == 200:
        logging.info('APK file sent successfully.')
    else:
        logging.error(f'Failed to send APK file. Status code: {response.status_code}, Response: {response.text}')
        send_message(chat_id, f"\n {apk_link}\n{persian_date}\n برنامه oblivion جایگزین وارپ")
    files['document'].close()


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
    release_url = f'https://github.com{release_tag}'.replace('/tag/', '/expanded_assets/')

    response = rs.get(release_url)
    if response.status_code != 200:
        logging.error(f'Failed to fetch the release page. Status code: {response.status_code}')
        return None, None

    soup = BeautifulSoup(response.text, 'html.parser')

    apkv2ray_link = None
    priorities = ['universal']

    for priority in priorities:
        for a_tag in soup.find_all('a', href=True):
            if a_tag['href'].endswith('.apk') and priority in a_tag['href'].lower():
                apkv2ray_link = 'https://github.com' + a_tag['href']
                break
        if apkv2ray_link:
            break

    if not apkv2ray_link:
        # If no prioritized APK found, fall back to any APK
        for a_tag in soup.find_all('a', href=True):
            if a_tag['href'].endswith('.apk'):
                apkv2ray_link = 'https://github.com' + a_tag['href']
                break

    if not apkv2ray_link:
        logging.error('No APK file found in the latest release.')
        return None, None

    logging.info(f'APK URL: {apkv2ray_link}')

    apkv2ray_filename = os.path.basename(apkv2ray_link)

    # Check if file already exists
    if os.path.exists(apkv2ray_filename):
        logging.info(f'APK file already exists: {apkv2ray_filename}')
        return apkv2ray_filename, apkv2ray_link

    response = rs.get(apkv2ray_link)
    if response.status_code != 200:
        logging.error(f'Failed to download the APK file. Status code: {response.status_code}')
        return None, None

    with open(apkv2ray_filename, 'wb') as f:
        f.write(response.content)

    logging.info(f'APK file downloaded: {apkv2ray_filename}')
    return apkv2ray_filename, apkv2ray_link


session = rs.Session()
apkv2ray_filename, apkv2ray_link = get_latest_v2ray_apk()


def send_apkv2ray_to_telegram_channel(apkv2ray_filename, bot_token, chat_id, max_retries=3):
    persian_date = get_persian_date_time()
    url = f'https://api.telegram.org/bot{bot_token}/sendDocument'

    if get_file_size(apkv2ray_filename) > 50:  # Adjust 50 MB limit as necessary
        logging.info(f'File size {apkv2ray_filename} is too large. Sending link instead.')
        send_message(chat_id, f"\n {apkv2ray_link}\n{persian_date}\n برنامه‌ای سریع و ساده برای اجرای سرورهای v2ray\nاین برنامه را نصب کنید و سپس یکی از فایلهای .txt را باز کرده و محتوای آن را در برنامه کپی کنید یا اگر زیاد بود share کنید. ")

        return

    files = {'document': open(apkv2ray_filename, 'rb')}
    data = {'chat_id': chat_id,
            'caption': f"\n {apkv2ray_link}\n{persian_date}\n برنامه‌ای سریع و ساده برای اجرای سرورهای v2ray\nاین برنامه را نصب کنید و سپس یکی از فایلهای .txt را باز کرده و محتوای آن را در برنامه کپی کنید یا اگر زیاد بود share کنید. "}

    for attempt in range(max_retries):
        try:
            response = rs.post(url, files=files, data=data)
            response.raise_for_status()
            logging.info('APK file sent successfully.')
            return
        except (RequestException, SSLError) as e:
            logging.error(f'Attempt {attempt + 1} failed: {str(e)}')
            if attempt < max_retries - 1:
                sleep(5)  # Wait for 5 seconds before retrying
            else:
                send_message(chat_id, f"\n {apkv2ray_link}\n{persian_date}\n برنامه‌ای سریع و ساده برای اجرای سرورهای v2ray\nاین برنامه را نصب کنید و سپس یکی از فایلهای .txt را باز کرده و محتوای آن را در برنامه کپی کنید یا اگر زیاد بود share کنید. ")
        finally:
            files['document'].close()


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

    # Send SSTP Servers document
    send_document(chat_id, r"sstp.csv",f'SSTP Servers https://evhr.sabaat.ir/ ✅- {persian_date}')

    # Download and send MTProto proxies
    proxi = rs.get(
        'https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/proxies')
    soup = BeautifulSoup(proxi.content, "html.parser")
    mtprototext = soup.get_text()
    with open("mtproto.txt", "w") as f:
        f.write(mtprototext)
    send_document(chat_id, 'mtproto.txt',f'پروکسی تلگرام \n https://mtproto.sabaat.ir/\n - {persian_date}')

    # Define links and their names
    links = [
        ('https://vl.sabaat.ir/sub'),
        ('https://fin.hore.workers.dev/sub/fin.sabaat.ir.txt'),
        ('https://raw.githubusercontent.com/mahdibland/SSAggregator/master/sub/sub_merge_base64.txt'),
        ('https://raw.githubusercontent.com/mahdibland/SSAggregator/master/sub/sub_merge.txt'),
        ('https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/splitted/ssr.txt'),
        ('https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/splitted/ss.txt'),
        ('https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/splitted/trojan.txt'),
        ('https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/splitted/vmess.txt')
    ]
    names = ['Worker .ir', 'Worker .link', 'mahdibland Base64', 'mahdibland MIX',
             'mahdibland ssr', 'mahdibland Shadowsucks', 'mahdibland trojan', 'mahdibland vmess']

    # Assuming links and names are lists of equal length
    for link, name in zip(links, names):
        # Check if the link ends with '.txt'
        if link.endswith('.txt'):
            file_name = link.split("/")[-1]  # Extract file name from URL
            try:
                response = rs.get(link)
                response.raise_for_status()  # Raise exception for HTTP errors

                content = response.text

                # Save content to a .txt file
                with open(file_name, 'w', encoding='utf-8') as f:  # Specify encoding
                    f.write(content)

                # Send the .txt file
                send_document(chat_id, file_name, f'برای استفاده در برنامه‌های v2ray \n{persian_date} \n{name}\n {link}')

            except rs.exceptions.RequestException as e:
                logging.error(f"Error retrieving {link}: {e}")
            except UnicodeEncodeError as e:
                logging.error(f"Error writing {link} content: {e}")
            finally:
                if os.path.exists(file_name):  # Clean up the file
                    os.remove(file_name)

        else:
            # For links that do not end with '.txt', append '.txt' and handle them similarly
            txt_link = f"{link}.txt"
            # Extract file name from URL
            file_name = f"{txt_link.split('/')[-1]}"
            try:
                response = rs.get(txt_link)
                response.raise_for_status()  # Raise exception for HTTP errors

                content = response.text

                # Save content to a .txt file
                with open(file_name, 'w', encoding='utf-8') as f:  # Specify encoding
                    f.write(content)

                # Send the .txt file
                send_document(chat_id, file_name, f'برای استفاده در برنامه‌های v2ray \n{persian_date} \n{name} (treated as .txt)\n {txt_link}')

            except rs.exceptions.RequestException as e:
                logging.error(f"Error retrieving {txt_link}: {e}")
            except UnicodeEncodeError as e:
                logging.error(f"Error writing {txt_link} content: {e}")
            finally:
                if os.path.exists(file_name):  # Clean up the file
                    os.remove(file_name)

    # Send warp links
    inb = []
    try:
        for name, link in warplink.items():
            inb.append([InlineKeyboardButton(name, url=link)])
        r_markup = InlineKeyboardMarkup(inb)
        send_message(chat_id, f'وارپ پر سرعت بدون عوض کردن ای پی', r_markup)
    except Exception as e:
        logging.error(f"Error sending warp links: {e}")

    # Send V2Ray links
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
    try:
        bot_token = '6210383014:AAHGwo4q87zwKTjO1WgJWrbjEgx5V-TO8_A'
        chat_id = '@SSTPV2RAY'
        apkv2ray_filename, apkv2ray_link = get_latest_v2ray_apk()
        apk_filename, apk_link = get_latest_oblivion_apk()

        if apk_filename and apk_link:
            send_apk_to_telegram_channel(apk_filename, bot_token, chat_id)
            os.remove(apk_filename)

        if apkv2ray_filename and apkv2ray_link:
            send_apkv2ray_to_telegram_channel(
                apkv2ray_filename, bot_token, chat_id)
            os.remove(apkv2ray_filename)

        send_server_list(bot_token, chat_id)
    except Exception as e:
        logging.exception("An unexpected error occurred:")
