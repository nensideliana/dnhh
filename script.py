import requests
from bs4 import BeautifulSoup
import spotipy
import spotipy.util as util
import sys 

if len(sys.argv) != 4:
    print('Need 3 parameters: username, client id, client secret')
    exit(1)

username = sys.argv[1]
client_id = sys.argv[2]
client_secret = sys.argv[3]

content = requests.get('https://www.hotnewhiphop.com/songs/').content
soup = BeautifulSoup(content, "html.parser")

title_list = soup.select('.cover-title')
artists_list  = soup.select('.grid-item-artists')
songs = {}

for i in range(len(title_list)):
    title = title_list[i].get_text().strip()
    artist = artists_list[i].get_text().strip().replace('\xa0',' ')
    songs[title] = artist

t = list(songs.keys())[0]
a = list(songs.values())[0]
print(t,a)

scope='playlist-modify-private'
token = util.prompt_for_user_token(username, scope,client_id=client_id,client_secret=client_secret,redirect_uri='http://localhost:8888/callback/')
if token:
    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlist_create('nensideliana','Daily New Hip Hop',public=False)
else:
    print("Can't get token for ", username)


# results = sp.search(q='Tyler the creator new magic', limit=20)
# for i, t in enumerate(results['tracks']['items']):
#     print(' ', i, t['name'])