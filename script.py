import requests
from bs4 import BeautifulSoup
import re

content = requests.get('https://www.hotnewhiphop.com/songs/').content
soup = BeautifulSoup(content, "html.parser")

title_list = soup.select('.cover-title')
artists_list  = soup.select('.grid-item-artists')
songs = {}
for i in range(len(title_list)):
    title = title_list[i].get_text().strip()
    artist = artists_list[i].get_text().strip().replace('\xa0',' ')
    songs[title] = artist

print(songs)