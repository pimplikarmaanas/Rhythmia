import math
import pandas as pd
import time
from collections import deque
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import tkinter as tk
from PIL import ImageTk, Image

song_queues, df = {}, None
root, song_label, current_heartrate, song_tempo = None, None, None, None
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

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb   

def create_window():
    global root, song_label, current_heartrate, song_tempo
    font_tuple = ("Segoe UI", 12)
    root = tk.Tk()
    bg_color = 'white'
    root.geometry("800x800")
    root.configure(bg=bg_color)
    song_label = tk.Label(font = font_tuple, text="Currently playing:",bg=bg_color)
    song_tempo = tk.Label(font = font_tuple, text="", bg=bg_color)

    current_heartrate = tk.Label(font = font_tuple, text="", bg=bg_color)
    path = "./images/stickfigure_running.gif"
    photo = ImageTk.PhotoImage(Image.open(path))
    label = tk.Label(root, image = photo, bg=bg_color)

    label.pack(pady=20)
    frameCnt = 9
    frames = [tk.PhotoImage(file=path, format = 'gif -index %i' %(i)) for i in range(frameCnt)]
    song_label.pack()
    song_tempo.pack()
    current_heartrate.pack()
    def update(ind):
        frame = frames[ind]
        ind += 1
        if ind == frameCnt:
            ind = 0
        speed = int((200-df.iloc[index]['heart-rate'])/2)
        new_color = _from_rgb((255,0,0))
        label.configure(image=frame,bg=new_color)
        root.after(speed, update, ind)
    root.after(0, update, 0)

def updater():    
    global index

    if index == len(df):
        exit(0)

    
    current_song = sp.current_user_playing_track()
    try:
        tempo = sp.audio_features(tracks=[current_song['item']['uri']])[0]['tempo']
    except:
        print("Can't get tempo")

    song_label.configure(text="Current Song: "+current_song['item']['name'])
    song_tempo.configure(text=tempo)

    cur = df.iloc[index]
    current_heartrate.configure(text=cur)

    index += 1

    # call again after each second
    root.after(2000, updater)


def run():
    initialize()
    create_window()

    updater()
    root.mainloop()

if __name__ == "__main__":
    run()