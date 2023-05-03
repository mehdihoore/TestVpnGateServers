# TestVpnGateServers
This is a script to test SSTP VPN servers and find the fastest one. It does the following:

1-Sends a GET request to a webpage containing a table of SSTP VPN servers.
2-Extracts the table data and puts it into a Pandas DataFrame.
3-Cleans the DataFrame by removing unnecessary columns and performing string replacements.
4-Tests each server in the DataFrame by its port using PowerShell.
5-Connects to the fastest server using a socket connection. If no server can be connected to, it outputs a message saying so.
6-The script saves the original and cleaned data to Excel files and the test results to a sheet in the same file.







