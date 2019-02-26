class RequestError(Exception):
    """The base class for all errors."""

    def __init__(self, code, error, retry_after=None):
        pass


class Unauthorized(RequestError):
    """Raised if your API Key is invalid or blocked."""

    def __init__(self, url, code):
        self.code = code
        self.error = 'Your API Key is invalid or blocked.\nURL: ' + url
        super().__init__(self.code, self.error)


class NotFoundError(RequestError):
    """Raised if an invalid player tag or club tag has been passed."""

    def __init__(self, invalid_chars, code):
        self.code = code
        self.error = 'An incorrect tag has been passed.\nInvalid Characters: ' + ', '.join(invalid_chars)
        super().__init__(self.code, self.error)


class RateLimitError(RequestError):
    """Raised when the rate limit is reached."""
    def __init__(self, url, code, retry_after):
        self.code = code
        self.retry_after = retry_after
        self.error = 'The rate limit has been reached.\nURL: ' + url
        super().__init__(self.code, self.error, retry_after=self.retry_after)


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


class MaintenanceError(RequestError):
    """Raised if there is a maintenance break."""

    def __init__(self, url, code):
        self.code = code
        self.error = 'There is currently a maintenance break. Please be patient and try again later.\nURL: ' + url
        super().__init__(self.code, self.error)
