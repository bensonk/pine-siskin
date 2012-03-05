#!/usr/bin/env python
import urlparse
import oauth2 as oauth
from config import conf, update_config

request_token_url = 'http://twitter.com/oauth/request_token'
access_token_url = 'http://twitter.com/oauth/access_token'
authorize_url = 'http://twitter.com/oauth/authorize'

consumer = oauth.Consumer(conf['consumer_key'], conf['consumer_secret'])
client = oauth.Client(consumer)

resp, content = client.request(request_token_url, "GET")
if resp['status'] != '200':
    raise Exception("Invalid response %s." % resp['status'])

request_token = dict(urlparse.parse_qsl(content))

print "Go to the following link in your browser:"
print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
print 

oauth_verifier = raw_input('After authorizing me, enter the pin here: ')

token = oauth.Token(request_token['oauth_token'],
    request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)
client = oauth.Client(consumer, token)

resp, content = client.request(access_token_url, "POST")
auth = dict(urlparse.parse_qsl(content))

update_config('auth', auth)
