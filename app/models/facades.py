import datetime
import auth


def login_user(request_handler, user):
    if user:
        user.last_login = datetime.datetime.now()
        user.login_count += 1
        user.save()
        auth.set_login_cookie(request_handler, user.email)
        return True
    return False
