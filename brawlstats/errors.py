class RequestError(Exception):
    """The base class for all errors."""

    def __init__(self, code, error):
        pass


class BadRequest(RequestError):
    """Raised if you sent a bad request to the API."""

    def __init__(self, url, code):
        self.code = code
        self.error = 'You sent a bad request the API.\nURL: ' + url
        super().__init__(self.code, self.error)


class NotFoundError(RequestError):
    """Raised if the tag was not found."""

    def __init__(self, url, code):
        self.code = code
        self.error = 'The tag you entered was not found.\nURL: ' + url
        super().__init__(self.code, self.error)


class Unauthorized(RequestError):
    """Raised if your API Key is invalid or blocked."""

    def __init__(self, url, code):
        self.code = code
        self.error = 'Your API Key is invalid or blocked.\nURL: ' + url
        super().__init__(self.code, self.error)


class InvalidTag(RequestError):
    """Raised if an invalid player tag or band tag has been passed."""

    def __init__(self, url, code):
        self.code = code
        self.error = 'An incorrect tag has been passed.\nURL: ' + url
        super().__init__(self.code, self.error)


class UnexpectedError(RequestError):
    """Raised if an unknown error has occured."""

    def __init__(self, url, code):
        self.code = code
        self.error = 'An unexpected error has occured.\nURL: ' + url
        super().__init__(self.code, self.error)


class ServerError(RequestError):
    """Raised if the API is down."""

    def __init__(self, url, code):
        self.code = code
        self.error = 'The API is down. Please be patient and try again later.\nURL: ' + url
        super().__init__(self.code, self.error)
