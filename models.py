class Tweet(object):
  def __init__(self, data = None):
    """Represents a tweet.  If provided, loads json-decoded data from the twitter API"""
    if data:
      self.load(data)

  def load(self, data):
    """Loads json-decoded data from the twitter API"""
    self.user = "!!!"
    self.time = "!!!"
    self.text = "!!!"
    try:
      self.user_name = data['user']['name'].encode('utf-8', 'ignore')
      self.user_handle = data['user']['screen_name'].encode('utf-8', 'ignore')
      self.time = data['created_at']
      self.text = data['text'].encode('utf-8', 'ignore')
      self.status_id = data['id']
    except:
      print "ERROR: Failed to parse tweet with following text: \n\n-----\n{}-----\n\n".format(data)

  def __str__(self):
    try:
      return "{0} (@{1}) at {2}:\n    {3}\n".format(self.user_name, self.user_handle, self.time, self.text)
    except:
      return "--- incomplete tweet ---"


class Deletion(object):
  def __init__(self, data = None):
    """Represents a tweet deletion.  If provided, loads json-decoded data from the twitter API"""
    if data:
      self.load(data)

  def load(self, data):
    """Loads json-decoded data from the twitter API"""
    self.status_id = data['delete']['status']['id']
    self.user_id = data['delete']['status']['user_id']

  def __str__(self):
    try:
      return "<Tweet deletion: id {0} by user id {1}>".format(self.status_id, self.user_id)
    except:
      return "<Empty deletion>"

class Event(object):
  def __init__(self, data):
    # TODO: Make events polymorphic and awesome, with subclasses for all known
    # event types
    self._load(data)

  def _load(self, data):
    self.event_type = data['event']

  def __str__(self):
    try:
      return "<Event: {0}>".format(self.event_type)
    except:
      return "<Emtpy event>"

if __name__ == "__main__":
  from datetime import datetime
  t = Tweet()
  t.user = "bensonk42"
  t.time = datetime.now()
  t.text = "Setting up my twttr"
  print t
