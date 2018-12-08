# Change Log
All notable changes to this project will be documented in this file.

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