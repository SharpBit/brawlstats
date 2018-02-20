# Profile
A full profile of a player (all its statistics)
```py
import abrawlpy
import asyncio

client = abrawlpy.Client('token')
async def main():
    profile = await client.get_profile('UG99J2') # get a player profile
    print(profile.name) # prints 'joeycipp'

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

### Methods

`get_band`<br>
    full-`bool`<br>
    Returns: [Band](https://github.com/SharpBit/abrawlpy/blob/master/docs/band.md) if `full=True` else [SimpleBand](https://github.com/SharpBit/abrawlpy/blob/master/docs/band.md#simpleband) or `None` if no band. Default=`False`

### Attributes

| Name | Type |
|------|------|
| `tag` | str |
| `id.high` | int |
| `id.low` | int |
| `name` | str |
| `brawlers_unlocked` | int |
| `brawlers` | List\[[Brawler](https://github.com/SharpBit/abrawlpy/blob/master/docs/brawler.md), [Brawler](https://github.com/SharpBit/abrawlpy/blob/master/docs/brawler.md)\] |
| `victories` | int |
| `showdown_victories` | int |
| `trophies` | int |
| `highest_trophies` | int |
| `band` | [SimpleBand](https://github.com/SharpBit/abrawlpy/blob/master/docs/band.md#simpleband) |
