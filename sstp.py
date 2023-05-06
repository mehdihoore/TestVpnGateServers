import requests as rs
import pandas as pd
from bs4 import BeautifulSoup
import re
import subprocess

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
    print(sorted_df)


    def test_server(server, port):
        command = f"echo open {server} {port};sleep 1;echo vpn;sleep 1;echo vpn | sstp-client --log-level 0 --stdin".encode()
        powershell = subprocess.Popen(['powershell.exe', '-Command', '-'], stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = powershell.communicate(command)
        return error.decode()
    # apply the test_server function to each row of the DataFrame and store the results in new columns
    sorted_df['ping'] = ''
    sorted_df['test_result'] = ''
    for i, row in sorted_df.iterrows():
        server = row['server']
        port = row['port']
        ping = ''
        test_result = ''
        if port is not None:
            ping_command = f"Test-NetConnection -ComputerName {server} -Port {port} | Select-Object -ExpandProperty PingSucceeded"
            ping_result = subprocess.run(['powershell', '-Command', ping_command], capture_output=True, text=True)
            if ping_result.stdout.strip().lower() == 'true':
                ping = 'Success'
                test_result = test_server(server, port)
            else:
                ping = 'Failed'
        else:
            test_result = test_server(server, '443')
        sorted_df.at[i, 'ping'] = ping
        sorted_df.at[i, 'test_result'] = test_result

    # save the updated DataFrame to the sstp.xlsx file
    sorted_df.to_excel('sstp2.xlsx', sheet_name='results', index=False)
