#!/usr/bin/python3

from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import re

url = 'https://www.archlinux.org/'
html = urlopen(url).read()

soup = BeautifulSoup(html, 'lxml')

pacstrings = os.popen('pacman -Q').read().strip().split('\n')
packages = dict()
for pacstr in pacstrings:
    packages[pacstr.split(' ')[0]] = pacstr.split(' ')[1]

titles = []

name_replace_pattern = re.compile('(>=|\s).*')
version_replace_pattern = re.compile('[\w\d]+(>=| )([\d\.-]+).*')

news = soup.select_one('div#news')

for h4 in news.select('h4'):
    text = h4.select_one('a').text
    if not 'manual intervention' in text:
        continue
    package = name_replace_pattern.sub('', text)
    version = version_replace_pattern.sub(r'\2', text)
    if package not in packages:
        continue
    if version == packages[package]:
        continue 
    titles.append(package)

for title in titles:
    print(title)
