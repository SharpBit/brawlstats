class RequestError(Exception):
    """The base class for all errors."""

    def __init__(self, code, message):
        pass

    def __str__(self):
        return self.message


class Forbidden(RequestError):
    """Raised if your API Key is invalid."""

    def __init__(self, code, url, message):
        self.code = code
        self.url = url
        self.message = message
        super().__init__(self.code, self.message)


class NotFoundError(RequestError):
    """Raised if an invalid player tag or club tag has been passed."""

    def __init__(self, code, **kwargs):
        self.code = code
        self.message = 'An incorrect tag has been passed.'
        self.reason = kwargs.pop('reason', None)
        self.invalid_chars = kwargs.pop('invalid_chars', [])
        if self.reason:
            self.message += '\nReason: {}'.format(self.reason)
        elif self.invalid_chars:
            self.message += 'Invalid characters: {}'.format(', '.join(self.invalid_chars))
        super().__init__(self.code, self.message)


class RateLimitError(RequestError):
    """Raised when the rate limit is reached."""

    def __init__(self, code, url):
        self.code = code
        self.url = url
        self.message = 'The rate limit has been reached.'
        super().__init__(self.code, self.message)


class UnexpectedError(RequestError):
    """Raised if an unknown error has occured."""

    def __init__(self, url, code, text):
        self.code = code
        self.url = url
        self.message = 'An unexpected error has occured.\n{text}'
        super().__init__(self.code, self.message)


class ServerError(RequestError):
    """Raised if the API is down."""

    def __init__(self, code, url):
        self.code = code
        self.url = url
        self.message = 'The API is down. Please be patient and try again later.'
        super().__init__(self.code, self.message)
