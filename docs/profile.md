# Profile
A full profile of a player (all its statistics)

### Methods
`get_band()`- Parameters: None, Returns [Band](https://github.com/SharpBit/abrawlpy/blob/master/docs/band.md) or `None` if no clan.

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
| `band.high` | int |
| `band.low` | int |

Note: The band attribute returns a simple band object, which the `get_band()` method returns a full band object.
