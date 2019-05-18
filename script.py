import requests
from bs4 import BeautifulSoup
import re

content = requests.get('https://www.hotnewhiphop.com/songs/').content
soup = BeautifulSoup(content, "html.parser")

title = soup.select('.cover-title')[0].get_text().strip()
artists  = soup.select('.grid-item-artists')[0].get_text().strip()
artists = artists.replace('\xa0',' ')
songs = {}
songs[title] = artists
print(title)
print(artists)
print(songs)