from handler import Handler
from login import Login
import webapp2
from signup import Signup, Logout
from google.appengine.ext import db
import re
from entry import Entry
import logging
from google.appengine.api import memcache
import time

def make_entry (keyname, entry_content, name = ""):
    entry = Entry(key_name = keyname, content = entry_content,
                            subject = name)
    entry.put()

def cache_entry(subject, update = False):
    cache_post = memcache.get(subject)
    if update or cache_post is None:
        logging.error('updating cache and hitting db')
        post_key = db.Key.from_path('Entry',subject)
        cache_post = db.get(post_key)
        memcache.set(subject,cache_post)
    return cache_post

class EditPage(Handler):
    def get(self, name):
        cookie, user = self.check_if_logged_in()
        self.set_current_url()

        check_cache = memcache.get(name)
        content = ""
        if check_cache:
            post_key = db.Key.from_path('Entry',name)
            cache_post = db.get(post_key)
            content = cache_post.content

        url = self.request.url
        history_url = '/_history' + name
        self.render("wiki_edit.html", j_content = content, user = user,
                    j_editlink = url, j_historylink = history_url)

    def post(self,name):
        entry_content = self.request.get('content')

        # #store it in database and update cache
        logging.error("adding to db")

        #add the previous version
        current_time = str(time.time())
        full_name = name + '_' + current_time
        #back up the current to db
        make_entry(full_name, entry_content, name)

        #overwrite the current version with the new one
        make_entry(name, entry_content)

        cache_entry(name,True)
        #make sure that content isnt escaped!
        self.redirect(name)



class WikiPage(Handler):

    def get(self, topic):
        self.set_current_url()
        cookie, user = self.check_if_logged_in()

        v_param = self.request.get('v')
        version_url = '%s?v=%s' % (topic,str(v_param))
        newurl = '/edit_' + topic
        history_url = '/_history' + topic

        if v_param:
            entry = db.GqlQuery("SELECT * FROM Entry WHERE subject = :subject and version = :version ", subject = topic, version = int(v_param))
            entry = list(entry)[0]

            #get content for that version
            self.render('wiki_entry.html', user = user, j_content = entry.content,
                        j_editlink = newurl, j_historylink = history_url)

        else:
            #check if this exists
            post = cache_entry(topic)

            if not post:
                self.redirect(newurl)
            if post:
                self.render('wiki_entry.html',
                            j_content = post.content, user = user,
                            j_editlink = newurl,
                            j_historylink = history_url)



class Error(Handler):
    def get (self):
        cookie, user = self.check_if_logged_in()
        if user:
            self.redirect('/edit_/error')
        if not user:
            self.render('error.html')

class HistoryPage(Handler):
    def get(self,name):
        cookie, user = self.check_if_logged_in()
        entries = db.GqlQuery("SELECT * FROM Entry WHERE subject = :subject ORDER BY created DESC", subject = name)
        entries = list(entries)

        length = len(entries)
        for entry in entries:
            entry.version = length
            entry.put()
            length = length - 1

        newurl = '/edit_' + name
        self.render('history.html',user = user, j_entries = entries, j_name = name, j_editlink = newurl)

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'

application = webapp2.WSGIApplication([
                               ('/signup', Signup),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/edit_' + PAGE_RE, EditPage),
                               ('/_history' + PAGE_RE, HistoryPage),
                               (PAGE_RE, WikiPage)],
                              debug=True)
