import os
import argparse
import subprocess


parser = argparse.ArgumentParser(description="ReconScript")
parser.add_argument('--host', type=str, metavar='', required=True, help='IP Address of the host')
parser.add_argument('--output', type=str, metavar='', required=True,
                        help='Output directory for scan (Full Path) (Example : /home/user/)')
args = parser.parse_args()

ip = args.host

def main(output,ip):
    try:
        os.mkdir("{}/SMB".format(output))  # Creates the "SMB" directory
    except:
        pass
    try:
        os.mkdir("{}/SMB/downloadedFiles".format(output))
    except:
        pass

    global authType
    authType = 0
    output = subprocess.check_output("smbmap -H {} -u 'admin' -p 'admin' -q ".format(ip), shell=True)
    if output == b'':
        authType = 1
        output = subprocess.check_output("smbmap -H {}".format(ip), shell=True)
    else:
        pass
    listing = str(output).split("\\n\\t")
    listing.pop(0)
    listing.pop(0)
    shareList = []
    for x in listing:
        if x.split(" ")[1] != '':
            new = x.split(" ")
            nshare = new[0] + " " + new[1]
            shareList.append(nshare)
        else:
            shareList.append(x.split(" ")[0])

    return shareList


def getFiles(shares,output,ip):
    global authType
    for share in shares:
        if " " in share:
            new = share.split(" ")
            newShare = new[0] + new[1]
            path = "{}/SMB/downloadedFiles/{}".format(output, newShare)
        else:
            path = "{}/SMB/downloadedFiles/{}".format(output, share)
        try:
            os.mkdir(path)
        except:
            pass
        if authType == 0:
            os.system("cd {} && smbget -a -R 'smb://dummy:dummy@{}/{}'".format(path,ip,share))
        else:
            os.system("cd {} && smbget -a -R 'smb://{}/{}'".format(path, ip, share))

def userOutputSMB(ip,output):
    global authType
    if authType == 0:
        os.system("crackmapexec smb {} --shares -u 'admin' -p 'admin' | tee {}/SMB/CME.txt".format(ip,output))
    else:
        os.system("smbmap -H {} -R | tee {}/SMB/smbmap.txt".format(ip,output))


if __name__ == '__main__':
    shareList = main(args.output, args.host)
    userOutputSMB(args.host,args.output)
    getFiles(shareList,args.output,args.host)
    os.system("echo '[!] Done, you can now close this window'")

