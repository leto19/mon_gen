import html2text
from bs4 import BeautifulSoup,SoupStrainer
import requests
import os

def get_monster(url = "http://5e.d20srd.org/srd/monsters/dragonsMetallic.htm"):
    
    if requests.get(url).status_code == 404:
        print("page not found, trying non 5e")
        url = url.replace("5e.","")
        print(url)
    content = requests.get(url).text
    title = url.split("/")[-1].replace(".htm","")
    content = content.split('<div class="footer">')[0]
    letter_index = title[0].upper()
    formatted_content = content.split("<h1>")[1:]
    #print(formatted_content)
    for entry in formatted_content:
        if len(entry) >= 10:
            #print(entry)
            soup2 = BeautifulSoup(entry,"lxml")
            
            if not os.path.exists('monsters/%s' % letter_index):
                os.makedirs('monsters/%s' % letter_index)

            with open("monsters/%s/%s.html" % (letter_index,title),"a+") as f:
                f.write(soup2.prettify())
        
def process_list():
    monster_page_url = "http://5e.d20srd.org/indexes/monsters.htm"
    monster_list_content = requests.get(monster_page_url).text
    monster_list_content = monster_list_content.split('<h2><a href="/srd/monsters/intro.htm">Introduction (Reading the Entries)</a></h2>')[1]
    monster_list_content = monster_list_content.split('<div class="footer">')[0]
    soup = BeautifulSoup(monster_list_content,"lxml",parse_only=SoupStrainer("a"))
    rel_link_list = list()
    for link in soup:
        if link.has_attr('href'):
            print(link)
            rel_link = link['href']
            rel_link = rel_link.replace("spectre","specter")
            striped_rel_link = rel_link.split("#")
            print(striped_rel_link)
            if striped_rel_link[0] not in rel_link_list:
                print("Processing %s"% rel_link)
                get_monster("http://5e.d20srd.org%s"% rel_link)
                rel_link_list.append(rel_link)
process_list()
