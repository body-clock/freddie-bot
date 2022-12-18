import random
import os
import requests
from lyricsgenius import Genius
import tweepy
import boto3

genius_user_token = os.environ['GENIUS_USER_TOKEN']
genius = Genius(genius_user_token)

kitty_key = os.environ['KITTY_KEY']


def clean_lyrics(input_list):
    input_list[:] = [lyric for lyric in input_list if lyric != '' and '[' not in lyric]
    del input_list[-1]
    return input_list


def select_lyrics(input_list):
    first_lyric = random.choice(input_list)
    if input_list.index(first_lyric) != (len(input_list) - 1):
        second_lyric = lyrics_list[lyrics_list.index(first_lyric) + 1]
        return first_lyric + '\n' + second_lyric
    else:
        return first_lyric


def get_cat_image():
    response = requests.get(f'https://api.thecatapi.com/v1/images/search').json()[0]
    print(response['url'])


with open('songs.csv', 'r') as fil:
    songs = [line.rstrip('\n') for line in fil]

# song = genius.search_song("FUCK WHAT YOU CLAIM", "Freddie Dredd")
song = genius.search_song(random.choice(songs), "Freddie Dredd")
lyrics = song.lyrics
lyrics_list = clean_lyrics(str.splitlines(lyrics))
print(select_lyrics(lyrics_list))
get_cat_image()
