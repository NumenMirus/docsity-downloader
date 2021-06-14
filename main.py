from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from parsers import blurred_parser, covered_parser, download_files, free_parser
from os import path
import requests
from tqdm import tqdm

#url = "https://www.docsity.com/en/analisi-la-luppa-di-giovanni-verga/2690000/"

#------------------------------------------------------------------------------
#-------------------------------GUI--------------------------------------------
#------------------------------------------------------------------------------

print("╔═══╗        ╔═══╗   ╔╗            ╔╗              ╔╗            ╔╗       ")
print("╚╗╔╗║        ║╔═╗║  ╔╝╚╗           ║║              ║║            ║║       ")
print(" ║║║║╔══╗╔══╗║╚══╗╔╗╚╗╔╝╔╗ ╔╗    ╔═╝║╔══╗╔╗╔╗╔╗╔═╗ ║║ ╔══╗╔══╗ ╔═╝║╔══╗╔═╗")
print(" ║║║║║╔╗║║╔═╝╚══╗║╠╣ ║║ ║║ ║║    ║╔╗║║╔╗║║╚╝╚╝║║╔╗╗║║ ║╔╗║╚ ╗║ ║╔╗║║╔╗║║╔╝")
print("╔╝╚╝║║╚╝║║╚═╗║╚═╝║║║ ║╚╗║╚═╝║    ║╚╝║║╚╝║╚╗╔╗╔╝║║║║║╚╗║╚╝║║╚╝╚╗║╚╝║║║═╣║║ ")
print("╚═══╝╚══╝╚══╝╚═══╝╚╝ ╚═╝╚═╗╔╝    ╚══╝╚══╝ ╚╝╚╝ ╚╝╚╝╚═╝╚══╝╚═══╝╚══╝╚══╝╚╝ ")
print("                        ╔═╝║                                              ")
print("                        ╚══╝                                              ")

print("\nBenvenuto! Sei qui per aggirare la censura eh?")

n = int(input("\nCosa vuoi fare?\n1) Scaricare tutte le immagini sfocate dalla pagina\n2) Scaricare una sola immagine sfocata\n\n"))

if n == 1:
    url = input("\nInserisci il link della pagina: ") 
    path = input("Inserisci il percorso: ")
    pagine = int(input("Quante pagine ha il documento?  "))

    if '/en/' in url:
            url = url.replace('/en/', '/it/')
    
    if 'desktop' in path:
        path = path.replace('desktop', 'Desktop')
    if path[-1] != '/':
        path = path + '/'

elif n == 2:
    url = input("\nInserisci il link dell'immagine sfocata: ")
    path = input("Inserisci il percorso: ")

    
#------------------------------------------------------------------------------
#----------------------------FETCHING IMAGES-----------------------------------
#------------------------------------------------------------------------------

#sets the driver to chrome
driver = webdriver.Chrome("./chromedriver")

#opens website from url
driver.get(url)
print(driver.title)

time.sleep(2)

#find and accepts cookies
cookie = driver.find_element_by_id("CybotCookiebotDialogBodyButtonAccept")
cookie.click()
time.sleep(1)

#open the document preview
button = driver.find_element_by_link_text("VEDI L'ANTEPRIMA")
button.click()

time.sleep(2)

#scroll the page to load all the images
print("scrolling...")
html = driver.find_element_by_tag_name('html')
html.click()

#find how much to scroll based on number of pages
#pag = driver.find_element_by_class_name("dsy-heading dsy-heading--muted dsy-heading--uppercase dsy-heading--center dsy-heading--tiny")
#num = pag.text
for i in tqdm(range(pagine*2)):
    html.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5)

time.sleep(2)

#extract all page wrappers
print("\nparsing...")
wrappers = driver.find_elements_by_class_name("dsy-page__wrapper")

#extract all <div> from page wrapper
divs = []
for i in wrappers:
    divs.append(i.find_elements_by_tag_name("div"))

#print("links: %d" %len(divs))

#filter all categories of censorship
blurred = []
covered = []
free = []
#divis is a list of lists, and tqdm is the progressbar
for i in tqdm(divs):
    #j becomes every element of i (sublist of divs[])
    for j in i:
        temp = j.get_attribute('class')
    
        #filtering based on the class name
        if temp == "dsy-page__content dsy-page__content--blur_be":
            blurred.append(i)
            break
        elif temp == "dsy-page__content dsy-page__content--free":
            free.append(i)
            break
        elif temp == "dsy-page__content dsy-page__content--blur_fe":
            covered.append(i)
            break
        else:
            pass

#print useful informaton
print("\nTOTAL: %d\tblurred: %d\tcovered: %d\tfree: %d" %(len(divs), len(blurred), len(covered), len(free)))

#------------------------------------------------------------------------------
#----------------------------ANALIZING RESULTS---------------------------------
#------------------------------------------------------------------------------

result = blurred_parser(blurred)
download_files(result, path)
covered_parser(covered, path)
free_parser(free, path)

#------------------------------------------------------------------------------
#--------------------------DOWNLOADING RESULTS---------------------------------
#------------------------------------------------------------------------------

#download_files(result, path)

#print(blurred)
#print(covered)
#print(glass)
#print(free)

driver.quit()