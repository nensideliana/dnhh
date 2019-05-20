import requests
from bs4 import BeautifulSoup
import spotipy
import spotipy.util as util
import sys 
import datetime

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
    main_artist = artists_list[i].find('em').get_text().strip()
    songs[title] = [artist,main_artist]


#get token to access spotify data
scope='playlist-modify-private'
token = util.prompt_for_user_token(username, scope,client_id=client_id,client_secret=client_secret,redirect_uri='http://localhost:8888/callback/')

if token:
    sp = spotipy.Spotify(auth=token)

    #create the playlist
    dt = datetime.datetime.today()
    date = str(dt.year) + '/' + str(dt.month) + '/' + str(dt.day)
    playlists = sp.user_playlist_create(username,'DNHH '+ date,public=False)
    playlist_id = playlists['id']

    tracks = []

    #search for tracks in dictionary and add track id's to playlist
    for title in songs.keys():

        artist = songs[title][0]
        main_artist = songs[title][1]
        results = sp.search(q='track:' + title + ' ' + artist, type='track')

        #if there are search results
        if(any(results) and results['tracks']['total'] != 0):
          
            #get first result
            item = results['tracks']['items'][0]

            search_title = item['name']
            print('title:',search_title)
            search_artist = item['artists'][0]['name']
            print('artist:',search_artist)
            search_id = item['id']
            print('id:',search_id)

            tracks.append(search_id)
        
        #if no results try again with only the main artist
        else:
            results = sp.search(q='track:' + title + ' ' + main_artist, type='track')
            
            if(any(results) and results['tracks']['total'] != 0):
          
                #get first result
                item = results['tracks']['items'][0]

                search_title = item['name']
                print('title:',search_title)
                search_artist = item['artists'][0]['name']
                print('artist:',search_artist)
                search_id = item['id']
                print('id:',search_id)

                tracks.append(search_id)

    #add all songs to the playlist
    sp.user_playlist_add_tracks(username, playlist_id, tracks, position=None)

else:
    print("Can't get token for ", username)
