import streamlit as st
import spotipy # type: ignore
import os
import time
from spotipy.oauth2 import SpotifyOAuth # type: ignore

scope = 'user-modify-playback-state user-read-playback-state'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=st.secrets.id,
                                               client_secret=st.secrets.secret,
                                               redirect_uri='https://spotipy.streamlit.app:8080/',
                                               scope=scope))

def sync():
    return sp.current_playback()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def playpause():
    current_playback = sync()
    if current_playback and current_playback['is_playing']:
        sp.pause_playback()
    else:
        sp.start_playback()

def shuffle():
    current_playback = sync()
    if current_playback:
        shuffle_state = current_playback['shuffle_state']
        sp.shuffle(not shuffle_state)

def repeat():
    current_playback = sync()
    if current_playback:
        repeat_state = current_playback['repeat_state']
        if repeat_state == 'context':
            sp.repeat('off')
        else:
            sp.repeat('context')

def volume():
    current_playback = sync()
    if current_playback:
        volume_percent = current_playback['device']['volume_percent']
        percentage = input(f"Volume > {volume_percent}\nVolume > ")
        try:
            percentage = int(percentage)
            if 0 <= percentage <= 100:
                sp.volume(percentage)
            else:
                print("Error")
        except ValueError:
            print("Error")

def info():
    current_playback = sync()
    if current_playback:
        progress_ms = current_playback["progress_ms"]
        duration_ms = current_playback["item"]["duration_ms"]
        playback_percent = (progress_ms / duration_ms) * 100
        title = current_playback["item"]["name"]
        artists = [artist["name"] for artist in current_playback["item"]["artists"]]
        artist_names = ", ".join(artists)
        album = current_playback["item"]["album"]["name"]

        return title, artist_names, album, playback_percent

def position():
    current_playback = sync()
    if current_playback:
        position = current_playback["item"]["duration_ms"] * int(input("Position > ")) / 100
        sp.seek_track(int(position))

def continuousinfo():
    while True:
        info()
        time.sleep(3)

def nextsong():
    sp.next_track()

def prevsong():
    sp.previous_track()

def device():
    devices = sp.devices()
    for i, device in enumerate(devices['devices'], 1):
        print(f"{i}. {device['name']}")
    num = input("Device > ")
    try:
        num = int(num)
        if 1 <= num <= len(devices['devices']):
            device_name = devices['devices'][num - 1]['id']
            sp.transfer_playback(device_name, True)
        else:
            print("Error")
    except ValueError:
        print("Error")

def queue():
    queue = sp.queue()
    for i, item in enumerate(queue['queue'], 1):
        artists = [artist['name'] for artist in item['artists']]
        artist_names = ", ".join(artists)
        print(f"{i}. {item['name']} - {artist_names}")

# Streamlit

st.title("Spotipy")
st.write()

while True:
    title, artist_names, album, playback_percent = info()
    print(f"Title: {title}")
    print(f"Artist: {artist_names}")
    print(f"Album: {album}")
    print(f"Playback: {playback_percent}")
    time.sleep(1)
