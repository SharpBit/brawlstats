class RequestError(Exception):
    """The base class for all errors."""

    def __init__(self, code, message, retry_after=None):
        pass

    def __str__(self):
        return self.message


class Unauthorized(RequestError):
    """Raised if your API Key is invalid or blocked."""

    def __init__(self, code, url):
        self.code = code
        self.url = url
        self.message = 'Your API Key is invalid or blocked.'
        super().__init__(self.code, self.message)


class Forbidden(RequestError):
    """Raised if the IP using the token was not whitelisted."""

    def __init__(self, code, url, message):
        self.code = code
        self.url = url
        self.message = message
        super().__init__(self.code, self.message)


class NotFoundError(RequestError):
    """Raised if an invalid player tag or club tag has been passed."""

    def __init__(self, code, invalid_chars=[]):
        self.code = code
        self.message = 'An incorrect tag has been passed.\nInvalid Characters: ' + ', '.join(invalid_chars)
        self.invalid_chars = invalid_chars
        super().__init__(self.code, self.message)


class RateLimitError(RequestError):
    """Raised when the rate limit is reached."""
    def __init__(self, code, url, retry_after):
        self.code = code
        self.url = url
        self.retry_after = retry_after
        self.message = 'The rate limit has been reached.\nRetry after: {}s'.format(retry_after)
        super().__init__(self.code, self.message, retry_after=self.retry_after)


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


class MaintenanceError(RequestError):
    """Raised if there is a maintenance break."""

    def __init__(self, code, url):
        self.code = code
        self.url = url
        self.message = 'There is currently a maintenance break. Please be patient and try again later.'
        super().__init__(self.code, self.message)
