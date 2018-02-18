from setuptools import setup, find_packages

setup(
    name='abrawlpy',
    version='1.4.0',
    description='An async Python API wrapper for the Brawl Stars API',
    long_description='This package include an easy to use async Client to get Brawl Stars player and band statistics, as well as events. Github: https://github.com/SharpBit/abrawlpy',
    url='https://github.com/SharpBit/abrawlpy',
    author='SharpBit',
    author_email='uworst888@gmail.com',
    license='MIT',
    keywords=['brawl stars, abrawlpy, api-wrapper, async'],
    packages=find_packages(),
    install_requires=['aiohttp', 'python-box']
)
