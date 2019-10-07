import requests 
import json
import base64
import pprint
from crawtool.anagojsono import jsonkansaja
from crawtool.crawling import get_data
from crawtool.ner_hit_api import *
from crawtool import dbtool as dbt
import hashlib
from selenium.webdriver.chrome.options import Options
import datetime
import argparse
import datetime
from tqdm import tqdm

API_Ner = "https://apiserver.nergrit.addnotes.id/api/syncnerb64/"
API_Emotion = "https://apiserver3.nergrit.addnotes.id/api/emot_anlzb64/"
  
 
parser = argparse.ArgumentParser(description='Scrapping Instagram from Acount')
parser.add_argument('--akun_name', default='detikcom', help='username akun facebook yang akan di scrapping')
parser.add_argument('--Pages',type=int, default='5', help='banyak pages yang akan di scrapping')


args = parser.parse_args()

dx_id_name            = None
dx_url_media          = None
dx_url_link           = None
dx_caption            = None
# dx_type_media    = "Post Facebook"
dx_created_at         = None
dx_post_created       = None
dx_num_share          = None
dx_num_comment        = None
dx_num_likes          = None
# print(dx_num_comment, dx_num_likes)
dx_NER                = None
dx_comment_emotionya  = None
dx_account_comment    = None
dx_id_collection      = None
dx_id_collection      = None
dx_link_url           = "https://www.facebook.com/"

options = Options()
options.add_argument("user-data-dir=crawtool/.config/selenium")
options.add_argument("headless")

print("Scrapping Facebook.....")
hasil = get_data(args.akun_name, pages=args.Pages, options=options)  #nama akun , berapa banyak pages yang dibuka 

print("Analysis NER and Emotion.....")
for i in tqdm(range(len(hasil))):
    teks = hasil[i]['caption']
    # print(teks)
    try:
        Ner = dict({"NER": get_ner(teks)})
    except:
        Ner = dict({"NER": get_ner_dict(teks)})

    emot = []
    for j in range(len(hasil[i]['komentar'])):
        # print("Analysis ")
        komens = hasil[i]['komentar'][j]
        emot.append({'Komentar': komens, 'Emotion':get_emot(hasil[i]['komentar'][j])})
    komens = hasil[i]['komentar']
    hasil[i]['komentar'] =  emot
    #hasil[i].update(Ner)
    

# pprint.pprint(hasil)
#datas = hasil
# datas = get_hasil(root_akun =args.root_akun , max_media = args.max_media)
# print(datas[0]["num_comment"], "\n\n")
# print(datas[0]["num_likes"], "\n\n")
# data = json.dumps(datas)
# print(data, "\n")

# print(datas)
# print("lendt", len(datas) )

print("Input into Database....")
for abc in tqdm(range(0, len(hasil))):
    #print(datas[abc])
    dx_id_name            = hasil[abc]["akun_name"]
    dx_url_media          = hasil[abc]["url_post"]
    dx_url_link           = hasil[abc]["link_url"]
    dx_caption            = hasil[abc]["caption"]
    # dx_type_media    = "Post Facebook"
    dx_created_at         = str(datetime.datetime.now())
    dx_post_created       = str(hasil[abc]["created_at"])
    dx_num_share          = hasil[abc]["num_share"]
    dx_num_comment        = int(hasil[abc]["num_komen"])
    dx_num_likes          = int(hasil[abc]["num_like"])
    # print(dx_num_comment, dx_num_likes)
    #dx_NER                = json.dumps(hasil[abc]["NER"])        # cant use NER for a while
    dx_comment_emotionya  = json.dumps(hasil[abc]["komentar"])
    dx_account_comment    = json.dumps(hasil[abc]["data_komentar"])
    dx_id_collection      = hashlib.md5(dx_caption.encode()) 
    dx_id_collection      = dx_id_collection.hexdigest() 

    if (type(dx_link_url) == type(None)):
        dx_link_url = "PrivateID"
    if(type(dx_id_collection) == type(None)):
        print("Account being stopped by Facebook xD")
        exit(1)

    sql = """
    SELECT id_collection from collect_facebook where id_collection='%s';
    """ % (dx_id_collection)

    conn    = dbt.get_db_conn()
    cursor  = conn.cursor()
    cursor.execute(sql)
    record  = cursor.fetchone()
    if (type(record) != type(None)):
        print("Data %s exists. Not inputing duplicate data" % (dx_id_collection))
        dbt.pconnection.putconn(conn)
    else:
        sql = """
        INSERT INTO collect_facebook(akun_name, url_fb, isi_url_fb, caption, waktu_crawl, tanggal_posting,
        num_share, num_coment, num_likes, hasil_emotion, data_komentar, id_collection)
        VALUES('%s', '%s', '%s', '%s', '%s', '%s', 
        '%s','%i', '%i', '%s', '%s', '%s');
        """ % (dx_id_name, dx_url_media, dx_url_link, dx_caption, dx_created_at, dx_post_created, 
        dx_num_share, dx_num_comment, dx_num_likes, dx_comment_emotionya, dx_account_comment, dx_id_collection
        )
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        dbt.pconnection.putconn(conn)
        print ("Insert DB %s finished" %(dx_id_collection))

exit(0)