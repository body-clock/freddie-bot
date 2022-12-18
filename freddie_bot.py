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

auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
auth.set_access_token(twitter_access_token, twitter_access_secret)
api = tweepy.API(auth)


def clean_lyrics(input_list):
    input_list[:] = [lyric for lyric in input_list if lyric != '' and '[' not in lyric]
    del input_list[-1]
    return input_list


def select_lyrics(input_list):
    first_lyric = random.choice(input_list)
    if input_list.index(first_lyric) != (len(input_list) - 1):
        second_lyric = input_list[input_list.index(first_lyric) + 1]
        return first_lyric + '\n' + second_lyric
    else:
        return first_lyric


def get_cat_image_url():
    response = requests.get(f'https://api.thecatapi.com/v1/images/search').json()[0]
    print(response)
    return response['url']


def get_ext_from_url(input_url):
    path = urlparse(input_url).path
    ext = os.path.splitext(path)[1]
    return ext


def download_cat_image(input_url):
    ext = get_ext_from_url(input_url)
    img_data = requests.get(input_url, stream=True).content
    img = BytesIO(img_data)
    # connect to s3 bucket
    bucket = 'wiki-diptych-bucket'
    s3 = boto3.client('s3',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)
    # upload image to s3
    img_name = f'image{ext}'
    s3.upload_fileobj(img, bucket, img_name)
    # download into lambda tmp directory
    s3_resource = boto3.resource('s3',
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key)
    s3_resource.Bucket(bucket).download_file(f'{img_name}', f'/tmp/{img_name}')
    # delete from s3
    s3.delete_object(Bucket=bucket, Key=img_name)


def download_csv_from_aws(bucket_name, file_name, file_path):
    s3_resource = boto3.resource('s3',
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key)
    s3_resource.Bucket(bucket_name).download_file(file_name, file_path)


def lambda_handler(event, context):
    download_csv_from_aws('freddie-bot', 'songs.csv', '/tmp/songs.csv')

    with open('/tmp/songs.csv', 'r') as fil:
        songs = [line.rstrip('\n') for line in fil]

    genius = Genius(genius_user_token)
    song = genius.search_song(random.choice(songs), "Freddie Dredd")

    lyrics = song.lyrics
    lyrics_list = clean_lyrics(str.splitlines(lyrics))

    url = get_cat_image_url()
    download_cat_image(url)

    final_lyrics = select_lyrics(lyrics_list)
    api.update_status_with_media(final_lyrics, f'/tmp/image{get_ext_from_url(url)}')
