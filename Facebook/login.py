import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup 
import psutil
import random
import time
import hashlib
from datetime import datetime
import pandas as pd
from tqdm import tqdm
import json
import shutil

################################################################## Password Encode 
def encode_pass(paswords):
    result = ''
    for i in paswords:
        result = result+"*"
    return result

############################################## Config
with open("credential.json", "r") as f:
    conf_db = json.load(f)
nope = conf_db["akun"][0]["email/phone"]
pasw = conf_db["akun"][0]["password"]

############################################################## Delete Sesion
try:
  shutil.rmtree(r'selenium')
except:
  pass

######################################################## login
option = Options()
option.add_argument("user-data-dir=selenium")
# option.add_argument("headless")
driver = webdriver.Chrome(options=option, executable_path=r'chromedriver.exe') 
driver.get('https://m.facebook.com/')

print('Login To Facebook...')
print('Email/Phone \t: '+nope)
print('Password \t: '+encode_pass(pasw))

name = driver.find_element_by_name('email')
name.send_keys(nope)
pasword = driver.find_element_by_name('pass')
pasword.send_keys(pasw)
pasword.send_keys(Keys.RETURN)

WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, '_2pii')))
# soup = BeautifulSoup(driver.page_source, 'lxml')
# neks = soup.find("div", {"class":"_2pii"}).find("a").get('href')
# driver.get('https://m.facebook.com/'+str(neks))
driver.find_element_by_xpath('//*[@id="root"]/div[1]/div/div/div[3]/div[2]/form/div/button').click()

time.sleep(5)
driver.close()