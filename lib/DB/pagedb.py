from google.appengine.ext import db

def page_key(group = 'pages'):
    return db.Key.from_path('wiki', group)

class Page(db.Model):
    last_modified = db.DateTimeProperty(auto_now = True)

    def get_content(self, v_num=None):
        if not v_num:
            return self.current_v()
        return PageContent.get_by_id(ids=int(v_num), parent=page_key())

    def current_v(self):
        return self.sorted_versions()[-1]

    def sorted_versions(self):
        versions = sorted(self.pages, key=lambda page: page.created)
        return versions


class PageContent(db.Model):
    page = db.ReferenceProperty(Page,
                                collection_name = "pages")
    
    created = db.DateTimeProperty(auto_now_add = True)
    content = db.TextProperty(required = True)