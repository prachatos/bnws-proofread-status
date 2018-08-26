# -*- coding: utf-8 -*-

import datetime
import logging
import os
import sys
import time

import ConfigParser

import wikitools

config = ConfigParser.ConfigParser()
config.read("config.ini")

wiki_username = config.get('settings', 'wiki_username')
wiki_password = config.get('settings', 'wiki_password')
wikisource_language = config.get('settings', 'wikisource_language')
fpage = config.get('settings', 'pagefirst')
lpage = config.get('settings', 'pagelast')
book = config.get('settings', 'book_name')

wiki_url = "https://" + wikisource_language + ".wikisource.org/w/api.php"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')

if not os.path.isdir("./log"):
    os.mkdir("./log")

# create a file handler
log_file = './log/proofread-status-change_' + timestamp + '_log.txt'

handler = logging.FileHandler(log_file)
handler.setLevel(logging.INFO)

# create a logging format

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger

logger.addHandler(handler)

try:
    wiki = wikitools.wiki.Wiki(wiki_url)
except:
    message = "Can not connect with wiki. Check the URL"
    logger.info(message)
    sys.exit()

login_result = wiki.login(username=wiki_username, password=wiki_password)
message = "Login Status = " + str(login_result)
logging.info(message)

if login_result:
    message = "\n\nLogged in to " + wiki_url.split('/w')[0]
    logging.info(message)
else:
    message = "Invalid username or password error"
    logging.info(message)
    sys.exit()
    

def change_status(pagename):
    page = wikitools.Page(wiki, "Page:" + pagename, followRedir=True)
    print page

    logging.info("Editing " + "https://" + wikisource_language + ".wikisource.org/wiki/" + page.title)
    content = page.getWikiText()

    new_content = content.replace('pagequality level="3"', 'pagequality level="4"')

    if new_content != content:
        page.edit(text=new_content, summary="[[বিষয়শ্রেণী:বৈধকরণ]]")
        logging.info("Changed level to 4")
    else:
        logging.info("Page is not currently at level 3")


def to_bn(num):
    bn = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯']
    ans = ''
    if int(num) < 10: return bn[int(num)]
    while int(num) > 0:
        ans = bn[int(num) % 10] + ans
        num = str(int(int(num) / 10))
    return ans


counter = int(fpage)

while counter <= int(lpage):
    logging.info("Page no = " + str(counter))

    filename = book.split("File:")[1]

    change_status(filename.strip() + "/" + to_bn(counter))

    counter = counter + 1
    print counter

