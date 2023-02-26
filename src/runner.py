import math
import random
import pandas as pd
import time
from collections import deque
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import tkinter as tk
from PIL import ImageTk, Image
from model import Model

song_queues, df = {}, None
root, song_label, current_heartrate, song_tempo = None, None, None, None
sp, player = None, None
index = 0
model = None
initial_id = None
prev_song = None

def initialize():

    global sp, player, df, song_queues, model, prev_song
    df = pd.read_csv("../data/UserTracks.csv", header=0)

    for index, row in df.iterrows():
        tempo = math.floor(row['Tempo']/10) * 10

        if tempo not in song_queues:
            song_queues[tempo] = []
        song_queues[tempo].append(({row['Track Name']: row['Artist']}, row['id']))
    
    for key, lst in song_queues.items():
        random.shuffle(lst)
        song_queues[key] = deque(lst)
    
    model = Model()

    df = pd.read_csv("../data/Exercise_G_cleaned.txt", sep=" ", header=0)

    cid = '57ef9b0e6675422b85dd36560b6858b2'
    secret = 'c8c81952436b4836afb1ff32ae6417da'
    red='http://localhost:7777/callback'
    username = 'd0ngus'
    scope = 'user-read-playback-state'

    token = SpotifyOAuth(username= username, scope=scope, client_id =cid, client_secret=secret, redirect_uri=red)
    player_token = SpotifyOAuth(username= username, scope='user-modify-playback-state', client_id =cid, client_secret=secret, redirect_uri=red)

    if token:
        sp = spotipy.Spotify(auth_manager= token)
        player = spotipy.Spotify(auth_manager=player_token)
    else:
        print("Can't get token for", username)

    addSongToQueue(df.iloc[0]['heart-rate'])
    prev_song = sp.current_user_playing_track()['item']['id']

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return '%02x%02x%02x' % rgb   

def create_window():
    global root, song_label, current_heartrate, song_tempo, song_bpm
    font_tuple = ("Segoe UI", 12)
    root = tk.Tk()
    bg_color = 'white'
    root.geometry("800x800")
    root.configure(bg=bg_color)
    song_label = tk.Label(font = font_tuple, text="Currently playing:",bg=bg_color,fg='black')
    song_tempo = tk.Label(font = font_tuple, text="", bg=bg_color,fg='black')
    song_bpm = tk.Label(font = font_tuple, text="", bg=bg_color,fg='black')

    current_heartrate = tk.Label(font = font_tuple, text="", bg=bg_color, fg='black')
    path = "./images/stickfigure_running.gif"
    photo = ImageTk.PhotoImage(Image.open(path))
    label = tk.Label(root, image = photo, bg=bg_color)

    label.pack(pady=20)
    frameCnt = 9
    frames = [tk.PhotoImage(file=path, format = 'gif -index %i' %(i)) for i in range(frameCnt)]
    song_label.pack()
    song_tempo.pack()
    song_bpm.pack()
    current_heartrate.pack()
    def update(ind):
        frame = frames[ind]
        ind += 1
        if ind == frameCnt:
            ind = 0
        speed = int((200-df.iloc[index]['heart-rate'])/2)
        num = int(255*abs((math.sin(ind/(5)))))
        new_color = "#"+_from_rgb((255,num,num))
        label.configure(image=frame,bg=new_color)
        root.after(speed, update, ind)

    root.after(0, update, 0)

def updater():    
    global index, prev_song

    if index == len(df):
        exit(0)
    
    song_label.configure(text="Current Song: "+sp.current_user_playing_track()['item']['name']+" - "+str([x['name'] for x in sp.current_user_playing_track()['item']['artists']]))
    feature = sp.audio_features(sp.current_user_playing_track()['item']['id'])
    song_bpm.configure(text="Song BPM: "+str(feature[0]['tempo']))

    cur = df.iloc[index]
    current_heartrate.configure(text="Heart-rate: "+str(cur['heart-rate']))
    index += 1

    # theres no songs in the queue
    cur_song = sp.current_user_playing_track()['item']['id']
    if cur_song != prev_song:
        update_queue()
        prev_song = cur_song

    # call again after each second
    root.after(2000, updater)

def update_queue():    
    addSongToQueue(df.iloc[index]['heart-rate'])

def addSongToQueue(hr):

    key = math.floor(hr/10) * 10
    song = song_queues[key].popleft()

    features = sp.audio_features(song[1])
    player.add_to_queue(features[0]['uri'])

    song_queues[key].append(song)

def run():
    initialize()
    create_window()

    updater()
    root.mainloop()

if __name__ == "__main__":
    run()