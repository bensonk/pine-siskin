#!/usr/bin/env python
from config import oauth_token, oauth_secret
from streaming_twitter import TwitterClient
from urllib2 import HTTPError, URLError
from models import Tweet

# Twitter home timeline URL
url = "https://userstream.twitter.com/2/user.json"
client = TwitterClient(oauth_token, oauth_secret)
try:
  def printer(t): print t
  client.watch(url, printer)
except HTTPError, e:
  print "The server couldn't fulfill the request."
  print 'Error code: ', e.code
  print 'Body: ', e.read()
except URLError, e:
  print "We failed to reach a server."
  print 'Reason: ', e.reason
