import handlers

ROUTES = [
    ('/', handlers.HomeHandler),
    ('/admin', handlers.AdminHandler),
    ('/profile', handlers.ProfileHandler),
    ('/url', handlers.CreateUrlApiHandler),
    ('/register', handlers.RegistrationHandler),
    ('/login', handlers.LoginHandler),
    ('/logout', handlers.LogoutHandler),
    ('/google_login', handlers.GoogleLogin),
    ('/url/([^/]+)', handlers.GetUrlApiHandler),
    ('/([^/]+)', handlers.GetUrlRedirectHandler),
    ('/(.*)', handlers.NotFoundHandler),
]
