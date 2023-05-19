import requests as rs
import pandas as pd
from bs4 import BeautifulSoup
import sqlite3
import speedtest
from tqdm import tqdm
import ping3

#etes = rs.get('http://103.201.129.226:14684/en/').text
# get user input for URL

url = input("Please enter a valid URL: ")

while True:
    try:
        response = rs.get(url)
        if response.status_code == 200:
            break
        else:
            print("The URL is not responding with a 200 status code. Please enter a different URL.")
            url = input("Please enter a valid URL: ")

    except:
        print("The URL is invalid. Please enter a different URL.")
        url = input("Please enter a valid URL: ")
def measure_ping_time(host):
    ping3.EXCEPTIONS = True
    try:
        rtt = ping3.ping(host)
        if rtt is not None:
            return round(rtt * 1000, 2)  # Convert to milliseconds and round to 2 decimal places
        else:
            return 'Timeout'  # Indicate timeout if ping is unsuccessful
    except ping3.errors.PingError:
        return 20000  # Indicate error if an exception occurs


etes = rs.get(url).text
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
    #sorted_df.to_excel('sstp.xlsx', sheet_name='Servers')
    sorted_df['sstp_link'] = '<a href="' + sorted_df['sstp'] + '">' + sorted_df['sstp'] + '</a>'
    #sorted_df.to_html('sstp.html', escape=False, index=False)
    pingi = []
    with tqdm(total=len(sorted_df['server'])) as pbar:
        for i in range(len(sorted_df['server'])):
            try:
                pingi.append(measure_ping_time(sorted_df['server'][i]))
                print(measure_ping_time(sorted_df['server'][i]))
                # update the progress bar
                pbar.update(1)
            except Exception as e:
                print(f"Error occurred for server {i}: {str(e)}")
                continue
    sorted_df['Ping in'] = pingi
    sorted_df = sorted_df.sort_values(by=['Ping in'], ascending=True)
    ser = pd.DataFrame(sorted_df[['country', 'Ping Time', 'Ping in', 'server', 'sstp_link']])
    ser['server'].to_csv('sstp.csv', index=False)
    ser.to_csv('data.csv', index=False)
    # sorted_df.to_excel('\\\srv1\\General\\hoore\\sstp.xlsx', sheet_name='Servers')
    # sorted_df.to_html('\\\srv1\General\\hoore\\sstp.html', escape=False, index=False)
    print(sorted_df)

# create a DataFrame from the table
df = pd.read_csv('sstp.csv', sep='\t')
while True:      # keep looping until we break out of the loop
    try:
        spidtestnumserver= int(input(f"how many of {len(ser['server'])} servers do you want to check speedTest? "))
        break    # exit the loop if the previous line succeeded
    except ValueError:
        print("Please enter an integer!")

# select the top 10 servers
top_10_servers = df.head(spidtestnumserver)

# create a Speedtest object
st = speedtest.Speedtest(secure=True)

# create a list to store the speed test results
speed_test_results = []
ss = []

# loop through the top 10 servers and check the speed


# create a tqdm instance with the total number of servers to loop through
with tqdm(total=len(top_10_servers)) as pbar:
    for server in top_10_servers['server']:
        try:
            # update the progress bar for each server
            pbar.set_description(f"Checking speed for server: {server}\n")
            st.get_best_server()
            download_speed = st.download() / 1024 / 1024
            upload_speed = st.upload() / 1024 / 1024
            print(f"\nDownload speed: {download_speed:.2f} Mbps")
            print(f"Upload speed: {upload_speed:.2f} Mbps")
            speed_test_results.append(
                f"Download speed: {download_speed:.2f} Mbps , Upload speed: {upload_speed:.2f} Mbps")
            ss.append(server)
            # update the progress bar
            pbar.update(1)
        except Exception as e:
            print(f"Error occurred for server {server}: {str(e)}")
            continue

# add the speed test results as a new column to the DataFrame
testspeed = pd.DataFrame({'speed_test_r': speed_test_results, 'server': ss})

# merge the top 10 servers back into the original DataFrame
result = pd.merge(ser, testspeed, on='server', how='left')
result['server'].to_csv('server.csv', index=False)
result = result.drop('server', axis=1)

# Generate a single button that triggers ping for all servers
ping_button = '<button onclick="pingAllServers()">Ping All</button>'
result.to_excel('sstp.xlsx', index=False)
result.to_html('sstp.html', escape=False, index=False)

# Replace the placeholder string with the ping button

sorted_df['sstp'].to_csv('sstp_a.csv', index=False)
sorted_df['country'].to_csv('country.csv', index=False)
df1 = pd.read_csv('sstp_a.csv', sep='\t')
df2 = pd.read_csv('server.csv', sep='\t')
df3 = pd.read_csv('country.csv', sep='\t')
servers = df2['server'].tolist()
countries = df3['country'].tolist()
sstp_links = df1['sstp'].tolist()

conn = sqlite3.connect('servers.db')
c = conn.cursor()
# create a list of tuples containing the data for the three columns
#data = [(servers[i], countrys[i], sstp_link[i]) for i in range(len(servers))]

# create the table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS SSTP (
             server_name TEXT,
             country_name TEXT,
             sstp_link TEXT
             )''')
# loop through the data and insert if the sstp_link does not exist
for i in range(len(servers)):
    sstp_link = sstp_links[i]
    server_name = servers[i]
    country_name = countries[i]
    sstp_link_str = ','.join(sstp_link)
    # check if sstp_link already exists
    c.execute("SELECT sstp_link FROM SSTP WHERE sstp_link=?", (sstp_link_str,))
    existing_link = c.fetchone()

    # insert the data if sstp_link does not exist
    if existing_link is None:
        c.execute("INSERT INTO SSTP (server_name, country_name, sstp_link) VALUES (?, ?, ?)",
                  (server_name, country_name, sstp_link))
        print(f"Inserted {server_name} - {country_name} - {sstp_link} into SSTP table.")
    else:
        print(f"{sstp_link} already exists in SSTP table.")

# commit changes and close the connection
conn.commit()
conn.close()
