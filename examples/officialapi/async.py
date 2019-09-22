import brawlstats
import asyncio

client = brawlstats.OfficialAPI('token', is_async=True)
# Do not post your token on a public github

# await only works in an async loop
async def main():
    player = await client.get_profile('GGJVJLU2')
    print(player.trophies)  # access attributes using dot.notation
    print(player.solo_victories)  # access using snake_case instead of camelCase

    club = await player.get_club()
    print(club.tag)
    members = await club.get_members()
    best_players = members[:5]  # members sorted by trophies, gets best 5 players
    for player in best_players:
        print(player.name, player.trophies)

    ranking = await client.get_rankings('players', limit=5)  # gets top 5 players
    for player in ranking:
        print(player.name, player.rank)

    battles = await client.get_battle_logs('GGJVJLU2')
    print(battles[0].battle.mode)

# run the async loop
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
