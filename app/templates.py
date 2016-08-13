import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def render(template_name, template_variables, self):
    template_file = "templates/" + template_name + ".html"
    template = JINJA_ENVIRONMENT.get_template(template_file)
    self.response.out.write(template.render(template_variables))
