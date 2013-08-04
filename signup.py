import webapp2
from handler import Handler

from signupdef import valid_username, valid_email, valid_password
from google.appengine.ext import db #so can use databases
from cookiedef import hash_str, make_secure_val, check_secure_val
from user import User

class Signup(Handler):

    def write_form(self, error_username = "", error_password = "", error_vpassword = "",
                   error_email = "", username = "", password = "", vpassword = "", email = ""):
        self.render('signup.html', j_error_username = error_username, j_error_password = error_password,
                     j_error_vpassword = error_vpassword, j_error_email = error_email, j_username = username,
                     j_password = password, j_vpassword = vpassword, j_email = email)

    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        self.write_form()

    def post(self):
        #get parameters out of the request
        user_username = self.request.get('username')
        user_password = self.request.get('password')
        user_vpassword = self.request.get('verify')
        user_email = self.request.get('email')

        username = valid_username(user_username)
        password = valid_password(user_password)
        vpassword = valid_password(user_vpassword)
        email = valid_email(user_email)

        match = password == vpassword

        params = {"username": username, "password": password, "vpassword": match, "email": email}

        errors = {"username": "That is not a valid username.",
                  "password": "That is not a valid password.",
                  "vpassword": "The passwords don't match.",
                  "email": "That is not a valid email address."}

        been_here = visit_cookie_str = self.request.cookies.get('username')

        users = db.GqlQuery("SELECT * from User")
        error_flag = False

        for user in users:
            if user.username == username:
                params["username"] = False
                errors["username"] = "User already exists."
                error_flag = True

        if not error_flag and username and password:
            #log them in
            if not self.check_if_logged_in()[0]:
                self.log_in_user(username)
                #sore user and redirect them to main page
                new_cookie_val = make_secure_val(username)
                u = User(username = username, password = new_cookie_val)
                u.put()
            self.redirect('/')
        else:
        #figure out which is in error
            username_error = ""
            password_error = ""
            matchpw_error = ""
            email_error = ""

            password = ""
            vpassword = ""

            for param in params:
                if params[param] == False or params[param] == None:
                    if param == 'username':
                        username_error = errors[param]
                    if param == 'password':
                        password_error = errors[param]
                    if param == 'vpassword':
                        matchpw_error = errors[param]
                    if param == 'email':
                        email_error = errors[param]

            self.write_form(username_error, password_error, matchpw_error, email_error,user_username, password, vpassword,user_email)

class Logout(Handler):
    def get(self):
        self.redirect('/')
        visit_cookie_str = self.request.cookies.get('username')
        if visit_cookie_str:
            self.response.headers.add_header('Set-Cookie', 'username =', path = '/')

#application = webapp2.WSGIApplication([('/logout', LogoutHandler),('/signup', Signup), ('/signup/welcome', WelcomeHandler)], debug = True)
