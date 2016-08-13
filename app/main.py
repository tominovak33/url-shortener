#!/usr/bin/env python

import os
import webapp2

import routes


# When running on Google App Engine turn debugging off
if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
    debug_setting = False
# When running locally set debug on
else:
    debug_setting = True

app = webapp2.WSGIApplication(routes.ROUTES, debug=debug_setting)
