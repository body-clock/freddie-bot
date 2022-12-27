import modules.s3_utils as s3_utils
import modules.lyric_utils as lyric_utils
import modules.cat_image_utils as cat_image_utils
import modules.twitter_utils as twitter_utils


def lambda_handler(event, context):
    """Called by AWS Lambda function"""
    bucket_name = 'freddie-bot'
    artist = "Freddie Dredd"

    songs_csv_path = s3_utils.download_csv_from_aws(bucket_name, 'songs.csv', '/tmp/songs.csv')
    songs_list = lyric_utils.create_list_from_csv(songs_csv_path)
    random_song = lyric_utils.pick_random_song(songs_list, artist)

    lyrics = random_song.lyrics
    dirty_lyrics_list = str.splitlines(lyrics)
    clean_lyrics_list = lyric_utils.clean_lyrics(dirty_lyrics_list)
    final_lyrics = lyric_utils.select_lyrics(clean_lyrics_list)
    print(final_lyrics)

    url = cat_image_utils.get_cat_image_url()
    print(url)
    cat_image_in_memory = cat_image_utils.download_image_to_memory(url)

    ext = cat_image_utils.get_ext_from_url(url)
    image_file_name = f'cat{ext}'  #
    s3_utils.upload_image_to_s3(cat_image_in_memory, bucket_name, image_file_name)
    s3_utils.download_image_from_s3(bucket_name, image_file_name, f'/tmp/{image_file_name}')
    s3_utils.delete_image_from_s3(bucket_name, image_file_name)

    twitter_utils.upload_tweet_with_image(final_lyrics, f'/tmp/{image_file_name}')
    print("Tweet successful!")
