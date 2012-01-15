#!/usr/bin/env python
from config import oauth_token, oauth_secret
from streaming_twitter import TwitterClient
import simplejson as json
from pprint import pprint
from urllib2 import HTTPError, URLError

# Twitter home timeline URL
url = "https://userstream.twitter.com/2/user.json"
friends = []

def handle_init(json_str):
  global friends
  friends = json.loads(json_str)['friends']

def handle_tweets(json_str):
  try: 
    tweet = json.loads(json_str)
    info = { "user": tweet['user']['name'].encode('utf-8', 'ignore'), "time": tweet['created_at'], "text": tweet['text'].encode('utf-8', 'ignore') }
    print("{user} at {time}:\n    {text}\n".format(**info))
  except:
    # This is to handle unexpected characters more gracefully. Ideally we'd
    # have some sort of logging facility here. 
    pass

client = TwitterClient(oauth_token, oauth_secret)
try:
  tweet_stream = client.get(url)
  handle_init(tweet_stream.readline())
  for line in tweet_stream:
    handle_tweets(line)
except HTTPError, e:
  print "The server couldn't fulfill the request."
  print 'Error code: ', e.code
  print 'Body: ', e.read()
except URLError, e:
  print "We failed to reach a server."
  print 'Reason: ', e.reason
