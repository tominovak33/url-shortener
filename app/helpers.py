import json
import datetime
import os
from lib.bcrypt import bcrypt

# Patch the default json encoder to be able to deal with datetime objects
# http://stackoverflow.com/questions/455580/json-datetime-between-python-and-javascript/32224522#32224522
# TODO: throw exception if still un-serializable
json.JSONEncoder.default = lambda self, obj: (obj.isoformat() if isinstance(obj, datetime.datetime) else None)

def encode_json(data):
    return json.dumps(data)

def get_current_time():
    return datetime.datetime.now()

# If cookie expiration is not specifed, set it to 1 week ( 10080 seconds)
def set_cookie(request_handler, name, value, expiration_time=10080):
    request_handler.response.set_cookie(name, value, expires=(datetime.datetime.now() + datetime.timedelta(minutes=expiration_time)), path='/')

def destroy_cookie(request_handler, name):
    request_handler.response.set_cookie(name, "", expires=datetime.datetime.now(), path='/')

def get_cookie(name, self):
    if self.request.cookies.get(name):
        return self.request.cookies.get(name)
    return False

def is_local_environment():
    """
    Determing if the current site is running on the cloud (real) app-engine or on a local dev server
    :return: Boolean True if local dev server False if not
    """
    if os.getenv('SERVER_SOFTWARE', '').startswith('Dev'):
        return True
    return False

# [START Password Hashing]
"""
bcrypt stores metadata about the hashed password (such as the salt, the amount of hash rounds etc) in the password hash
itself rather than storing the salt separately.
So once the password is hashed initially using bcrypt.hashpw(password_plaintext, bcrypt.gensalt(2)) (as this passes in a
randomly generated salt) calling the same function again will not give the same result
(thanks to the random salt earlier). Imagine this as md5(password_plaintext + str(uuid.uuid4()))
Therefore using the same function to check if a password input matches a stored hash is not an option. However bcrypt
can accept an existing bcrypt hash as the 'salt' to its hashpw function (rather than a randomly generated new salt.
It will then figure out the original salt and number of rounds used to create the existing hash
(thanks to the metadata mentioned earlier) and use the same settings to hash the plaintext pwd supplied.
So if the two hashes match then it proves that the plaintext input matches the initial one too.
So to simplify in pseudo code:
hash1 = bcrypt.hashpw(password_input_1, bcrypt.gensalt(2))
hash2 = bcrypt.hashpw(password_input_2, hash1)
if hash1 == hash2 then password_input_1 == password_input_2
"""

NUM_BCRYPT_ROUNDS = 5

def hash_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt(NUM_BCRYPT_ROUNDS))


def check_password(password, hashed_password):
    return bcrypt.hashpw(password, hashed_password)

# [END Password Hashing]

def dev_write_to_file(file_name, content):
    if os.environ.get('SERVER_SOFTWARE','').startswith('Dev'):
        from google.appengine.tools.devappserver2.python.stubs import FakeFile
        FakeFile.ALLOWED_MODES = frozenset(['a','r', 'w', 'rb', 'U', 'rU'])
        f = open(file_name, 'w')
        # Note: as FakeFile only fakes the file write methods, ensure that the directory you wish to write to already
        # exists as you cant use python's `os.makedirs` to create it if not
        f.write(content)
        f.close()
    else:
        logging.warn("Cannot do file I/O on when running on Cloud App Engine")
        return False
