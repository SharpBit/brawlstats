# Change Log
All notable changes to this project will be documented in this file.

## [2.3.11] - 7/3/19
### Fixed
- Fixed the sync version of the wrapper to not raise a RuntimeWarning due to using `asyncio.sleep()` instead of `time.sleep()`

## [2.3.10] - 7/2/19
### Added
- New brawler tick

## [2.3.9] - 5/27/19
### Fixed
- Renamed ricochet to rico
- Fixed the sync client when not using `prevent_ratelimit`
### Added
- Bibi!

## [2.3.8] - 5/21/19
### Changed
- Changed the Base URL back to the new URL.
- Now waits the number of seconds instead of raising a `RateLimitError` when a rate limit will be detected BEFORE it requests.

## [2.3.7] - 5/5/19
### Changed
- Changed the BASE URL to the old API URL. VERSION 2.3.6 WILL NOT WORK DUE TO API TIMEOUT ISSUES. PLEASE UPDATE.

## [2.3.6] - 4/27/19
### Added
- Rosa to the brawler list
- `prevent_ratelimit` option when initializing a client to wait when chaining requests
### Changed
- Base URL for requests to [the new API URL](https://api.brawlapi.cf/v1)
- Ratelimit updated to API's 3 requests per second

## [2.3.5] - 4/15/19
### Fixed
- Fixed the rate limit handler when error code 429 was returned by the API.

## [2.3.4] - 4/10/19
### Fixed
- Fixed a [mistake](https://github.com/SharpBit/brawlstats/pull/24) where `time()` was being called directly (instead of `time.time()`)

## [2.3.3] - 4/5/19
### Added
- Added carl to the brawler list
### Changed
- Renamed `Profile` class to `Player`

## [2.3.2] - 3/10/19
### Fixed
- Allows users to pass in a connector for the async client which fixes issue #19.

## [2.3.1] - 3/9/19
### Added
- Creates requests with gzip encoding enabled to cut request times.
- Detect a rate limit before it requests from the API.
### Changed
- Changed the request log.
- No longer imports itself in `utils.py` for the version number.

## [2.3.0] - 3/4/19
### Added
- Added caching that clears after 180 seconds to not spam the API with the same requests.
### Fixed
- Fixed debug on the sync client.

## [2.2.8] - 3/4/19
### Added
- Added the text that the API returns when an `UnexpectedError` is raised. If you see this, you should report the error to the [discord server](https://discord.me/BrawlAPI)
### Fixed
- Fixed the club search request URL
- Fixed sync `search_club`

## [2.2.7] - 2/27/19
### Fixed
- Fixed issue [#20](https://github.com/SharpBit/brawlstats/issues/20)
### Removed
- Removed `pytest` from the package requirements.

## [2.2.6] - 2/26/19
### Fixed
- Club search actually returns a list now.
### Changed
- Added wrapper and python version numbers to the User Agent when making API requests.
- `url` param in the client changed to `base_url`

## [2.2.5] - 2/25/19
### Added
- `debug` option to pass in when intializing `brawlstats.core.Client` to log requests.

## [2.2.4] - 2/24/19
### Fixed
- Fixed [installation error](https://github.com/SharpBit/brawlstats/issues/17) where the `constants.json` info key was removed.

## [2.2.3] - 2/18/19
### Added
- Added gene to the list of brawlers to get for the brawler leaderboard.

## [2.2.2] - 2/3/19
### Fixed
- Fixed `search_club()`
- Fixed some attribute typos in docs for the Misc category

## [2.2.1] - 1/30/19
### Fixed
- Providing no loop while setting `is_async` to `True` now correctly defaults to `asyncio.get_event_loop()`
- Fixed the URL for `get_club()`
- Fixed some typos in docs
- Fixed attribute charts in docs

## [2.2.0] - 1/29/19
### Changed
- Change the way you get a brawler with `get_leaderboard()`
- Updated documentation for added keys

## [2.1.13] - 1/18/19
### Added
- Search Clubs (`search_club()`)
- Season and Shop Data (`get_misc()`)

## [2.1.12] - 1/5/19
### Added
- Loop parameter for the client for aiohttp sessions if one has not yet been specified. If you specify a session, you must set the loop to that session before you pass it in otherwise the loop will not be applied.

## [2.1.11] - 12/24/18
### Added
- MaintenanceError raised when the game is undergoing maintenance.

## [2.1.10] - 12/13/18
### Fixed
- Fix any data that involves a list (Leaderboard)

## [2.1.9] - 12/11/18
### Added
- `get_datetime` function for easier date and time conversions

## [2.1.8] - 12/10/18
### Changed
- No longer need to access a players or clubs attribute when getting a leaderboard

## [2.1.7] - 12/9/18
### Fixed
- Fixed a bug in the sync version of `get_constants()` where there was an extra `await`

## [2.1.6] - 12/8/18
### Added
- Constants extracted from the Brawl Stars App using `Client.get_constants`

## [2.1.5] - 12/5/18
BREAKING CHANGES: Brawl Stars dev team changed "Band" to "Club". This update fixes all of that.
### Changed
- `Band` has been changed to `Club`
- `SimpleBand` has been changed to `PartialClub`
- Documentation has been updated for this
- All methods that originally had "band" in them have been changed to "club"
- All attributes that originally had "band" in them have been changed to "club"

## [2.1.4] - 12/2/18
### Added
- `RateLimitError` to handle the 2 requests/sec ratelimit of the API.

## [2.1.3] - 12/2/18
### Added
- Remove warnings and stuff to prevent memory leaks and fix session initialization (PR from Kyber)

## [2.1.2] - 12/2/18
### Added
- Resp accessible in data models via `Model.resp`
- Added documentation for below change and new attributes that the API introduced.
### Changed
- `InvalidTag` changed to `NotFoundError`

## [2.1.1] - 12/1/18
### Added
- Allows developers to change the base URL to make request to. This addresses [issue #6](https://github.com/SharpBit/brawlstats/issues/6)

## [2.1.0] - 11/29/18
### Added
- Synchronous support! You can now set if you want an async client by using `is_async=True`
### Fixed
- `asyncio.TimeoutError` now properly raises `ServerError`
### Removed
- `BadRequest` and `NotFoundError` (negates v2.0.6). These were found to not be needed

## [2.0.7] - 11/29/18
### Added
- Support for the new `/events` endpoint for current and upcoming event rotations
### Changed
- Change the Unauthorized code from 403 to 401 due to API error code changes

## [2.0.6] - 11/25/18
### Added
- `BadRequest` and `NotFoundError` for more API versatility

## [2.0.5] - 11/24/18
### Fixed
- Leaderboards fixed

## [2.0.0] - 11/19/18
### Added
- Support for the brand new API at https://brawlapi.cf/api