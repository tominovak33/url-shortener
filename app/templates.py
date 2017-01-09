import jinja2
import os
import config

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# def render(template_name, template_variables, request_handler):
#     template_file = "templates/" + template_name + ".html"
#     template = JINJA_ENVIRONMENT.get_template(template_file)
#     request_handler.response.out.write(template.render(template_variables))


def render(request_handler, template_file_name, template_variables):
    output = generate_html(template_file_name, template_variables)
    return request_handler.response.out.write(output)


def generate_html(template_file_name, template_variables):
    # builds the path to the template
    if ".html" not in template_file_name:
        template_file_name += ".html"

    template_variables['STATIC_ROOT'] = config.STATIC_ROOT

    # loads it into the Jinja environment
    template_file = JINJA_ENVIRONMENT.get_template(template_file_name)
    # outputs the HTML from the rendered template and variables
    return template_file.render(template_variables)
