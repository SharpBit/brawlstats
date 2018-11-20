# Member
Returns some info about a band member. Get this by accessing [Band](https://github.com/SharpBit/brawlstats/blob/master/docs/band.md).members
```py
members = band.members
print(members[0].name, members[0].role) # prints best player's name and role (sorted by trophies)
```

### Attributes

| Name | Type |
|------|------|
| `id.high` | int |
| `id.low` | int |
| `tag` | str |
| `name` | str |
| `role` | str |
| `exp_level` | int |
| `trophies` | int |
| `avatar_id` | int |
| `avatar_url` | str |
