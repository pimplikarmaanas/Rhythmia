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

cid = '93386766d8f54f0fa5a8aebd30b14296'
secret = '6be032e5e0ed43c2bef1c9a82925ab6f'
red='http://localhost:7777/callback'
username = 'd0ngus'


scope = 'playlist-read-private'
token = util.prompt_for_user_token(username, scope=scope, client_id=cid, client_secret=secret, redirect_uri=red)

if token:
    sp = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)

results = sp.current_user_playlists(limit=50, offset=0)
print(results)


