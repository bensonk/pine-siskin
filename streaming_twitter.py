#!/usr/bin/python
import time
import oauth2 as oauth
import urllib2 as urllib
import socket
import simplejson as json
from simplejson.decoder import JSONDecodeError
from config import consumer_secret, consumer_key
from models import Tweet
socket._fileobject.default_bufsize = 0

class TwitterClient(object):
  def __init__(self, token, secret):
    self.consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    self.token = oauth.Token(token, secret)
    self.tweets = []
    self.friends = []

  def handle_init(self, friend_json):
    self.friends.extend(json.loads(friend_json)['friends'])

  def handle_tweet(self, tweet_json, callback):
    try: 
      tweet = Tweet(json.loads(tweet_json))
      self.tweets.append(tweet)
      callback(tweet)
    except JSONDecodeError as e:
      # This is to handle empty messages and unexpected characters more
      # gracefully. We might want to have some sort of logging facility here. 
      pass

  def watch(self, url, callback):
    tweet_stream = self.get(url)
    self.handle_init(tweet_stream.readline())
    for line in tweet_stream:
      self.handle_tweet(line, callback)

  def get(self, url):
    # Set parameters
    params = {
        'oauth_version': "1.0",
        'oauth_nonce': oauth.generate_nonce(),
        'oauth_timestamp': int(time.time()),
        'oauth_token': self.token.key,
        'oauth_consumer_key': self.consumer.key
    }

    # Build and sign request
    oauth_req = oauth.Request(method="GET", url=url, parameters=params)
    signature_method = oauth.SignatureMethod_HMAC_SHA1()
    oauth_req.sign_request(signature_method, self.consumer, self.token, include_body_hash=False)

    # Make a urllib request object and open the connection
    headers = oauth_req.to_header()
    headers['User-agent'] = "Pine Siskin/0.1"
    headers['Accept-Encoding'] = "*/*"
    req = urllib.Request(url=url, headers=headers)
    connection = urllib.urlopen(req)
    return connection
