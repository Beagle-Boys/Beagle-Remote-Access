import string
import random
import bcrypt

class Auth:
    def __init__(self,password_length=10):
        self.PASSWORD_LENGTH = 10
        self.key = ''
        self.salt = bcrypt.gensalt()
        self.generateRandomPasscode()
        pass
    
    def generateRandomPasscode(self):
        #passcode = ''.join(random.choices(string.ascii_letters + string.digits, k=self.PASSWORD_LENGTH))
        passcode = "12345"
        #hashed = bcrypt.hashpw(bytes(passcode,encoding='utf-8'),self.salt)
        self.key = passcode
        print('## Passcode refreshed ##')
        return passcode
    
    def matchesPasscode(self,passcode):
        hashed = bcrypt.hashpw(bytes(passcode,encoding='utf-8'),self.salt)
        current = bytes(self.key,encoding='utf-8')
        return bcrypt.checkpw(current,hashed)
    
    def gen_cookie(self):
        cookie_b = bcrypt.hashpw(bytes(self.key,encoding='utf-8'),self.salt)
        cookie = cookie_b.decode('utf-8')
        return cookie
    
    def isAuthenticated(self,cookie):
        current = bytes(self.key,encoding='utf-8')
        hashed = bytes(cookie,encoding='utf-8')
        isAuth = bcrypt.checkpw(current,hashed)
        print('recieved',cookie,' : ',current, " : " ,isAuth)
        return isAuth
