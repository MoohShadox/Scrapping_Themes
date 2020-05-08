from threading import Thread

import requests
from bs4 import BeautifulSoup
import re



def search_google(word):
    q = word
    req = "" \
              "https://www.google.com/search?sxsrf=ALeKk00qvKIIlXBzy_WC_Kz0EjwMovhgQw%3A1586432749774&source=hp&ei=7QqPXv3CLeKZlwTLjL_ACA&q="+q+"&oq=a&gs_lcp=CgZwc3ktYWIQARgAMgQIIxAnMgQIIxAnMgQIIxAnMgQIABBDMgQIABBDMgQIABBDMgUIABCDATIFCAAQgwEyAggAMgIIAEoICBcSBDBnNTdKBwgYEgMwZzFQhQ5YhQ5goxZoAXAAeACAAS6IAS6SAQExmAEAoAEBqgEHZ3dzLXdpeg&sclient=psy-ab"
    r = requests.get(req)
    soupe = BeautifulSoup(r.content,'html.parser')
    #print(soupe.prettify())
    L = soupe.find_all("a")
    Ret = []

    for i in L:
        #print(i["href"])
        S = i["href"].replace("%25C3%25A9",'é').replace("%25C3%25A8","è").replace("%2527","'").replace("%23"," ")
        if(len(re.findall("/url\?q=(https://fr.wikipedia.org/wiki/(.+?))&",S)) > 0):
            #print(re.findall("/url\?q=(https://fr.wikipedia.org/wiki/(.+?))&",S)[0])
            Ret = re.findall("/url\?q=(https://fr.wikipedia.org/wiki/(.+?))&",S)[0]
            break
    return Ret




def get_Portails(page_wikipedia):
    r = requests.get(page_wikipedia)
    soupe = BeautifulSoup(r.content,'html.parser')
    L = soupe.find_all("a")
    Ret = set()
    for i in L:
        if(i.get('href') != None):
            S = i.get('href').replace("%25C3%25A9",'é').replace("%25C3%25A8","è").replace("%2527","'").replace("%23"," ")\
                .replace("%C3%A9","é").\
                replace("%C3%82","Â").replace("%C3%A8","è").replace("%C3%A2","â").\
                replace("%C3%AF","ï").replace("%C3%8E","Î").replace("%C3%AA","ê").replace("%27","'").replace("%C3%89","É").replace("%C3%A7","ç")
            R = re.findall("/wiki/Portail:(.+)",S)
            if(len(R)>0 and str(R[0]) != "Accueil"):
                Ret.add(str(R[0]))
    return Ret





