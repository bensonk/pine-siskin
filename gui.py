import sys, gtk, json
from threading import Thread
from config import config
from streaming_twitter import TwitterClient
from urllib2 import HTTPError, URLError
from models import Tweet

# Twitter home timeline URL
url = "https://userstream.twitter.com/2/user.json"
friends = []



class PineSiskinWindow(object):
  def on_window_destroy(self, widget, data=None):
    gtk.main_quit()

  def add_tweet(self, tweet):
    current_text = text_display.get_buffer()
    text_display.set_buffer(current_text + tweet)

  def __init__(self):
    builder = gtk.Builder()
    builder.add_from_file("ui.xml")
    self.window = builder.get_object("window")
    self.text_display = builder.get_object("text_display")
    builder.connect_signals(self)

if __name__ == "__main__":
  app = PineSiskinWindow()

  def twitter_listener():
    # TODO
    pass

  Thread(target=twitter_listener).start()

  # Start the gui
  app.window.show()
  gtk.main()
