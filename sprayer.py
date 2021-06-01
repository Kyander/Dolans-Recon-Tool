import os
import sys
import threading

wordlist = sys.argv[1]
host = sys.argv[2]
services = sys.argv[3]
rootDir = sys.argv[4]


def bruteFTP(host,wordlist, rootDir):
    rootDir = os.path.join(rootDir, "spray")
    #print(rootDir)
    try:
        os.mkdir(rootDir)
    except:
        pass
    bruteFTPcmd = "hydra -s 21 -t 20 -L {} -e s ftp://{} -o {}/FTP.txt -I ".format(wordlist, host, rootDir)
    #print(bruteFTPcmd)
    os.system(bruteFTPcmd)

def bruteSSH(host,wordlist, rootDir):
    rootDir = os.path.join(rootDir, "spray")
    #print(rootDir)
    try:
        os.mkdir(rootDir)
    except:
        pass
    bruteSSHcmd = "hydra -s 22 -t 20 -L {} -e s ssh://{} -o {}/SSH.txt -I ".format(wordlist, host, rootDir)
    #print(bruteSSHcmd)
    os.system(bruteSSHcmd)



tbruteFTP = threading.Thread(target=bruteFTP, args=(host,wordlist,rootDir,))
tbruteSSH = threading.Thread(target=bruteSSH, args=(host, wordlist, rootDir,))
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


