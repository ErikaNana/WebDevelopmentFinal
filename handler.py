import os
import webapp2
import jinja2
from cookiedef import hash_str, make_secure_val, check_secure_val
from google.appengine.api import memcache

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

#all the methods that all of the different components will use
class Handler(webapp2.RequestHandler):
    def check_if_logged_in(self):
        visit_cookie_str = self.request.cookies.get('username')
        cookie_val = None
        if visit_cookie_str: #if have cookie
            cookie_val = check_secure_val(visit_cookie_str) #decode it, get username
        if cookie_val: #if have valid result
        #user is logged in, just go back front page
            return True, cookie_val
        return False, cookie_val

    def log_in_user(self,username):
        new_cookie_val = make_secure_val(username)
        self.response.headers.add_header('Set-Cookie', 'username = %s' % str(new_cookie_val), path = '/')

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_current_url(self):
        current_path = self.request.url
        memcache.set('current path', current_path)
