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
from dataCollection import dataCollection
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing
import pickle

class Model:
    def __init__(self):
        self.user_tracks = None
        self.unlistened = None
        self.knn = None

        self.__init_model()
    
    def __init_model(self):
        dt = pd.read_csv('../data/dt.csv')
        dt= dt.drop(columns= ['Unnamed: 0'])
        song_data = dt.drop(columns=['id','Track Name','Artist','Liked'])
        scaler = preprocessing.MinMaxScaler()
        names = song_data.columns
        dt[names] = scaler.fit_transform(dt[names])
        self.unlistened = dt.loc[dt['Liked']==0]
        self.user_tracks = dt.loc[dt['Liked']==1]
        song_data = self.unlistened.drop(columns=['id','Track Name','Artist','Liked'])   
        #training model
        self.knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=21, n_jobs=-1)
        self.knn.fit(song_data)

    def getPlaylist(self, song_names):
        self.__init_model()
        self.user_tracks = pd.read_csv('../data/UserTracks.csv')
        reval = pd.DataFrame()
        for song in song_names:
            metadata = self.user_tracks.loc[(self.user_tracks['Track Name'] == song) &(self.user_tracks['Artist'] == song_names[song])].drop(columns = ['id','Unnamed: 0','uri','Track Name','Artist','Liked'])
            
            metadata = sklearn.preprocessing.normalize(metadata, axis=1)
            distances , indices = self.knn.kneighbors(metadata,n_neighbors=21)
            indis = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1],reverse=True)[:0:-1]
            recommend_frame = []
            for index,distance in indis:
                recommend_frame.append({'Title':self.unlistened.iloc[index]['Track Name'],'Artist':self.unlistened.iloc[index]['Artist'], 'Id':self.unlistened.iloc[index]['id']})
            reccs = pd.DataFrame(recommend_frame)
            reval = reval.append(reccs)
        return reval.reset_index(drop=True)

if __name__ == "__main__":
    songrecs = {'':'Jaden'}

    #getting playlist
    m = Model()
    playlist = m.getPlaylist(songrecs)
    print(playlist)
    
