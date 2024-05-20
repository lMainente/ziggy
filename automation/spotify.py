import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = 'your id'
client_secret = 'your client secrte'

scope = "user-read-playback-state,user-modify-playback-state"
redirect_uri = "http://localhost:8080/callback"  # Dummy
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))
def play_track(track_name):
    results = sp.search(q=track_name, limit=1, type='track')
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        sp.start_playback(uris=[track_uri])
    else:
        print("Track not found.")

def play_playlist(playlist_name):
    results = sp.search(q=playlist_name, limit=1, type='playlist')
    if results['playlists']['items']:
        playlist_uri = results['playlists']['items'][0]['uri']
        sp.start_playback(context_uri=playlist_uri)
    else:
        print("Playlist not found.")

def pause():
    sp.pause_playback()

def resume():
    sp.start_playback()

def main():
    while True:
        action = input("What do you want to do? (play/pause/resume): ")
        if action.lower() == 'play':
            choice = input("Do you want to play a specific song or a playlist? (song/playlist): ")
            if choice.lower() == 'song':
                song_name = input("name of the song: ")
                play_track(song_name)
            elif choice.lower() == 'playlist':
                playlist_name = input("name of the playlist: ")
                play_playlist(playlist_name)
            else:
                print("error.")
        elif action.lower() == 'pause':
            pause()
        elif action.lower() == 'resume':
            resume()
        else:
            print("eror.")

main()