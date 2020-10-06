import asyncio

import brawlstats

# Do not post your token on a public github!
client = brawlstats.Client('token', is_async=True)


# await only works in an async loop
async def main():
    player = await client.get_profile('V2LQY9UY')
    print(player.trophies)  # access attributes using dot.notation
    print(player.solo_victories)  # use snake_case instead of camelCase

    club = await player.get_club()
    if club is not None:  # check if the player is in a club
        print(club.tag)
        members = await club.get_members()  # members sorted by trophies

        # gets best 5 players or returns all members if the club has less than 5 members
        index = max(5, len(members))
        best_players = members[:index]
        for player in best_players:
            print(player.name, player.trophies)  # prints name and trophies

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

    # Gets a player's recent battles
    battles = await client.get_battle_logs('UL0GCC8')
    print(battles[0].battle.mode)

# run the async loop
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
