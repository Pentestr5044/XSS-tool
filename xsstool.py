import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests as req
import argparse
from pyfiglet import Figlet
from termcolor import colored


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
headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}
urlpass3=[]
url = args.url
userAgent = args.userAgent
customPayload = args.wordlist
threadCount = args.threads
delay = args.seconds
print(url, userAgent, delay, customPayload, threadCount)
# crawler functions and first file to be collected (urls, patterns discovered.)
def crawl(arg1, arg2):
    global urlpass3
    urlpass2= []
    urlpass = []
    c = 0
    if len(url) > 0 and c == 0:
        try:
            r = req.get(url, headers=headers)
            bs = BeautifulSoup(r.text,'html.parser')
            inTag=bs.find_all('input')
            print('input tags are: ', inTag)
            for i in bs.find_all("a", href=True):
                urlpass.append(i.get('href'))
            print(urlpass)
            for u in urlpass:
                if href in u:
                    r1 = req.get(u, headers=headers)
                    bs1 = BeautifulSoup(r1.text, 'html.parser')
                    for p in bs1.find_all("a", href=True):
                        urlpass2.append(p.get('href'))
            for i in urlpass2:
                if href in i:
                    urlpass3.append(i)
                    #saving the urls in a list of one url per line!!
        except ConnectionError:
            print('This site is not reachable')
    return

#logic for input requests and XSS payload injection



if len(url) > 0:
    href = urlparse(url).netloc
    crawl(url,href)
    print(len(urlpass3))#for and saving urls to file

