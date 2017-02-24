from bs4 import BeautifulSoup
import urllib.request
from re import compile
from DB import Controls

def CheckForDuplicates(Files):
    seen = set()

    for file in Files:
        if file not in seen:
            seen.add(file)
        #else:
            #print('Duplicate File : "%s"' % (file))
    return (seen)

def MakeSoup(url, filetype):
    Website = urllib.request.urlopen(url)
    soup = BeautifulSoup(Website, "html.parser")

    Files = []
    for file in soup.findAll('a', href=compile(str(filetype))):
        Files.append(file['href'])

    print(len(Files))
    return Files
