import requests
from bs4 import BeautifulSoup

content = requests.get('https://www.hotnewhiphop.com/songs/').content
soup = BeautifulSoup(content, "html.parser")

print(soup.div)