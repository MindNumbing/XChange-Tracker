from bs4 import BeautifulSoup
from urllib.request import urlopen
from re import compile
from config import FILETYPE
from flask import flash


def check_for_duplicates(files):
    seen = set()
    for file in files:
        if file not in seen:
            seen.add(file)
    return seen


def make_soup(url):
    try:
        website = urlopen(url)
    except ValueError:
        flash('Invalid URL', 'danger')
        return

    soup = BeautifulSoup(website, "html.parser")

    files = []
    for file in soup.findAll('a', href=compile(str(FILETYPE))):
        files.append(file['href'])

    if files == []:
        flash('No files found on provided website', 'info')
        return

    files = check_for_duplicates(files)

    return files
