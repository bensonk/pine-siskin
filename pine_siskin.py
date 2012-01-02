#!/usr/bin/env python
from streaming_twitter import TwitterClient
import simplejson as json
from pprint import pprint

# Twitter home timeline URL
url = "https://api.twitter.com/1/statuses/home_timeline.json?include_entities=true&count=10"

# bensonk42 token & secret
oauth_token = '15141419-udnhEyudjY4ovrRIh1WAmamXcUCgY99ATm1P8CwVg'
oauth_secret = 'Qw4qu5MYxE7mxdM9NpEm4J7aNXXvFP57c3Hkx6botoA'

client = TwitterClient(oauth_token, oauth_secret)
tweet_stream = client.get(url)
for line in tweet_stream:
  tweets = json.loads(line)
  for tweet in tweets:
    info = { "user": tweet['user']['name'].encode('utf-8', 'ignore'), "time": tweet['created_at'], "text": tweet['text'].encode('utf-8', 'ignore') }
    print("{user} at {time}:\n    {text}\n".format(**info))
