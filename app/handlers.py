import webapp2
import templates

from models import url_model as url_model
import helpers


class BaseHandler(webapp2.RequestHandler):
    def render_page(self, template_file, template_variables):
        templates.render(template_file, template_variables, self)

    def json_response(self, data):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(helpers.encode_json(data))


class HomeHandler(BaseHandler):
    def get(self):
        self.render_page('home', {})


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
        url.save()
        response_data = url.get_values()
        self.json_response(response_data)
