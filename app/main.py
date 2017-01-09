#!/usr/bin/env python

import os
import webapp2
import config as site_config

import routes


# When running on Google App Engine turn debugging off
if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
    debug_setting = False
# When running locally set debug on
else:
    debug_setting = True

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': site_config.SESSIONS_SECRET,
}

app = webapp2.WSGIApplication(routes.ROUTES, debug=debug_setting, config=config)
