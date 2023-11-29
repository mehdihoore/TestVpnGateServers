import requests as rs
import pandas as pd
from bs4 import BeautifulSoup
from jdatetime import date as jdate

etes = rs.get('http://146.70.205.2:6283/en/').text
soup = BeautifulSoup(etes, "html.parser")
tbody = soup.find("table")
if tbody is not None:
    tbody_content = tbody.contents

    # Create a list to store the table data
    table_data = []

    # Loop through the <tr> tags in the <tbody> content and extract the table data
    for tr in tbody_content:
        if tr.name == "tr":
            row_data = []
            for td in tr.children:
                if td.name == "td":
                    row_data.append(td.text.strip())
            table_data.append(row_data)

    # Create a pandas DataFrame object from the table data
    df = pd.DataFrame(table_data)
    # create a new DataFrame with columns 0, 1, 3, and 7 of the original DataFrame
    new_df = df[[0, 1, 3, 7]].copy()
    # rename column 7 to sstp
    new_df = new_df.rename(columns={7: 'sstp'})
    new_df = new_df.rename(columns={0: 'country'})
    new_df = new_df.rename(columns={1: 'DDNS hostnameIP Address(ISP hostname)'})
    new_df = new_df.rename(columns={3: 'Ping Time'})
    # perform the string replacements on column 'sstp'
    new_df['sstp'] = new_df['sstp'].str.replace('MS-SSTPConnect guideSSTP Hostname :', '')
    new_df['sstp'] = new_df['sstp'].str.replace('MS-SSTPWindows Vista,7, 8, RTNo client required', '')
    # remove any rows with empty values in column 'sstp'
    new_df = new_df[new_df['sstp'].notna() & (new_df['sstp'] != '')]
    # extract the value 'Ping: XX ms' from column 2
    new_df['Ping Time'] = new_df['Ping Time'].str.extract(r'Ping:\s*(\d+)\s*ms')
    new_df = new_df.fillna(666)
    new_df['Ping Time'] = new_df['Ping Time'].astype(int)
    df[7] = df[7].str.replace('MS-SSTPConnect guideSSTP Hostname :', '')
    df[7] = df[7].str.replace('MS-SSTPWindows Vista,7, 8, RTNo client required', '')
    df = df[df[7].notna() & (df[7] != '')]
    # separate the server name and port number in column 'sstp'
    new_df[['server', 'port']] = new_df['sstp'].str.split(':', expand=True)
    # export the resulting DataFrame to an Excel file
    df[7].to_csv('rowsstp.csv', index=False)
    sorted_df = new_df.sort_values(by=['Ping Time'], ascending=True)
    sorted_df.reset_index(drop=True, inplace=True)
    sorted_df.to_csv('sstps.csv')
    sorted_df['sstp_link'] = '<a href="' + sorted_df['sstp'] + '">' + sorted_df['sstp'] + '</a>'
    sorted_df.to_html('sstp.html', escape=False, index=False)
    ser = pd.DataFrame(sorted_df[[ 'country','Ping Time','sstp_link' ]])
    
    print(sorted_df)
    ser.to_html('sstp.html', escape=False, index=False)
