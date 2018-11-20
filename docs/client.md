# Client
This is an async, easy to use, and clean client to get Brawl Stars statistics.

### Initialization
Import brawlstats and create the client like so:
```py
import brawlstats

client = brawlstats.Client('token', timeout=3)
```
Note: Do not put your API key on a public github repo.
### Parameters

| Name | Type | Default |
|------|------|---------|
| token | str | **Required** |
| \*\*timeout | int | 5 |
| \*\*session | session | aiohttp.ClientSession() |
| \*\*loop | loop | None |

Get your token by typing `.getToken` in the [Discord Server](https://discord.me/BrawlAPI).


### Methods

`get_profile`<br />
    tag-`str` A valid player tag<br />
    Returns: [Profile](https://github.com/SharpBit/brawlstats/blob/master/docs/profile.md)<br />
`get_band`<br />
    tag-`str` A valid player tag<br />
    full-`bool` [Band](https://github.com/SharpBit/brawlstats/blob/master/docs/band.md) if `full` is `True` else [SimpleBand](https://github.com/SharpBit/brawlstats/blob/master/docs/band.md#simpleband) or `None` if no band. Default = `False`.<br />
`get_leaderboard`<br />
    p_or_b-`str` Must be 'players' or 'bands' or else it will return a `ValueError`<br />
    count-`int` The number of players/bands to get.
    Returns: List\[[LBPlayer](https://github.com/SharpBit/brawlstats/master/docs/leaderboard.md#player), [LBPlayer](https://github.com/SharpBit/brawlstats/master/docs/leaderboard.md#player)\] or List\[[LBBand](https://github.com/SharpBit/brawlstats/master/docs/leaderboard.md#band), [LBBand](https://github.com/SharpBit/brawlstats/master/docs/leaderboard.md#band)\]
