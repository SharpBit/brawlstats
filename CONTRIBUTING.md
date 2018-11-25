# Contributing

1. Fork the repository
2. Clone the repository (`git clone https://github.com/username/brawlstats`)
3. Checkout in a new branch (`git checkout -b feature-name`)
4. Install all test dependencies (`pip install -r tests/requirements.txt`)
5. Make your edits
6. Add the necessary tests in the `tests` folder
7. Add the necessary documentation and docstrings
8. Fill up the `tests/.env` file with the suitable tokens
9. Run `flake8` from the root folder (there are certain ignored errors defined in `tox.ini`)
10. Run `python tests/test.py` from the root folder and ensure the tests are configured correctly and they return OK. ServerErrors and warnings can be disregarded.
11. Open your PR
