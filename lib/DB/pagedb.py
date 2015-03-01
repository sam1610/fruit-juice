from google.appengine.ext import db

class Page(db.Model):
    last_modified = db.DateTimeProperty(auto_now = True)

    def get_content(self, v_num=None):
        if not v_num or not str(v_num).isdigit():
            v_num = self.current_v()
        return self.pages.filter('version =', int(v_num)).get()

    def current_v(self):
        return self.sorted_versions()[-1].version

    def sorted_versions(self):
        versions = sorted(self.pages, key=lambda page: page.created)
        return versions


class PageContent(db.Model):
    page = db.ReferenceProperty(Page,
                                collection_name = "pages")
    
    created = db.DateTimeProperty(auto_now_add = True)
    content = db.TextProperty(required = True)
    version = db.IntegerProperty(required = True, default = 0)