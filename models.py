class Tweet(object):
  def __init__(self, data = None):
    """Creates a tweet.  If provided, loads json-decoded data from the twitter API"""
    if data:
      self.load(data)

  def load(self, data):
    """Loads json-decoded data from the twitter API"""
    try:
      self.user = data['user']['name'].encode('utf-8', 'ignore')
      self.time = data['created_at']
      self.text = data['text'].encode('utf-8', 'ignore')
    except:
      print "ERROR: Failed to parse tweet"

  def __str__(self):
    if self.user and self.time and self.text:
      return "{0} at {1}:\n    {2}\n".format(self.user, self.time, self.text)
    else:
      return "--- incomplete tweet ---"

if __name__ == "__main__":
  from datetime import datetime
  t = Tweet()
  t.user = "bensonk42"
  t.time = datetime.now()
  t.text = "Setting up my twttr"
  print t
