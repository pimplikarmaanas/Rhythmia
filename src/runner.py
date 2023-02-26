import math
import pandas as pd
import time
from collections import deque

song_queues = {}

def initialize():
    df = pd.read_csv("../data/UserTracks.csv", header=0)

    for index, row in df.iterrows():
        tempo = math.floor(row['Tempo']/10) * 10

        if tempo not in song_queues:
            song_queues[tempo] = deque()
        song_queues[tempo].append((row['Track Name'], row['id']))


def run():
    df = pd.read_csv("../data/Exercise_G_cleaned.txt", sep=" ", header=0)
    
    i = 0
    for index, row in df.iterrows():
        if i == 10:
            break
        print(row['time'], " ", row['heart-rate'])
        time.sleep(1)
        i += 1

if __name__ == "__main__":
    if not song_queues:
        initialize()
    print(song_queues.keys())