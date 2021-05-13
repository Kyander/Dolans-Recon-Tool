This is a python3.8 tool that automates basic reconning.

# What it does :

1. does a full ports nmap scan.
2. runs a gobuster on every webservice found.
3. Extracts all HTML comments from each page found in gobuster.
4. checks FTP anonymous login and checks if anonymous can upload files.
5. option to bruteforce FTP with common users/pass list.
6. option to bruteforce SSH with common users/pass list.
7. option to bruteforce SMB with common users/pass list.
8. gets all SMB shares
9. attempts to download all smb shares to folders
10. outputs everything in a directory.

# To Install :

pip3 install -r requirements.txt


# Usage :

1. Make sure to run main.py in it's directory.
2. python3 main.py --host (IP) --output (full path of desired output folder, example : /home/user/here/) --wordlist (path to wordlist to use for gobuster)

