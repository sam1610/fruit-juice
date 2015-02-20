import webapp2
from lib import utils
from lib.DB import userdb


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return utils.render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class FrontHandler(Handler):
    def get(self):
        self.render('front.html')