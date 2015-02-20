from handlers import * #Solo hay handlers, por lo que no causa problemas con el namespace.

app = webapp2.WSGIApplication([
    ('/', FrontHandler),
    ('/signup/?', SignUpHandler)
], debug=True)
