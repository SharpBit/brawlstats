from setuptools import setup, find_packages

import json
import urllib.request

with open('README.rst', encoding='utf8') as f:
    long_description = f.read()

setup(
    name='brawlstats',
    version='2.1.11',
    description='An async Python API wrapper for the unofficial Brawl Stars API',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/SharpBit/brawlstats',
    author='SharpBit',
    author_email='sharpbit3618@gmail.com',
    license='MIT',
    keywords=['brawl stars, brawlstats, api-wrapper, async'],
    packages=find_packages(),
    install_requires=['aiohttp', 'python-box', 'requests'],
    python_requires='>=3.5',
    project_urls={
        'Source Code': 'https://github.com/SharpBit/brawlstats',
        'Issue Tracker': 'https://github.com/SharpBit/brawlstats/issues',
        'Documentation': 'https://brawlstats.readthedocs.io/',
    },
    classifiers=[
        'Development Status :: 4 - Production/Mostly Stable',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment :: Real Time Strategy and Action',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Natural Language :: English'
    ]
)

# Reload Constants
try:
    data = json.loads(urllib.request.urlopen('https://fourjr-webserver.herokuapp.com/bs/constants').read())
except (TypeError, urllib.error.HTTPError, urllib.error.URLError):
    pass
else:
    if data:
        del data['info']
        with open('brawlstats/constants.json', 'w') as f:
            json.dump(data, f)