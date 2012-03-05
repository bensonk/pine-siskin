#!/usr/bin/env python
import urlparse, SimpleHTTPServer, SocketServer, oauth2
from config import config, update_config
from pprint import pprint

request_token_url = 'http://twitter.com/oauth/request_token'
access_token_url = 'http://twitter.com/oauth/access_token'
authorize_url = 'http://twitter.com/oauth/authorize'

consumer = oauth2.Consumer(config['consumer']['key'], config['consumer']['secret'])
client = oauth2.Client(consumer)

resp, content = client.request(request_token_url, "GET")
if resp['status'] != '200':
    raise Exception("Invalid response %s." % resp['status'])

request_token = dict(urlparse.parse_qsl(content))

print "Go to the following link in your browser:"
print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
print 

oauth_token = ""
oauth_verifier = ""
class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  def do_GET(self, *args):
    global oauth_token, oauth_verifier
    creds = urlparse.parse_qs(urlparse.urlparse(self.path)[4])
    oauth_token = creds['oauth_token']
    oauth_verifier = creds['oauth_verifier']
    self.send_response(200, "OK")
    self.end_headers()
    print "Path: " + self.path
    self.wfile.write("<html><head><title>Thanks!</title></head><body><h3>Thanks, you're logged in!</h3></body></html>")

httpd = SocketServer.TCPServer(("", 8000), MyHandler)
httpd.handle_request()


token = oauth2.Token(request_token['oauth_token'],
    request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)
client = oauth2.Client(consumer, token)

resp, content = client.request(access_token_url, "POST")
auth = dict(urlparse.parse_qsl(content))
print "Authorized!"
pprint(auth)

update_config('auth', auth)
