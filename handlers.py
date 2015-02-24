import webapp2
from google.appengine.ext import db
from lib import utils
from lib.DB.userdb import User
from lib.DB.pagedb import Page
import time


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


class SignUpHandler(Handler):
    def get(self):
        self.render("signup.html")

    def post(self):
        error_flag = False      

        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        args = dict(username = username, email = email)
        
        if not utils.valid_username(username):
            args['error_name'] = "That's not a valid username."
            error_flag = True
        dbo = User.all().filter("username",username)
        if dbo.get():
            args['error_name'] = "The user already exists."
            error_flag = True
        if not utils.valid_password(password):
            args['error_pass'] = "That's not a valid password."
            error_flag = True
        if not password == verify:
            args['error_verify'] = "Your passwords didn't match."
            error_flag = True
        if email != "" and not utils.valid_email(email):
            args['error_email'] = "That's not a valid email."
            error_flag = "True"

        if error_flag:
            self.render("signup.html", **args)
        else:
            password = utils.make_pw_hash(username, password)
            if email:
                u = User(username = username, password = password, email = email)
            else:
                u = User(username = username, password = password)

            u.put()

            secure_username = utils.make_secure_val(str(username))
            self.response.headers.add_header('Set-Cookie', 'username=%s; Path=/' % secure_username)
            self.redirect("/")


class LoginHandler(Handler):
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")

        if username and password:
            user = User.all().filter("username", username).get()
            if user:
                h = user.password
                if utils.valid_pw(username, password, h):           
                    secure_username = utils.make_secure_val(str(username))
                    self.response.headers.add_header('Set-Cookie', 'username=%s; Path=/' % secure_username)
                    self.redirect('/')
                    return
        error = "Invalid login"
        self.render("login.html", username = username, error_login = error)


class EditPage(Handler):
    def render_form(self, content="", error=""):
        self.render("newpage.html", content=content, error=error)

    def get(self, page_id):
        page = Page.get_by_key_name(page_id)
        if not page:
            self.render_form()
        else:
            self.write("La pagina ya existe.")

    def post(self, page_id):
        content = self.request.get("content")

        if content:
            new_page = Page(key_name = page_id, content=content)
            new_page.put()
            time.sleep(1)            
            self.redirect('/%s' % page_id)
        else:
            self.render_form(content = content, error = "Content, please!")


class WikiPage(Handler):
    def get(self, page_id):
        page = Page.get_by_key_name(page_id)
        if page:
            self.write(page.content)
        else:
            self.redirect('/_edit/%s' % page_id)


