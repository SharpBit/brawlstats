from setuptools import setup, find_packages

with open('README.rst', encoding='utf8') as f:
    long_description = f.read()

setup(
    name='brawlstats',
    version='2.0.6',
    description='An async Python API wrapper for the unofficial Brawl Stars API',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/SharpBit/brawlstats',
    author='SharpBit',
    author_email='sharpbit3618@gmail.com',
    license='MIT',
    keywords=['brawl stars, brawlstats, api-wrapper, async'],
    packages=find_packages(),
    install_requires=['aiohttp', 'python-box']
)
