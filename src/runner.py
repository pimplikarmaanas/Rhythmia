import math
import pandas as pd
import time
from collections import deque
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import tkinter as tk
from PIL import ImageTk, Image

song_queues, df = {}, None
root, song_label, current_heartrate = None, None, None
sp, player = None, None
index = 0

def initialize():
    global sp, player, df

    df = pd.read_csv("../data/UserTracks.csv", header=0)

    for index, row in df.iterrows():
        tempo = math.floor(row['Tempo']/10) * 10

        if tempo not in song_queues:
            song_queues[tempo] = deque()
        song_queues[tempo].append((row['Track Name'], row['id']))

    df = pd.read_csv("../data/Exercise_G_cleaned.txt", sep=" ", header=0)

    cid = 'b68f441e3f5b45988f09af6a4d151f9a'
    secret = '928b1fe81599460dbfea921c25c238b9'
    red='http://localhost:7777/callback'
    username = 'yanytheboy'
    scope = 'user-read-playback-state'

    token = SpotifyOAuth(username= username, scope=scope, client_id =cid, client_secret=secret, redirect_uri=red)
    player_token = SpotifyOAuth(username= username, scope='user-modify-playback-state', client_id =cid, client_secret=secret, redirect_uri=red)

    if token:
        sp = spotipy.Spotify(auth_manager= token)
        player = spotipy.Spotify(auth_manager=player_token)
    else:
        print("Can't get token for", username)

    # track = sp.current_user_playing_track()
    # print(track['item']['name'])


def create_window():
    global root, song_label, current_heartrate

    root = tk.Tk()
    root.geometry("800x800")
    song_text = tk.Label(text="Currently playing:", height=5)
    song_label = tk.Label(text="Was goody", width=25, height=5)
    current_heartrate = tk.Label(text="", width=25, height=10)
    path = "./images/stickfigure_running.gif"
    photo = ImageTk.PhotoImage(Image.open(path))
    label = tk.Label(root, image = photo)
    label.pack()
    frameCnt = 5
    frames = [tk.PhotoImage(file=path, format = 'gif -index %i' %(i)) for i in range(frameCnt)]
    song_text.pack(pady=100)
    song_label.pack()
    current_heartrate.pack()
    def update(ind):
        frame = frames[ind]
        ind += 1
        if ind == frameCnt:
            ind = 0
        label.configure(image=frame)
        root.after(100, update, ind)
    root.after(0, update, 0)
    root.mainloop()

def updater():    
    global index

    if index == len(df):
        exit(0)

    song_label.configure(text=sp.current_user_playing_track()['item']['name'])

    cur = df.iloc[index]
    current_heartrate.configure(text=cur)

    index += 1

    # call again after each second
    root.after(1000, updater)


def run():
    initialize()
    create_window()

    updater()
    root.mainloop()

if __name__ == "__main__":
    run()