import os
import requests
from urllib.parse import urlparse
from io import BytesIO


def get_cat_image_url():
    """Get URL for a random cat image"""
    return requests.get('https://api.thecatapi.com/v1/images/search').json()[0]['url']


def get_ext_from_url(url):
    """Gets a file extension from a URL"""
    path = urlparse(url).path
    return os.path.splitext(path)[1]


def download_image_to_memory(url):
    """Use BytesIO to download an image from URL into memory"""
    img_data = requests.get(url, stream=True).content
    return BytesIO(img_data)