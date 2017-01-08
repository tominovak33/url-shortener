import helpers
from lib import jwt
import time
import logging
from models.user import User
import config

audience = "https://url.tomi33.co.uk"
algorithm = 'HS256'

LOGIN_EXPIRY_TIME = 86400  # 60 days, specified in minutes (60*24*60)

def generate_auth_token(user_key, lang='en-gb'):
    payload = {
        'iss': 'auth@tomi33.co.uk',
        'sub': 'auth@tomi33.co.uk',
        'aud': audience,
        'iat': int(time.time()),
        'exp': int(time.time() + LOGIN_EXPIRY_TIME),
        'user_key': user_key,
    }

    encoded = jwt.encode(payload, config.secret_key, algorithm=algorithm)

    return encoded


def decode_auth_token(token):
    try:
        return jwt.decode(token, config.secret_key, audience=audience, algorithms=algorithm)
    except:
        logging.error("Error decoding JWT login token")
        return False


def get_currently_logged_in_user(request_handler):
    user_email = get_currently_logged_in_user_identifier(request_handler)
    if user_email:
        return User.get_by_email(user_email)
    return None


def get_currently_logged_in_user_identifier(request_handler):
    token = helpers.get_cookie('auth_token', request_handler)
    if token and token != '':
        return get_user_key_from_token(token)
    else:
        return None


def get_user_key_from_token(token):
    try:
        payload = decode_auth_token(token)
        if int(payload['exp']) > int(time.time()):
            user_key_str = payload['user_key']
            return user_key_str
        return False
    except:
        logging.error("Error getting user from decoded JWT token")
        return False


def set_login_cookie(request_handler, user_name):
    cookie_value = generate_auth_token(user_name)
    helpers.set_cookie(request_handler, 'auth_token', cookie_value, expiration_time=LOGIN_EXPIRY_TIME)


def destroy_login_cookie(request_handler):
    helpers.destroy_cookie(request_handler, 'auth_token')
