from os import path
import requests

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

url = input("\nInserisci il link dell'immagine sfocata: ")
path = input("Inserisci il percorso: ")

download_files(get_unblurred_url(url), path)