class RequestError(Exception):
    '''The base class for all errors.'''

    def __init__(self, code, error):
        pass


class Unauthorized(RequestError):
    '''Raised when your API Key is incorrect.'''

    def __init__(self, url):
        self.code = 403
        self.error = 'Your API Key is incorrect.\nURL: ' + url
        super().__init__(self.code, self.error)


class InvalidTag(RequestError):
    '''Raised when an invalid player or band tag has been passed.'''

    def __init__(self, url):
        self.code = 404
        self.error = 'An incorrect tag has been passed.\nURL: ' + url
        super().__init__(self.code, self.error)


class UnexpectedError(RequestError):
    '''Raised when an unknown error has occured.'''

    def __init__(self, url):
        self.code = 500
        self.error = 'An unexpected error has occured. Please contact us.\nURL: ' + url
        super().__init__(self.code, self.error)


class ServerError(RequestError):
    '''Raised when the API is down.'''

    def __init__(self, url):
        self.code = 503
        self.error = 'The API is down. Please be patient and try again later.\nURL: ' + url
        super().__init__(self.code, self.error)
