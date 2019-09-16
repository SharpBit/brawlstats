import brawlstats

client = brawlstats.OfficialAPI('token')
# Do not post your token on a public github

player = client.get_profile('GGJVJLU2')
print(player.trophies)  # access attributes using dot.notation
print(player.solo_victories)  # access using snake_case instead of camelCase

club = player.get_club()
print(club.tag)
best_players = club.get_members()[:5]  # members sorted by trophies, gets best 5 players
for player in best_players:
    print(player.name, player.trophies)  # prints name and trophies

ranking = client.get_rankings('players', limit=5)  # gets top 5 players
for player in ranking:
    print(player.name, player.rank)

battles = client.get_battle_logs('GGJVJLU2')
print(battles[0].battle.mode)
