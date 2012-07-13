

class HttpError(Exception):
    def __init__(self, message, code = 400):
        self.status_code = code
        Exception.__init__(self, {'code': code, 'msg': message})
        
class AuthError(HttpError):
    def __init__(self, message, code = 400):
        HttpError.__init__(self, message, code)

class LookupError(HttpError):
    def __init__(self, message, code = 404):
        HttpError.__init__(self, message, code)
        
class FileError(HttpError):
    def __init__(self, message, code = 404):
        HttpError.__init__(self, message, code)