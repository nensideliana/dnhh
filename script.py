import requests
from bs4 import BeautifulSoup
import spotipy
import spotipy.util as util
import sys 
import json

#check for parameters
if len(sys.argv) != 4:
    print('Need 3 parameters: username, client id, client secret')
    sys.exit()
else:
    username = sys.argv[1]
    client_id = sys.argv[2]
    client_secret = sys.argv[3]

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
    songs[title] = artist

t = list(songs.keys())[0]
a = list(songs.values())[0]
print(t,a)

#get token to access spotify data
scope='playlist-modify-private'
token = util.prompt_for_user_token(username, scope,client_id=client_id,client_secret=client_secret,redirect_uri='http://localhost:8888/callback/')

tracks = []

if token:
    sp = spotipy.Spotify(auth=token)

    #create the playlist
    playlists = sp.user_playlist_create(username,'Daily New Hip Hop',public=False)
    playlist_id = playlists['id']
    
    #To check if playlist exists
    # user_playlists = sp.user_playlists(username)
    # print(user_playlists['items'][0]['name'])

    results = sp.search(q='track:' + t, type='track')
    item = results['tracks']['items'][0]

    search_title = item['name']
    print('title:',search_title)
    search_artist = item['artists'][0]['name']
    print('artist:',search_artist)
    search_id = item['id']
    print('id:',search_id)

    tracks.append(search_id)

    #add to playlist
    sp.user_playlist_add_tracks(username, playlist_id, tracks, position=None)

else:
    print("Can't get token for ", username)


# results = sp.search(q='Tyler the creator new magic', limit=20)
# for i, t in enumerate(results['tracks']['items']):
#     print(' ', i, t['name'])