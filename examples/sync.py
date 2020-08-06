import brawlstats

# Do not post your token on a public github!
client = brawlstats.Client('token')


player = client.get_profile('GGJVJLU2')
print(player.trophies)  # access attributes using dot.notation
print(player.solo_victories)  # use snake_case instead of camelCase

club = player.get_club()
print(club.tag)
members = club.get_members()  # members sorted by trophies
best_players = members[:5]  # gets best 5 players
for player in best_players:
    print(player.name, player.trophies)  # prints name and trophies

# get tag for each member
player_tags = [member.tag for member in members]

# get every member in the club as player
players = client.get_players(player_tags)

# print highest trophies for top 5 members
for player in players[:5]:
    print(player.highest_trophies)

# gets top 5 players in the world
ranking = client.get_rankings(ranking='players', limit=5)
for player in ranking:
    print(player.name, player.rank)

# get top 5 mortis players in the US
ranking = client.get_rankings(
    ranking='brawlers',
    region='us',
    limit=5,
    brawler='mortis'
)
for player in ranking:
    print(player.name, player.rank)

battles = client.get_battle_logs('GGJVJLU2')
print(battles[0].battle.mode)
