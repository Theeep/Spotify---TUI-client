import os
from blessed import Terminal
from verbs import Verbs
from ui import TUI
import urls
import spotipy
import spotipy.util as util
from localSecret import CLIENT_ID,CLIENT_SECRET
client_id = CLIENT_ID
client_secret = CLIENT_SECRET 
redirect_uri=   "https://localhost/fake2718:8080"

username = USERNAME
scopesList = ['user-read-currently-playing'
             ,'user-modify-playback-state'
             ,'user-read-playback-state']
scopes = ' '.join(scopesList)
token = util.prompt_for_user_token(username,scopes,client_id,client_secret,redirect_uri,show_dialog=True)

#Blessed initalization
term = Terminal()
reqVerbs = Verbs(token)
tui = TUI(term,reqVerbs)



def getCurrSongNameArtist(json):
    song = json['item']['name']
    artists = [elem['name'] for elem in json['item']['artists']]
    artists = '/'.join(artists)
    songInfo = "{} - {}".format(song,artists) 
    return songInfo




while(True):
    cpJson   = reqVerbs.getRequest(urls.currPlayingURL)
    songInfo = getCurrSongNameArtist(cpJson)
    tui.displayUI(songInfo)
