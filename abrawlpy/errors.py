'''
MIT License

Copyright (c) 2018 SharpBit

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


class RequestError(Exception):
    '''The base class for all errors.'''

    def __init__(self, code, error):
        pass


class Forbidden(RequestError):
    '''Raised when your API Key is blocked'''

    def __init__(self):
        self.code = 401
        self.error = 'Your API Key has been blocked by the API.'
        super().__init__(self.code, self.error)


class InvalidTag(RequestError):
    '''Raised when an invalid player or band tag has been passed'''

    def __init__(self):
        self.code = 404
        self.error = 'An incorrect tag has been passed.'
        super().__init__(self.code, self.error)



class UnexpectedError(RequestError):
    '''Raised when an unknown error has occured'''

    def __init__(self):
        self.code = 500
        self.error = 'An unexpected error has occured. Please contact us.'
        super().__init__(self.code, self.error)
        


class ServerError(RequestError):
    '''Raised when the API is down'''

    def __init__(self):
        self.code = 504
        self.error = 'The API is down. Please be patient and try again later.'
        super().__init__(self.code, self.error)
        
 
