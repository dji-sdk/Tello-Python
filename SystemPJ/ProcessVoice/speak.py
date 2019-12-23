from mutagen.mp3 import MP3 as mp3
import pygame
import time


def mp3play(name):
    filename = name
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    mp3_length = mp3(filename).info.length
    pygame.mixer.music.play(1)
    time.sleep(mp3_length + 0.25)
    pygame.mixer.music.stop()

if __name__ == "__main__":
	mp3play("/Users/shoda/Tello-Python/SystemPJ/ProcessVoice/speech_20191223054237114.mp3")