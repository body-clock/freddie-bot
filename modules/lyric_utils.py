import random
from lyricsgenius import Genius
import boto3
import os

aws_access_key_id = os.environ['AWS_ID']
aws_secret_access_key = os.environ['AWS_SECRET']
s3_client = s3 = boto3.client('s3',
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key)

genius_user_token = os.environ['GENIUS_USER_TOKEN']


def create_list_from_csv(path):
    """Turn a CSV into a Python list"""
    with open(path, 'r') as fil:
        return [line.rstrip('\n') for line in fil]


def pick_random_song(songs_list, artist):
    """Connect to Genius API and get a random song from artist"""
    genius = Genius(genius_user_token)
    return genius.search_song(random.choice(songs_list), artist)


def clean_lyrics(dirty_lyric_list):
    """Remove list values with empty strings and brackets and delete the last element"""
    clean_lyric_list = [lyric for lyric in dirty_lyric_list if lyric and '[' not in lyric]
    return clean_lyric_list[:-1]


def select_lyrics(clean_lyric_list):
    """Pick lyrics from the cleaned up list of lyrics"""
    first_index = random.randint(0, len(clean_lyric_list) - 2)
    first_lyric = clean_lyric_list[first_index]
    second_lyric = clean_lyric_list[first_index + 1]
    return f"{first_lyric}\n{second_lyric}"