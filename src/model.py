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

global user_tracks
global unlistened 

def getPlaylist(song_names):
    reval = pd.DataFrame()
    for song in song_names:
        metadata = user_tracks.loc[(user_tracks['Track Name'] == song) &(user_tracks['Artist'] == song_names[song])].drop(columns = ['id','Track Name','Artist','Liked'])
        metadata =sklearn.preprocessing.normalize(metadata, axis=1)
        distances , indices = knn.kneighbors(metadata,n_neighbors=21)
        indis = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1],reverse=True)[:0:-1]
        recommend_frame = []
        for index,distance in indis:
            recommend_frame.append({'Title':unlistened.iloc[index]['Track Name'],'Artist':unlistened.iloc[index]['Artist']})
        reccs = pd.DataFrame(recommend_frame)
        reval = reval.append(reccs)
    return reval.reset_index(drop=True)


if __name__ == "__main__":
    dt = pd.read_csv('../data/dt.csv')
    dt= dt.drop(columns= ['Unnamed: 0'])
    song_data = dt.drop(columns=['id','Track Name','Artist','Liked'])
    scaler = preprocessing.MinMaxScaler()
    names = song_data.columns
    dt[names] = scaler.fit_transform(dt[names])
    unlistened = dt.loc[dt['Liked']==0]
    user_tracks = dt.loc[dt['Liked']==1]
    song_data = unlistened.drop(columns=['id','Track Name','Artist','Liked'])   
    #training model
    knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=21, n_jobs=-1)
    knn.fit(song_data)

    songrecs = {'Ditto':'NewJeans'}

    #getting playlist
    playlist = getPlaylist(songrecs)
    print(playlist)
    
