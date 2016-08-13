import handlers

ROUTES = [
    ('/', handlers.HomeHandler),
    ('/url', handlers.CreateUrlHandler),
    ('/url/([^/]+)', handlers.GetUrlHandler),
]
