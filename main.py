import webapp2
import handlers

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([('/signup', handlers.SignUpHandler),
                               ('/login', handlers.LoginHandler),
                               ('/logout', handlers.LogoutHandler),
                               ('/_edit' + PAGE_RE, handlers.EditPage),
                               ('/_history' + PAGE_RE, handlers.HistoryHandler)
                               (PAGE_RE, handlers.WikiPage),
                               ],
                              debug=True)