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

def tgl(text):
    now = datetime.now()
    
    y = now.strftime("%Y")
    
    s = text.split()
    j = 0
    m = 0
    if len(s)==5:
        if s[1] == 'Januari':
            bln = 1
        elif s[1] == 'Februari':
            bln = 2
        elif s[1] == 'Maret':
            bln = 3
        elif s[1] == 'April':
            bln = 4
        elif s[1] == 'Mei':
            bln = 5
        elif s[1] == 'Juni':
            bln = 6
        elif s[1] == 'Juli':
            bln = 7
        elif s[1] == 'Agustus':
            bln = 8
        elif s[1] == 'September':
            bln = 9
        elif s[1] == 'Oktober':
            bln = 10
        elif s[1] == 'November':
            bln = 11
        elif s[1] == 'Desember':
            bln = 12
        
        wkt = s[-2].replace(".", " ")
        angka = wkt.split()
        # print(angka)
        j = angka[0]
        m = angka[1]
        h = s[0]
    else:
        if s[1]=='jam':
            j = s[0]
            m = now.strftime("%M")
        elif s[1]=='menit':
            j = now.strftime("%H")
            m = s[0]
        bln = now.strftime("%m")
        h = now.strftime("%d")
    
    return datetime(int(y), int(bln), int(h), int(j), int(m), 0)

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
    
def get_post(driver, p):
        
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, 'BrowseResultsContainer')))
    except:
        pass
    soup = BeautifulSoup(driver.page_source, 'lxml')
    browse = soup.find("div", {"class":"_2v9s"}, recursive=True)
    Pages = browse.findAll("div", {"id":"BrowseResultsContainer"}, recursive=True)
    get = Pages[0].findAll("div", {"data-module-role":"PUBLIC_POSTS"})
    gett = get[p].find("div",{"data-module-result-type":"story"}).find("div")
    posting = driver.find_element_by_id(gett['id']).click()
    url_post = driver.current_url
    
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'story_body_container')))
    except:
        pass
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.ID, 'MPhotoUpperContent')))
    except:
        pass
    sop = BeautifulSoup(driver.page_source, 'lxml')
    try:
        body_tab = sop.find("div", {"class":"story_body_container"})
        poster_tab = body_tab.find("div", {"class":"_7om2 _52wc"})
        poster = poster_tab.find("a").get("href")
    except:
        try:
            body_tab = sop.find("div", {"id":"MPhotoUpperContent"})
            poster_tab = body_tab.find("div", {"class":"msg"})
            poster = poster_tab.find("a").get("href")
        except:
            body_tab = sop.find("div", {"id":"MPhotoContent"})
            poster_tab = body_tab.find("div", {"class":"msg"})
            poster = poster_tab.find("a").get("href")
    url_akun = "https://m.facebook.com/"+str(poster)
    
    try:
        tl = body_tab.find("div", {"data-sigil":"m-feed-voice-subtitle"}).text
    except:
        header = sop.find("div", {"id":"MPhotoUpperContent"})
        tl = header.find("abbr").text
    tgl_post = tgl(tl)
    
    return url_post, url_akun, tgl_post

def get_post_detail(soup):
    # Mendaptkan Caption
    try:
        caption = soup.find("div", {"class":"story_body_container"}).find("div", {"class":"_5rgt _5nk5"}).text
    except:
        caption = soup.find("div", {"id":"MPhotoUpperContent"}).find("div",{"class":"c"}).find("div", {"class":"msg"}).find("div").text

    hashtag = get_hastag(caption)
    
    try:
        url_link = get_url(caption)
    except:
        try:
            url_link = soup.find("a", {"aria-labelledby":"u_7_2"}).get("href")
        except:
            url_link = None
    
    # Mendapatkan tgl post
    try:
        header = soup.find("header", {"class":"_7om2 _1o88 _77kd _5qc1"})
        tl = header.find("div", {"data-sigil":"m-feed-voice-subtitle"}).text
    except:
        header = soup.find("div", {"id":"MPhotoUpperContent"})
        tl = header.find("abbr").text
    try:
        tgl_post = tgl(tl)
    except:
        tgl_post = datetime.now()
        
    try:
        body_tab = soup.find("div", {"class":"story_body_container"})
        poster_tab = body_tab.find("div", {"class":"_7om2 _52wc"})
        poster = poster_tab.find("a").get("href")
    except:
        body_tab = soup.find("div", {"id":"MPhotoUpperContent"})
        poster_tab = body_tab.find("div", {"class":"msg"})
        poster = poster_tab.find("a").get("href")

    url_akun = "https://m.facebook.com/"+str(poster)
    
    return caption, hashtag, url_link, tgl_post, url_akun

