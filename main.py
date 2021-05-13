import nmap3
import pydirbuster
import argparse
import os
import sys
import threading
from ftplib import FTP
from bs4 import BeautifulSoup, Comment
import requests
import smbclient

'''
Grabs HTML comments from dirbusted findings.

'''
global commentsExists
commentsExists = False


def commentGrabber(logfile, host, dir):
    global commentsExists
    print("COMMENT GRABBER")
    try:
        os.mkdir("{}/html".format(dir))  # Creates the "HTML" directory
    except:
        pass
    fileComments = os.path.join("{}/html/".format(dir), "comments.txt")  # the comments.txt path

    with open(logfile) as a:  # Puts every gobusted findings from the file inside a list
        content = a.readlines()

    content = [x.strip() for x in content]
    urls = []

    for file in content:  # Creates the urls (appends gobusted findings to url) for requests
        fileFormat = file.split(' ')[0]
        urls.append("{}{}".format(host, fileFormat))

    if commentsExists == False:
        f = open(fileComments, "w+")  # Creates the comments.txt file
        f.write("ALL THE COMMENTS EXTRACTED :\n\n")
        f.close()
        commentsExists = True
    else:
        pass
    for url in urls:  # Grabs all comments and writes it to comments.txt
        r = requests.get(url, verify=False)
        content = r.text
        soup = BeautifulSoup(content, 'html.parser')
        f = open(fileComments, "a")
        f.write("{} :\n\n".format(url))
        f.close()
        for x in soup.findAll(text=lambda text: isinstance(text, Comment)):
            f = open(fileComments, "a")
            f.write(x)
            f.close()


def bust(url, wordlist, logfile, dir):  # THIS IS THE THREADED FUNCTION
    # print(Debug)
    command = "python3 ./busterScript.py --url {} --wordlist {} --output {}".format(url, wordlist, logfile)
    if Debug == True:
        print("DEBUG INFO ------- DIRBUST -------\n")
        print("URL : {}\nWORDLIST : {}\nLOGFILE : {}\nCOMMAND : {}".format(url, wordlist, logfile, command))
    else:
        pass

    os.system("xterm -geometry 90x30+1920+0 -e {}".format(command))
    try:
        commentGrabber(logfile, url, dir)
    except:
        print("[!!!] Could not grab comments from {} !".format(url))


def dirbuster(urls, wordlist, logfiles, dir):  # This starts the threads, passing it all it needs.
    i = 0
    for url in urls:
        threader = threading.Thread(target=bust, args=(url, wordlist, logfiles[i], dir))
        threader.start()
        i += 1

def bruteSSH(rootDir, host):
    try:
        os.mkdir("{}/brute".format(rootDir))  # Creates the "brute" directory
    except:
        pass

    command = "hydra -s 22 -L ./wordlist/top-usernames-shortlist.txt -P ./wordlist/UserPassCombo-Jay.txt -vV ssh://{} -o {}/brute/SSH.txt".format(
        host, rootDir)
    os.system("xterm -geometry 90x30+1920+1080 -e {}".format(command))


def smbCheck(host,rootDir):
    command = "python3 smbCheck.py --host {} --output {}".format(host,rootDir)
    print(command)
    os.system("xterm -geometry 90x30+0+540 -hold -e {}".format(command))

def bruteFTP(rootDir, host):
    try:
        os.mkdir("{}/brute".format(rootDir))  # Creates the "brute" directory
    except:
        pass
    command = "hydra -s 21 -t 20 -L ./wordlist/top-usernames-shortlist.txt -P ./wordlist/UserPassCombo-Jay.txt -vV ftp://{} -o {}/brute/FTP.txt".format(host,rootDir)
    os.system("xterm -geometry 90x30+1920+1080 -e {}".format(command))

