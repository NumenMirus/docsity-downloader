from urllib3 import request
from tqdm import tqdm
import requests
from os import path

#get the link to the unblurred image
def _get_unblurred_url(url):
    t = str(type(url))
    #check if url is a list or a single element
    if t == "<class 'list'>":
        res = []
        for i in url:
            temp = i.replace("documents_pages_blur", "documents_pages")
            res.append(temp)
    else:
        res = url.replace("documents_pages_blur", "documents_pages")
    return res

#downloads the image to the specified path
def download_files(url, path):
        #filename is equal to the image name in the link
        local_filename = url.split('/')[-1]
        with requests.get(url, stream=True) as r:
            #print("Scaricando...")
            with open(path + local_filename, 'wb') as f:
                #print("Scrivendo i dati nel file...")
                for chunk in r.iter_content(chunk_size=2024):
                    f.write(chunk)
        f.close()
        #print("Completato!")
        #print("File salvato come: "+local_filename)

#extract the link to the blurred images, return alist of unblurred images links
def blurred_parser(blurred):
    imgs = []
    print("saving files...")
    for i in tqdm(blurred):
        #filename is equal to the image name in the link
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

#extract the link to the blurred images, return alist of unblurred images links
def blurred_parser(blurred):
    imgs = []
    print("\nparsing blurred images...")
    for i in tqdm(blurred):
        #cicles trough all the elements of the list blurred[]
        for j in i:
            temp = []
            cl = j.get_attribute("class") #cl becomes the class name of the element

            #filter the other tu sub-types of blurring
            if cl == "dsy-page__image h0":
                link = (j.get_attribute("style"))
                link = link[23:-3]
                imgs.append(link)
                break
            else:
                images = j.find_elements_by_tag_name('img') #extracts image tag lines
                for k in images:
                    temp.append(k.get_attribute("src"))
                for l in temp:
                    if "documents_pages_blur" in l:
                        imgs.append(l)
                        break
                    else:
                        pass

    temp = _get_unblurred_url(imgs)
    print(temp)
    #res = set(temp) #used to transform th list in a set to remove duplicates, now solved
    return temp

def covered_parser(covered):
    pass