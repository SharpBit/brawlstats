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

`get_profile`<br>
    tag-`str` A valid player tag<br>
    Returns: [Profile](https://github.com/SharpBit/abrawlpy/blob/master/docs/profile.md)<br>
`get_band`<br>
    tag-`str` A valid player tag<br>
    full-`bool` [Band](https://github.com/SharpBit/abrawlpy/blob/master/docs/band.md) if `full` is `True` else [SimpleBand](https://github.com/SharpBit/abrawlpy/blob/master/docs/band.md#simpleband) or `None` if no band. Default = `False`.<br>
    (why am i using talking like a ternary operator)
`get_leaderboard`<br>
    p_or_b-`str` 'players' or 'bands'<br>
    count-`int` The number of players/bands to get.
    Returns: List\[[LBPlayer](), [LBPlayer]()\] or List\[[LBBand](), [LBBand]()\]
