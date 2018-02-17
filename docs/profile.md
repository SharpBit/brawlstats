# Profile
A full profile of a player (all its statistics)
```py
profile = await client.get_profile('UG99J2')
print(profile.name) # prints the player's name
```

### Methods
| Name | Parameter | Type |
|------|-----------|------|
| `get_band` | full=False (Default) | [SimpleBand](https://github.com/SharpBit/abrawlpy/blob/master/docs/band.md#simpleband) or `None` if no band |
| `get_band` | full=True | [Band](https://github.com/SharpBit/abrawlpy/blob/master/docs/band.md) or `None` if no band |

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

Note: The band attribute returns a [simple band object](https://github.com/SharpBit/abrawlpy/blob/master/docs/band.md), while the `get_band()` method returns a [full band object](https://github.com/SharpBit/abrawlpy/blob/master/docs/band.md).
