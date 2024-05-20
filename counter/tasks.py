import requests

from redis import Redis
from rq import Queue

queue = Queue(connection=Redis())

def count_words_at_url(url):
    """Just an example function that's called async."""
    resp = requests.get(url)
    return len(resp.text.split())