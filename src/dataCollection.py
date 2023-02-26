import sys
import requests
import json
import os
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import oauth2
import pandas as pd
import numpy as np
import sklearn
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors


def playlist_to_dataframe(playlist_id_list,liked):
    data = [] 
    current_track = []
    for item in playlist_id_list:
        songs= sp.playlist_items(item, fields=None, limit=100, offset=0, market=None, additional_types=('track', 'episode'))
        for i in range(0,len(songs['items'])):
            if(songs['items'][i]['track'] is not None):
                features = sp.audio_features(songs['items'][i]['track']['id'])
                if(features[0] is not None):
                    current_track =[songs['items'][i]['track']['id'],songs['items'][i]['track']['name'],songs['items'][i]['track']['artists'][0]['name']]
                    feature_list = [features[0]['acousticness'],features[0]['danceability'],features[0]['energy'],features[0]['instrumentalness'],features[0]['liveness'],features[0]['loudness'],features[0]['speechiness'],features[0]['tempo'],features[0]['time_signature'],liked]
                    current_track = current_track+feature_list
                    data.append(current_track)
    return data




if __name__ == '__main__':
    
    cid = '93386766d8f54f0fa5a8aebd30b14296'
    secret = '6be032e5e0ed43c2bef1c9a82925ab6f'
    red='http://localhost:7777/callback'
    username = 'd0ngus'
    scope = 'playlist-read-private'
    token = SpotifyOAuth(username= username, scope=scope, client_id =cid, client_secret=secret, redirect_uri=red)

    if token:
        sp = spotipy.Spotify(auth_manager= token)
    else:
        print("Can't get token for", username)

    results = sp.current_user_playlists(limit=50, offset=0)
    playlists = []
    for i in  range (len(results['items'])):
        playlists.append(results['items'][i]['id'])
    user_tracks = pd.DataFrame(playlist_to_dataframe(playlists,1), columns = ['id', 'Track Name','Artist','Acousticness','Daceability','Energy','Instrumentalness','Liveness','Loudness','Speechiness','Tempo','Time Signature','Liked'])
    user_tracks = user_tracks.drop_duplicates(subset=['Track Name', 'Artist'], keep='first')
    #songs from user 
    user_tracks = user_tracks.reset_index(drop=True)
    user_tracks.to_csv('UserTracks.csv')
   

    splay = sp.user_playlists('spotify')
    slst = []
    for i in range (5):
        slst.append(splay['items'][i]['id'])

    # songs from spotify
    spotify_tracks = pd.DataFrame(playlist_to_dataframe(slst,0), columns = ['id', 'Track Name','Artist','Acousticness','Daceability','Energy','Instrumentalness','Liveness','Loudness','Speechiness','Tempo','Time Signature','Liked'])

    spotify_tracks.to_csv('SpotifyTracks.csv')





