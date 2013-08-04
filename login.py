import webapp2

from signupdef import valid_username, valid_password
from google.appengine.ext import db #so can use databases
from handler import Handler
from user import User
from cookiedef import hash_str, make_secure_val, check_secure_val
from google.appengine.api import memcache
#maybe later store current url in memcache, so when login it goes back to
#where you came from


class Login(Handler):
    def write_form(self, error_username = "", error_password = "",  username = "", password = ""):
        self.render('login.html', j_error_username = error_username, j_error_password = error_password,
                     j_username = username, j_password = password)

    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        self.write_form()

    def post(self):
        #get parameters out of the request
        user_username = self.request.get('username')
        user_password = self.request.get('password')

        username = valid_username(user_username)
        password = valid_password(user_password)

        params = {"username": username, "password": password}

        errors = {"username": "That is not a valid username.",
                  "password": "That is not a valid password."}

        #login is validated
        if username and password:
            user_logged_in = self.check_if_logged_in()[0]
            if user_logged_in:
                previous_url = memcache.get("current path")
                self.redirect(previous_url)

            if not user_logged_in:
                #if first time, set a cookie
                new_cookie_val = make_secure_val(username)
                self.response.headers.add_header('Set-Cookie', 'username = %s' % str(new_cookie_val), path = '/')
                u = User(username = username, password = new_cookie_val)
                u.put()
                #need to change this to url just came from if can
                previous_url = memcache.get("current path")
                self.redirect(previous_url)

        else:
        #figure out which is in error
            username_error = ""
            password_error = ""

            password = ""

            for param in params:
                if params[param] == False or params[param] == None:
                    if param == 'username':
                        username_error = errors[param]
                    if param == 'password':
                        password_error = errors[param]

            self.write_form(username_error, password_error,user_username, password)
