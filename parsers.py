from urllib3 import request
from tqdm import tqdm


import requests
from os import path

def _get_unblurred_url(url):
    t = str(type(url))
    if t == "<class 'list'>":
        res = []
        for i in url:
            temp = i.replace("documents_pages_blur", "documents_pages")
            res.append(temp)
    else:
        res = url.replace("documents_pages_blur", "documents_pages")
    return res

def download_files(url, path):
    print("saving files...")
    for i in tqdm(url):
        local_filename = i.split('/')[-1]
        with requests.get(i, stream=True) as r:
            #print("Scaricando...")
            with open(path + local_filename, 'wb') as f:
                #print("Scrivendo i dati nel file...")
                for chunk in r.iter_content(chunk_size=2024):
                    f.write(chunk)
        f.close()
        #print("Completato!")
        #print("File salvato come: "+local_filename)

def blurred_parser(blurred):
    imgs = []
    print("\nparsing blurred images...")
    for i in tqdm(blurred):
        for j in i:
            temp = []
            cl = j.get_attribute("class")

            if cl == "dsy-page__image h0":
                link = (j.get_attribute("style"))
                link = link[23:-3]
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

    temp = _get_unblurred_url(imgs)
    res = set(temp)
    return res