# Contributing

1. Fork the repository
2. Clone the repository (`git clone https://github.com/username/brawlstats.git`)
3. Checkout in a new branch (`git checkout -b feature-name`)
4. Install all test dependencies (`pip install -r tests/requirements.txt`)
5. Make your edits
6. Add the necessary tests in the `tests` folder
7. Add the necessary documentation and docstrings
8. Add the necessary points to `CHANGELOG.md`
9. Fill up the `.env` file
10. Run `tox` from the root folder and ensure the tests are configured correctly and they return OK. `ServerError` can be disregarded.
11. Open your PR

Do not increment version numbers but update `CHANGELOG.md`