import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

test_playlist = '3PZikEpiKbaFO2fnXCdGYk'
yeehaw = '1vM6RlrdwaMBD57SEXByU2'

playlist = []

tracklist = sp.playlist_items(test_playlist)
for t in tracklist['items']:
    track = {}
    track['name'] = t['track']['name']
    track['artists'] = [a['name'] for a in t['track']['artists']]
    track['id'] = t['track']['id']
    track['added'] = t['added_at']
    playlist.append(track)

with open("test_playlist.json", "w") as out_file:
    json.dump(playlist, out_file, indent = 2)