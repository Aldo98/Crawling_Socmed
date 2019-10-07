import requests 
import json
import base64

#import anagojsono
from .anagojsono import jsonkansaja


API_ENDPOINT = ["https://apiserver.nergrit.addnotes.id/api/syncnerb64/",
                "https://apiserver3.nergrit.addnotes.id/api/emot_anlzb64/"]
  
 
teks = 'Jokowi pergi ke pasar, dan dia pergi bersama bapak nya ke suatu tempat di Jakarta'

def get_ner(teks):
    teks = str(base64.b64encode(teks.encode("utf-8")), "utf-8")

    # data to be sent to api 
    datax = {
    "b64text": teks
    }

    # sending post request and saving response as response object 
    hasil = requests.post(url = API_ENDPOINT[0], data = json.dumps(datax))
    
    # extracting response text 
    hasils = hasil.text

    dicth = json.loads(hasils)
    dictx = dicth["NER"]["entities"]
    dictx = json.dumps(dictx)
    strdictx = str(dictx)
    del(dicth)
    del(dictx)
    strdictx = strdictx.replace("[", "")
    strdictx = strdictx.replace("]", "")
    dictx = json.dumps(strdictx)
    hass = jsonkansaja(dictx)
    # print (hass, "\n\n")
    return(json.loads(hass))

def get_emot(teks):
    teks = str(base64.b64encode(teks.encode("utf-8")), "utf-8")

    # data to be sent to api 
    datax = {
    "b64text": teks
    }

    # sending post request and saving response as response object 
    hasil = requests.post(url = API_ENDPOINT[1], data = json.dumps(datax))
    
    # extracting response text 
    hasils = hasil.text
    dicth = json.loads(hasils)
    dictx = dicth["EAN"]
    return(dictx)

#print(get_emot(teks))
# hasil = get_ner(teks)
# print(hasils)
# print(type(hasils))

# dicth = json.loads(hasil)
# dictx = dicth["NER"]["entities"]
# dictx = json.dumps(dictx)
# strdictx = str(dictx)
# del(dicth)
# del(dictx)
# strdictx = strdictx.replace("[", "")
# strdictx = strdictx.replace("]", "")
# dictx = json.dumps(strdictx)
# print(hasil)
