#!/usr/bin/python
import time
import oauth2 as oauth
import urllib2 as urllib
import socket
from config import consumer_secret, consumer_key
socket._fileobject.default_bufsize = 0
debug = True


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
    oauth_req = oauth.Request(method="GET", url=url, parameters=params)
    signature_method = oauth.SignatureMethod_HMAC_SHA1()
    oauth_req.sign_request(signature_method, self.consumer, self.token, include_body_hash=False)
    if debug:
      print("Normalized Parameters:\n\t{}".format(oauth_req.get_normalized_parameters()))

    # Make a urllib request object and open the connection
    headers = oauth_req.to_header()
    headers['User-agent'] = "Pine Siskin/0.1"
    headers['Accept-Encoding'] = "*/*"
    if debug:
      print("Headers:")
      for k in headers:
        print("\t{}: {}".format(k,headers[k]))
    req = urllib.Request(url=url, headers=headers)
    connection = urllib.urlopen(req)
    return connection
