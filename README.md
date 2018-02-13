# abrawlpy
An async python wrapper for the [Brawl Stars API](http://brawlstars-api.herokuapp.com/api)
### Installation
Install the beta version by typing this into your console
```
pip install abrawlpy
```
Note: The wrapper and API are both still in beta<br>
If you would like to test the *beta* version, type in
```
pip install git+https://github.com/SharpBit/abrawlpy
```
### Documentation
Documentation is coming soon! If you would like to help, DM SharpBit#9614 on discord.
### Misc
If you come across an issue in the wrapper, please [create an issue](https://github.com/SharpBit/abrawl-py) and I will look into it ASAP.

### Examples

```py
import abrawlpy
import asyncio

client = abrawlpy.Client('token', timeout=5)
# Do not post your token on a public github


async def main():
    player = await client.get_profile('UG99J2')
    print(player.trophies) # access attributes using dot notation.
    print(player.showdown_victories) # access using snake_case instead of camelCase
    # band = await player.get_band() This is coming soon 
    # print(band.tag)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
