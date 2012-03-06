#!/usr/bin/env python
from streaming_twitter import TwitterClient
from urllib2 import HTTPError, URLError
from models import Tweet

# Twitter home timeline URL
url = "https://userstream.twitter.com/2/user.json"
client = TwitterClient()

if __name__ == "__main__":
  from sys import argv
  if len(argv) == 1:
    def printer(t): print t
    client.watch(url, printer)
  else:
    client.tweet(" ".join(argv[1:]))
