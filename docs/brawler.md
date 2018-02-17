# Brawler
Returns a brawler object with the following attributes.
You can retrieve a profile's brawler info by getting the player's brawler attribute.
```py
brawlers = profile.brawlers
top_brawler = brawlers[0] # first index in list = highest trophies
print(top_brawler.name, top_brawler.trophies) # prints best brawler's name and trophies

### Attributes

| Name | Type |
|------|------|
| `type` | int |
| `name` | str |
| `unk1` | int |
| `trophies` | int |
| `highest_trophies` | int |
| `upgrades_power` | int |
