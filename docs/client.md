# Client
This is an async easy to use and clean client to get Brawl Stars statistics

### Initialization
Import abrawlpy and create the client like so:
```py
import abrawlpy

client = abrawlpy.Client('token', timeout=5)
```
Note: Do not put your API key on a public github repo.
### Parameters

| Name | Type | Default |
|------|------|---------|
| token | str | None- required |
| timeout | int | 10 |

### Methods

| Method | Parameter | Type |
|--------|-----------|------|
| `get_profile` | Tag[str] | [Profile](https://github.com/SharpBit/abrawlpy/blob/master/docs/profile.md) |
| `get_band` | Tag[str] | [Band](https://github.com/SharpBit/abrawlpy/blob/master/docs/band.md)
