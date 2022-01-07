import os
import sys
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests as req
import argparse
from pyfiglet import Figlet
from termcolor import colored, cprint
from fake_useragent import UserAgent
ua = UserAgent()
# needed for windows cli to reflect the color!!
os.system('color')

# custom ascii art header
headerset = Figlet(font='poison', width=150)
header = headerset.renderText('XSS-Granted')
print(colored(header, 'green', 'on_grey'))
# argparse variables and help descriptions.
parser = argparse.ArgumentParser(
    prog='XSS-Granted',
    description="This is an XSS tool for crawling/testing/and scraping data related to Cross Site Scripting Vulnerabilities. Happy Hacking!! "
)
parser.add_argument(
    '-u',
    '--url',
    type=str,
    help="This flag allows you to set the starting url of the target please enter full http/https URL "
)
parser.add_argument(
    '-d',
    '--domain',
    type=str,
    help="This flag allows you to set the starting domain of the target  to confirm match please enter root domain yahoo.com etc "
)
parser.add_argument(
    '-t',
    '--threads',
    type=int,
    help="This flag for adjusting the thread count default is 2",
    default=2
)
parser.add_argument(
    '-s',
    '--seconds',
    type=int,
    help="Set the milliseconds between requests default will be 500",
    default=500
)
parser.add_argument(
    '-w',
    '--wordlist',
    type=str,
    help="This flag allows you to use your own custom wordlist for Payloads, This tool will then use the wordlist and generate mutations of the wordlist to try and execute a XSS attack."
)
parser.add_argument(
    '-ua',
    '--userAgent',
    help="Use this flag for random user agent headers, helpful when bypassing blockers on agent headers ",
    action='store_true'
)
parser.set_defaults(ua=False)
args = parser.parse_args()
print(args)
# variables for requests.

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
urlpass3 = []
url = args.url
userAgent = args.userAgent
customPayload = args.wordlist
threadCount = args.threads
delay = args.seconds
domain = args.domain
print(url, userAgent, delay, customPayload, threadCount)


# crawler functions and first file to be collected (urls, patterns discovered.)
def crawl(arg1, arg2):
    global urlpass3
    urlpass2 = []
    urlpass = []
    c = 0
    if len(url) > 0 and c == 0:
        try:
            r = req.get(url, headers=headers)
            bs = BeautifulSoup(r.text, 'html.parser')
            inTag = bs.find_all('input')
            print('input tags are: ', inTag)
            for i in bs.find_all("a", href=True):
                urlpass.append(i.get('href'))
            print(urlpass)
            for u in urlpass:
                if domain in u:
                    r1 = req.get(u, headers=headers)
                    bs1 = BeautifulSoup(r1.text, 'html.parser')
                    for p in bs1.find_all("a", href=True):
                        urlpass2.append(p.get('href'))

            for i in urlpass2:
                test_case = urlparse(i)
                if test_case.netloc == domain:
                    if domain in i:
                        urlpass3.append(i)

                    # saving the urls in a list of one url per line!!
        except ConnectionError:
            print('This site is not reachable')
    return
def crawl2(arg1, arg2):
    global urlpass3
    urlpass2 = []
    urlpass = []
    c = 0
    if len(url) > 0 and c == 0:
        try:
            r = req.get(url, headers=rheaders)
            bs = BeautifulSoup(r.text, 'html.parser')
            inTag = bs.find_all('input')
            print('input tags are: ', inTag)
            for i in bs.find_all("a", href=True):
                urlpass.append(i.get('href'))
            print(urlpass)
            for u in urlpass:
                if domain in u:
                    r1 = req.get(u, headers=rheaders)
                    bs1 = BeautifulSoup(r1.text, 'html.parser')
                    for p in bs1.find_all("a", href=True):
                        urlpass2.append(p.get('href'))

            for i in urlpass2:
                test_case = urlparse(i)
                if test_case.netloc == domain:
                    if domain in i:
                        urlpass3.append(i)

                    # saving the urls in a list of one url per line!!
        except ConnectionError:
            print('This site is not reachable')
    return

# logic for scraping wayback with verified url list
urls_found = []


def lol(domain):
    global urls_found
    url = "http://web.archive.org/cdx/search/cdx?url={}*&output=json&collapse=urlkey".format(domain)
    response = req.get(url, timeout=3, verify=False)
    if response:
        tmp = json.loads(response.text)
    for item in tmp:
            if item[2] not in urls_found:
                    urls_found.append(item[2])


if len(url) > 0:
    crawl(url, domain)
    file = open('urls.txt', 'a')
    for i in set(urlpass3):
        file.write(i+'\n')
    cprint('File Created!!!', 'green')
    file.close()
    a = open('urls.txt', 'r')
    for i in a:
        lol(i)
    a.close()
    for i in urls_found:
        print(i)

if len(url) > 0 and userAgent == True:
    rheaders = {
        'user-agent': str(ua.random)
    }
    crawl2(url,domain)
    file = open('urls1.txt', 'a')
    for i in set(urlpass3):
        file.write(i + '\n')
    cprint('File Created Urls1.txt Thank you for using a random user agent header!!!', 'green')
    file.close()
    a = open('urls1.txt', 'r')
    for i in a:
        lol(i)
    a.close()
    for i in urls_found:
        print(i)
