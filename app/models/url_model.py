from google.appengine.ext import ndb
from random import randint
from datetime import datetime
from models.user import User


class Url(ndb.Model):
    short_url = ndb.StringProperty(indexed=True)
    full_url = ndb.StringProperty(indexed=False)
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    user = ndb.KeyProperty(kind=User, default=None)
    uses = ndb.IntegerProperty(default=0)
    last_use = ndb.DateTimeProperty()

    def set_short_url(self):
        self.short_url = generate_unique_short_url()

    def set_full_url(self, full_url):
        self.full_url = full_url

    def get_full_url(self):
        return self.full_url

    def set_user(self, user):
        if user and user.key:
            self.user = user.key
        else:
            self.user = None

    def get_user(self):
        if self.user:
            return self.user.get()
        return None

    def save(self):
        self.put()

    def use(self):
        self.last_use = datetime.now()
        self.uses += 1
        return self.save()

    def get_values(self):
        return self.to_dict()

    @staticmethod
    def get_by_user(user):
        if user and user.key:
            # TODO: paginate query
            return Url.query(Url.user == user.key).fetch()
        return None

    @staticmethod
    def get_anonymous_urls():
        # TODO: paginate query
        return Url.query(Url.user == None).fetch()

def generate_unique_short_url(max_length=6):
    access_code_alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    short_url = ''

    length = randint(6, max_length)

    for i in range(length):
        short_url += access_code_alphabet[randint(0, len(access_code_alphabet)-1)]

    # There is a potential chance that as more unique strings are generated and stored, this recursive function
    # will be called multiple times, causing the program to start to slow down and theoretically it would
    # eventually to enter a pseudo-infinite loop
    # However with an alphabet of 62 characters and a string length length of 6, there are over 56.8 Billion
    # (62 to the power of 6) possible unique strings to generate.
    # So even after close to 10 billion existing entries, there is still less than a 1 in 5 chance of a randomly
    # generated string to fail this initial uniqueness check.
    # By which point the system would probably have run into larger issues than having to call this function twice
    if not check_short_url_is_unique(short_url):
        short_url = generate_unique_short_url()

    return short_url


def check_short_url_is_unique(short_url):
    if not get_by_short_url(short_url):
        return True
    return False


def get_by_short_url(short_url):
    url = False
    res = Url.query(Url.short_url == short_url).fetch(1)
    for item in res:
        if item.short_url == short_url:
            url = item
            url.use()
            break
    return url


