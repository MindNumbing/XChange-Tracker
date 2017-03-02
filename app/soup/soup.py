from bs4 import BeautifulSoup
import urllib.request
from re import compile

filetype = '.pdf'

def CheckForDuplicates(Files):
    seen = set()
    for file in Files:
        if file in seen:
            print('Duplicate File : "%s"' % (file))
        else:
            seen.add(file)
    return seen

def MakeSoup(url):
    global filetype

    Website = urllib.request.urlopen(url)
    soup = BeautifulSoup(Website, "html.parser")

    Files = []
    for file in soup.findAll('a', href=compile(str(filetype))):
        Files.append(file['href'])

    Files = CheckForDuplicates(Files)

    return Files
