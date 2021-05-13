import os
import pydirbuster
import argparse


'''
Imports to overwrite :

'''
import requests, urllib.request
from requests_ntlm import HttpNtlmAuth
from random import shuffle, choice
import concurrent.futures
import argparse
from string import ascii_letters
import sys, time
import pydirbuster
from pathlib import Path
from collections import defaultdict
from tqdm import tqdm

'''
Overwriting pydirbuster to allow https support.
'''


def _brute(self, client: requests.Session, url: str, filename: str, pbar):
    """Function that sends the http requests and processes the response.
       param: client - The Session object to send requests.
       type: requests.Session
       param: url - Website base url.
       type: str
       param: filename - File on webserver to request.
       type: str"""
    resp = client.get(url + filename, verify=False)
    pbar.update(1)
    if resp.status_code in self.codes:
        result = f"/{filename} (Status : {resp.status_code})"
        self.results[resp.status_code].append(filename)
        tqdm.write(result)
        if self.logfile:
            with open(self.logfile, 'a') as f:
                f.write(result + '\n')


def Run(self):
    """The main function of the Pybuster class. This function kicks off and
       controls all of the scanning, the checks on whether the server is down
       or is wildcard matching, and returns a results dictionary that has keys
       that correspond to various http response codes and values that are lists
       of filenames that came back with the corresponding response code."""
    try:
        import ssl
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        r = urllib.request.urlopen(self.url + ''.join(choice(ascii_letters) for i in range(60)), context=ctx)
        tqdm.write(r.status)
    except urllib.error.HTTPError:
        r = None
    except urllib.error.URLError:
        tqdm.write(f"Do you have the proper address? Because {self.url} seems to be down.")
        sys.exit(1)
    if r and not self.force:
        tqdm.write("Website is wildcard matching. Do you really want to bruteforce this website?")
        sys.exit(0)
    if bool(self.user) and bool(self.password):
        r = requests.post(self.url, auth=HttpNtlmAuth(self.user, self.password))
        if r.status_code != 200:
            tqdm.write("Don't have proper credentials. Please recheck.")
            sys.exit(0)
    if self.logfile:
        with open(self.logfile, 'w'):
            pass
    client = requests.Session()
    client.headers['User-Agent'] = self.user_agent
    list_length = len(self.wordlist) * len(self.exts)
    wordlist = (i + e for i in self.wordlist for e in self.exts)
    clientpool, urllist = (client for i in range(list_length)), (self.url for i in range(list_length))
    pbar = tqdm(total=list_length, leave=False)
    pbars = (pbar for i in range(list_length))
    self._header()
    with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
        try:
            start = time.perf_counter()
            executor.map(self._brute, clientpool, urllist, wordlist, pbars)
        except:
            executor.shutdown()
    self._print_func()
    self._print_func(f"Time elapsed : {time.perf_counter() - start}")
    return self.results


pydirbuster.Pybuster._brute = _brute
pydirbuster.Pybuster.Run = Run

'''
Overwritting Pydribuster ^^^^
'''


parser = argparse.ArgumentParser(description="ReconScript")
parser.add_argument('--url', type=str, metavar='', required=True, help='IP Address of the host')
parser.add_argument('--output', type=str, metavar='', required=True,
                        help='Output directory for scan (Full Path) (Example : /home/user/)')
parser.add_argument('--wordlist', type=str, metavar='', required=True, help='Wordlist to use for dirbust')
args = parser.parse_args()

#print(args.url)

test = args.url

port = test.split(":")[2]
if port == "443":
    new = test.split(":")[0] = "https"
    old = test.split(":")[1]
    old2 = test.split(":")[2]
    combine = new+":" + old + ":" + old2



    webbuster = pydirbuster.Pybuster(url=combine,wordfile=args.wordlist,logfile=args.output,codes=["200","201","202","301","302","405"])
    try:
        webbuster.Run()
    except:
        print("failed")
else:
    pass

webbuster = pydirbuster.Pybuster(url=args.url,wordfile=args.wordlist,logfile=args.output,codes=["200","201","202","301","302","405"])

try:
    webbuster.Run()
except:
    print("failed")
