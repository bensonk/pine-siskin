#!/usr/bin/env python
from config import oauth_token, oauth_secret
from streaming_twitter import TwitterClient
import simplejson as json
from pprint import pprint
from urllib2 import HTTPError, URLError

# Twitter home timeline URL
url = "https://api.twitter.com/1/statuses/home_timeline.json?include_entities=true&count=10"
#url = "https://userstream.twitter.com/2/user.json"

client = TwitterClient(oauth_token, oauth_secret)
try:
  tweet_stream = client.get(url)
  for line in tweet_stream:
    tweets = json.loads(line)
    for tweet in tweets:
      info = { "user": tweet['user']['name'].encode('utf-8', 'ignore'), "time": tweet['created_at'], "text": tweet['text'].encode('utf-8', 'ignore') }
      print("{user} at {time}:\n    {text}\n".format(**info))
except HTTPError, e:
  print "The server couldn't fulfill the request."
  print 'Error code: ', e.code
  print 'Body: ', e.read()
except URLError, e:
  print "We failed to reach a server."
  print 'Reason: ', e.reason
