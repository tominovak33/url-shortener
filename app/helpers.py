import json
import datetime

# Patch the default json encoder to be able to deal with datetime objects
# http://stackoverflow.com/questions/455580/json-datetime-between-python-and-javascript/32224522#32224522
# TODO: throw exception if still un-serializable
json.JSONEncoder.default = lambda self, obj: (obj.isoformat() if isinstance(obj, datetime.datetime) else None)

def encode_json(data):
    return json.dumps(data)
