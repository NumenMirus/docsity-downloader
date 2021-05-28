from urllib3 import request


import requests
from os import path

def get_unblurred_url(url):
    temp = url.replace("documents_pages_blur", "documents_pages")
    return temp

def download_files(url, path):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        #print("Scaricando...")
        with open(path + local_filename, 'wb') as f:
            #print("Scrivendo i dati nel file...")
            for chunk in r.iter_content(chunk_size=2024):
                f.write(chunk)
    f.close()
    #print("Completato!")
    print("File salvato come: "+local_filename)

def blurred_parser(blurred):
    imgs = []
    for i in blurred:
        for j in i:
            temp = []
            cl = j.get_attribute("class")

            if cl == "dsy-page__image h0":
                link = (j.get_attribute("style"))
                link.replace('background-image: url("', '')
                link.replace('")', '')
                #link = link(23:-3)
                imgs.append(link)
                break
            else:
                images = j.find_elements_by_tag_name('img')
                for k in images:
                    temp.append(k.get_attribute("src"))
                    for l in temp:
                        if "documents_pages_blur" in l:
                            imgs.append(l)
                            break
                        else:
                            pass
    res = set(imgs)
    return res