import sys
import spotipy
import spotipy.util as util
import pandas as pd

scope = 'user-library-read'

# export SPOTIPY_CLIENT_ID ='c4bfe10bf6304a8ba3e075e878ec5ddf'
# export SPOTIPY_CLIENT_SECRET='0da11797bf604e32b624cf82cea5600a'
# export SPOTIPY_REDIRECT_URI='SpotifyData://returntoapp'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username, scope, client_id='c4bfe10bf6304a8ba3e075e878ec5ddf',client_secret='0da11797bf604e32b624cf82cea5600a',redirect_uri='SpotifyData://returntoapp')

sp = spotipy.Spotify(auth = token)
playlists = sp.featured_playlists()
# playlists = sp.user_playlists(username)
# playlistName = playlists['playlists']['items'][1]['id']

# # playlist = playlists['items'][0]['id']
# results = sp.search(q=query, limit=limit, type='playlist')
stuff = []
for playlist in playlists['playlists']['items']:
    # results = sp.user_playlist(playlist['owner']['id'], playlist['id'], fields="tracks,next")
    results = sp.user_playlist(playlist['owner']['id'], playlist['id'])
    playlistInfo = [results['name']]
    playlistInfo.append(results['followers']['total'])
    playlistInfo.append(len(results['tracks']['items']))
    averageSongPopularity = 0
    howExplicit = 0
    averageSongLength = 0
    artists = []
    for track in results['tracks']['items']:
        averageSongPopularity += float(track['track']['popularity'])/float(len(results['tracks']['items']))
        howExplicit += float(track['track']['explicit'])/float(len(results['tracks']['items']))
        averageSongLength += float(track['track']['duration_ms'])/float(len(results['tracks']['items']))
        artists.append(track['track']['album']['artists'][0]['name'])
    print artists
    playlistInfo.append(averageSongPopularity)
    playlistInfo.append(howExplicit)
    playlistInfo.append(averageSongLength)
    playlistInfo.append(artists)
    stuff.append(playlistInfo)
    DataFrame = pd.DataFrame(stuff)
    DataFrame.columns = ['Name', 'Followers', 'NumTracks', 'Avg Song Pop', 'Explicitness', 'Avg Song Len', 'Artist']
    DataFrame.to_csv('SpotifyData')
