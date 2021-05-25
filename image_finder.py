from bs4 import BeautifulSoup
import urllib
import re

def find_images(url):
    html_page = urllib.requests.urlopen(url)
    soup = BeautifulSoup(html_page)
    images = []
    for img in soup.findAll('img'):
        images.append(img.get('src'))

    return images

def image_parser(images):
    new = []
    for link in images:
        if link.find("documents_pages_blur"):
            new.append(link)
    
    return new
