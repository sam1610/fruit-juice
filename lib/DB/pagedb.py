from google.appengine.ext import db


#This function creates a key to assign a parent to each instance
def page_key(group = 'pages'):
    return db.Key.from_path('wiki', group)


#Page class, with multiple versions per page
#One to many relation with PageContent
class Page(db.Model):
    last_modified = db.DateTimeProperty(auto_now = True)

    def get_content(self, v_num=None):
        if not v_num:
            return self.current_v()
        return PageContent.get_by_id(ids=int(v_num), parent=page_key())

    #Return the latest version
    def current_v(self):
        versions = self.sorted_versions()
        if versions:
            return self.sorted_versions()[0]

    #Return list of versions sorted from old to new
    def sorted_versions(self):
        versions = sorted(
            self.pages, key=lambda page: page.created, reverse=True
            )
        return versions


class PageContent(db.Model):
    page = db.ReferenceProperty(Page,
                                collection_name = "pages")
    
    created = db.DateTimeProperty(auto_now_add = True)
    content = db.TextProperty(required = True)