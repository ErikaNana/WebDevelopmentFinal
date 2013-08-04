class Check_Login(Handler):
    def logged_in(self):
        visit_cookie_str = self.request.cookies.get('username')
        cookie_val = None
        if visit_cookie_str: #if have cookie
            cookie_val = check_secure_val(visit_cookie_str) #decode it
        if cookie_val: #if have valid result
        #user is logged in, just go back front page
            return True, cookie_val
        return False, cookie_val
