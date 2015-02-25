from google.appengine.ext import db

class Page(db.Model):
    last_modified = db.DateTimeProperty(auto_now = True)

    def get_by_v_number(self, v_num):
    	return self.pages.filter('version =', v_num).get()

    def current_v(self):
    	c_version = 0
    	for page in self.pages:
    		if page.version > c_version:
    			c_version = page.version
    	return c_version


class PageContent(db.Model):
	page = db.ReferenceProperty(Page,
								collection_name = pages)
	
	created = db.DateTimeProperty(auto_now_add = True)
	content = db.TextProperty(required = True)
	version = db.IntegerProperty(required = True)