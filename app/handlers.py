import webapp2
import templates

from google.appengine.api import users as g_users

from models import url_model as url_model
from models import facades
from models.user import User
from models.url_model import Url
import helpers
import logging
import auth
import time


def check_login():
    def the_decorator(get_or_post_method):
        def inner_login_checker(request_handler, *args, **kwargs):
            if request_handler.current_user:
                return request_handler.redirect("/")
            else:
                return get_or_post_method(request_handler, *args, **kwargs)
        return inner_login_checker
    return the_decorator


def login_required(google_default=False):
    def the_decorator(get_or_post_method):
        def inner_login_checker(request_handler, *args, **kwargs):
            if request_handler.current_user:
                return get_or_post_method(request_handler, *args, **kwargs)
            else:
                if google_default:
                    google_login_url = g_users.create_login_url(request_handler.request.path)
                    return request_handler.redirect(google_login_url)
                return request_handler.redirect("/login")
        return inner_login_checker
    return the_decorator


class BaseHandler(webapp2.RequestHandler):
    def render_page(self, template_file, template_variables):
        template_variables['current_user'] = self.current_user

        if self.google_user:
            template_variables['logout_url'] = g_users.create_logout_url(self.request.uri)
            template_variables['logout_url_text'] = 'Logout'
        else:
            template_variables['logout_url'] = '/logout'
            template_variables['logout_url_text'] = 'Logout'

        templates.render(self, template_file, template_variables)

    def json_response(self, data):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(helpers.encode_json(data))

    def handle_exception(self, exception, debug_mode):
        logging.exception(exception)
        self.error(500)
        self.render_page('errors/500', {})

    def dispatch(self):
        global_debug_stats = {}
        global_debug_stats['request_start_time'] = time.time()

        self.current_user = None
        self.google_user = None
        self.current_user = auth.get_currently_logged_in_user(self)

        if not self.current_user:
            google_account = g_users.get_current_user()
            if google_account:
                google_based_user = User.get_by_user(google_account)
                if google_based_user:
                    # Google account already has an associated local user, so log in as that
                    self.current_user = self.google_user = google_based_user
                else:
                    # register new google user as local user
                    user = User(id=google_account.user_id())
                    user.user_id = google_account.user_id()
                    user.email = google_account.email()
                    user.save()
                    self.current_user = self.google_user = user

        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            global_debug_stats['request_end_time'] = time.time()
            request_time = global_debug_stats['request_end_time'] - global_debug_stats['request_start_time']
            logging.info("Served request in {0} milliseconds".format(request_time*1000))
            if request_time > 0.1:
                logging.error("Request taking too long")


class HomeHandler(BaseHandler):
    def get(self):
        self.render_page('home', {})


class ProfileHandler(BaseHandler):
    @login_required()
    def get(self):
        user_urls = Url.get_by_user(self.current_user)
        template_variables = {
            'user_urls': user_urls
        }
        self.render_page('profile', template_variables)


class GoogleLogin(BaseHandler):
    @login_required(google_default=True)
    def get(self):
        self.redirect('/')


class AdminHandler(BaseHandler):
    @login_required()
    def get(self):
        anonymous_urls = Url.get_anonymous_urls()
        template_variables = {
            'anonymous_urls': anonymous_urls
        }
        return self.render_page('admin', template_variables)


class GetUrlApiHandler(BaseHandler):
    def get(self, route):
        url = url_model.get_by_short_url(route)
        if url:
            response_data = url.get_values()
            self.json_response(response_data)
            return
        else:
            self.json_response({"error": "No url was found matching that request"})


class GetUrlRedirectHandler(BaseHandler):
    def get(self, route):
        url = url_model.get_by_short_url(route)
        if url:
            full_url = str(url.get_full_url())
            if full_url.find('http://') == -1 and full_url.find('https://') == -1:
                full_url = '//' + full_url

            self.redirect(full_url)
            return
        else:
            self.json_response({"error": "No url was found matching that request"})


class CreateUrlApiHandler(BaseHandler):
    def post(self):
        full_url = self.request.get('full_url')
        url = url_model.Url()
        url.set_short_url()
        url.set_full_url(full_url)
        url.set_user(self.current_user)
        url.save()
        response_data = url.get_values()
        self.json_response(response_data)


class RegistrationHandler(BaseHandler):
    def get(self):
        return self.render_page('registration', {})

    def post(self):
        User.register(self.request.get('email_address'), self.request.get('password'))
        return self.response.write("Done")


class LoginHandler(BaseHandler):
    def get(self):
        return self.render_page('login', {})

    def post(self):
        email_address = self.request.get('email_address', None)
        user = User.get_by_email(email_address)
        if user and user.password == helpers.check_password(self.request.get('password'), user.password):
            facades.login_user(self, user)
            return self.response.write("Valid")
        else:
            logging.info("Failed login attempt for user: {0}".format(email_address))
            return self.response.write("Invalid")


class LogoutHandler(BaseHandler):
    @login_required()
    def get(self):
        auth.destroy_login_cookie(self)


class NotFoundHandler(BaseHandler):
    def get(self, _):
        self.error(404)
        self.render_page("errors/404", {})
