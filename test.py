url = "https://www.docsity.com/it/letteratura-inglese-la-fiaba-letteraria-inglese/2642957/"

from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from parsers import blurred_parser

driver = webdriver.Chrome("/home/numen/Desktop/progetti/docsity-downloader/chromedriver")

driver.get(url)
print(driver.title)

time.sleep(2)

cookie = driver.find_element_by_id("CybotCookiebotDialogBodyButtonAccept")
cookie.click()
time.sleep(1)

button = driver.find_element_by_link_text("VEDI L'ANTEPRIMA")
button.click()

time.sleep(2)

print("scrolling...")
html = driver.find_element_by_tag_name('html')
html.click()
for i in range(50):
    html.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5)


time.sleep(2)

print("parsing...")
wrappers = driver.find_elements_by_class_name("dsy-page__wrapper")

links = []
for i in wrappers:
    links.append(i.find_elements_by_tag_name("div"))

print("links: %d" %len(links))

blurred = []
covered = []
glass = []
free = []
for i in links:
    for j in i:
        temp = j.get_attribute('class')
    
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

print("blurred: %d\tcovered: %d\tglass: %d\tfree: %d" %(len(blurred), len(covered), len(glass), len(free)))

#------------------------------------------------------------------------------
#----------------------------ANALIZING RESULTS---------------------------------
#------------------------------------------------------------------------------

print(blurred_parser(blurred))

#print(blurred)
#print(covered)
#print(glass)
#print(free)

driver.quit()