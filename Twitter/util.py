import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup 
import random
import time
import pandas
from tqdm import tqdm
from datetime import datetime
import re

def get_hastag(tags):
    hastag = []
    try:
        hastag = [tag.strip("#") for tag in tags.split() if tag.startswith("#")]
    except:
        pass
    return hastag

def get_url(teks):
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    url = re.findall(pattern, teks)
    url_fixed = []
    for i in range(len(url)):
        url_fixed.append(escp_postgrestr(url[i]))
    return url_fixed

def escp_postgrestr(txtt):
    if (type(txtt)== type(None)):
        return " " 
    else:
        txtt = txtt.replace("'", "''")
        return txtt
    
def get_post(post):
    tweet = post.find('div',{'class':"css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0"}).text
    
    detail_post = post.find("a",{"class":"r-qvutc0","role":"link"})
    link_stat = 'https://twitter.com{}'.format(detail_post.get('href'))
    
    return tweet, link_stat

def get_comment(soup, caption, df0):
    comments = soup.find_all("article",{"class":"css-1dbjc4n","role":"article","data-focusable":"true"})
    # print(len(comments))
    for com in comments:
        try:
            comment = com.find('div',{'class':"css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0"}).text
            df = pandas.DataFrame({"post":[caption],
                                    "comment": [comment],
                                    "parrent_comment":[None]})
            df0 = df0.append(df)
        except:
            df = pandas.DataFrame({"post":[caption],
                                    "comment": [None],
                                    "parrent_comment":[None]})
            df0 = df0.append(df)
    return df0