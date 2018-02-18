# Exceptions and Error Handling

If something you did is incorrect, chances are this wrapper will send you an error saying what's wrong. Here are the errors with their reasons, when they are raised, what is raised, and how to solve each issue.

### Errors

| Code | Name | Reason |
|------|------|--------|
| Any | RequestError | Base class for all exceptions. Used to catch any error. |
| 401 | Forbidden | Your API Key has been blocked by the API. |
| 404 | InvalidTag | An incorrect player or band tag has been passed. |
| 500 | UnexpectedError | An unexpected error has occured. Please [contact us.](https://github.com/SharpBit/abrawlpy/issues) |
| 504 | ServerError | The API is down. Please be patient and try again later. |

### How to Handle Exceptions
The first way to handle all exceptions in this library is to catch the base class, `RequestError`. You can do this using a simple try and except statement. If you are unfamiliar with try and except statements, I recommend you watch this [tutorial](https://youtu.be/NIWwJbo-9_8).<br><br>
Example:
```py
try:
    profile = await client.get_profile('2PP')
except abrawlpy.errors.RequestError as e:
    print(e.code + ': ' + e.error)
```
If the API was down, it would print: `504: The API is down. Please be patient and try again later.`<br>
If your API key in your Client was incorrect, it would print: `401: Your API Key has been blocked by the API.`<br>
However, if you only want to catch a specific error, you can do that as well. For example:
```py
try:
    tag = input('Enter a band tag:\n')
    band = await client.get_band(tag) # user input may not be correct
    # therefore, catch `InvalidTag`
except abrawlpy.errors.InvalidTag:
    print('Invalid Tag.')
```
If you don't want to type `abrawlpy.errors.Error` every single time, you can fix this by simply typing
```py
from abrawlpy.errors import *
```
Now, you can type this safely:
```py
except RequestError as e:
    print(e.code, e.error)
```
I hope this helped you to run your program smoothly without getting it interrupted every time by errors! If you find an error in my errors (errorception) or a bug in the wrapper (possible `500: UnexcpectedError`), please create a new issue [here](https://github.com/SharpBit/abrawlpy/issues).

