from google.appengine.ext import db

class Entry(db.Model):
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    subject = db.StringProperty()
    version = db.IntegerProperty(default = 0)