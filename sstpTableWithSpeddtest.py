import requests as rs
import pandas as pd
from bs4 import BeautifulSoup
from jdatetime import date as jdate

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
    df[7].to_csv('rowsstp.csv', index=False)
    sorted_df = new_df.sort_values(by=['Ping Time'], ascending=True)
    sorted_df.reset_index(drop=True, inplace=True)
    sorted_df.to_csv('sstps.csv')
    sorted_df['sstp_link'] = '<a href="' + sorted_df['sstp'] + '">' + sorted_df['sstp'] + '</a>'
    sorted_df.to_html('sstp.html', escape=False, index=False)
    ser = pd.DataFrame(sorted_df[[ 'country','Ping Time','sstp_link' ]])
    
    print(sorted_df)
    ser.to_html('sstp.html', escape=False, index=False)
    shamsi_date = jdate.today().strftime('%Y-%m-%d')

    # Style the DataFrame for HTML representation without index
    styled_df = ser.style\
        .set_table_attributes('class="dataframe"')\
        .set_table_styles([
            {'selector': 'thead', 'props': [('background-color', 'lightgrey')]}
        ])\
        .set_caption(f"SSTP SERVER LIST @ {shamsi_date}")\
        .set_properties(**{'text-align': 'center'})\
        .hide_index()

    # Add filter for every column
    for col in sorted_df.columns:
        if col != 'sstp_link':
            styled_df = styled_df.set_table_styles([{
                'selector': f'th.col_heading_{col}',
                'props': 'font-size: 14px'
            }])

    # Add dropdown filter for the 'country' column
    country_filter = sorted_df['country'].unique().tolist()
    country_filter.insert(0, 'Select All')
    country_dropdown_html = '<select id="filterCountry" onchange="filterTable()">{}</select>'.format(
        ''.join([f'<option value="{country}">{country}</option>' for country in country_filter])
    )

    # HTML template with JavaScript for filtering
    html_template = f'''
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
          /* Add some basic CSS styles to make the table responsive */
          table {{
            width: 100%;
            border-collapse: collapse;
          }}
        
          th,
          td {{
            border: 1px solid #dddddd;
            /* Light gray border between cells */
            padding: 8px;
            text-align: left;
            /* Align table cell text to the left */
            min-width: 1px;
            /* Set minimum width to 1px */
            max-width: 100%;
            /* Set maximum width to 100% */
            overflow: hidden;
            /* Hide any overflowing content */
            white-space: nowrap;
            /* Prevent text from wrapping */
          }}
        
          /* Apply styles for the table header */
          thead th {{
            background-color: #f2f2f2;
            /* Light gray background color */
            color: #333333;
            /* Dark gray text color */
            font-weight: bold;
            /* Bold font weight for header text */
            text-align: center;
            /* Center header text */
          }}
        
          /* Apply custom font to the table */
          table {{
            font-family: Tahoma, sans-serif;
          }}
        
          /* Make the table responsive */
          @media screen and (max-width: 200px) {{
        
            /* For smaller screens, reduce font size and wrap table cells */
            th,
            td {{
              font-size: 14px;
              white-space: wrap;
            }}
          }}
        </style>
        <div class="header" style="background-color: #f2f2f2;">
          <h1>SSTP SERVER LIST @ {shamsi_date}</h1>
        </div>
    </head>
    <body>
        {country_dropdown_html}
        
        <input type="text" id="filterPingTime" oninput="filterTable()" placeholder="Filter by Ping Time">
        
        <input type="text" id="filterSstpLink" oninput="filterTable()" placeholder="Filter by SSTP Link">
        {styled_df.hide().render()}
        
        <script>
          // Function to populate the country filter dropdown menu
          function populateCountryFilter() {{
            const filterCountry = document.getElementById('filterCountry');
            const countries = new Set(); // Use a Set to collect unique country names

            // Iterate through the table rows and collect unique country names
            const rows = document.querySelectorAll('tbody tr');
            rows.forEach(row => {{
              const countryCell = row.querySelector('td:nth-child(1)');
              if (countryCell) {{
                countries.add(countryCell.textContent.trim());
              }}
            }});

            // Clear previous options and add new options for each country
            filterCountry.innerHTML = '<option value="">All Countries</option>';
            countries.forEach(country => {{
              const option = document.createElement('option');
              option.value = country;
              option.textContent = country;
              filterCountry.appendChild(option);
            }});
          }}

          // Call the populateCountryFilter function initially to populate the dropdown menu
          populateCountryFilter();

          // Add event listeners to the input fields for filtering
          function filterTable() {{
            const inputCountry = document.getElementById('filterCountry').value.toLowerCase();
            const inputPingTime = document.getElementById('filterPingTime').value.toLowerCase();
            const inputSstpLink = document.getElementById('filterSstpLink').value.toLowerCase();

            const rows = document.getElementsByTagName('tr');

            for (let i = 1; i < rows.length; i++) {{
              const row = rows[i];
              const country = row.children[0].innerText.toLowerCase();
              const pingTime = row.children[1].innerText.toLowerCase();
              const sstpLink = row.children[2].innerText.toLowerCase();

              if (
                country.includes(inputCountry) &&
                pingTime.includes(inputPingTime) &&
                sstpLink.includes(inputSstpLink)
              ) {{
                row.style.display = 'table-row';
              }} else {{
                row.style.display = 'none';
              }}
            }}
          }}
        </script>
    </body>
    </html>
    '''

    # Save the HTML with styles and filters to a file
    with open('sstp.html', 'w', encoding='utf-8') as file:
        file.write(html_template)
