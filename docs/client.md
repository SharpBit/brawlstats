# Client
This is an async easy to use and clean client to get Brawl Stars statistics

### Initialization
Import abrawlpy and create the client like so:
```py
import abrawlpy

client = abrawlpy.Client('token', timeout=3)
```
Note: Do not put your API key on a public github repo.
### Parameters

| Name | Type | Default |
|------|------|---------|
| token | str | **Required** |
| \*\*timeout | int | 5 |
| \*\*session | session | aiohttp.ClientSession() |
| \*\*loop | loop | None |

Get your token by typing `#getToken` in the [API Server](https://discord.gg/6FtGdX7).


### Methods

| Method | Parameter | Type |
|--------|-----------|------|
| `get_profile` | Tag[str] | [Profile](https://github.com/SharpBit/abrawlpy/blob/master/docs/profile.md) |
| `get_band` | Tag[str], Full[bool]=False | [Band](https://github.com/SharpBit/abrawlpy/blob/master/docs/band.md)
