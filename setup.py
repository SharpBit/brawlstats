from setuptools import setup, find_packages

setup(
    name='brawlstats',
    version='2.0.0',
    description='An async Python API wrapper for the unofficial Brawl Stars API',
    long_description='This package include an easy to use async Client to get Brawl Stars player and band statistics, and the leaderboard. Github: https://github.com/SharpBit/brawlstats',
    url='https://github.com/SharpBit/brawlstats',
    author='SharpBit',
    author_email='sharpbit3618@gmail.com',
    license='MIT',
    keywords=['brawl stars, brawlstats, api-wrapper, async'],
    packages=find_packages(),
    install_requires=['aiohttp', 'python-box']
)
