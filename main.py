from os import path
import requests
import image_finder as im

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

def get_unblurred_url(url):
    temp = url.replace("documents_pages_blur", "documents_pages")
    return temp


print("Benvenuto! Sei qui per aggirare la censura eh?")

n = int(input("\nCosa vuoi fare?\n1) Scaricare tutte le immagini sfocate dalla pagina\n2) Scaricare una sola immagine sfocata\n"))

if n == 1:
    url = input("\nInserisci il link della pagina: ")
    path = input("Inserisci il percorso: ")
    images = im.find_images(url)
    blurred = im.image_parser(images)

    print(images)
    print(blurred)

elif n == 2:
    url = input("\nInserisci il link dell'immagine sfocata: ")
    path = input("Inserisci il percorso: ")

    download_files(get_unblurred_url(url), path)