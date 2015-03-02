import webapp2
from google.appengine.ext import db
from lib import utils
from lib.DB.userdb import User
from lib.DB import pagedb
from google.appengine.api import memcache


def page_cache(page_id):
    page = memcache.get(page_id)
    if not page:
        page = pagedb.Page.get_by_key_name(key_names=page_id, parent=pagedb.page_key())
        memcache.set(page_id, page)
    return page


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return utils.render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = utils.make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie', '%s=%s; Path=/' % (name, cookie_val)
            )

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and utils.check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('username', user.key().id())

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        username = self.read_secure_cookie('username')
        self.user = username and User.get_by_id(int(username))
        self.version = self.request.get("v")

    def get_page(self, page_id):
        return pagedb.Page.get_by_key_name(key_names=page_id, parent=pagedb.page_key())

    def get_version(self, page_id):
        page = self.get_page(page_id)
        if page:
            return page.get_content(self.version)

    def v_url(self):
        if self.version:
            return "?v=%s" % self.version
        return ""


class SignUpHandler(Handler):
    def get(self):
        self.render("signup.html")

    def post(self):
        error_flag = False      

        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        args = dict(username = username)
        
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
            args['password'] = utils.make_pw_hash(username, password)
            if email:
                args['email'] = email
            
            user = User(**args)
            user.put()

            self.login(user)
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
                    self.login(user)
                    self.redirect('/')
                    return
        args = dict(username=username, error_login="Invalid login")
        self.render("login.html", **args)


class EditPage(Handler):
    def render_form(self, page_id="", content="", error=""):
        self.render("newpage.html", page_id=page_id, content=content, error=error)

    def get(self, page_id):
        params = dict(page_id=page_id)
        if self.user:
            page_object = self.get_version(page_id)
            if page_object:
                params['content'] = page_object.content        
            self.render_form(**params)
        else:
            self.redirect('/login')

    def add_version(self, page_id, content):
        new_page = pagedb.Page.get_or_insert(key_name=page_id, parent=pagedb.page_key())
        pagedb.PageContent(page=new_page, content=content, parent=pagedb.page_key()).put()
    
    def post(self, page_id):
        content = self.request.get("content")
        if content:
            self.add_version(page_id, content)
            self.redirect('%s' % page_id)
        else:
            self.render_form(content = content, error = "Content, please!")


class WikiPage(Handler):
    def get(self, page_id):        
        params = dict(page_id=page_id, version=self.v_url())
        page_object = self.get_version(page_id)
        if page_object:
            params['content'] = page_object.content
            self.render("wikipage.html", **params)
        else:
            self.redirect('/_edit%s' % page_id)


class HistoryHandler(Handler):
    def get(self, page_id):
        page = self.get_page(page_id)
        if page:
            self.render("history.html", page_id=page_id, pages=page.sorted_versions())
        else:
            self.write("Sorry, the page doesn't exist.")

class LogoutHandler(Handler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'username=%s; Path=/' % "")
        self.redirect(self.request.referer)