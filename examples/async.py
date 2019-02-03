import brawlstats
import asyncio

client = brawlstats.Client('token', is_async=True)
# Do not post your token on a public github

# await only works in an async loop
async def main():
    player = await client.get_profile('GGJVJLU2')
    print(player.trophies) # access attributes using dot.notation
    print(player.solo_showdown_victories) # access using snake_case instead of camelCase

    club = await player.get_club()
    print(club.tag)
    best_players = club.members[0:3] # members sorted by trophies, gets best 3 players
    for player in best_players:
        print(player.name, player.trophies)

    leaderboard = await client.get_leaderboard('players', count=5) # gets top 5 players
    for player in leaderboard:
        print(player.name, player.position)

    events = await client.get_events()
    print(events.current[0].map_name)

    misc = await client.get_misc()
    print(misc.time_until_season_ends)

    search = await client.search_club('Cactus Bandits')
    print(search[0].tag)

# run the async loop
loop = asyncio.get_event_loop()
loop.run_until_complete(main())