#!/usr/bin/python
import time, socket, json
import oauth2 as oauth
import urllib2 as urllib
from urllib import urlencode
from config import config
from models import Tweet
socket._fileobject.default_bufsize = 0
update_endpoint = 'https://twitter.com/statuses/update.json'

class TwitterClient(object):
  def __init__(self):
    self.consumer = oauth.Consumer(key=config['consumer']['key'], secret=config['consumer']['secret'])
    self.token = oauth.Token(config['auth']['oauth_token'], config['auth']['oauth_token_secret'])
    self.tweets = []
    self.friends = []
    self.client = oauth.Client(self.consumer, self.token)

  def handle_init(self, friend_json):
    self.friends.extend(json.loads(friend_json)['friends'])

  def tweet(self, text, msg_dict={}):
    if len(text) > 140:
      raise ValueError('Tweet was too long')
    msg_dict['status'] = text
    message_body = urlencode(msg_dict)
    resp, content = self.client.request(update_endpoint, 'POST', message_body, include_body_hash=False)
    print 'Response: {}'.format(resp)
    print 'Response content: {}'.format(content)

  def handle_message(self, tweet_json, callback):
    try: 
      message = json.loads(tweet_json)
      if 'delete' in message:
        # TODO: Create a delete model and do something worthwhile with it
        pass
      else:
        tweet = Tweet(message)
        self.tweets.append(tweet)
        callback(tweet)
    except ValueError as e:
      # This is to handle empty messages and unexpected characters more
      # gracefully. We might want to have some sort of logging facility here. 
      pass

  def watch(self, url, callback):
    error_count = 0
    while True:
      try:
        last_connection = time.time()
        tweet_stream = self.get(url)
        self.handle_init(tweet_stream.readline())
        for line in tweet_stream:
          self.handle_message(line, callback)
      except IOError as error:
        error_count += 1
        print "Connection failed with error '{}'.  Error count is {}".format(error, error_count)
        delay = time.time() - last_connection
        if delay < 120:
          # Mandated exponential backoff
          time.sleep(2 ** error_count)
        else:
          # If we've successfully kept a connection open for at least 2
          # minutes, we can reset our error count. 
          error_count = 0


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
