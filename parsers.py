from urllib3 import request
from tqdm import tqdm
import requests
from os import path
import pypandoc
import time

nome_file = 0

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
def download_files(urls, path):
    global nome_file
    for url in urls:
        #filename is equal to the image name in the link
        with requests.get(url, stream=True) as r:
            #print("Scaricando...")
            with open(path + (str(nome_file)+url[-1:-5]), 'wb') as f:
                #print("Scrivendo i dati nel file...")
                for chunk in r.iter_content(chunk_size=2024):
                    f.write(chunk)
        f.close()
        nome_file += 1
        #print("Completato!")
        #print("File salvato come: "+(str(nome_file)+url[-1:-5]))

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
        time.sleep(0.5)

    temp = _get_unblurred_url(imgs)
    #res = set(temp) #used to transform the list in a set to remove duplicates, now solved
    return temp

def covered_parser(covered, path):
    global nome_file
    temp = []
    new = []
    for i in covered:
        for j in i:
            #gets all the starting point of .docx file from html
            if j.get_attribute("class") == "pf w0 h0":
                new.append(j)
                break
    
    print("grabbing covered PDFs..")
    n = 0
    for i in tqdm(new):
        #convert html to .docx and save it
        s = i.get_attribute('innerHTML')
        full_path = path + str(nome_file) + '.docx'
        docx = pypandoc.convert(source=s, format='html', to='docx', outputfile=full_path, extra_args=['-RTS'])
        nome_file += 1
        time.sleep(0.5)
    
def free_parser(free, path):
    global nome_file
    temp = []
    new = []
    for i in free:
        for j in i:
            #gets all the starting point of .docx file from html
            if j.get_attribute("class") == "pf w0 h0":
                new.append(j)
                break
    
    print("grabbing free PDFs..")
    for i in tqdm(new):
        #convert html to .docx and save it
        s = i.get_attribute('innerHTML')
        full_path = path + str(nome_file) + '.docx'
        docx = pypandoc.convert(source=s, format='html', to='docx', outputfile=full_path, extra_args=['-RTS'])
        nome_file += 1
        time.sleep(0.5)