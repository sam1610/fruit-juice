from handlers import * #Solo hay handlers, por lo que no causa problemas.

app = webapp2.WSGIApplication([
    ('/', FrontHandler),
    ('/signup/?', SignUpHandler),
    ('/login/?', LoginHandler)
], debug=True)