def get_detail_comment(soup):
    # Get Comment
    comment_noReply = soup.find("div", {"data-sigil":"comment-body"})
    comment= comment_noReply.text

    # Extract Hastag
    hashtag = get_hastag(comment_noReply.text)

    # Extract url
    url = get_url(comment_noReply.text)

    # Get Username
    person_noReply = soup.find("div",{"class": "_2b05"})
    username = person_noReply.text

    # Get URL User
    user = soup.find("div",{"class": "_2a_j"}).find("a").get("href")
    url_user = "https://m.facebook.com"+user

    # Get img_url
    try:
        img_url_tab = soup.find("div", {"_2b1t attachment"}).find("a")
        img_url = img_url_tab.get("href")
    except:
        img_url = None

    # Get Like
    try:
        like_tab = soup.find("span",{"class":"_14va"})
        like = int(like_tab.text)
    except:
        like = 0

    # Get Uniqe Value from Comment
    url_comment = soup.get("id")
    
    return comment, hashtag, url, username, url_user, img_url, like, url_comment

def get_comment(driver, caption, df0):

    soup = BeautifulSoup(driver.page_source, 'lxml')
    klik = soup.find_all("div", {"class":"async_elem"})
    
    o = 0
    while True:
        try:
            next_id = klik[-1].get("id")
    #         print(next_id)
            driver.find_element_by_id(next_id).click()
            klik = soup.find_all("div", {"class":"async_elem"})
            time.sleep(2)
            o = o +1
            if o >= 10:
                break
        except:
            break
            
    # Get Comment Tab
    soup = BeautifulSoup(driver.page_source, 'lxml')

    comment_tab = soup.find("div", {"class": "_333v _45kb"})
    if comment_tab != None:
        comments_noReply = comment_tab.findAll("div", {"class":"_2a_i"}, recursive=True)

        # Get per 1 Data
        for i in tqdm(range(len(comments_noReply)), desc = "Getting Comment Detail From Post"):
            # Get Detail 
            comment, hashtag, url, username, url_user, img_url, like, url_comment = get_detail_comment(comments_noReply[i])

            df = pandas.DataFrame({"post":[caption],
                                    "comment": [comment],
                                    "parrent_comment":[None]})
            df0 = df0.append(df)
        # For unlock comment with reply
        main_window = driver.current_window_handle
        klik_ = soup.find_all("div", {"class":"_2a_m"})
        for k in klik_:
            id_reply = k.find_all("div")[0].get("id")
            try:
                driver.find_element_by_id(id_reply).click()
            except Exception as err:
                pass

        driver.switch_to_window(main_window)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        comment_tab = soup.find("div", {"class": "_333v _45kb"})
        comments_withReply = comment_tab.findAll("div", {"class":"_2a_i _2a_l"}, recursive=True)

        for i in (range(len(comments_withReply))):
            # Get Detail 
            p_comment, hashtag, url, username, url_user, img_url, like, url_comment = get_detail_comment(comments_withReply[i])

            comments_ = comments_withReply[i].findAll("div", {"class":"_2a_i"}, recursive=True)
            num_replyed_comment = len(comments_)


            # print(child_parent )
            # Get per 1 Data
            for j in tqdm(range(num_replyed_comment), desc = "Getting Detail from Replyed Comment {}".format(str(i))):
                comment, hashtag, url, username, url_user, img_url, like, url_comment = get_detail_comment(comments_[j])

                df = pandas.DataFrame({"post":[caption],
                                        "comment": [comment],
                                        "parrent_comment":[p_comment]})
                df0 = df0.append(df)
    else:
        print("There's No Comment")
    return df0