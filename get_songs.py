import requests
from bs4 import BeautifulSoup

#grab content to scrape
content = requests.get('https://www.hotnewhiphop.com/songs/').content
soup = BeautifulSoup(content, "html.parser")

#grab all title and artist tags
title_list = soup.select('.cover-title')
artists_list  = soup.select('.grid-item-artists')

#grab the text from these tags and put them in a dictionary in the form title:artist
songs = {}
for i in range(len(title_list)):
    title = title_list[i].get_text().strip()
    artist = artists_list[i].get_text().strip().replace('\xa0',' ')
    main_artist = artists_list[i].find('em').get_text().strip()
    songs[title] = [artist,main_artist]
