#!/usr/bin/python
import time
import oauth2 as oauth
import urllib2 as urllib

# Pine Siskin key & secret
consumer_key = "0QfgB8xEzGWR3WmnLV7UQ"
consumer_secret = "AbKKg0rmvAHfvt6jgYOUfdhP4LDaiaQ9zVf1roMCjU"


class TwitterClient(object):
  def __init__(self, token, secret):
    self.consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    self.token = oauth.Token(token, secret)


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
    #url = "http://localhost:26001/1/statuses/home_timeline.json?include_entities=true"
    oauth_req = oauth.Request(method="GET", url=url, parameters=params)
    signature_method = oauth.SignatureMethod_HMAC_SHA1()
    oauth_req.sign_request(signature_method, self.consumer, self.token)

    # Make a urllib request object and open the connection
    headers = oauth_req.to_header()
    headers['User-agent'] = "Pine Siskin/0.1"
    req = urllib.Request(url=url, headers=headers)
    connection = urllib.urlopen(req)
    return connection
