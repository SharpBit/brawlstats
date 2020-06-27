import brawlstats
import asyncio

# Do not post your token on a public github!
client = brawlstats.Client('token', is_async=True)


# await only works in an async loop
async def main():
    player = await client.get_profile('GGJVJLU2')
    print(player.trophies)  # access attributes using dot.notation
    print(player.solo_victories)  # use snake_case instead of camelCase

    club = await player.get_club()
    print(club.tag)
    members = await club.get_members()  # members sorted by trophies
    best_players = members[:5]  # gets best 5 players
    for player in best_players:
        print(player.name, player.trophies)

    # get top 5 players in the world
    ranking = await client.get_rankings(ranking='players', limit=5)
    for player in ranking:
        print(player.name, player.rank)

    # get top 5 mortis players in the US
    ranking = await client.get_rankings(
        ranking='brawlers',
        region='us',
        limit=5,
        brawler='mortis'
    )
    for player in ranking:
        print(player.name, player.rank)

    battles = await client.get_battle_logs('GGJVJLU2')
    print(battles[0].battle.mode)

# run the async loop
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
