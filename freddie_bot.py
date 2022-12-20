import random
import os
import requests
from lyricsgenius import Genius
from urllib.parse import urlparse
import tweepy
import boto3
from io import BytesIO

genius_user_token = os.environ['GENIUS_USER_TOKEN']

twitter_consumer_key = os.environ['TWITTER_CONSUMER_KEY']
twitter_consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
twitter_access_token = os.environ["TWITTER_ACCESS_TOKEN"]
twitter_access_secret = os.environ["TWITTER_ACCESS_SECRET"]

aws_access_key_id = os.environ['AWS_ID']
aws_secret_access_key = os.environ['AWS_SECRET']
s3_client = s3 = boto3.client('s3',
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key)

auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
auth.set_access_token(twitter_access_token, twitter_access_secret)
api = tweepy.API(auth)


def download_csv_from_aws(bucket_name, file_name, file_path):
    """Download a CSV from AWS to a path"""
    s3_resource = boto3.resource('s3',
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key)
    s3_resource.Bucket(bucket_name).download_file(file_name, file_path)
    return file_path


def create_list_from_csv(path):
    """Turn a CSV into a Python list"""
    with open(path, 'r') as fil:
        songs = [line.rstrip('\n') for line in fil]
        return songs


def pick_random_song(songs_list, artist):
    """Connect to Genius API and get a random song from artist"""
    genius = Genius(genius_user_token)
    song = genius.search_song(random.choice(songs_list), artist)
    return song


def clean_lyrics(dirty_lyric_list):
    """Remove list values with empty strings and brackets and delete the last element"""
    clean_lyric_list = [lyric for lyric in dirty_lyric_list if lyric and '[' not in lyric]
    return clean_lyric_list[:-1]


def select_lyrics(clean_lyric_list):
    """Pick lyrics from the cleaned up list of lyrics"""
    first_lyric = random.choice(clean_lyric_list)
    # the first lyric will sometimes be the last element of the list, so we need to make sure that
    # we don't pick the next element in the list if that is the case (because it doesn't exist)
    if clean_lyric_list.index(first_lyric) != (len(clean_lyric_list) - 1):
        second_lyric = clean_lyric_list[clean_lyric_list.index(first_lyric) + 1]
        return first_lyric + '\n' + second_lyric
    else:
        return first_lyric

def select_lyrics(clean_lyric_list):
    """Pick lyrics from the cleaned up list of lyrics"""
    first_index = random.randint(0, len(clean_lyric_list) - 2)
    first_lyric = clean_lyric_list[first_index]
    second_lyric = clean_lyric_list[first_index + 1]
    return f"{first_lyric}\n{second_lyric}"


def get_cat_image_url():
    """Get URL for a random cat image"""
    response = requests.get(f'https://api.thecatapi.com/v1/images/search').json()[0]
    return response['url']


def get_ext_from_url(url):
    """Gets a file extension from a URL"""
    path = urlparse(url).path
    ext = os.path.splitext(path)[1]
    return ext


def download_image_to_memory(url):
    """Use BytesIO to download an image from URL into memory"""
    img_data = requests.get(url, stream=True).content
    img = BytesIO(img_data)
    return img


def upload_image_to_s3(image, bucket, image_name):
    """Upload image to s3 bucket"""
    s3_client.upload_fileobj(image, bucket, image_name)


def download_image_from_s3(bucket, image_name, download_path):
    """Download image into lambda /tmp/ directory"""
    s3_resource = boto3.resource('s3',
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key)
    s3_resource.Bucket(bucket).download_file(image_name, download_path)


def delete_image_from_s3(bucket, image_name):
    """Delete image from s3 bucket"""
    s3.delete_object(Bucket=bucket, Key=image_name)


def lambda_handler(event, context):
    """Called by AWS Lambda function"""
    bucket_name = 'freddie-bot'
    artist = "Freddie Dredd"

    songs_csv_path = download_csv_from_aws(bucket_name, 'songs.csv', '/tmp/songs.csv')
    songs_list = create_list_from_csv(songs_csv_path)
    random_song = pick_random_song(songs_list, artist)

    lyrics = random_song.lyrics
    dirty_lyrics_list = str.splitlines(lyrics)
    clean_lyrics_list = clean_lyrics(dirty_lyrics_list)
    final_lyrics = select_lyrics(clean_lyrics_list)
    print(final_lyrics)

    url = get_cat_image_url()
    print(url)
    cat_image_in_memory = download_image_to_memory(url)

    ext = get_ext_from_url(url)
    image_file_name = f'cat{ext}'  #
    upload_image_to_s3(cat_image_in_memory, bucket_name, image_file_name)
    download_image_from_s3(bucket_name, image_file_name, f'/tmp/{image_file_name}')
    delete_image_from_s3(bucket_name, image_file_name)

    api.update_status_with_media(final_lyrics, f'/tmp/{image_file_name}')
