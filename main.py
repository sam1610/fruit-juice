from handlers import * #Solo hay handlers, por lo que no causa problemas con el namespace.

app = webapp2.WSGIApplication([
    ('/', FrontHandler)
], debug=True)
