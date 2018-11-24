import brawlstats
import asyncio

loop = asyncio.get_event_loop() # do this if you don't want to get a bunch of warnings
client = brawlstats.Client('token', loop=loop)
# Do not post your token on a public github

# await only works in an async loop
async def main():
    player = await client.get_profile('GGJVJLU2')
    print(player.trophies) # access attributes using dot notation.
    print(player.solo_showdown_victories) # access using snake_case instead of camelCase

    band = await player.get_band(full=True) # full=True gets the full Band object
    print(band.tag)
    best_players = band.members[0:3] # members sorted by trophies, gets best 3 players
    for player in best_players:
        print(player.name, player.trophies) # prints name and trophies

    leaderboard = await client.get_leaderboard('players', 5) # gets top 5 players
    for player in leaderboard:
        print(player.name, player.position)

# run the async loop
loop.run_until_complete(main())