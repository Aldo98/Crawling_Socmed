from facebook_scraper import get_posts
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import pprint
import datetime
from tqdm import tqdm
from os import system, name


def extract_info(i, nama, lokasi_tab, location, created, followers, akun, url):
    for entiti in lokasi_tab:
        split = entiti.text.split()
        #print(split)
        if split[0]=='Dari' or split[0]=='Tinggal':
            location[i]= entiti.text
        elif split[0]=='Bergabung':
            created[i] = entiti.text
        elif split[0]=='Diikuti':
            followers[i] = split[2]
    info = {"name": nama.text, "url_akun": "https://m.facebook.com"+url, 
            "lokasi": location[i], "followers": followers[i],
            "created_at": created[i]}
    akun.append(info)
    
    return akun

def akun_info(url_media, driver, soup):
    main_window = driver.current_window_handle
    akuns = soup.find_all("div", {"class":"_2b00"})
    account = []
    name = []
    followers = []
    location = []
    url_akun = []
    created = []
    i = 0
    for akun in tqdm(akuns):
        followers.append(' ')
        location.append(' ')
        url_akun.append(' ')
        created.append(' ')
        driver.switch_to_window(main_window)
        driver.execute_script("window.open();")
        driver.switch_to_window(driver.window_handles[1])
        url = akun.find('a').get('href')
        driver.get("https://m.facebook.com"+url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
    
        lokasi_tab = soup.find_all("div", {"class":"_4g34 _5b6q _5b6p _5i2i _52we"})
        try:
            nama = soup.find("div", {"class":"_52jc _1lk9 _2pi0"})
            if nama.text not in name:
                name.append(nama.text)
                url_akun.append("https://m.facebook.com"+url)
                account = extract_info(i, nama, lokasi_tab, location, created, followers, account, url)
                

        except:
            nama = soup.find("div", {"class":"_59k _2rgt _1j-f _2rgt"})
            if nama.text not in name:
                name.append(nama.text)
                url_akun.append("https://m.facebook.com"+url)
                account = extract_info(i, nama, lokasi_tab, location, created, followers, account, url)
        
        #print(account[i])
        #print('\n')
        i = i+1
        driver.close()
        
        
    driver.switch_to_window(main_window)

    driver.close()
    
    return account

def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def get_data(akun_name, pages=10, options = Options().add_argument("user-data-dir=crawtool/.config/selenium")):
    hasil = []
    for post in tqdm(get_posts(akun_name, pages=pages)):
        #driver = webdriver.Chrome()
        #driver.get(post['post_url'])
        #page_source = driver.page_source
        #if post['comments']!=0:
        #pprint(post)
        time = post['time']
        now = datetime.datetime.now()
        if time.day >= now.day-1 and time.month == now.month and time.year == now.year:     #cek apakah itu postingan 1 hari kebelakang atau bukan
            # options = Options()
            # options.add_argument("user-data-dir=.config/selenium")
            driver = webdriver.Chrome(options=options)      
            driver.get(post['post_url'])
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')

            comment_tab = soup.find("div", {"class": "_333v _45kb"})
            like_tab = soup.find("div", {"class":"_1g06"})
            akuns = soup.find_all("div", {"class":"_2b00"})
            bagikan_tab = soup.find("div", {"class":"_43lx _55wr"})

            try:
                post['likes'] = like_tab.text
                post['shares'] = bagikan_tab.text
            except:
                pass
            
            print("\nGet Akun Info...")
            info_akun = akun_info(post['post_url'], driver, soup)

            comment_noReply = []
            person_noReply = []
            comment_withReply = []
            person_withReply = []


            try:
                comments_withReply = comment_tab.findAll("div", {"class":"_2a_i _2a_l"}, recursive=False)
                comments_noReply = comment_tab.findAll("div", {"class":"_2a_i"}, recursive=False)
                persons_withreply = comment_tab.findAll("div", {"class":"_2b05"}, recursive=False)
                persons_noReply = comment_tab.findAll("div", {"class":"_2b05"}, recursive=False)
                for j in range(len(comments_noReply)):
                    comment_noReply.append(comments_noReply[j].find("div", {"data-sigil":"comment-body"}))
                    person_noReply.append(comments_noReply[j].find("div",{"class": "_2b05"}))
                    comment_noReply[j] = comment_noReply[j].text
                    person_noReply[j] = person_noReply[j].text

                for k in range(len(comments_withReply)):
                    comment_withReply.append(comments_withReply[k].find("div", {"data-sigil":"comment-body"}))
                    person_withReply.append(comments_withReply[k].find("div",{"class": "_2b05"}))
                    comment_withReply[k] = comment_withReply[k].text
                    person_withReply[k] = person_withReply[k].text

                comment_noReply.extend(comment_withReply)
            except:
                pass
            hasil.append({"akun_name": akun_name, "url_post": post['post_url'], "link_url": post['link'],
                          "caption": post['text'], "num_like": post['likes'], "num_share": post['shares'],
                          "data_komentar": info_akun, "komentar": comment_noReply, "num_komen":  len(comment_noReply),
                          "created_at": post['time']})
        else:
            pass
        clear()
        print("Scrapping Facebook.....\n")
    
    print("Crawling Finished....")

    return hasil

#pprint.pprint(get_data('pertamina', pages=1))