class nmapScan:
    '''
    __INIT__ :
    Initiate the nmap3 object and host variable.
    Do an -sV scan and save it to self.result.
    Format the result into a list self.openPorts.

    '''

    def __init__(self, host, rootDir, *args, **kwargs):
        global Debug  # Boolean to skip nmap scan
        Debug = kwargs.get('Debug')
        try:
            os.mkdir(os.path.join(rootDir, "nmap"))
        except:
            pass
        self.rootDir = rootDir  # This is where all the files of the scan will be outputed
        self.webServices = ["Microsoft IIS httpd", "Apache httpd", "nginx", "Apache Tomcat", "MiniServ",
                            "lighttpd","Microsoft HTTPAPI httpd"]  # Let's only do common webservices.
        self.host = host
        self.nmap = nmap3.Nmap()
        if Debug == True:
            self.result = {'192.168.241.116': {'osmatch': {}, 'ports': [{'protocol': 'tcp', 'portid': '22', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '63', 'service': {'name': 'ssh', 'product': 'OpenSSH', 'version': '7.4', 'extrainfo': 'protocol 2.0', 'method': 'probed', 'conf': '10'}, 'cpe': [{'cpe': 'cpe:/a:openbsd:openssh:7.4'}], 'scripts': []}, {'protocol': 'tcp', 'portid': '80', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '63', 'service': {'name': 'http', 'product': 'Apache httpd', 'version': '2.4.6', 'extrainfo': '(CentOS)', 'method': 'probed', 'conf': '10'}, 'cpe': [{'cpe': 'cpe:/a:apache:http_server:2.4.6'}], 'scripts': []}, {'protocol': 'tcp', 'portid': '139', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '63', 'service': {'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: SAMBA', 'hostname': 'CASSIOS', 'method': 'probed', 'conf': '10'}, 'cpe': [{'cpe': 'cpe:/a:samba:samba'}], 'scripts': []}, {'protocol': 'tcp', 'portid': '445', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '63', 'service': {'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: SAMBA', 'hostname': 'CASSIOS', 'method': 'probed', 'conf': '10'}, 'cpe': [{'cpe': 'cpe:/a:samba:samba'}], 'scripts': []}, {'protocol': 'tcp', 'portid': '8080', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '63', 'service': {'name': 'http-proxy', 'servicefp': 'SF-Port8080-TCP:V=7.91%I=7%D=5/12%Time=609C7365%P=x86_64-pc-linux-gnu%r(GetRequest,429,"HTTP/1\\.1\\x20200\\x20\\r\\nX-Content-Type-Options:\\x20nosniff\\r\\nX-XSS-Protection:\\x201;\\x20mode=block\\r\\nCache-Control:\\x20no-cache,\\x20no-store,\\x20max-age=0,\\x20must-revalidate\\r\\nPragma:\\x20no-cache\\r\\nExpires:\\x200\\r\\nX-Frame-Options:\\x20DENY\\r\\nContent-Type:\\x20text/html;charset=UTF-8\\r\\nContent-Language:\\x20en-US\\r\\nDate:\\x20Thu,\\x2013\\x20May\\x202021\\x2000:28:33\\x20GMT\\r\\nConnection:\\x20close\\r\\n\\r\\n<!doctype\\x20html>\\n<html\\x20lang=\\"en\\">\\n\\n<head>\\n\\x20\\x20<meta\\x20charset=\\"utf-8\\">\\n\\x20\\x20<meta\\x20http-equiv=\\"x-ua-compatible\\"\\x20content=\\"ie=edge\\">\\n\\x20\\x20<meta\\x20name=\\"viewport\\"\\x20content=\\"width=device-width,\\x20initial-scale=1\\">\\n\\n\\x20\\x20<title></title>\\n\\n\\x20\\x20<link\\x20rel=\\"stylesheet\\"\\x20href=\\"/css/main\\.css\\">\\n\\x20\\x20\\n</head>\\n\\n<body>\\n\\t\\n\\t<div\\x20class=\\"small-container\\">\\n\\t\\t<div\\x20class=\\"flex-row\\">\\n\\t\\t\\t<h1>Recycler\\x20Management\\x20System</h1>\\n\\t\\t</div>\\n\\t\\t<div\\x20class=\\"flex-row\\">\\n\\t\\t\\t<img\\x20src=\\"/images/factory\\.jpg\\"\\x20class=\\"round-button\\">\\n\\t\\t</div>\\x20\\n\\n\\t</div>\\n\\t<br>\\n\\t<div\\x20class=\\"small-container\\">\\n\\n\\t\\t\\t<div\\x20class=\\"flex-small\\">Control\\x20system\\x20for\\x20the\\x20factory\\x20")%r(HTTPOptions,12B,"HTTP/1\\.1\\x20200\\x20\\r\\nAllow:\\x20GET,HEAD,OPTIONS\\r\\nX-Content-Type-Options:\\x20nosniff\\r\\nX-XSS-Protection:\\x201;\\x20mode=block\\r\\nCache-Control:\\x20no-cache,\\x20no-store,\\x20max-age=0,\\x20must-revalidate\\r\\nPragma:\\x20no-cache\\r\\nExpires:\\x200\\r\\nX-Frame-Options:\\x20DENY\\r\\nContent-Length:\\x200\\r\\nDate:\\x20Thu,\\x2013\\x20May\\x202021\\x2000:28:33\\x20GMT\\r\\nConnection:\\x20close\\r\\n\\r\\n")%r(RTSPRequest,24E,"HTTP/1\\.1\\x20400\\x20\\r\\nContent-Type:\\x20text/html;charset=utf-8\\r\\nContent-Language:\\x20en\\r\\nContent-Length:\\x20435\\r\\nDate:\\x20Thu,\\x2013\\x20May\\x202021\\x2000:28:33\\x20GMT\\r\\nConnection:\\x20close\\r\\n\\r\\n<!doctype\\x20html><html\\x20lang=\\"en\\"><head><title>HTTP\\x20Status\\x20400\\x20\\xe2\\x80\\x93\\x20Bad\\x20Request</title><style\\x20type=\\"text/css\\">body\\x20{font-family:Tahoma,Arial,sans-serif;}\\x20h1,\\x20h2,\\x20h3,\\x20b\\x20{color:white;background-color:#525D76;}\\x20h1\\x20{font-size:22px;}\\x20h2\\x20{font-size:16px;}\\x20h3\\x20{font-size:14px;}\\x20p\\x20{font-size:12px;}\\x20a\\x20{color:black;}\\x20\\.line\\x20{height:1px;background-color:#525D76;border:none;}</style></head><body><h1>HTTP\\x20Status\\x20400\\x20\\xe2\\x80\\x93\\x20Bad\\x20Request</h1></body></html>");', 'method': 'probed', 'conf': '10'}, 'scripts': []}], 'hostname': [], 'macaddress': None, 'state': {'state': 'up', 'reason': 'echo-reply', 'reason_ttl': '63'}}, 'stats': {'scanner': 'nmap', 'args': '/usr/bin/nmap -oX - -sV -p- -oN /home/Kyand/OSPG/Cassios/reconScript/nmap/nmap_scan.txt 192.168.241.116', 'start': '1620865849', 'startstr': 'Wed May 12 20:30:49 2021', 'version': '7.91', 'xmloutputversion': '1.05'}, 'runtime': {'time': '1620865901', 'timestr': 'Wed May 12 20:31:41 2021', 'summary': 'Nmap done at Wed May 12 20:31:41 2021; 1 IP address (1 host up) scanned in 51.31 seconds', 'elapsed': '51.31', 'exit': 'success'}}
        else:
            print("[!] nmap scan is running...")
            self.result = self.nmap.nmap_version_detection(self.host, args="-p- -oN {}/nmap/nmap_scan.txt".format(
                rootDir))  # -sV -p- -oN (rootDir/nmap_scant.txt) scan
            print("[!] nmap scan has completed!")
            print(self.result)
        self.openPorts = []
        # print(self.result)
        for ports in self.result[self.host]["ports"]:
            # print(ports)
            self.openPorts.append(ports)


    def tsmbCheck(self):
        print("[!] Starting SMB thread!")
        x1 = threading.Thread(target=smbCheck, args=(self.host,self.rootDir,))
        x1.start()

    '''
    Runs funct
    '''

    def check(self, dWordList):
        global SSL
        for port in self.result[self.host]['ports']:
            number = port['portid']
            if number == "443":
                SSL = True
            else:
                SSL = False

        self.dirbust(dWordList)  # Does dirbust AND extracts comments
        for port in self.result[self.host]['ports']:
            number = port['portid']
            if number == "21":
                self.checkFTP()
            elif number == "22":
                answ = input("[!] Do you wish to bruteforce SSH? (y/n) ")
                if answ == "y":
                    self.tBruteSSH()
                else:
                    pass
                pass
            elif number == "445":
                self.tsmbCheck()
                pass
            else:
                pass

    '''
    portScan:
    Simply returns the list of openPorts

    Example use :

    host = "10.10.10.204"
    result = nmapScan(host).listOpenPorts()
    for r in result:
        print(r)    
    '''

    def listOpenPorts(self):
        return self.openPorts


    def tBruteSSH(self):
        x= threading.Thread(target=bruteSSH, args=(self.rootDir,self.host,))
        x.start()

    def tBruteFTP(self):
        x = threading.Thread(target=bruteFTP, args=(self.rootDir,self.host,))
        x.start()
    '''
    Do regular FTP checks (check anon login, check perms)

    '''

    def checkFTP(self):
        rootDir = os.path.join(self.rootDir, "ftp")  # /ftp directory
        try:
            os.mkdir(os.path.join(self.rootDir, "ftp"))  # Create /ftp directory
        except:
            pass
        f = open("{}/results.txt".format(rootDir), "w+")  # Create results.txt file
        ftp = FTP(self.host)  # initate ftp object
        try:  # Check anonymous login
            ftp.login()
            f.write("Ftp anonymous : [WORKS]\n")
            f.close()
            answ = input("[!] FTP anonymous works, do you still want to bruteforce it? (y/n) ")
            if answ == "y":
                self.tBruteFTP()
            else:
                pass
            try:  # test file upload (creates test.jpg, trys to upload it, removes it, writes in results.txt)
                fileTest = open('test.jpg', 'w+')
                ftp.storbinary('STOR kitten.jpg', fileTest)
                fileTest.close()
                os.remove('test.jpg')
                f = open("{}/results.txt".format(rootDir), "a")
                f.write("File upload : [WORKS]\n")
                f.close()

            except:
                f = open("{}/results.txt".format(rootDir), "a")
                f.write("File upload : [FAILED]\n")
                f.close()



        except:
            f.write("Ftp anonymous : [FAILED]\n")
            f.close()
            pass

    '''
    Returns dictionary of PORT:SERVICE_NAME

    Example use :

    host = "10.10.10.204"
    result = nmapScan(host).services()
    print(result)
    '''

    def listServices(self):
        self.servicesDict = {}
        for port in self.openPorts:
            try:  # If dictionary does not have "product" key, skip. (Theres probably a better way to do this)
                self.servicesDict[port['portid']] = port['service']['product']
            except:
                pass
        return self.servicesDict  # dictionary PORT:SERVICE_NAME

    '''
    Used by dirbust function, creates log files. (Full path + name which is PORT_dirbust.txt)

    '''

    def createLogFiles(self, dir):
        self.logFiles = []  # list of full path
        try:
            os.mkdir(os.path.join(dir, "dirbust"))
        except:
            pass
        for url in self.urls:  # Creates full path
            if SSL == True:
                port = "SSL"
            else:
                port = url.split(":")[2]
            name = "{}_dirbust.txt".format(port)
            self.logFiles.append("{}/dirbust/{}".format(dir, name))
        return self.logFiles  # Return list

    '''
    This is the function that when called, will run a dirbuster on each webservice.

    It needs a wordlist file, thats it!

    Needs https support to be added.
    '''

    def dirbust(self, wordfile):
        self.webServicePorts = []  # list of ports that are running http services
        self.urls = []  # list of url + port ready to dirbust.
        serviceList = self.listServices()  # Gets a list of the services.
        for port in serviceList:
            if serviceList[port] in self.webServices:  # If service_name is a web service
                self.webServicePorts.append(port)  # append the port to list
            else:
                pass
        for port in self.webServicePorts:  # Create url for dirbust.
            if SSL == True:
                if port == "80":
                    url = "https://{}".format(self.host)
                else:
                    url = "https://{}:{}".format(self.host, port)
            else:
                url = "http://{}:{}".format(self.host, port)
            self.urls.append(url)
        logFiles = self.createLogFiles(self.rootDir)  # Creates logFile Paths
        dirbuster(self.urls, wordfile, logFiles, self.rootDir)  # Starts the threads


if __name__ == "__main__":
    '''
    Argparse stuff (Comment out when debugging)

    '''

    parser = argparse.ArgumentParser(description="ReconScript")
    parser.add_argument('--host', type=str, metavar='', required=True, help='IP Address of the host')
    parser.add_argument('--output', type=str, metavar='', required=True,
                        help='Output directory for scan (Full Path) (Example : /home/user/)')
    parser.add_argument('--wordlist', type=str, metavar='', required=True, help='Wordlist to use for dirbust')
    args = parser.parse_args()

    host = args.host
    rootDir = os.path.join(args.output, "reconScript")  # path to create directory
    try:  # Check if it exists (THeres a better way to do it!)
        os.mkdir(rootDir)
    except:
        print("{} Already exists, will output everything there.".format(rootDir))
        pass
    wordlist = args.wordlist
    result = nmapScan(host, rootDir, Debug=False).check(wordlist)  # Regular portScan



