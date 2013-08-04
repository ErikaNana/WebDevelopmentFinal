#import hashlib
import hmac


#def hash_str(s):
    #return hashlib.md5(s).hexdigest()

SECRET = 'imsosecret'

#get a string and return its hash value (more secure with hmac)
def hash_str(s):
        return hmac.new(SECRET,s).hexdigest()

#get a string and return a string and its hash value seperated by |
def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

#gets a cookie and makes sure that its value is equal to the hash that it was sent with
def check_secure_val(h):
    val = h.split('|')[0]  #split the string based on the | and store the first value of that list into val.  Has to be | b/c GAE has issues with , in cookies
    if h == make_secure_val(val):
        return val
