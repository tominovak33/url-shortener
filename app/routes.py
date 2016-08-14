import handlers

ROUTES = [
    ('/', handlers.HomeHandler),
    ('/url', handlers.CreateUrlApiHandler),
    ('/url/([^/]+)', handlers.GetUrlApiHandler),
    ('/([^/]+)', handlers.GetUrlRedirectHandler),
]
