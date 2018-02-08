from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name='abrawlpy',
    version='1.1.2',
    description='An async Python API wrapper for the Brawl Stars API',
    long_description=long_description,
    url='https://github.com/SharpBit/brawlstars',
    author='SharpBit',
    author_email='uworst888@gmail.com',
    license='MIT',
    keywords=['brawl stars, abrawl-py, api-wrapper, async'],
    packages=find_packages(),
    install_requires=['aiohttp', 'python-box']
)
