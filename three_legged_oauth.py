#!/usr/bin/env python
import urlparse, SimpleHTTPServer, SocketServer, oauth2

def do_login():
  from config import config, update_config
  request_token_url = 'http://twitter.com/oauth/request_token'
  access_token_url = 'http://twitter.com/oauth/access_token'
  authorize_url = 'http://twitter.com/oauth/authorize'
  success_html = "<html><head><title>Thanks!</title></head><body><h3>Thanks, you're logged in!</h3><p>Feel free to close this window and return to the app.</p></body></html>"
  consumer = oauth2.Consumer(config['consumer']['key'], config['consumer']['secret'])
  client = oauth2.Client(consumer)

  resp, content = client.request(request_token_url, "GET")
  if resp['status'] != '200':
      raise Exception("Invalid response %s." % resp['status'])

  request_token = dict(urlparse.parse_qsl(content))

  print "Please visit the following link in your browser:"
  print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])

  oauth_token = ""
  oauth_verifier = ""
  class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def log_request(code, size):
      pass # Skip logging output
    def do_GET(self, *args):
      global oauth_token, oauth_verifier
      creds = urlparse.parse_qs(urlparse.urlparse(self.path)[4])
      oauth_token = creds['oauth_token']
      oauth_verifier = creds['oauth_verifier']
      self.send_response(200, "OK")
      self.end_headers()
      self.wfile.write(success_html)

  httpd = SocketServer.TCPServer(("", 8000), MyHandler)
  httpd.handle_request()

  token = oauth2.Token(request_token['oauth_token'],
      request_token['oauth_token_secret'])
  token.set_verifier(oauth_verifier)
  client = oauth2.Client(consumer, token)

  resp, content = client.request(access_token_url, "POST")
  auth = dict(urlparse.parse_qsl(content))
  print "Authorized!  Your pine siskin config file has been updated."

  update_config('auth', auth)

if __name__ == "__main__":
  print "Doing twitter login, buckle your seatbelts."
  do_login()
