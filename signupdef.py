import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")  #username
USER_RE2 = re.compile(r"^[\S]+@[\S]+\.[\S]+$")  #email
USER_RE3 = re.compile(r"^.{3,20}$")     #password

def valid_username(username):
    if USER_RE.match(username):
        return username


def valid_password(password):
    if USER_RE3.match(password):
        return password

def valid_email(email):
    if email == "":
        return True
    if USER_RE2.match(email):
        return email
