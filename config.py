import base64, json
from os.path import expanduser
conf_file = "~/.pine-siskin.json"

try:
  with file(expanduser(conf_file)) as config_file:
    config = json.load(config_file)
except IOError as e:
  config = {}

# Augment config with Pine Siskin key & secret
config['consumer'] = {'key': base64.b64decode('SktLeGlVNmNBQ1JvZHdqZ3VudkN3dw=='),
  'secret': base64.b64decode('OTY2MUpxSGtMVnF2cXZSMXM4Q25vM3k5MndKY1M4Y2FNcnFldVp0bnM=')}

def update_config(k, v):
  config[k] = v
  consumer = config['consumer']
  config['consumer'] = None
  with file(expanduser(conf_file), 'w') as config_file:
    json.dump(config, config_file)
  config['consumer'] = consumer

# If there's no auth, we'll take some initiative and try to do a login
if 'auth' not in config:
  config['auth'] = {}
  from three_legged_oauth import do_login
  do_login()
