from bs4 import BeautifulSoup
from urllib3 import request
from tqdm import tqdm
import requests
from os import path
import pypandoc
import time
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import  mm

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
            with open(path + ((str(nome_file)+'.png')+url[-1:-5]), 'wb') as f:
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
    
    print("\ngrabbing covered PDFs..")
    n = 0
    # for i in tqdm(new):
        #convert html to .docx and save it
        # s = i.get_attribute('innerHTML')
        # full_path = path + str(nome_file) + '.docx'
        # docx = pypandoc.convert(source=s, format='html', to='docx', outputfile=full_path, extra_args=['-RTS'])
        # nome_file += 1
        # time.sleep(0.5)

    for i in tqdm(new):
        PDF_parser(i, path)

    
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
    
    print("\ngrabbing free PDFs..")
    # for i in tqdm(new):
    #     #convert html to .docx and save it
    #     s = i.get_attribute('innerHTML')
    #     full_path = path + str(nome_file) + '.docx'
    #     docx = pypandoc.convert(source=s, format='html', to='docx', outputfile=full_path, extra_args=['-RTS'])
    #     nome_file += 1
    #     time.sleep(0.5)
    for i in tqdm(new):
        PDF_parser(i, path)

def add_title(doc, text):
    doc.append(Spacer(1, 1.5))
    doc.append(Paragraph(text, ParagraphStyle(name="titolo",fontName="Helvetica-Bold",fontSize=16,alignment=TA_CENTER)))
    doc.append(Spacer(1, 20))

    return doc

def add_paragraph(doc, text):
    doc.append(Paragraph(text, ParagraphStyle(name="corpo", fontName="Helvetica",fontSize=12,alignment=TA_JUSTIFY)))
    doc.append(Spacer(1, 1.5))

    return doc

def PDF_parser(element, path):
    global nome_file
    soup = BeautifulSoup(element.get_attribute('innerHTML'), features='lxml')
    paragraphs = soup.find_all('div')

    document = []
    for p in paragraphs:
        stile = p.attrs['class']
        if stile[0] == 'pi':
            pass
        elif stile[3] == 'h1':
            add_title(document, p.text)
        elif 'pc' not in stile:
            add_paragraph(document, p.text)

    SimpleDocTemplate((path + str(nome_file)), pagesize=A4, rightMargin=2*mm, leftMargin=20*mm, topMargin=18*mm, bottomMargin=2*mm).build(document)
    nome_file += 1
    