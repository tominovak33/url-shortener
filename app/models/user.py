from google.appengine.ext import ndb
import helpers


class User(ndb.Model):
    user_id = ndb.StringProperty() # Used for tying google accounts to local accounts even if google details change, this won't
    email = ndb.StringProperty(indexed=True)
    password = ndb.StringProperty(indexed=True)
    date_registered = ndb.DateTimeProperty(auto_now_add=True)
    login_count = ndb.IntegerProperty(default=0)
    last_login = ndb.DateTimeProperty()

    def save(self):
        self.put()

    @classmethod
    def get_by_user(cls, user):
        # https://cloud.google.com/appengine/docs/python/users/userobjects
        return cls.query().filter(cls.user_id == user.user_id()).get()

    @staticmethod
    def register(email_address, password):
        user = User()
        user.email = email_address.lower()
        print "Password"
        print password
        user.password = helpers.hash_password(password)

        return user.save()

    @staticmethod
    def get_user_by_id(id):
        user = False
        query = User.query(User.user_id == id).fetch(1)
        for res in query:
            if res.user_id == id:
                user = res
                break
        return user


    @staticmethod
    def get_by_email(email_address):
        user = False
        query = User.query(User.email == email_address.lower()).fetch(1)
        for item in query:
            if item.email == email_address:
                user = item
                break
        return user
