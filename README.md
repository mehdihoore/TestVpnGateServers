Server Speed Test
This Python script performs a speed test on various servers and exports the results to Excel files. The script uses the Requests library to get the HTML content of a website that contains a table of servers and their associated information. Then, it uses BeautifulSoup to parse the HTML and extract the data from the table.

Once the data is extracted, the script creates a pandas DataFrame object from the table data and manipulates it to extract the relevant information. It then applies a ping test to each server in the DataFrame using the Test-NetConnection PowerShell cmdlet and the sstp-client tool.

Finally, the script exports the resulting DataFrame to two Excel files: one containing the original data and one containing the ping test results.

Requirements
To run this script, you will need:

Python 3.6 or higher
The Requests library
The pandas library
The BeautifulSoup library
The Test-NetConnection PowerShell cmdlet (included in Windows)
The sstp-client tool (available for download from https://sstp-client.sourceforge.net/)
Usage
To use this script:

Clone the repository to your local machine.
Install the required libraries.
Ensure that Test-NetConnection and sstp-client are installed and in your PATH.
Open a terminal or command prompt in the repository directory.
Run the script using python server_speed_test.py.
The script will output the results to the console and save them to Excel files in the same directory.







