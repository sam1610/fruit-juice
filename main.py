import webapp2
import handlers

PAGE_RE = r'((?:[a-zA-Z0-9_-]+/?)*)'

app = webapp2.WSGIApplication([
    ('/', handlers.FrontHandler),
    ('/signup/?', handlers.SignUpHandler),
    ('/login/?', handlers.LoginHandler),
    ('/_edit/' + PAGE_RE, handlers.EditPage),
    ('/' + PAGE_RE, handlers.WikiPage),
    ('/welcome', Welcome)
], debug=True)
