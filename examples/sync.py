import brawlstats

client = brawlstats.Client('token')
# Do not post your token on a public github

player = client.get_profile('GGJVJLU2')
print(player.trophies) # access attributes using dot notation.
print(player.solo_showdown_victories) # access using snake_case instead of camelCase

band = player.get_band(full=True) # full=True gets the full Band object
print(band.tag)
best_players = band.members[0:3] # members sorted by trophies, gets best 3 players
for player in best_players:
    print(player.name, player.trophies) # prints name and trophies

leaderboard = client.get_leaderboard('players', 5) # gets top 5 players
for player in leaderboard.players:
    print(player.name, player.position)

events = client.get_events()
print(events.current[0].has_modifier)