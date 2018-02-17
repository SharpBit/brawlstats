# Member
Returns some info about a band member. Get this by accessing the band's `band_members`
```py
members = band.band_members
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
