import requests as rs
import pandas as pd
from bs4 import BeautifulSoup
import re
import subprocess
import speedtest

etes = rs.get('http://103.201.129.226:14684/en/').text
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
    df[7].to_excel('rowsstp.xlsx')
    sorted_df = new_df.sort_values(by=['Ping Time'], ascending=True)
    sorted_df.reset_index(drop=True, inplace=True)
    sorted_df.to_excel('sstp.xlsx', sheet_name='Servers')
    sorted_df['sstp_link'] = '<a href="' + sorted_df['sstp'] + '">' + sorted_df['sstp'] + '</a>'
    sorted_df.to_html('sstp.html', escape=False, index=False)
    ser = pd.DataFrame(sorted_df[[ 'country','server','sstp_link' ]])
    ser['server'].to_csv('sstp.csv', index=False)
    print(sorted_df)

    

# create a DataFrame from the table
df = pd.read_csv('sstp.csv', sep='\t')

# select the top 5 servers. 
#You can adjust the number of rows to test by changing the df.head() function call to df.head(n) where n is the number of rows you want to test. 
top_10_servers = df.head(10)

# create a Speedtest object
st = speedtest.Speedtest(secure=True)

# create a list to store the speed test results
speed_test_results = []
ss = []

# loop through the top 10 servers and check the speed
for server in top_10_servers['server']:
    print(f"Checking speed for server: {server}")
    st.get_best_server()
    download_speed = st.download() / 1024 / 1024
    upload_speed = st.upload() / 1024 / 1024
    print(f"Download speed: {download_speed:.2f} Mbps")
    print(f"Upload speed: {upload_speed:.2f} Mbps")
    speed_test_results.append(f"Download speed: {download_speed:.2f} Mbps , Upload speed: {upload_speed:.2f} Mbps")
    ss.append(server)

# add the speed test results as a new column to the DataFrame
testspeed = pd.DataFrame({'speed_test_r':speed_test_results, 'server':ss})


# merge the top 10 servers back into the original DataFrame
result = pd.merge(ser, testspeed,on='server', how='left')
result = result.drop('server', axis=1)
result.to_html('sstp.html', escape=False, index=False)





