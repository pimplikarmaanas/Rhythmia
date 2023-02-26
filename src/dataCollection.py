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

class dataCollection:

    def __init__(self):
        self.token = None

        # call main
        self.main()

    def __str__(self):
        print(self.token, " ", self.user_tracks, " ", self.spotify_tracks)

    def main(self):
        cid = '93386766d8f54f0fa5a8aebd30b14296'
        secret = '6be032e5e0ed43c2bef1c9a82925ab6f'
        red='http://localhost:7777/callback'
        username = 'd0ngus'
        scope = 'playlist-read-private'
        self.token = SpotifyOAuth(username= username, scope=scope, client_id =cid, client_secret=secret, redirect_uri=red)

        if self.token:
            self.sp = spotipy.Spotify(auth_manager= self.token)
        else:
            print("Can't get self.token for", username)

        results = self.sp.current_user_playlists(limit=50, offset=0)
        playlists = []
        for i in  range (len(results['items'])):
            playlists.append(results['items'][i]['id'])
        self.user_tracks = pd.DataFrame(self.playlist_to_dataframe(playlists,1), columns = ['id', 'Track Name','Artist','Acousticness','Daceability','Energy','Instrumentalness','Liveness','Loudness','Speechiness','Tempo','Time Signature','Liked'])
        self.user_tracks = self.user_tracks.drop_duplicates(subset=['Track Name', 'Artist'], keep='first')
        #songs from user 
        self.user_tracks = self.user_tracks.reset_index(drop=True)
        self.user_tracks.to_csv('UserTracks.csv')
    
        
        splay = self.sp.user_playlists('spotify')
        slst = []
        for i in range (len(splay['items'])):
            slst.append(splay['items'][i]['id'])

        # songs from spotify
        self.spotify_tracks = pd.DataFrame(self.playlist_to_dataframe(slst,0), columns = ['id', 'Track Name','Artist','Acousticness','Daceability','Energy','Instrumentalness','Liveness','Loudness','Speechiness','Tempo','Time Signature','Liked'])
        frames = [self.user_tracks,self.spotify_tracks]
        dt = pd.concat(frames)
        dt = dt.drop_duplicates(subset=['Track Name', 'Artist'], keep='first')
        dt = dt.reset_index(drop=True)
        dt.to_csv('dt.csv')
        self.spotify_tracks.to_csv('SpotifyTracks.csv')

    def playlist_to_dataframe(self, playlist_id_list,liked):
        data = [] 
        current_track = []
        for item in playlist_id_list:
            songs= self.sp.playlist_items(item, fields=None, limit=100, offset=0, market=None, additional_types=('track', 'episode'))
            for i in range(0,len(songs['items'])):
                if(songs['items'][i]['track'] is not None):
                    features = self.sp.audio_features(songs['items'][i]['track']['id'])
                    if(features[0] is not None):
                        current_track =[songs['items'][i]['track']['id'],songs['items'][i]['track']['name'],songs['items'][i]['track']['artists'][0]['name']]
                        feature_list = [features[0]['acousticness'],features[0]['danceability'],features[0]['energy'],features[0]['instrumentalness'],features[0]['liveness'],features[0]['loudness'],features[0]['speechiness'],features[0]['tempo'],features[0]['time_signature'],liked]
                        current_track = current_track+feature_list
                        data.append(current_track)
        return data
