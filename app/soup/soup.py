from bs4 import BeautifulSoup
from urllib.request import urlopen
from re import compile
from config import FILETYPE
from flask import flash
import urllib


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
    for file in soup.findAll('a'):
        current_file = file.get('href')
        if current_file.endswith('pdf'):
            print(current_file)
            files.append(current_file)

    files = check_for_duplicates(files)

    return files
