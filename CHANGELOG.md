# Change Log
All notable changes to this project will be documented in this file.

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