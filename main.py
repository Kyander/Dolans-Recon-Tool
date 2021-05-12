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
            self.result = {'192.168.241.55': {'osmatch': {}, 'ports': [{'protocol': 'tcp', 'portid': '21', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'ftp', 'product': 'FileZilla ftpd', 'version': '0.9.41 beta', 'ostype': 'Windows', 'method': 'probed', 'conf': '10'}, 'cpe': [{'cpe': 'cpe:/o:microsoft:windows'}], 'scripts': []}, {'protocol': 'tcp', 'portid': '80', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'http', 'product': 'Apache httpd', 'version': '2.4.43', 'extrainfo': '(Win64) OpenSSL/1.1.1g PHP/7.4.6', 'method': 'probed', 'conf': '10'}, 'cpe': [{'cpe': 'cpe:/a:apache:http_server:2.4.43'}], 'scripts': []}, {'protocol': 'tcp', 'portid': '135', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'msrpc', 'product': 'Microsoft Windows RPC', 'ostype': 'Windows', 'method': 'probed', 'conf': '10'}, 'cpe': [{'cpe': 'cpe:/o:microsoft:windows'}], 'scripts': []}, {'protocol': 'tcp', 'portid': '139', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'netbios-ssn', 'product': 'Microsoft Windows netbios-ssn', 'ostype': 'Windows', 'method': 'probed', 'conf': '10'}, 'cpe': [{'cpe': 'cpe:/o:microsoft:windows'}], 'scripts': []}, {'protocol': 'tcp', 'portid': '443', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'http', 'product': 'Apache httpd', 'version': '2.4.43', 'extrainfo': '(Win64) OpenSSL/1.1.1g PHP/7.4.6', 'tunnel': 'ssl', 'method': 'probed', 'conf': '10'}, 'cpe': [{'cpe': 'cpe:/a:apache:http_server:2.4.43'}], 'scripts': []}, {'protocol': 'tcp', 'portid': '445', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'microsoft-ds', 'method': 'table', 'conf': '3'}, 'scripts': []}, {'protocol': 'tcp', 'portid': '3306', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'mysql', 'servicefp': 'SF-Port3306-TCP:V=7.91%I=7%D=5/12%Time=609C56CD%P=x86_64-pc-linux-gnu%r(NULL,4D,"I\\0\\0\\x01\\xffj\\x04Host\\x20\'192\\.168\\.49\\.241\'\\x20is\\x20not\\x20allowed\\x20to\\x20connect\\x20to\\x20this\\x20MariaDB\\x20server")%r(GetRequest,4D,"I\\0\\0\\x01\\xffj\\x04Host\\x20\'192\\.168\\.49\\.241\'\\x20is\\x20not\\x20allowed\\x20to\\x20connect\\x20to\\x20this\\x20MariaDB\\x20server")%r(Kerberos,4D,"I\\0\\0\\x01\\xffj\\x04Host\\x20\'192\\.168\\.49\\.241\'\\x20is\\x20not\\x20allowed\\x20to\\x20connect\\x20to\\x20this\\x20MariaDB\\x20server");', 'method': 'table', 'conf': '3'}, 'scripts': []}, {'protocol': 'tcp', 'portid': '5040', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'unknown', 'method': 'table', 'conf': '3'}, 'scripts': []}, {'protocol': 'tcp', 'portid': '7680', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '127', 'service': {'name': 'pando-pub', 'method': 'table', 'conf': '3'}, 'scripts': []}], 'hostname': [], 'macaddress': None, 'state': {'state': 'up', 'reason': 'echo-reply', 'reason_ttl': '127'}}, 'stats': {'scanner': 'nmap', 'args': '/usr/bin/nmap -oX - -sV -p- -oN /home/Kyand/autorecon/reconscript/apptest/reconscript/reconScript/nmap/nmap_scan.txt 192.168.241.55', 'start': '1620858443', 'startstr': 'Wed May 12 18:27:23 2021', 'version': '7.91', 'xmloutputversion': '1.05'}, 'runtime': {'time': '1620858739', 'timestr': 'Wed May 12 18:32:19 2021', 'summary': 'Nmap done at Wed May 12 18:32:19 2021; 1 IP address (1 host up) scanned in 295.99 seconds', 'elapsed': '295.99', 'exit': 'success'}}
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
                    self.tBruteSSH()
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
    result = nmapScan(host, rootDir, Debug=True).check(wordlist)  # Regular portScan



