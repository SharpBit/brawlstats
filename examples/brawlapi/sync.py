import brawlstats

client = brawlstats.BrawlAPI('token')
# Do not post your token on a public github

player = client.get_profile('GGJVJLU2')
print(player.trophies)  # access attributes using dot.notation
print(player.solo_showdown_victories)  # access using snake_case instead of camelCase

club = player.get_club()
print(club.tag)
best_players = club.members[:5]  # members sorted by trophies, gets best 5 players
for player in best_players:
    print(player.name, player.trophies)  # prints name and trophies

leaderboard = client.get_leaderboard('players', limit=5)  # gets top 5 players
for player in leaderboard:
    print(player.name, player.position)

events = client.get_events()
print(events.current[0].map_name)

battles = client.get_battle_logs('GGJVJLU2')
print(battles[0].battle.mode)

misc = client.get_misc()
print(misc.time_until_season_ends)

search = client.search_club('Cactus Bandits')
print(search[0].tag)
