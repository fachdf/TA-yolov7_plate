# from server import *
import time
import sys
import playsound
import requests,json
import os
os.add_dll_directory(os.getcwd())

def test():
    # Set the API endpoint URL
    
        start_time = time.time()
        url = 'http://127.0.0.1:5000/upload'

        # Set the request headers
        headers = {"Content-Type": "image/jpeg"}
        
        response = requests.post(url)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(response.text)    
        print(f"Elapsed time: {elapsed_time} seconds")

def print_func():
    print("args")

def play_sound():
    # sound_file = 'sound/verifikasi_gagal.mp3'
    # player = vlc.MediaPlayer("file://" + sound_file)
    playsound.playsound('sound\\500.mp3', True)
    playsound.playsound('sound\\502.mp3', True)
    playsound.playsound('sound\\503.mp3', True)
    playsound.playsound('sound\\505.mp3', True)
    #playsound.
    #player.play()

if __name__ == '__main__':
    #globals()[sys.argv[1]]()
    play_sound()